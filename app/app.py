import reflex as rx
from rxconfig import config
from typing import List, Dict
from reflex_calendar import calendar
import plotly.express as px

selected_course_data = None

class State(rx.State):
    """The app state."""
    courses: List[Dict[str, int]] = [
        {"name": "Introduction to Reflex", "progress": 30, "times_per_section" : [30, 45, 25], "avg_times_per_section" : [10, 15, 15], "assignment_scores" : [85, 90, 70]},
        {"name": "Advanced Reflex Techniques", "progress": 60,"times_per_section" : [20, 65, 15], "avg_times_per_section" : [10, 15, 15], "assignment_scores" : [55, 80, 55]},
        {"name": "Reflex UI Design", "progress": 85, "times_per_section" : [10, 10, 15], "avg_times_per_section" : [10, 15, 15],"assignment_scores" : [50, 60, 70]},
    ]

    selected_section: Dict[str, int] = {}

    avg_time_per_section: List[int] = [40, 30, 25]

    @rx.event
    def set_section(self, str):
        self.selected_section = str

    selected_course: Dict[str, int] = None

    @rx.event
    def set_course(self, course_name: str):
        """Set the selected course and redirect."""
        course = next(
            (course for course in self.courses if course["name"] == course_name),
            None
        )

        if course:
            self.selected_course = course
            return rx.redirect(f"/course/{course_name}")
        
    def get_course(self) -> str:
        return self._selected_course

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
    name = rx.heading(rx.State.name)


    print(selected_course_data)

    return rx.recharts.bar_chart(
        rx.recharts.bar(
            data_key="progress",
        ),
        rx.recharts.bar(
            data_key="avg_times_per_section",
        ),
        rx.recharts.x_axis(),
        rx.recharts.y_axis(),
        data=State.courses,
        width="50%",
        height= 600,
    )


    # time_fig = px.bar(
    #         x=list(range(1, len(State.selected_course["times_per_section"]) + 1)),
    #         y=State.selected_course["times_per_section"],
    #         title="Time per Course Section",
    #         labels={"x": "Section", "y": "Time (minutes)"},
    #     )
    # time_fig.add_hline(y=course_time_avg, line_color="red", line_dash="dash", annotation_text="Avg Time")


    # return rx.cond(
    #     State.selected_course,
    #     lambda: rx.vstack(
    #         rx.plotly(time_fig, height="300px")
    #     ),
    #         rx.heading("Course not found", font_size="24px", padding="20px")
    #     )

    return name


app = rx.App()
app.add_page(index)
app.add_page(course_details, route="/course/[name]")
