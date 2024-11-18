import json
import reflex as rx
from typing import List, Dict

from utils.avg_calculators import get_avg_for_task, get_avg_for_module
from utils.chart_factory import ComparisonChartFactory
from utils.json_converter import CourseDataAdapter
from utils.utils import merge_module_progress, merge_task_progress
from ..templates import template

courseData = CourseDataAdapter()
student_progress = courseData.get_course_statistics("app/jsons/student_course_statistics_example.json")
all_students_progress = courseData.get_course_statistics("app/jsons/all_students_course_statistics_example.json")

bar_chart_builder = ComparisonChartFactory.get_chart_builder("bar")
# line_chart_builder = ComparisonChartFactory.get_chart_builder("line")

class State(rx.State):
    average_students_time = get_avg_for_module(all_students_progress, 'times')
    course_time_data: List[Dict[str, list]] = merge_module_progress(student_progress, average_students_time, type='times')
    average_students_score = get_avg_for_module(all_students_progress, 'scores')
    course_score_data: List[Dict[str, list]] = merge_module_progress(student_progress, average_students_score, type='scores')
    selected_section: Dict[str, int]= {}
    module: str = ''
    modules: List[str] = ["All modules"] + [mdl["name"] for mdl in course_time_data]

    @rx.event
    def set_module(self, str):
        self.module = str
        if str == 'All modules':
            average_students_time = get_avg_for_module(all_students_progress, 'times')
            self.course_time_data = merge_module_progress(student_progress, average_students_time, type='times')
            average_students_score = get_avg_for_module(all_students_progress, 'scores')
            self.course_score_data = merge_module_progress(student_progress, average_students_score, type='scores')
        else:
            average_students_time = get_avg_for_task(all_students_progress, str, 'times')
            self.course_time_data = merge_task_progress(student_progress, average_students_time, 'times', str)
            average_students_score = get_avg_for_task(all_students_progress, str, 'scores')
            self.course_score_data = merge_task_progress(student_progress, average_students_score, 'scores', str)


@template(route="/course/[name]", title="Course Details")
def course_statistics() -> rx.Component:
    return rx.container(
        rx.container(
            rx.select(State.modules, default_value='All modules', on_change=State.set_module, margin = "50 0 0 0px")
        ),
        rx.heading("Course time spent"),
        bar_chart_builder.build_chart(State.course_time_data, "Student progress", "Average progress", 600),
        rx.heading("Course scores"),
        bar_chart_builder.build_chart(State.course_score_data, "Student progress", "Average progress", 600),
        width="100%",
    )
