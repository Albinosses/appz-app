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
                        padding="0.5em 1em",
                        width="200px",
                        on_click=rx.redirect('/requirements-analysis')
                    ),
                    rx.button(
                        "Planning",
                        padding="0.5em 1em",
                        width="200px",
                        on_click=rx.redirect('/planning')
                    ),
                    rx.button(
                        "Modeling",
                        padding="0.5em 1em",
                        width="200px",
                        on_click=rx.redirect('/modeling')
                    ),
                    rx.button(
                        "Developing",
                        padding="0.5em 1em",
                        width="200px",
                        on_click=rx.redirect('/developing')
                    ),
                    rx.button(
                        "Testing",
                        padding="0.5em 1em",
                        width="200px",
                        on_click=rx.redirect('/testing')
                    ),
                    rx.button(
                        "Result analysis",
                        padding="0.5em 1em",
                        width="200px",
                        on_click=rx.redirect('/result-analysis'),
                        height="2em",
                    ),

                    spacing="1em",
                    justify_content="center",
                    align_items="center",
                    width="100%",
                ),
            width="100%",
            justify_content="center",
            align_items="center",
            padding="20px",
            border_radius="12px",
        )