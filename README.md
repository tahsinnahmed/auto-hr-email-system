# Auto HR Email System

When HR adds a new employee to OrangeHRM with an email in the Contact Details tab, this service detects them within minutes. It generates a message and sends it individually and automatically. This approach eliminates manual typing, forgotten follow-ups, and inconsistency between hires.

## How It Works

### Architecture

<img width="5559" height="2662" alt="deepseek_mermaid_20261011_fb43d8" src="https://github.com/user-attachments/assets/cf0b1a95-e81b-41a3-9208-cba809203b67" />

### 1. OAuth Authorization

Authorize the application through OrangeHRM on the first run.

<img width="513" height="471" alt="AHRES-1" src="https://github.com/user-attachments/assets/ddb1b7fa-291e-4feb-a852-db1bda649762" />

### 2. Service Startup

The launcher initializes MySQL, starts the poller, and launches the FastAPI server.

<img width="1915" height="1014" alt="AHRES-2" src="https://github.com/user-attachments/assets/3fc7ffd1-61de-4d0b-b2e8-b99b17473256" />

### 3. Auto Detection and Mail Sending

The system detects new employees, retrieves their contact details, sends welcome emails, and saves the records.

<img width="1908" height="498" alt="AHRES-3" src="https://github.com/user-attachments/assets/1a726873-d1de-4598-9d93-ee8fef795ac8" />

### 4. Email Receiver

New employees receive a personalized email with their start date and first-day instructions.

<img width="905" height="904" alt="AHRES-4" src="https://github.com/user-attachments/assets/3750f133-869c-4ebb-a8af-31daf200b00a" />

## Features

- **Automatic detection** — Checks OrangeHRM every five minutes.
- **Personalized emails** — Includes employee details and onboarding instructions.
- **Duplicate prevention** — Prevents employees from being processed twice.
- **OAuth 2.0** — Supports automatic access-token refresh.
- **MySQL persistence** — Records processed employees.
- **Missing-email handling** — Skips employees without a personal email until it becomes available.
- **Webhook support** — Provides an HTTP endpoint for triggering onboarding.
- **Dry-run mode** — Tests the workflow without sending emails.

## Tech Stack

| Component | Technology |
|---|---|
| HR System | OrangeHRM |
| Language | Python 3.10+ |
| API Framework | FastAPI |
| Scheduler | APScheduler |
| Database | MySQL |
| Database Driver | PyMySQL |
| HTTP Client | httpx |
| Configuration | python-dotenv |

## Prerequisites

- [Python 3.10+](https://www.python.org/downloads/)
- [XAMPP](https://www.apachefriends.org/)
- [OrangeHRM](https://www.orangehrm.com/)
- Gmail or another SMTP provider
- SMTP credentials or a Gmail App Password

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/tahsinnahmed/auto-hr-email-system.git
cd auto-hr-email-system
```

### 2. Configure OrangeHRM

Register an OAuth client in OrangeHRM with the following settings:

- **Name:** Auto HR Email System
- **Redirect URI:** `http://localhost:8765/callback`
- **Grant Type:** Authorization Code
- **Confidential Client:** Enabled

Save the Client ID and Client Secret for configuration.

### 3. Configure Environment Variables

Create a `.env` file containing your OrangeHRM, MySQL, and SMTP settings.

### 4. Run the Service

Start the service by clicking the `start.bat` file.

## Troubleshooting

- **No email sent:** Verify the employee's personal email and SMTP configuration.
- **OAuth errors:** Check the client credentials and redirect URI.
- **Optional write-back returns `403 Forbidden`:** OrangeHRM custom fields may not be configured. Email delivery is unaffected.

## License

See the repository for license information.
