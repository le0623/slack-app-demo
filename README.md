# Slack Automation Bot with Block Kit

A comprehensive Slack app example demonstrating automation capabilities using Block Kit for rich, interactive UI components.

## Features

- 🤖 **Interactive Messages** - Rich Block Kit messages with buttons and actions
- 📝 **Task Management** - Create and manage tasks with modals
- 📋 **Approval Workflows** - Request and manage approvals with interactive buttons
- 🔄 **Workflow Automation** - Track and display workflow status
- ⏰ **Scheduled Tasks** - Automated daily reports and task reminders using APScheduler
- 🏠 **Home Tab** - Customizable dashboard in Slack home tab
- 💬 **Slash Commands** - `/automation` command to access automation features

## Block Kit Components

The app includes reusable Block Kit components:

- Headers and sections
- Buttons and action blocks
- Modals for form inputs
- Date pickers and select menus
- Context blocks and dividers
- Workflow status messages
- Approval request messages

## Setup Instructions

### 1. Create a Slack App

1. Go to [api.slack.com/apps](https://api.slack.com/apps)
2. Click "Create New App" → "From scratch"
3. Name your app and select your workspace
4. Go to "OAuth & Permissions" and add the following Bot Token Scopes:
   - `app_mentions:read`
   - `chat:write`
   - `commands`
   - `users:read`
   - `channels:read`
   - `im:write`
   - `im:read`
   - `channels:history`
   - `app_home:write` (for home tab)
   - `views:write` (for modals)
   - `views:read` (for modals)
5. Install the app to your workspace
6. Copy the "Bot User OAuth Token" (starts with `xoxb-`)

### 2. Enable Socket Mode (Optional but Recommended)

1. Go to "Socket Mode" in your app settings
2. Enable Socket Mode
3. Create an app-level token with `connections:write` scope
4. Copy the token (starts with `xapp-`)

### 3. Get Signing Secret

1. Go to "Basic Information"
2. Copy the "Signing Secret"

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
SLACK_BOT_TOKEN=xoxb-your-bot-token
SLACK_APP_TOKEN=xapp-your-app-token
SLACK_SIGNING_SECRET=your-signing-secret
PORT=3000
HOST=0.0.0.0
SLACK_CHANNEL_ID=#general
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the Application

#### Option A: Socket Mode (Recommended for Development)

Socket Mode is easier for local development as it doesn't require a public URL:

```bash
python app_socket_mode.py
```

#### Option B: HTTP Mode (Recommended for Production)

For production deployments with a public URL:

```bash
python app.py
```

Or using uvicorn directly:

```bash
uvicorn app:app --host 0.0.0.0 --port 3000 --reload
```

### 7. Configure Slack Event Subscriptions (for HTTP mode)

If not using Socket Mode:

1. Go to "Event Subscriptions" in your app settings
2. Enable Events
3. Set Request URL to: `https://your-domain.com/slack/events`
4. Subscribe to bot events:
   - `app_home_opened`
   - `message.channels`
   - `message.im`

### 8. Enable Home Tab

1. Go to "App Home" in your app settings
2. Enable "Home Tab"
3. Enable "Messages Tab" (optional, for DM functionality)
4. Save changes

### 9. Configure Slash Command

1. Go to "Slash Commands" in your app settings
2. Create a new command:
   - Command: `/automation`
   - Request URL: `https://your-domain.com/slack/events` (or use Socket Mode)
   - Short description: "Automation commands"

## Usage Examples

### Slash Command

Type `/automation` in any channel to see available automation commands.

### Interactive Messages

- Click "View Workflow" to see workflow automation example
- Click "Create Task" to open a task creation modal
- Click "Request Approval" to create an approval request

### Task Management

1. Click "Create Task" button
2. Fill in the modal form:
   - Task Title (required)
   - Description (optional)
   - Priority (High/Medium/Low)
   - Due Date (optional)
3. Submit to create the task

### Approval Workflows

1. Click "Request Approval" button
2. An approval request message will be posted
3. Use the "Approve" or "Reject" buttons to respond
4. The message will update with the approval status

### Scheduled Automation

The app includes two scheduled tasks:

- **Daily Report** - Sent every day at 9 AM
- **Task Reminder** - Sent every hour for pending tasks

You can customize the schedule in `app.py`:

```python
# Schedule daily report at 9 AM
scheduler.add_job(
    send_daily_report,
    trigger=CronTrigger(hour=9, minute=0),
    id="daily_report"
)

# Schedule task reminder every hour
scheduler.add_job(
    check_pending_tasks,
    trigger=CronTrigger(minute=0),
    id="task_reminder"
)
```

## Project Structure

```
slack-bot/
├── app.py                    # Main application with FastAPI (HTTP mode)
├── app_socket_mode.py        # Alternative startup with Socket Mode
├── block_kit_components.py   # Reusable Block Kit components
├── config.py                 # Configuration settings
├── examples.py               # Example usage of Block Kit components
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables (create this)
├── .gitignore               # Git ignore file
└── README.md                 # This file
```

## Block Kit Components

All Block Kit components are defined in `block_kit_components.py`:

- `create_header_block()` - Header blocks
- `create_section_block()` - Section blocks with text
- `create_button_block()` - Interactive buttons
- `create_actions_block()` - Action blocks with buttons
- `create_task_modal()` - Task creation modal
- `create_approval_message()` - Approval request message
- `create_workflow_message()` - Workflow status message
- `create_dashboard_home_tab()` - Home tab dashboard

## Customization

### Adding New Automation

1. Create Block Kit components in `block_kit_components.py`
2. Add event handlers in `app.py`
3. Add scheduled tasks if needed
4. Update the home tab with new actions

### Modifying Scheduled Tasks

Edit the scheduler jobs in `app.py`:

```python
scheduler.add_job(
    your_function,
    trigger=CronTrigger(hour=9, minute=0),
    id="your_job_id"
)
```

## Security Notes

- Never commit your `.env` file to version control
- Keep your Slack tokens secure
- Use environment variables for all secrets
- Enable request verification using the signing secret

## Troubleshooting

### App not responding to events

- Verify your bot token is correct
- Check that event subscriptions are configured
- Ensure your Request URL is accessible
- Check logs for error messages

### Scheduled tasks not running

- Verify APScheduler is started: `scheduler.start()`
- Check cron trigger syntax
- Verify bot has permissions to post messages
- Check logs for errors

### Modals not opening

- Verify trigger_id is valid
- Check that modal view is properly formatted
- Ensure bot has necessary scopes

## Resources

- [Slack Block Kit](https://api.slack.com/block-kit)
- [Slack API Documentation](https://api.slack.com/)
- [Slack Bolt for Python](https://slack.dev/bolt-python/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [APScheduler Documentation](https://apscheduler.readthedocs.io/)

## License

MIT License

