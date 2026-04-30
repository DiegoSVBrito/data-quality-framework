import pytest
import yaml
from pathlib import Path


CONTRACTS_DIR = Path("contracts")


@pytest.fixture(params=["transaction_contract.yaml", "customer_contract.yaml"])
def contract(request):
    path = CONTRACTS_DIR / request.param
    with open(path) as f:
        return yaml.safe_load(f)


def test_contract_has_name(contract):
    assert "name" in contract


def test_contract_has_schema(contract):
    assert "schema" in contract
    assert len(contract["schema"]) > 0


def test_contract_has_quality_rules(contract):
    assert "quality_rules" in contract
    assert len(contract["quality_rules"]) > 0


def test_contract_has_sla(contract):
    assert "sla" in contract
    assert "validation_frequency" in contract["sla"]


def test_contract_schema_has_required_fields(contract):
    for field_name, field_def in contract["schema"].items():
        if field_def.get("required"):
            assert "type" in field_def, f"Required field {field_name} missing type"


def test_contract_quality_rules_have_severity(contract):
    for rule in contract["quality_rules"]:
        assert "severity" in rule
        assert rule["severity"] in ["critical", "warning", "info"]
