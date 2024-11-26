"""The dashboard page."""
import json
from ..templates import template
import reflex as rx

class State(rx.State):
    pass

@template(route="/", title="Main")
def main() -> rx.Component:
    return rx.container(
        rx.flex(
            rx.button(
                "Requirements analysis",
                padding="1em 2em",  # Larger padding for bigger buttons
                font_size="16px",  # Increase font size for better visibility
                width="250px",  # Wider buttons
                height="60px",  # Increase height of buttons
                on_click=rx.redirect('/requirements-analysis'),
                background="#2980B9",
                color="white",
                border_radius="8px",
                box_shadow="0 4px 8px rgba(0, 0, 0, 0.1)",
                hover={"background": "#3498DB"},
                transition="background 0.3s",
            ),
            rx.button(
                "Planning",
                padding="1em 2em",
                font_size="16px",
                width="250px",
                height="60px",
                on_click=rx.redirect('/planning'),
                background="#27AE60",
                color="white",
                border_radius="8px",
                box_shadow="0 4px 8px rgba(0, 0, 0, 0.1)",
                hover={"background": "#2ECC71"},
                transition="background 0.3s",
            ),
            rx.button(
                "Modeling",
                padding="1em 2em",
                font_size="16px",
                width="250px",
                height="60px",
                on_click=rx.redirect('/modeling'),
                background="#F39C12",
                color="white",
                border_radius="8px",
                box_shadow="0 4px 8px rgba(0, 0, 0, 0.1)",
                hover={"background": "#F1C40F"},
                transition="background 0.3s",
            ),
            rx.button(
                "Developing",
                padding="1em 2em",
                font_size="16px",
                width="250px",
                height="60px",
                on_click=rx.redirect('/developing'),
                background="#E74C3C",
                color="white",
                border_radius="8px",
                box_shadow="0 4px 8px rgba(0, 0, 0, 0.1)",
                hover={"background": "#C0392B"},
                transition="background 0.3s",
            ),
            rx.button(
                "Testing",
                padding="1em 2em",
                font_size="16px",
                width="250px",
                height="60px",
                on_click=rx.redirect('/testing'),
                background="#9B59B6",
                color="white",
                border_radius="8px",
                box_shadow="0 4px 8px rgba(0, 0, 0, 0.1)",
                hover={"background": "#8E44AD"},
                transition="background 0.3s",
            ),
            rx.button(
                "Result analysis",
                padding="1em 2em",
                font_size="16px",
                width="250px",
                height="60px",
                on_click=rx.redirect('/result-analysis'),
                background="#34495E",
                color="white",
                border_radius="8px",
                box_shadow="0 4px 8px rgba(0, 0, 0, 0.1)",
                hover={"background": "#2C3E50"},
                transition="background 0.3s",
            ),
            spacing="1.5em",  # Increased spacing between buttons
            justify_content="center",
            align_items="center",
            width="100%",
            wrap="wrap",  # Allow buttons to wrap if necessary
        ),
        width="100%",
        justify_content="center",
        align_items="center",
        padding="30px",  # Increased padding for a better look
    )
