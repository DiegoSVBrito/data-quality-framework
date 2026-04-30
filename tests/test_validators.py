import pytest
import pandas as pd
from src.validators.transaction_validator import TransactionValidator
from src.validators.customer_validator import CustomerValidator


@pytest.fixture
def transaction_data():
    return pd.DataFrame({
        "transaction_id": ["TXN-A1B2C3D4", "TXN-E5F6G7H8", "TXN-I9J0K1L2"],
        "customer_id": ["CUST-001", "CUST-002", "CUST-003"],
        "amount": [100.50, 250.00, 99.99],
    })


@pytest.fixture
def customer_data():
    return pd.DataFrame({
        "customer_id": ["CUST-001", "CUST-002", "CUST-003"],
        "name": ["Alice", "Bob", "Carol"],
        "email": ["alice@example.com", "bob@example.com", "carol@example.com"],
        "age": [25, 30, 45],
    })


def test_transaction_validator_has_expectations(transaction_data):
    validator = TransactionValidator(transaction_data)
    expectations = validator.get_expectations()
    assert len(expectations) > 0
    assert any(e["expectation_type"] == "expect_column_values_to_be_unique" for e in expectations)


def test_customer_validator_has_expectations(customer_data):
    validator = CustomerValidator(customer_data)
    expectations = validator.get_expectations()
    assert len(expectations) > 0
    assert any(e["expectation_type"] == "expect_column_values_to_match_regex" for e in expectations)
