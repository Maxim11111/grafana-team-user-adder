# Grafana Team User Adder

## Description

**Grafana Team User Adder** is a utility that automates the addition of users to Grafana teams based on a list of email addresses. It periodically checks for users and adds them to the specified teams.

## Features

- Automatically adds users to specified Grafana teams.
- Supports retrying every 10 seconds until all users are added.
- Handles cases where users are already added to a team.
- Logs all actions and errors.
- Retrieves and displays all teams from Grafana.

## Requirements

- Docker
- Grafana instance with API key and administrator credentials

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/Maxim11111/grafana-team-user-adder.git
   cd grafana-team-user-adder
   ```

2. **Configuration**

   Create a `settings.json` file in the root directory and configure it as follows:

   ```json
   {
     "teams": [
       {
         "grafana_team_id": 1,
         "emails": ["user1@example.com", "user2@example.com"]
       },
       {
         "grafana_team_id": 2,
         "emails": ["user3@example.com", "user4@example.com"]
       }
     ],
     "grafana_url": "http://your_grafana_domain.com",
     "admin_user": "admin",
     "admin_password": "password",
     "service_token": "your_service_token"
   }
   ```

## Usage

### Commands

- **Start the main loop for adding users**:  
  ```bash
  ./run.sh --start
  ```

- **Stop the container**:  
  ```bash
  ./run.sh --stop
  ```

- **Restart the container**:  
  ```bash
  ./run.sh --restart
  ```

- **Fetch and display all Grafana teams**:  
  ```bash
  ./run.sh --teams
  ```

- **Display help message**:  
  ```bash
  ./run.sh help
  ```

## Logging

- All actions and errors are logged to `log_file.log` in the root directory.

## Feedback and Contribution

Feel free to open [Issues](https://github.com/Maxim11111/grafana-team-user-adder/issues) or submit [Pull Requests](https://github.com/Maxim11111/grafana-team-user-adder/pulls) for feedback or contributions.

## License

This project is licensed under the [MIT License](LICENSE).

## Authors

**Maxim Klyachev** — Author and Maintainer.