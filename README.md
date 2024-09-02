USE YOUR OWN CREDENTIALS TO RUN SERVER AND FETCH EMAILS

# Email Integration Project

This Django project is designed to integrate emails from various providers (Gmail, Yandex, Mail.ru) and display them in a simple web interface. The project includes real-time progress tracking using WebSockets and Django Channels.

## Features

- **Email Fetching**: Connects to IMAP servers of Gmail, Yandex, and Mail.ru to fetch emails.
- **Attachment Handling**: Saves email attachments locally on the server.
- **Real-Time Progress**: Uses WebSockets and Django Channels to provide real-time updates on email fetching progress.
- **Simple UI**: Displays a list of emails with their details and attachments in a table format.

## Installation

To get started with this project, follow these steps:

### Prerequisites

- Python 3.8+
- PostgreSQL
- Redis (for Channels)
- Git

### Setup

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/AlexanPetrov/email_integration.git
    cd email_integration
    ```

2. **Set Up the Virtual Environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set Up PostgreSQL Database**:
    - Ensure PostgreSQL is installed and running.
    - Create a new PostgreSQL database (e.g., `email_system`).
    - Update the `DATABASES` settings in `email_integration/settings.py` with your database credentials.

5. **Run Migrations**:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

6. **Create a Superuser**:
    ```bash
    python manage.py createsuperuser
    ```

7. **Run Redis Server**:
    - Ensure Redis is installed and running. You can start Redis with:
    ```bash
    redis-server
    ```

8. **Start the Development Server**:
    ```bash
    python manage.py runserver
    ```

## Usage

- **Access the Admin Interface**:
  - Navigate to `http://127.0.0.1:8000/admin/` and log in with your superuser credentials to manage email credentials.
  - Add email credentials (email and password) for Gmail, Yandex, or Mail.ru.

- **View Fetched Emails**:
  - Navigate to `http://127.0.0.1:8000/messages/` to view the list of emails fetched from the specified email accounts.

- **Real-Time Progress**:
  - The progress bar on the email list page will update in real-time as emails are fetched.

## Requirements

- **Django** 4.2+
- **Django Channels** 4.0.0
- **Channels Redis** 4.1.0
- **Daphne** 4.0.0
- **PostgreSQL** as the database
- **Redis** for managing WebSocket connections

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes. For major changes, please open an issue first to discuss what you would like to change.

## Contact

- **Author**: Alexander Petrovski
- **Email**: apfb11@gmail.com
