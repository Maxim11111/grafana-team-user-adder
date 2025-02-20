import requests
import json
import time
import logging
import signal
import sys

# Настройка логирования
logging.basicConfig(level=logging.INFO, filename='/app/log_file.log', filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s')

logging.info("Starting the process of adding users to Grafana teams.")

# Перехват SIGINT (например, Ctrl+C)
def signal_handler(sig, frame):
    logging.info('Process was interrupted. Exiting.')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Загрузка настроек
with open('settings.json') as f:
    settings = json.load(f)

grafana_url = settings["grafana_url"]
admin_user = settings["admin_user"]
admin_password = settings["admin_password"]
service_token = settings["service_token"]

# Подсчет команд и email-адресов
num_teams = len(settings["teams"])
num_emails = sum(len(team["emails"]) for team in settings["teams"])

# Вывод информации о количестве команд и email-адресов
print(f"Number of teams to process: {num_teams}")
print(f"Total number of emails to process: {num_emails}")

sys.stdout.flush()  # Обеспечение немедленного вывода
processed_emails = set()  # Сет для хранения успешно добавленных email

# Функция для добавления пользователей в команды
def add_users_to_teams():
    all_added = True

    for team in settings["teams"]:
        grafana_team_id = team["grafana_team_id"]
        emails = team["emails"]

        for email in emails:
            if email in processed_emails:
                continue  # Пропустить уже обработанные email

            try:
                # Проверяем наличие пользователя в Grafana
                response = requests.get(
                    f"{grafana_url}/api/users/lookup?loginOrEmail={email}",
                    auth=(admin_user, admin_password)
                )
                
                if response.status_code == 200:
                    user_id = response.json().get("id")
                    
                    # Добавляем пользователя в команду
                    add_response = requests.post(
                        f"{grafana_url}/api/teams/{grafana_team_id}/members",
                        headers={"Authorization": f"Bearer {service_token}"},
                        json={"userId": user_id}
                    )
                    
                    if add_response.status_code == 200:
                        logging.info(f"User {email} added to team {grafana_team_id}")
                        processed_emails.add(email)
                    elif add_response.status_code == 400:
                        error_message = add_response.json().get("message", "")
                        if error_message == "User is already added to this team":
                            logging.info(f"User {email} is already in team {grafana_team_id}")
                            processed_emails.add(email)
                        else:
                            all_added = False
                    else:
                        all_added = False
                        
                else:
                    all_added = False
                    
            except Exception as e:
                logging.error(f"An error occurred: {e}")
                all_added = False

    return all_added

def list_teams():
    try:
        response = requests.get(f"{grafana_url}/api/teams/search", headers={"Authorization": f"Bearer {service_token}"})
        if response.status_code == 200:
            teams = response.json().get("teams", [])
            
            # Определение ширины колонок
            name_width = max(len(team['name']) for team in teams) + 2
            id_width = max(len(str(team['id'])) for team in teams) + 2
            
            # Заголовок таблицы
            print(f"+{'-' * name_width}+{'-' * id_width}+")
            print(f"| {'Team Name'.ljust(name_width-1)}| {'ID'.ljust(id_width-1)}|")
            print(f"+{'-' * name_width}+{'-' * id_width}+")
            
            # Данные таблицы
            for team in teams:
                print(f"| {team['name'].ljust(name_width-1)}| {str(team['id']).ljust(id_width-1)}|")
            
            # Нижняя граница таблицы
            print(f"+{'-' * name_width}+{'-' * id_width}+")
        else:
            print("Failed to retrieve teams from Grafana.")
    except Exception as e:
        print(f"An error occurred while retrieving teams: {e}")

# Обработка команд
if len(sys.argv) > 1 and sys.argv[1] == '--teams':
    list_teams()
    sys.exit(0)

# Основной цикл
while True:
    if add_users_to_teams():
        logging.info("All users have been added to their respective teams. Exiting.")
        break
    
    time.sleep(10)