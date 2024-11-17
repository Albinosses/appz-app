from __future__ import annotations
import json
from abc import ABC, abstractmethod


class AverageScoreCalculator(ABC):
    @abstractmethod
    def get_avg_score(self, data, module_name='all'):
        pass


class AverageTaskScoreCalculator(AverageScoreCalculator):
    def get_avg_score(self, data, module_name):
        task_scores = {}
        task_counts = {}

        for course in data["results"]:
            for score_entry in course["scores"]:  # Iterate over the list of score dictionaries
                for module, tasks in score_entry.items():
                    if module_name and module != module_name:
                        continue
                    for task, score in tasks.items():
                        if task not in task_scores:
                            task_scores[task] = 0
                            task_counts[task] = 0
                        task_scores[task] += score
                        task_counts[task] += 1

        average_scores = [
            {"name": task, "Average progress": total_score / task_counts[task]}
            for task, total_score in task_scores.items()
        ]
        return average_scores


class AverageModuleScoreCalculator(AverageScoreCalculator):
    def get_avg_score(self, data):
        module_scores = {}
        module_task_counts = {}

        for course in data["results"]:
            for score_entry in course["scores"]:  # Iterate over the list of score dictionaries
                for module, tasks in score_entry.items():
                    if module not in module_scores:
                        module_scores[module] = 0
                        module_task_counts[module] = 0
                    for task, score in tasks.items():
                        module_scores[module] += score
                        module_task_counts[module] += 1

        average_module_scores = [
            {"name": module, "Average progress": total_score / module_task_counts[module]}
            for module, total_score in module_scores.items()
        ]
        return average_module_scores


class AverageScoreCalculatorFactory(ABC):
    @abstractmethod
    def create_score_calculator(self):
        pass

class AverageTaskScoreCalculatorFactory(AverageScoreCalculatorFactory):
    def create_score_calculator(self):
        return AverageTaskScoreCalculator()


class AverageModuleScoreCalculatorFactory(AverageScoreCalculatorFactory):
    def create_score_calculator(self):
        return AverageModuleScoreCalculator()
