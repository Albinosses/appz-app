from abc import ABC, abstractmethod

class DataAdapter(ABC):
    @abstractmethod
    def adapt(self, raw_data) -> dict:
        pass

class CourseDataAdapter(DataAdapter):
    def adapt(self, raw_data) -> dict:
        adapted_data = {"results": []}
        for course in raw_data.get("results", []):
            course_entry = {
                "name": raw_data.get("name", "Unknown Course"),
                "times": {}
            }
            times = course.get("times", {})
            for module, tasks in times.items():
                course_entry["times"][module] = tasks
            adapted_data["results"].append(course_entry)
        return adapted_data
