import json
from typing import TextIO


class DBCourseData:
    def get_course_statistics(self, source) -> dict:
        # in most cases we'll have some data base connector (Postgres or Snowflake), in this case we know how to transform data
        return source


class CourseDataStream:
    # but in our case we have json data stream, and we don't know how to transform data
    def get_course_data_stream(self, path) -> TextIO:
        return open(path)

class CourseDataAdapter(DBCourseData, CourseDataStream):
    # we use CourseDataAdapter to smoothly integrate stream to CourseData

    def get_course_statistics(self, path) -> dict:
        return json.load(self.get_course_data_stream(path))
