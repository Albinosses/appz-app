from __future__ import annotations
import json
from abc import ABC, abstractmethod


class AverageTimeCalculator(ABC):
    @abstractmethod
    def get_avg_time(self, data, module_name=None):
        pass


class AverageTaskTimeCalculator(AverageTimeCalculator):
    def get_avg_time(self, data, module_name):
        task_times = {}
        task_counts = {}

        for course in data["results"]:
            times = course["times"]
            for module, tasks in times.items():
                # If module_name is provided, process only that module
                if module_name and module != module_name:
                    continue
                for task, time in tasks.items():
                    if task not in task_times:
                        task_times[task] = 0
                        task_counts[task] = 0
                    task_times[task] += time
                    task_counts[task] += 1

        average_times = [
            {"name": task, "Average progress": total_time / task_counts[task]}
            for task, total_time in task_times.items()
        ]
        return average_times


class AverageModuleTimeCalculator(AverageTimeCalculator):
    def get_avg_time(self, data, module_name=None):
        module_times = {}
        module_task_counts = {}

        for course in data["results"]:
            times = course["times"]
            for module, tasks in times.items():
                # If module_name is provided, skip other modules
                if module_name and module != module_name:
                    continue
                if module not in module_times:
                    module_times[module] = 0
                    module_task_counts[module] = 0
                for task, time in tasks.items():
                    module_times[module] += time
                    module_task_counts[module] += 1

        average_module_times = [
            {"name": module, "Average progress": total_time / module_task_counts[module]}
            for module, total_time in module_times.items()
        ]
        return average_module_times


class AverageTimeCalculatorFactory(ABC):
    @abstractmethod
    def create_time_calculator(self):
        pass


class AverageTaskTimeCalculatorFactory(AverageTimeCalculatorFactory):
    def create_time_calculator(self):
        return AverageTaskTimeCalculator()


class AverageModuleTimeCalculatorFactory(AverageTimeCalculatorFactory):
    def create_time_calculator(self):
        return AverageModuleTimeCalculator()
