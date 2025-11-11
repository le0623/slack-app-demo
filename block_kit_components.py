"""
Block Kit Components for Slack App Automation
Contains reusable Block Kit UI components
"""
from typing import List, Dict, Any, Optional


def create_header_block(text: str) -> Dict[str, Any]:
    """Create a header block"""
    return {
        "type": "header",
        "text": {
            "type": "plain_text",
            "text": text,
            "emoji": True
        }
    }


def create_section_block(text: str, accessory: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Create a section block with optional accessory"""
    block = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": text
        }
    }
    if accessory:
        block["accessory"] = accessory
    return block


def create_button_block(
    text: str,
    action_id: str,
    value: Optional[str] = None,
    style: Optional[str] = None,
    url: Optional[str] = None
) -> Dict[str, Any]:
    """Create a button element"""
    button = {
        "type": "button",
        "text": {
            "type": "plain_text",
            "text": text
        },
        "action_id": action_id
    }
    if value:
        button["value"] = value
    if style:
        button["style"] = style
    if url:
        button["url"] = url
    return button


def create_actions_block(buttons: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Create an actions block with buttons"""
    return {
        "type": "actions",
        "elements": buttons
    }


def create_divider_block() -> Dict[str, Any]:
    """Create a divider block"""
    return {"type": "divider"}


def create_context_block(elements: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Create a context block"""
    return {
        "type": "context",
        "elements": elements
    }


def create_input_block(
    block_id: str,
    label: str,
    element: Dict[str, Any],
    hint: Optional[str] = None,
    optional: bool = False
) -> Dict[str, Any]:
    """Create an input block for modals"""
    block = {
        "type": "input",
        "block_id": block_id,
        "label": {
            "type": "plain_text",
            "text": label
        },
        "element": element
    }
    if hint:
        block["hint"] = {
            "type": "plain_text",
            "text": hint
        }
    if optional:
        block["optional"] = True
    return block


def create_text_input(
    action_id: str,
    placeholder: Optional[str] = None,
    initial_value: Optional[str] = None,
    multiline: bool = False
) -> Dict[str, Any]:
    """Create a text input element"""
    element = {
        "type": "plain_text_input",
        "action_id": action_id
    }
    if placeholder:
        element["placeholder"] = {
            "type": "plain_text",
            "text": placeholder
        }
    if initial_value:
        element["initial_value"] = initial_value
    if multiline:
        element["multiline"] = True
    return element


def create_select_menu(
    action_id: str,
    options: List[Dict[str, str]],
    placeholder: str = "Select an option"
) -> Dict[str, Any]:
    """Create a static select menu"""
    return {
        "type": "static_select",
        "action_id": action_id,
        "placeholder": {
            "type": "plain_text",
            "text": placeholder
        },
        "options": [
            {
                "text": {
                    "type": "plain_text",
                    "text": opt["text"]
                },
                "value": opt["value"]
            }
            for opt in options
        ]
    }


def create_datepicker(action_id: str, initial_date: Optional[str] = None) -> Dict[str, Any]:
    """Create a datepicker element"""
    element = {
        "type": "datepicker",
        "action_id": action_id,
        "placeholder": {
            "type": "plain_text",
            "text": "Select a date"
        }
    }
    if initial_date:
        element["initial_date"] = initial_date
    return element


def create_workflow_message(
    title: str,
    status: str,
    description: str,
    steps: List[Dict[str, str]]
) -> List[Dict[str, Any]]:
    """Create a workflow status message with Block Kit"""
    blocks = [
        create_header_block(f"🔄 {title}"),
        create_section_block(f"*Status:* {status}\n*Description:* {description}"),
        create_divider_block(),
        create_header_block("Workflow Steps")
    ]
    
    for i, step in enumerate(steps, 1):
        status_emoji = "✅" if step.get("status") == "completed" else "⏳"
        blocks.append(
            create_section_block(
                f"{status_emoji} *Step {i}:* {step['name']}\n_{step.get('description', '')}_"
            )
        )
    
    return blocks


def create_task_modal() -> Dict[str, Any]:
    """Create a modal for task creation"""
    return {
        "type": "modal",
        "callback_id": "create_task_modal",
        "title": {
            "type": "plain_text",
            "text": "Create Task"
        },
        "submit": {
            "type": "plain_text",
            "text": "Create"
        },
        "close": {
            "type": "plain_text",
            "text": "Cancel"
        },
        "blocks": [
            create_input_block(
                block_id="task_title",
                label="Task Title",
                element=create_text_input(
                    action_id="title_input",
                    placeholder="Enter task title"
                )
            ),
            create_input_block(
                block_id="task_description",
                label="Description",
                element=create_text_input(
                    action_id="description_input",
                    placeholder="Enter task description",
                    multiline=True
                ),
                optional=True
            ),
            create_input_block(
                block_id="task_priority",
                label="Priority",
                element=create_select_menu(
                    action_id="priority_select",
                    options=[
                        {"text": "High", "value": "high"},
                        {"text": "Medium", "value": "medium"},
                        {"text": "Low", "value": "low"}
                    ],
                    placeholder="Select priority"
                )
            ),
            create_input_block(
                block_id="task_due_date",
                label="Due Date",
                element=create_datepicker(action_id="due_date_picker"),
                optional=True
            )
        ]
    }


def create_approval_message(
    requester: str,
    request_type: str,
    details: str,
    request_id: str
) -> List[Dict[str, Any]]:
    """Create an approval request message"""
    return [
        create_header_block("📋 Approval Request"),
        create_section_block(
            f"*Requester:* {requester}\n"
            f"*Type:* {request_type}\n"
            f"*Details:* {details}"
        ),
        create_divider_block(),
        create_actions_block([
            create_button_block(
                text="✅ Approve",
                action_id="approve_request",
                value=request_id,
                style="primary"
            ),
            create_button_block(
                text="❌ Reject",
                action_id="reject_request",
                value=request_id,
                style="danger"
            ),
            create_button_block(
                text="ℹ️ View Details",
                action_id="view_details",
                value=request_id
            )
        ]),
        create_context_block([
            {
                "type": "mrkdwn",
                "text": f"Request ID: `{request_id}`"
            }
        ])
    ]


def create_dashboard_home_tab() -> Dict[str, Any]:
    """Create a home tab view with dashboard"""
    return {
        "type": "home",
        "blocks": [
            create_header_block("🏠 Automation Dashboard"),
            create_section_block(
                "Welcome to your automation dashboard! Use the buttons below to manage your workflows."
            ),
            create_divider_block(),
            create_section_block("*Quick Actions*"),
            create_actions_block([
                create_button_block(
                    text="📝 Create Task",
                    action_id="open_task_modal"
                ),
                create_button_block(
                    text="🔄 View Workflows",
                    action_id="view_workflows"
                ),
                create_button_block(
                    text="📊 View Reports",
                    action_id="view_reports"
                )
            ]),
            create_divider_block(),
            create_section_block("*Recent Activity*"),
            create_context_block([
                {
                    "type": "mrkdwn",
                    "text": "No recent activity"
                }
            ])
        ]
    }

