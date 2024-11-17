data = {
    "name": "Introduction to Reflex",
    "courses": [
        {
            "student_id": "eds3wrfed",
            "times": {
                "module1": {
                    "task1": 33,
                    "task2": 43
                },
                "module2": {
                    "task1": 32,
                    "task2": 43
                },
                "module3": {
                    "task1": 32,
                    "task2": 43
                }
            },
            "scores": [
                {
                    "module1": {
                        "task1": 32,
                        "task2": 43
                    },
                    "module2": {
                        "task1": 32,
                        "task2": 43
                    },
                    "module3": {
                        "task1": 32,
                        "task2": 43
                    }
                }
            ]
        }
    ]
}

def calculate_average_task_time(data):
    task_times = {}
    task_counts = {}

    for course in data["courses"]:
        times = course["times"]

        for module, tasks in times.items():
            for task, time in tasks.items():
                if task not in task_times:
                    task_times[task] = 0
                    task_counts[task] = 0
                task_times[task] += time
                task_counts[task] += 1

    average_times = {task: task_times[task] / task_counts[task] for task in task_times}
    return average_times

average_times = calculate_average_task_time(data)
def calculate_average_module_time(data):
    module_times = {}
    module_task_counts = {}

    # Обхід по курсам
    for course in data["courses"]:
        times = course["times"]

        # Обхід по модулях
        for module, tasks in times.items():
            if module not in module_times:
                module_times[module] = 0
                module_task_counts[module] = 0

            for task, time in tasks.items():
                module_times[module] += time
                module_task_counts[module] += 1

    # Обчислення середнього часу для кожного модуля
    average_module_times = {
        module: module_times[module] / module_task_counts[module]
        for module in module_times
    }
    return average_module_times

average_module_times = calculate_average_module_time(data)
print(average_module_times)

