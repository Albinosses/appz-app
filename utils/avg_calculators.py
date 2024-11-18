from __future__ import annotations


def get_avg_for_task(data, module_name, metric_type):
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

def get_avg_for_module(data, metric_type):
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
