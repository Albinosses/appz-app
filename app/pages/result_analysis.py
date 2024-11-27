"""The dashboard page."""
import json
from typing import Dict, List

from reflex import color
from reflex_calendar import calendar

from utils.connector_factory import DataConnectorFactory
from .. import styles
from ..templates import template

import reflex as rx

dataConnector = DataConnectorFactory.get_connector('json')


class State(rx.State):
    courses: List[Dict[str, int]] = dataConnector.get_student_courses('as32rf3es')
    print(courses)

    @rx.event
    def get_course(self, course):
        return rx.redirect(f"/course/{course}")


class NotificationState(rx.State):
    """State to manage notifications."""
    notifications: List[Dict[str, str]] = [
        {"id": 1, "title": "AI Fundamentals",
         "description": "You missed 6 tasks. This is a longer detailed explanation about the missed tasks and their impact on your progress.",
         "timestamp": "28.10.24 at 12:53"},
        {"id": 2, "title": "Kotlin Essentials",
         "description": "We have something important to share. Here's more context about the notification and why it matters.",
         "timestamp": "26.10.24 at 11:40"},
        {"id": 3, "title": "AI Fundamentals",
         "description": "You missed 4 tasks. These tasks are critical for the upcoming assessments.",
         "timestamp": "25.10.24 at 14:32"},
    ]

    expanded_notification: int = -1  # Store the ID of the expanded notification (-1 means none)

    @rx.event
    def toggle_expand(self, notification_id: int):
        """Toggle expansion of a notification."""
        self.expanded_notification = (
            -1 if self.expanded_notification == notification_id else notification_id
        )

    @rx.event
    def delete_notification(self, notification_id: int):
        """Delete a notification by its ID."""
        self.notifications = [
            notif for notif in self.notifications if notif["id"] != notification_id
        ]
        if self.expanded_notification == notification_id:
            self.expanded_notification = -1


def styled_course_component(course) -> rx.Component:
    """Styled course component with a course name, progress bar, and buttons."""
    return rx.hstack(
        # Course Name
        rx.text(
            course["name"],
            width="200px",
            font_size="18px",
            font_weight="bold",
            padding="0 20px",
        ),
        # Progress Bar
        rx.progress(
            value=course["progress"],
            max_value=100,
            width="10em",
            height="12px",
            border_radius="8px",
            color=rx.color("accent", 1),
            background="#34495E",
        ),
        rx.text(f"{course["progress"]}%", weight="bold"),
        # Buttons
        rx.hstack(
            rx.button(
                "Statistics",
                on_click=State.get_course(course["course_id"]),
                padding="10px 20px",
                margin="5px",
                font_size="14px",
                color="white",
                background="#2980B9",
                border_radius="5px",
                hover={"background": "#3498DB"},
                transition="background 0.2s",
            ),
            rx.button(
                "Go to course",
                padding="10px 20px",
                font_size="14px",
                margin="5px",

                color="white",
                background="#27AE60",
                border_radius="5px",
                transition="background 0.2s",
            ),
            spacing="15px",
        ),
        align_items="center",
        border_radius="8px",
        padding="10px",
        box_shadow="0 4px 8px rgba(0, 0, 0, 0.3)",
        margin="10px 0px 0px 0px",
        width="910px",
        background=styles.accent_bg_color,

    )


def render_notification_list() -> rx.Component:
    """Render a dynamic list of notifications with scroll capability."""
    return rx.container(
        rx.text('Notifications', weight='bold', font_size="20px", margin="10px 0px 5px 20px"),
        rx.box(
            rx.foreach(
                NotificationState.notifications,
                lambda notif: notification_item(
                    notif,
                    NotificationState.delete_notification,
                    NotificationState.toggle_expand,
                    NotificationState.expanded_notification == notif["id"],
                ),
            ),
            max_height="300px",  # Increased height for better readability
            overflow_y="auto",  # Enable scrolling
            background=styles.accent_bg_color,
            border_radius="10px",
            width="32em",
            height="18em",
        ),
        background=styles.accent_bg_color,
        border_radius="10px",
        width="34em",
        height="24em",
        box_shadow="0 4px 8px rgba(0, 0, 0, 0.3)",

    )


def notification_item(
        notif: Dict[str, str],
        delete_action,
        toggle_action,
        is_expanded: rx.Var,
) -> rx.Component:
    """Create a styled notification item with expand and delete buttons."""
    # Truncate description for the preview

    return rx.box(
        rx.vstack(
            # Header Section
            rx.hstack(
                rx.text(
                    notif["title"],
                    font_weight="bold",
                    flex="1",
                    font_size="16px",
                    margin='0 0 0 0.5em'
                ),
                rx.text(
                    notif["timestamp"],
                    color='gray',
                    font_size="12px",
                    flex="0.5",
                ),
                rx.button(
                    rx.cond(
                        is_expanded,
                        "Collapse",
                        "Expand",
                    ),
                    color='white',
                    on_click=lambda: toggle_action(notif["id"]),
                    background="#2980B9",
                    border_radius="5px",
                    font_size="12px",
                    hover={"background": "#3498DB"},
                    transition="background 0.2s",
                    width="70px",
                ),
                rx.button(
                    "Delete",
                    color='white',
                    on_click=lambda: delete_action(notif["id"]),
                    background="#E74C3C",
                    border_radius="5px",
                    font_size="12px",
                    hover={"background": "#C0392B"},
                    transition="background 0.2s",
                    width="70px",
                ),
                spacing="20px",
                align_items="center",
            ),
            # Expanded Content
            rx.cond(
                is_expanded,
                rx.text(
                    notif["description"],
                    margin_top="10px",
                    font_size="14px",
                    margin='0 0 0 0.5em'

                ),
                rx.text(
                    notif["description"][:60] + '...',
                    margin_top="10px",
                    font_size="14px",
                    margin='0 0 0 0.5em'

                ),
            ),
        ),
        padding="15px",
        margin="20px 20px 20px 20px",
        background=rx.color("accent", 1),
        border_radius="10px",
        box_shadow="0 2px 6px rgba(0, 0, 0, 0.2)",
        overflow="hidden",
    )


@template(route="/result-analysis", title="Result Analysis")
def result_analysis() -> rx.Component:
    """Main page displaying notifications and other components."""
    return rx.hstack(
        rx.container(
            rx.hstack(
                rx.container(
                    rx.text('Your Activity', weight='bold', font_size="20px", margin="10px 0px 5px 10px"),
                    calendar(
                        locale="en-US",
                        calendar_id="en-US",
                        border_radius="10px",
                        width="300px",
                        justify="center",
                        align="center",
                        margin="20px 0px 0px 0px"
                    ),
                    box_shadow="0 4px 8px rgba(0, 0, 0, 0.3)",
                    background=styles.accent_bg_color,
                    height="24em",
                    border_radius="10px",
                ),
                render_notification_list(),
                spacing="30px",
                margin_bottom="20px",
            ),
                rx.vstack(
                    rx.foreach(State.courses, styled_course_component),
                    width="600px",
                ),

        ),
        width="100%",
        justify_content="center",
    )
