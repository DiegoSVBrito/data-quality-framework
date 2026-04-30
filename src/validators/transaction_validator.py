from src.validators.base_validator import BaseValidator


class TransactionValidator(BaseValidator):
    def __init__(self, data):
        super().__init__(data, "transaction_suite")

    def get_expectations(self):
        return [
            {"expectation_type": "expect_column_to_exist", "kwargs": {"column": "transaction_id"}},
            {"expectation_type": "expect_column_to_exist", "kwargs": {"column": "customer_id"}},
            {"expectation_type": "expect_column_to_exist", "kwargs": {"column": "amount"}},
            {"expectation_type": "expect_column_values_to_not_be_null", "kwargs": {"column": "transaction_id"}},
            {"expectation_type": "expect_column_values_to_not_be_null", "kwargs": {"column": "customer_id"}},
            {"expectation_type": "expect_column_values_to_not_be_null", "kwargs": {"column": "amount"}},
            {"expectation_type": "expect_column_values_to_be_unique", "kwargs": {"column": "transaction_id"}},
            {"expectation_type": "expect_column_values_to_be_between", "kwargs": {"column": "amount", "min_value": 0.01, "max_value": 1000000}},
        ]
