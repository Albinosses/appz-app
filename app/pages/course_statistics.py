import json
import reflex as rx
from typing import List, Dict

from reflex import redirect

from utils.avg_calculators import CachingAverageCalculator, DefaultAverageCalculator
from utils.chart_factory import ComparisonChartFactory
from utils.connector_factory import DataConnectorFactory
from utils.utils import merge_module_progress, merge_task_progress

from ..templates import template

bar_chart_builder = ComparisonChartFactory.get_chart_builder("bar")
# line_chart_builder = ComparisonChartFactory.get_chart_builder("line")
averageCalculator = CachingAverageCalculator(DefaultAverageCalculator())
dataConnector = DataConnectorFactory.get_connector('json')

all_students_progress = dataConnector.get_all_students_progress('asdc3rwe')
student_progress = dataConnector.get_student_progress('t375f2d', 'asfvdx')


class State(rx.State):
    average_students_time = averageCalculator.get_avg_for_module(all_students_progress, 'times')
    course_time_data: List[Dict[str, list]] = merge_module_progress(student_progress, average_students_time,
                                                                    type='times')

    average_students_score = averageCalculator.get_avg_for_module(all_students_progress, 'scores')
    course_score_data: List[Dict[str, list]] = merge_module_progress(student_progress, average_students_score,
                                                                     type='scores')

    modules: List[str] = ["All modules"] + [mdl["name"] for mdl in course_time_data]
    module: str = "All modules"

    @rx.event
    def set_module(self, str):
        self.module = str
        if str == 'All modules':
            average_students_time = averageCalculator.get_avg_for_module(all_students_progress, 'times')
            self.course_time_data = merge_module_progress(student_progress, average_students_time, type='times')
            average_students_score = averageCalculator.get_avg_for_module(all_students_progress, 'scores')
            self.course_score_data = merge_module_progress(student_progress, average_students_score, type='scores')
        else:
            average_students_time = averageCalculator.get_avg_for_task(all_students_progress, str, 'times')
            self.course_time_data = merge_task_progress(student_progress, average_students_time, 'times', str)
            average_students_score = averageCalculator.get_avg_for_task(all_students_progress, str, 'scores')
            self.course_score_data = merge_task_progress(student_progress, average_students_score, 'scores', str)


@template(route="/course/[name]", title="Course Details")
def course_statistics() -> rx.Component:
    return rx.vstack(
        rx.button("<--", width='100px' , on_click=rx.redirect("/result-analysis"), margin_bottom='25px'),
        rx.select(State.modules, value=State.module, on_change=State.set_module, width='220px'),
        rx.heading("Course time spent"),
        bar_chart_builder.build_chart(State.course_time_data, "Student progress", "Average progress", 600),
        rx.heading("Course scores"),
        bar_chart_builder.build_chart(State.course_score_data, "Student progress", "Average progress", 600),
        width="100%",
    )