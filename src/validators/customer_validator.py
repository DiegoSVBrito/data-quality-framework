from src.validators.base_validator import BaseValidator


class CustomerValidator(BaseValidator):
    def __init__(self, data):
        super().__init__(data, "customer_suite")

    def get_expectations(self):
        return [
            {"expectation_type": "expect_column_to_exist", "kwargs": {"column": "customer_id"}},
            {"expectation_type": "expect_column_to_exist", "kwargs": {"column": "email"}},
            {"expectation_type": "expect_column_to_exist", "kwargs": {"column": "name"}},
            {"expectation_type": "expect_column_values_to_not_be_null", "kwargs": {"column": "customer_id"}},
            {"expectation_type": "expect_column_values_to_not_be_null", "kwargs": {"column": "name"}},
            {"expectation_type": "expect_column_values_to_be_unique", "kwargs": {"column": "customer_id"}},
            {
                "expectation_type": "expect_column_values_to_match_regex",
                "kwargs": {"column": "email", "regex": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"},
            },
            {"expectation_type": "expect_column_values_to_be_between", "kwargs": {"column": "age", "min_value": 18, "max_value": 120}},
        ]
