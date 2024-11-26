# Writing 10 modular tests for the DefaultAverageCalculator class based on the provided guidelines.

import unittest
from utils.avg_calculators import DefaultAverageCalculator

class TestDefaultAverageCalculator(unittest.TestCase):
    def setUp(self):
        self.calculator = DefaultAverageCalculator()
        self.sample_data = {
            "results": [
                {
                    "metrics": {
                        "module1": {"task1": 10, "task2": 20},
                        "module2": {"task1": 15}
                    }
                },
                {
                    "metrics": {
                        "module1": {"task1": 30, "task2": 40},
                        "module2": {"task1": 25}
                    }
                }
            ]
        }

    # 1. Test with valid data for get_avg_for_task
    def test_get_avg_for_task_valid(self):
        result = self.calculator.get_avg_for_task(self.sample_data, "module1", "metrics")
        self.assertEqual(result, [{"task1": 20.0}, {"task2": 30.0}])

    # 2. Test with valid data for get_avg_for_module
    def test_get_avg_for_module_valid(self):
        result = self.calculator.get_avg_for_module(self.sample_data, "metrics")
        self.assertEqual(result, [{"module1": 25.0}, {"module2": 20.0}])

    # 3. Test with empty data
    def test_get_avg_for_task_empty_data(self):
        empty_data = {"results": []}
        result = self.calculator.get_avg_for_task(empty_data, "module1", "metrics")
        self.assertEqual(result, [])

    # 4. Test with module_name that doesn't exist
    def test_get_avg_for_task_invalid_module(self):
        result = self.calculator.get_avg_for_task(self.sample_data, "nonexistent_module", "metrics")
        self.assertEqual(result, [])

    # 5. Test with null data
    def test_get_avg_for_task_null_data(self):
        with self.assertRaises(TypeError):
            self.calculator.get_avg_for_task(None, "module1", "metrics")

    # 6. Test with null metric type
    def test_get_avg_for_task_null_metric(self):
        with self.assertRaises(KeyError):
            self.calculator.get_avg_for_task(self.sample_data, "module1", None)

    # 7. Test for average calculation correctness
    def test_get_avg_for_task_calculation(self):
        result = self.calculator.get_avg_for_task(self.sample_data, "module2", "metrics")
        self.assertEqual(result, [{"task1": 20.0}])

    # 8. Test for KeyError when key is missing
    def test_get_avg_for_task_key_error(self):
        incomplete_data = {"results": [{"metrics": {}}]}
        with self.assertRaises(KeyError):
            self.calculator.get_avg_for_task(incomplete_data, "module1", "metrics")

    # 9. Test with a single result entry
    def test_get_avg_for_task_single_entry(self):
        single_data = {"results": [{"metrics": {"module1": {"task1": 50}}}]}
        result = self.calculator.get_avg_for_task(single_data, "module1", "metrics")
        self.assertEqual(result, [{"task1": 50.0}])

    # 10. Test with invalid input type for data
    def test_get_avg_for_task_invalid_input_type(self):
        with self.assertRaises(TypeError):
            self.calculator.get_avg_for_task("invalid_input", "module1", "metrics")

if __name__ == '__main__':
    unittest.main()


