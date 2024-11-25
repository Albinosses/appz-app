import json
from abc import ABC, abstractmethod

class DataConnector(ABC):
    @abstractmethod
    def get_student_progress(self, student_id: str, course_name:str ):
        pass

    @abstractmethod
    def get_all_students_progress(self, course_name: str):
        pass

    @abstractmethod
    def get_student_courses(self, student_id: str):
        pass


class SnowfalkeConnector(DataConnector):
    def get_student_progress(self, student_id: str, course_name: str):
        print("Student progress data found")

    def get_all_students_progress(self, course_name: str):
        print("All students progress data found")

    def get_student_courses(self, student_id: str):
        print("Student courses data found")

class JSONConnector(DataConnector):
    def get_student_progress(self, student_id: str, course_name: str):
        # mock just to save time
        return json.load(open(f"app/jsons/student_course_statistics_example.json"))

    def get_all_students_progress(self, course_name: str):
        # mock just to save time
        return json.load(open(f"app/jsons/all_students_course_statistics_example.json"))

    def get_student_courses(self, student_id: str):
        # mock just to save time
        return json.load(open(f"app/jsons/user_courses_example.json"))

class DataConnectorFactory:
    @staticmethod
    def get_connector(db_type: str) -> DataConnector:
        if db_type == "snowflake":
            return SnowfalkeConnector()
        elif db_type == "json":
            return JSONConnector()
        else:
            raise ValueError(f"Unknown database type: {db_type}")
