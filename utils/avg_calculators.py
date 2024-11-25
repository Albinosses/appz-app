from abc import ABC, abstractmethod
from typing import Dict, List
import json

class AverageCalculator(ABC):
    @abstractmethod
    def get_avg_for_task(self, data: Dict, module_name: str, metric_type: str) -> List[Dict[str, float]]:
        pass

    @abstractmethod
    def get_avg_for_module(self, data: Dict, metric_type: str) -> List[Dict[str, float]]:
        pass

class DefaultAverageCalculator(AverageCalculator):
    def get_avg_for_task(self, data: Dict, module_name: str, metric_type: str) -> List[Dict[str, float]]:
        task_metric = {}
        task_counts = {}

        for course in data["results"]:
            metrics = course[metric_type]
            for module, tasks in metrics.items():
                if module_name and module != module_name:
                    continue
                for task, metric in tasks.items():
                    if task not in task_metric:
                        task_metric[task] = 0
                        task_counts[task] = 0
                    task_metric[task] += metric
                    task_counts[task] += 1

        average_scores = [
            {"name": task, "Average progress": total_score / task_counts[task]}
            for task, total_score in task_metric.items()
        ]
        return average_scores

    def get_avg_for_module(self, data: Dict, metric_type: str) -> List[Dict[str, float]]:
        module_metric = {}
        module_task_counts = {}

        for course in data["results"]:
            metrics = course[metric_type]
            for module, tasks in metrics.items():
                if module not in module_metric:
                    module_metric[module] = 0
                    module_task_counts[module] = 0
                for task, metric in tasks.items():
                    module_metric[module] += metric
                    module_task_counts[module] += 1

        average_module_scores = [
            {"name": module, "Average progress": total_score / module_task_counts[module]}
            for module, total_score in module_metric.items()
        ]
        return average_module_scores

class CachingAverageCalculator(AverageCalculator):
    def __init__(self, calculator: AverageCalculator):
        self._calculator = calculator
        self._cache = {}

    def _generate_cache_key(self, method: str, *args, **kwargs) -> str:
        return json.dumps({"method": method, "args": args, "kwargs": kwargs}, sort_keys=True)

    def get_avg_for_task(self, data: Dict, module_name: str, metric_type: str) -> List[Dict[str, float]]:
        cache_key = self._generate_cache_key("get_avg_for_task", data, module_name, metric_type)
        if cache_key in self._cache:
            print(f"Кешований результат знайдено для ключа: {cache_key}")
            return self._cache[cache_key]

        print(f"Обчислення результату для ключа: {cache_key}")
        result = self._calculator.get_avg_for_task(data, module_name, metric_type)
        self._cache[cache_key] = result
        return result

    def get_avg_for_module(self, data: Dict, metric_type: str) -> List[Dict[str, float]]:
        cache_key = self._generate_cache_key("get_avg_for_module", data, metric_type)
        if cache_key in self._cache:
            print(f"Кешований результат знайдено для ключа: {cache_key}")
            return self._cache[cache_key]

        print(f"Обчислення результату для ключа: {cache_key}")
        result = self._calculator.get_avg_for_module(data, metric_type)
        self._cache[cache_key] = result
        return result
