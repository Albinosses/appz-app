from abc import ABC, abstractmethod
import reflex as rx
from typing import List, Dict

class ComparisonChartBuilder(ABC):
    @abstractmethod
    def build_chart(self, data: List[Dict], data_key1: str, data_key2: str, height: int) -> rx.Component:
        pass

class ComparisonBarChartBuilder(ComparisonChartBuilder):
    def build_chart(self, data: List[Dict], data_key1: str, data_key2: str, height: int) -> rx.Component:
        return rx.recharts.bar_chart(
            rx.recharts.bar(
                data_key=data_key1,
                stroke=rx.color("accent", 9),
                fill=rx.color("accent", 8),
            ),
            rx.recharts.bar(
                data_key=data_key2,
                stroke=rx.color("green", 9),
                fill=rx.color("green", 8),
            ),
            rx.recharts.x_axis(data_key="name"),
            rx.recharts.y_axis(),
            rx.recharts.legend(),
            data=data,
            height=height,
        )

class ComparisonLineChartBuilder(ComparisonChartBuilder):
    def build_chart(self, data: List[Dict], data_key1: str, data_key2: str, height: int) -> rx.Component:
        return rx.recharts.line_chart(
            rx.recharts.line(
                type="monotone",
                data_key=data_key1,
                stroke=rx.color("accent", 9),
            ),
            rx.recharts.line(
                type="monotone",
                data_key=data_key2,
                stroke=rx.color("green", 9),
            ),
            rx.recharts.x_axis(data_key="name"),
            rx.recharts.y_axis(),
            rx.recharts.legend(),
            data=data,
            height=height,
        )

class ComparisonChartFactory:
    @staticmethod
    def get_chart_builder(chart_type: str) -> ComparisonChartBuilder:
        if chart_type == "bar":
            return ComparisonBarChartBuilder()
        elif chart_type == "line":
            return ComparisonChartBuilder()
        else:
            raise ValueError(f"Unsupported chart type: {chart_type}")
