def merge_module_progress(student_progress, average_values, type):
    for module in average_values:
        if module["name"] in student_progress["results"][type]:
            student_progress_for_module = sum(student_progress["results"][type][module["name"]].values())
            module["Student progress"] = student_progress_for_module

    return average_values


def merge_task_progress(student_progress, average_values, progress_type, module_name=None):
    for task in average_values:
        for module, tasks in student_progress["results"][progress_type].items():
            if module_name and module != module_name:
                continue
            if task["name"] in tasks:
                task["Student progress"] = tasks[task["name"]]
                break

    return average_values

