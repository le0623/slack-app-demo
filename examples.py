"""
Example usage of Block Kit components
This file demonstrates how to use the Block Kit components in your Slack app
"""
from block_kit_components import (
    create_header_block,
    create_section_block,
    create_button_block,
    create_actions_block,
    create_workflow_message,
    create_approval_message,
    create_task_modal,
    create_dashboard_home_tab
)


def example_simple_message():
    """Example: Simple message with header and section"""
    blocks = [
        create_header_block("Hello from Block Kit! 👋"),
        create_section_block("This is a simple message using Block Kit components.")
    ]
    return blocks


def example_interactive_message():
    """Example: Interactive message with buttons"""
    blocks = [
        create_header_block("Interactive Message"),
        create_section_block("Click a button to interact:"),
        create_actions_block([
            create_button_block(
                text="Option 1",
                action_id="option_1",
                value="1"
            ),
            create_button_block(
                text="Option 2",
                action_id="option_2",
                value="2",
                style="primary"
            ),
            create_button_block(
                text="Cancel",
                action_id="cancel",
                style="danger"
            )
        ])
    ]
    return blocks


def example_workflow_status():
    """Example: Workflow status message"""
    workflow_steps = [
        {"name": "Step 1", "description": "Description of step 1", "status": "completed"},
        {"name": "Step 2", "description": "Description of step 2", "status": "completed"},
        {"name": "Step 3", "description": "Description of step 3", "status": "in_progress"},
        {"name": "Step 4", "description": "Description of step 4", "status": "pending"}
    ]
    
    blocks = create_workflow_message(
        title="Example Workflow",
        status="In Progress",
        description="This is an example workflow automation",
        steps=workflow_steps
    )
    return blocks


def example_approval_request():
    """Example: Approval request message"""
    blocks = create_approval_message(
        requester="John Doe",
        request_type="Budget Approval",
        details="Requesting approval for Q4 marketing budget of $50,000",
        request_id="req_12345"
    )
    return blocks


def example_home_tab():
    """Example: Home tab dashboard"""
    view = create_dashboard_home_tab()
    return view


# Example usage in Slack app:
# from slack_sdk import WebClient
# from examples import example_interactive_message
# 
# client = WebClient(token="your-bot-token")
# blocks = example_interactive_message()
# 
# client.chat_postMessage(
#     channel="#general",
#     blocks=blocks,
#     text="Interactive message"
# )

