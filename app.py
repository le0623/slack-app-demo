"""
Slack App with Block Kit Automation
Main application file using FastAPI and APScheduler
"""
import os
import logging
from datetime import datetime
from typing import Dict, Any

from fastapi import FastAPI, Request, Response, HTTPException
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_bolt import App
from slack_bolt.adapter.fastapi import SlackRequestHandler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from config import settings
from block_kit_components import (
    create_workflow_message,
    create_task_modal,
    create_approval_message,
    create_dashboard_home_tab,
    create_header_block,
    create_section_block,
    create_actions_block,
    create_button_block,
    create_divider_block,
    create_context_block
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Slack app
slack_app = App(
    token=settings.slack_bot_token,
    signing_secret=settings.slack_signing_secret
)
slack_handler = SlackRequestHandler(slack_app)

# Initialize FastAPI app
app = FastAPI(title="Slack Automation Bot")

# Initialize Slack WebClient
slack_client = WebClient(token=settings.slack_bot_token)

# Initialize scheduler
scheduler = BackgroundScheduler()
scheduler.start()


# Store for automation data (in production, use a database)
automation_store: Dict[str, Any] = {
    "tasks": [],
    "workflows": [],
    "approvals": []
}


# ==================== Slack Event Handlers ====================

@slack_app.event("app_home_opened")
def handle_app_home_opened(event, client):
    """Handle app home opened event"""
    try:
        user_id = event["user"]
        view = create_dashboard_home_tab()
        client.views_publish(user_id=user_id, view=view)
        logger.info(f"Published home tab for user {user_id}")
    except Exception as e:
        logger.error(f"Error publishing home tab: {e}")


@slack_app.event("message")
def handle_message(event, client):
    """Handle message events"""
    # Ignore bot messages
    if event.get("subtype") == "bot_message":
        return
    
    text = event.get("text", "").lower()
    channel = event["channel"]
    
    # Handle command messages
    if "hello" in text or "hi" in text:
        client.chat_postMessage(
            channel=channel,
            text="Hello! 👋 Use `/automation` to get started with automations."
        )
    elif "workflow" in text:
        send_workflow_example(client, channel)
    elif "task" in text:
        send_task_example(client, channel)
    elif "approval" in text:
        send_approval_example(client, channel, event["user"])


@slack_app.command("/automation")
def handle_automation_command(ack, body, client):
    """Handle /automation slash command"""
    ack()
    
    user_id = body["user_id"]
    channel_id = body["channel_id"]
    
    blocks = [
        create_header_block("🤖 Automation Commands"),
        create_section_block(
            "Available automation commands:\n\n"
            "• *Workflow* - View workflow automation example\n"
            "• *Task* - Create and manage tasks\n"
            "• *Approval* - Request approvals\n"
            "• *Schedule* - Schedule automated tasks"
        ),
        create_divider_block(),
        create_actions_block([
            create_button_block(
                text="🔄 View Workflow",
                action_id="view_workflow_example"
            ),
            create_button_block(
                text="📝 Create Task",
                action_id="open_task_modal"
            ),
            create_button_block(
                text="📋 Request Approval",
                action_id="request_approval"
            )
        ])
    ]
    
    client.chat_postMessage(
        channel=channel_id,
        blocks=blocks,
        text="Automation commands"
    )


@slack_app.action("open_task_modal")
def handle_open_task_modal(ack, body, client):
    """Open task creation modal"""
    ack()
    trigger_id = body["trigger_id"]
    modal = create_task_modal()
    client.views_open(trigger_id=trigger_id, view=modal)


@slack_app.view("create_task_modal")
def handle_task_modal_submit(ack, body, client):
    """Handle task modal submission"""
    ack()
    
    values = body["view"]["state"]["values"]
    user_id = body["user"]["id"]
    
    task_title = values["task_title"]["title_input"]["value"]
    task_description = values.get("task_description", {}).get("description_input", {}).get("value", "")
    task_priority = values["task_priority"]["priority_select"]["selected_option"]["value"]
    task_due_date = values.get("task_due_date", {}).get("due_date_picker", {}).get("selected_date", "")
    
    # Store task
    task = {
        "id": f"task_{datetime.now().timestamp()}",
        "title": task_title,
        "description": task_description,
        "priority": task_priority,
        "due_date": task_due_date,
        "created_by": user_id,
        "created_at": datetime.now().isoformat(),
        "status": "pending"
    }
    automation_store["tasks"].append(task)
    
    # Send confirmation message
    blocks = [
        create_header_block("✅ Task Created"),
        create_section_block(
            f"*Title:* {task_title}\n"
            f"*Priority:* {task_priority}\n"
            f"*Due Date:* {task_due_date if task_due_date else 'Not set'}\n"
            f"*Status:* Pending"
        )
    ]
    
    client.chat_postMessage(
        channel=body["user"]["id"],
        blocks=blocks,
        text=f"Task created: {task_title}"
    )


@slack_app.action("view_workflow_example")
def handle_view_workflow(ack, body, client):
    """Handle workflow view action"""
    ack()
    send_workflow_example(client, body["channel"]["id"])


@slack_app.action("request_approval")
def handle_request_approval(ack, body, client):
    """Handle approval request action"""
    ack()
    user_id = body["user"]["id"]
    channel_id = body["channel"]["id"]
    send_approval_example(client, channel_id, user_id)


@slack_app.action("approve_request")
def handle_approve(ack, body, client):
    """Handle approval action"""
    ack()
    request_id = body["actions"][0]["value"]
    user_id = body["user"]["id"]
    channel_id = body["channel"]["id"]
    
    # Update approval status
    for approval in automation_store["approvals"]:
        if approval["id"] == request_id:
            approval["status"] = "approved"
            approval["approved_by"] = user_id
            approval["approved_at"] = datetime.now().isoformat()
            break
    
    # Update message
    blocks = [
        create_header_block("✅ Request Approved"),
        create_section_block(f"Request `{request_id}` has been approved by <@{user_id}>"),
        create_context_block([
            {
                "type": "mrkdwn",
                "text": f"Approved at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            }
        ])
    ]
    
    client.chat_update(
        channel=channel_id,
        ts=body["message"]["ts"],
        blocks=blocks,
        text="Request approved"
    )


@slack_app.action("reject_request")
def handle_reject(ack, body, client):
    """Handle rejection action"""
    ack()
    request_id = body["actions"][0]["value"]
    user_id = body["user"]["id"]
    channel_id = body["channel"]["id"]
    
    # Update approval status
    for approval in automation_store["approvals"]:
        if approval["id"] == request_id:
            approval["status"] = "rejected"
            approval["rejected_by"] = user_id
            approval["rejected_at"] = datetime.now().isoformat()
            break
    
    # Update message
    blocks = [
        create_header_block("❌ Request Rejected"),
        create_section_block(f"Request `{request_id}` has been rejected by <@{user_id}>"),
        create_context_block([
            {
                "type": "mrkdwn",
                "text": f"Rejected at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            }
        ])
    ]
    
    client.chat_update(
        channel=channel_id,
        ts=body["message"]["ts"],
        blocks=blocks,
        text="Request rejected"
    )


# ==================== Helper Functions ====================

def send_workflow_example(client: WebClient, channel: str):
    """Send workflow example message"""
    workflow_steps = [
        {"name": "Data Collection", "description": "Collecting data from sources", "status": "completed"},
        {"name": "Data Processing", "description": "Processing collected data", "status": "completed"},
        {"name": "Report Generation", "description": "Generating final report", "status": "in_progress"},
        {"name": "Notification", "description": "Sending notifications", "status": "pending"}
    ]
    
    blocks = create_workflow_message(
        title="Daily Report Automation",
        status="In Progress",
        description="Automated daily report generation workflow",
        steps=workflow_steps
    )
    
    client.chat_postMessage(
        channel=channel,
        blocks=blocks,
        text="Workflow status"
    )


def send_task_example(client: WebClient, channel: str):
    """Send task example message"""
    blocks = [
        create_header_block("📝 Task Management"),
        create_section_block(
            "Click the button below to create a new task using our interactive modal."
        ),
        create_actions_block([
            create_button_block(
                text="Create Task",
                action_id="open_task_modal"
            )
        ])
    ]
    
    client.chat_postMessage(
        channel=channel,
        blocks=blocks,
        text="Task management"
    )


def send_approval_example(client: WebClient, channel: str, user_id: str):
    """Send approval request example"""
    request_id = f"req_{datetime.now().timestamp()}"
    
    approval = {
        "id": request_id,
        "requester": user_id,
        "type": "Budget Approval",
        "details": "Requesting approval for Q4 marketing budget",
        "status": "pending",
        "created_at": datetime.now().isoformat()
    }
    automation_store["approvals"].append(approval)
    
    blocks = create_approval_message(
        requester=f"<@{user_id}>",
        request_type="Budget Approval",
        details="Requesting approval for Q4 marketing budget",
        request_id=request_id
    )
    
    client.chat_postMessage(
        channel=channel,
        blocks=blocks,
        text="Approval request"
    )


# ==================== Scheduled Automation Tasks ====================

def send_daily_report():
    """Send daily automation report"""
    try:
        # Get a channel ID (replace with your channel ID)
        channel_id = os.getenv("SLACK_CHANNEL_ID", "#general")
        
        blocks = [
            create_header_block("📊 Daily Automation Report"),
            create_section_block(
                f"*Date:* {datetime.now().strftime('%Y-%m-%d')}\n"
                f"*Total Tasks:* {len(automation_store['tasks'])}\n"
                f"*Pending Approvals:* {len([a for a in automation_store['approvals'] if a['status'] == 'pending'])}\n"
                f"*Active Workflows:* {len(automation_store['workflows'])}"
            ),
            create_divider_block(),
            create_section_block("*Summary*\nAll systems are running smoothly! ✅")
        ]
        
        slack_client.chat_postMessage(
            channel=channel_id,
            blocks=blocks,
            text="Daily automation report"
        )
        logger.info("Sent daily report")
    except Exception as e:
        logger.error(f"Error sending daily report: {e}")


def check_pending_tasks():
    """Check and notify about pending tasks"""
    try:
        pending_tasks = [t for t in automation_store["tasks"] if t["status"] == "pending"]
        if pending_tasks:
            channel_id = os.getenv("SLACK_CHANNEL_ID", "#general")
            
            task_list = "\n".join([f"• {t['title']} (Priority: {t['priority']})" for t in pending_tasks[:5]])
            
            blocks = [
                create_header_block("⏰ Pending Tasks Reminder"),
                create_section_block(f"You have {len(pending_tasks)} pending task(s):\n\n{task_list}"),
                create_actions_block([
                    create_button_block(
                        text="View All Tasks",
                        action_id="view_tasks"
                    )
                ])
            ]
            
            slack_client.chat_postMessage(
                channel=channel_id,
                blocks=blocks,
                text="Pending tasks reminder"
            )
            logger.info(f"Sent reminder for {len(pending_tasks)} pending tasks")
    except Exception as e:
        logger.error(f"Error checking pending tasks: {e}")


# Schedule daily report at 9 AM
scheduler.add_job(
    send_daily_report,
    trigger=CronTrigger(hour=9, minute=0),
    id="daily_report",
    name="Send Daily Automation Report",
    replace_existing=True
)

# Schedule task reminder every hour
scheduler.add_job(
    check_pending_tasks,
    trigger=CronTrigger(minute=0),
    id="task_reminder",
    name="Check Pending Tasks",
    replace_existing=True
)


# ==================== FastAPI Routes ====================

@app.post("/slack/events")
async def slack_events(request: Request):
    """Handle Slack events"""
    return await slack_handler.handle(request)


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Slack Automation Bot",
        "status": "running",
        "scheduled_jobs": len(scheduler.get_jobs())
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host=settings.host,
        port=settings.port,
        reload=True
    )

