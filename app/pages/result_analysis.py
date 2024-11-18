"""The dashboard page."""
import json
from typing import Dict, List

from reflex_calendar import calendar

from utils.json_converter import CourseDataAdapter
from .. import styles
from ..templates import template

import reflex as rx

courseData = CourseDataAdapter()


class State(rx.State):
    courses: List[Dict[str, int]] = courseData.get_course_statistics("app/jsons/user_courses_example.json")

    @rx.event
    def get_course(self, course):
        return rx.redirect(f"/course/{course}")


def styled_course_component(course) -> rx.Component:
    """Styled course component with a course name, progress bar, and inactive buttons."""
    return rx.hstack(
        rx.text(course["name"], width="40%", font_size="18px", font_weight="bold", padding="0 20px"),

        rx.progress(
            value=course["progress"],
            max_value=100,
            width="50%",
            height="10px",
            border_radius="5px",
            color="lightblue",
            padding="0px"
        ),

        rx.button("Statistics", width="15%", padding="5px 15px", margin="0 15px",
                  on_click=State.get_course(course["course_id"])),

        rx.button("Go to course", width="15%", padding="5px 15px", margin="0 15px"),

        spacing="0",
        align_items="center",
        border="1px solid lightgray",
        border_radius="8px",
        padding="10px",
        box_shadow="0px 2px 8px rgba(0, 0, 0, 0.1)",
        margin="10px 0px 0px 0px",
    )


@template(route="/result-analysis", title="Result Analysis")
def result_analysis() -> rx.Component:
    return rx.container(
        rx.container(
            rx.hstack(
                rx.container(
                    calendar(locale="en-US", calendar_id="en-US"),
                    width="40%",  # 50% width
                ),

                rx.container(
                    rx.vstack(
                        rx.container(
                            rx.list(
                                rx.list.item("AI Fundamentals: You missed 3 tasks", margin='5px', padding="5px 10px",
                                             background=styles.accent_bg_color, font_size="15px", border_radius='5px'),
                                rx.list.item("AWS Crash Course: You missed 2 tasks", margin='5px', padding="5px 10px",
                                             background=styles.accent_bg_color, font_size="15px", border_radius='5px'),
                            ),
                            width="100%",
                            height="280px",
                            border="1px solid #ddd",
                            border_radius="10px",
                            box_shadow="0 2px 8px rgba(0, 0, 0, 0.1)",
                        ),
                    ),
                    width="50%",
                ),
            ),
            rx.foreach(State.courses, styled_course_component),
        ),
        width="100%",
    )
