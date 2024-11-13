import reflex as rx
from rxconfig import config
from typing import List, Dict
from reflex_calendar import calendar
import plotly.express as px

selected_course_data = None

class State(rx.State):
    """The app state."""
    courses: List[Dict[str, int]] = [
        {"name": "Introduction to Reflex", "progress": 30, "avg_progress": 60, "times_per_section" : [30, 45, 25], "avg_times_per_section" : [10, 15, 15], "assignment_scores" : [85, 90, 70], "avg_assignment_scores" : [70, 83, 75]},
        {"name": "Advanced Reflex Techniques", "progress": 60, "avg_progress": 60,"times_per_section" : [20, 65, 15], "avg_times_per_section" : [10, 15, 15], "assignment_scores" : [55, 80, 55], "avg_assignment_scores" : [60, 68, 65]},
        {"name": "Reflex UI Design", "progress": 85, "avg_progress": 60,"times_per_section" : [10, 10, 15], "avg_times_per_section" : [10, 15, 15],"assignment_scores" : [50, 60, 70], "avg_assignment_scores" : [65, 64, 70]},
    ]

    selected_section: Dict[str, int] = {}

    @rx.event
    def set_section(self, str):
        self.selected_section = str

    selected_course: List[Dict[str, int]] = None

    @rx.event
    def set_course(self, course_name: str):
        """Set the selected course with decomposed list values into array format."""
        course = next(
            (course for course in self.courses if course["name"] == course_name),
            None
        )

        if course:
            # Decompose lists into separate objects within an array
            decomposed_course = [
                {
                    "name": course["name"],
                    "progress": course["progress"],
                    "avg_progress": course["avg_progress"],
                    "times_per_section": course["times_per_section"][i],
                    "avg_times_per_section": course["avg_times_per_section"][i],
                    "assignment_scores": course["assignment_scores"][i],
                    "avg_assignment_scores": course["avg_assignment_scores"][i]
                }
                for i in range(len(course["times_per_section"]))
            ]
            self.selected_course = decomposed_course
            return rx.redirect(f"/course/{course_name}")
    

def styled_course_component(course) -> rx.Component:
    """Styled course component with a course name, progress bar, and inactive buttons."""
    return rx.hstack(
        # Course name with padding
        rx.text(course["name"], width="20%", font_size="18px", font_weight="bold", padding="0 20px"),
        
        # Progress bar with consistent size
        rx.progress(
            value=course["progress"],  # Progress value for each course
            max_value=100,
            width="50%",  # Ensure it takes up full width
            height="10px",  # Fixed height for the progress bar
            border_radius="5px",
            background="lightgrey",
            color="dodgerblue",  # Color for progress bar
            padding="0px"  # Removed padding to avoid unwanted space inside progress
        ),
        
        # Button for statistics
        rx.button("Statistics", width="15%", padding="5px 15px", margin="0 15px"),
        
        # Button to go to course
        rx.button("Go to course", width="15%", padding="5px 15px", margin="0 15px", on_click=State.set_course(course["name"])),
        
        spacing="0",  # Disable default spacing between items
        align_items="center",  # Align items vertically in the center
        border="1px solid lightgray",  # Border around the course component
        border_radius="8px",  # Rounded corners
        padding="10px",  # Padding inside the component
        background="white",  # Background color of the course component
        box_shadow="0px 2px 8px rgba(0, 0, 0, 0.1)"  # Shadow for visual appeal
    )

def header() -> rx.Component:
    """Styled header/navbar with navigation items."""
    return rx.container(
        rx.hstack(
            
            # Navbar items
            rx.hstack(
                rx.button("Home", width="10%", margin="0 10px", on_click=lambda: State.set_section("home")),
                rx.button("Requirements analysis", width="10%", margin="0 10px"),
                rx.button("Planning", width="10%", margin="0 10px"),
                rx.button("Modeling", width="10%", margin="0 10px"),
                rx.button("Developing", width="10%", margin="0 10px"),
                rx.button("Testing", width="10%", margin="0 10px"),
                rx.button("Result analysis", width="10%", margin="0 10px", on_click=lambda: State.set_section("analysis")),
            ),
            align_items="center",  # Center items vertically
            width="100%",  # Full width of the page
            padding="10px",  # Padding inside the header
            background="dodgerblue",  # Background color of the navbar
            color="white",  # Text color for navbar items
            box_shadow="0 4px 8px rgba(0, 0, 0, 0.1)",  # Shadow effect
        ),
        width="100%",  # Full width for the header
        position="relative",  # Fix the header to the top
        top="0",
        left="0",  # Align the header at the top
        z_index="1000",  # Ensure it stays above other elements
    )


def index() -> rx.Component:
    # Welcome Page (Index)
    
    return rx.container(
        header(),
        rx.cond(
            State.selected_section == "home",
            rx.container(
                rx.text("Welcome to the Home section!", font_size="24px", padding="20px"),
            )
        ),
        rx.cond(
            State.selected_section == "analysis",
            rx.container(rx.hstack(
                # Calendar component on the left side
                rx.container(
                    calendar(locale="en-US", calendar_id="en-US"),
                    width="50%",  # 50% width
                    height="300px",
                    padding="10px",  # Inner padding
                ),
            
            # Notifications list on the right side
                rx.container(
                    rx.vstack(
                        # Styled notification list
                        rx.container(
                            rx.list.unordered(
                                rx.list.item("Notification 1", font_size="16px", padding="10px 15px"),
                                rx.list.item("Notification 2", font_size="16px", padding="10px 15px"),
                                rx.list.item("Notification Yii3bAn", font_size="16px", padding="10px 15px"),
                            ),
                            width="100%",
                            height="300px",
                            border="1px solid #ddd",  # Light border
                            border_radius="10px",  # Rounded corners
                            background="white",  # Background color
                            padding="10px",  # Inner padding
                            box_shadow="0 2px 8px rgba(0, 0, 0, 0.1)",  # Subtle shadow
                        ),
                    ),
                    width="50%",  # 50% width
                ),
            ),
            
            # Color mode toggle button at the top-right corner
            rx.color_mode.button(position="top-right"),
            
            # Render the courses below the calendar and notifications
            rx.foreach(State.courses, styled_course_component),
            )
        )
    )


def course_details() -> rx.Component:
    return rx.container(
        rx.heading("Course time spent"),
        rx.recharts.bar_chart(
        rx.recharts.bar(
            data_key="times_per_section",
            stroke=rx.color("accent", 9),
            fill=rx.color("accent", 8),
        ),
        rx.recharts.bar(
            data_key="avg_times_per_section",
            stroke=rx.color("green", 9),
            fill=rx.color("green", 8),
        ),
        rx.recharts.x_axis(),
        rx.recharts.y_axis(),
        data=State.selected_course,
        width="50%",
        height= 600,
        ),

        rx.heading("Marks"),
        rx.recharts.bar_chart(
        rx.recharts.bar(
            data_key="assignment_scores",
            stroke=rx.color("accent", 9),
            fill=rx.color("accent", 8),
        ),
        rx.recharts.bar(
            data_key="avg_assignment_scores",
            stroke=rx.color("green", 9),
            fill=rx.color("green", 8),
        ),
        rx.recharts.x_axis(),
        rx.recharts.y_axis(),
        data=State.selected_course,
        width="50%",
        height= 600,
        ),

        rx.heading("Progress"),
        rx.recharts.radial_bar_chart(
        rx.recharts.radial_bar(
            data_key="progress",
            min_angle=90,
            background=True,
            label={
                "fill": "#666",
                "position": "insideStart",
            },
        ),
        rx.recharts.radial_bar(
            data_key="avg_progress",
            min_angle=15,
        ),
        inner_radius="10%",
        outer_radius="80%",
        start_angle=180,
        end_angle=0,
        data=[State.selected_course[0]],
        color=rx.color("accent", 9),   
        width=600,
        height=500,
        radial_axis={"domain": [0, 100]},
        legend={"verticalAlign": "middle", "align": "right"}
        )
    )


app = rx.App()
app.add_page(index)
app.add_page(course_details, route="/course/[name]")
