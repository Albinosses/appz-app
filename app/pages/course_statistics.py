import json
import reflex as rx
from typing import List, Dict


from utils.avg_time_calculator import AverageTaskTimeCalculatorFactory, AverageModuleTimeCalculatorFactory
from utils.avg_score_calculator import AverageTaskScoreCalculatorFactory, AverageModuleScoreCalculatorFactory
from utils.utils import merge_module_progress, merge_task_progress
from ..templates import template

courses = json.load(open("app/jsons/user_courses_example.json"))
student_progress = json.load(open("app/jsons/student_course_statistics_example.json"))
all_students_progress = json.load(open("app/jsons/all_students_course_statistics_example.json"))

AvgModuleTimeCalculator = AverageModuleTimeCalculatorFactory().create_time_calculator()
AvgTaskTimeCalculator = AverageTaskTimeCalculatorFactory().create_time_calculator()
AvgModuleScoreCalculator = AverageModuleScoreCalculatorFactory().create_score_calculator()
AvgTaskScoreCalculator = AverageTaskScoreCalculatorFactory().create_score_calculator()

class State(rx.State):
    courses: List[Dict[str, int]] = courses
    course_time_data: List[Dict[str, list]] = merge_module_progress(student_progress, AvgModuleTimeCalculator.get_avg_time(all_students_progress), type='times')
    course_score_data: List[Dict[str, list]] = merge_module_progress(student_progress, AvgModuleScoreCalculator.get_avg_score(all_students_progress), type='scores')
    selected_section: Dict[str, int] = {}
    module: str = ''
    modules: List[str] = ["All modules"] + [mdl["name"] for mdl in course_time_data]

    selected_course: Dict[str, int] = None

    @rx.event
    def set_module(self, str):
        self.module = str
        if str == 'All modules':
            self.course_time_data = merge_module_progress(student_progress, AvgModuleTimeCalculator.get_avg_time(all_students_progress), type='times')
            self.course_score_data = merge_module_progress(student_progress, AvgModuleScoreCalculator.get_avg_score(all_students_progress), type='scores')
        else:
            self.course_time_data = merge_task_progress(student_progress, AvgTaskTimeCalculator.get_avg_time(all_students_progress, str), 'times', str)
            self.course_score_data = merge_task_progress(student_progress, AvgTaskScoreCalculator.get_avg_score(all_students_progress, str), 'scores', str)


@template(route="/course/[name]", title="Course Details")
def course_statistics() -> rx.Component:
    return rx.container(
        rx.container(
            rx.select(State.modules, default_value='All modules', on_change=State.set_module, margin = "50 0 0 0px")
        ),
        rx.heading("Course time spent"),
        rx.recharts.bar_chart(
            rx.recharts.bar(
                data_key="Student progress",
                stroke=rx.color("accent", 9),
                fill=rx.color("accent", 8),
            ),
            rx.recharts.bar(
                data_key="Average progress",
                stroke=rx.color("green", 9),
                fill=rx.color("green", 8),
            ),
            rx.recharts.x_axis(data_key="name"),
            rx.recharts.y_axis(),
            rx.recharts.legend(),
            data=State.course_time_data,
            height=600,
        ),
        rx.heading("Course scores"),
        rx.recharts.bar_chart(
            rx.recharts.bar(
                data_key="Student progress",
                stroke=rx.color("accent", 9),
                fill=rx.color("accent", 8),
            ),
            rx.recharts.bar(
                data_key="Average progress",
                stroke=rx.color("green", 9),
                fill=rx.color("green", 8),
            ),
            rx.recharts.x_axis(data_key="name"),
            rx.recharts.y_axis(),
            rx.recharts.legend(),
            data=State.course_score_data,
            height=600,
        ),
        width="100%",
    )
