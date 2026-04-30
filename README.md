# Data Quality Framework

Data quality and governance framework with Great Expectations: schema validation, integrity tests, data contracts, and automated reporting.

## Architecture

```
+------------------+     +------------------+     +------------------+
|   Data Source    |     |   Great          |     |   Report +       |
|   (BigQuery /    |---->|   Expectations   |     |   Alert          |
|    CSV / API)    |     |   Validator      |     |                  |
+------------------+     +--------+---------+     +--------+---------+
                                  |                        |
                         +--------v---------+              |
                         |  Expectation     |              |
                         |  Suites          |     +--------v---------+
                         |  (transaction,   |     |   Data Contract  |
                         |   customer)      |     |   (YAML schema)  |
                         +------------------+     +------------------+
                                  |
                    +-------------+-------------+
                    |                           |
           +--------v---------+       +---------v--------+
           |  PASS            |       |  FAIL            |
           |  Data -> DW      |       |  DLQ + Notify    |
           |  (trust in data) |       |  (Slack/Email)   |
           +------------------+       +------------------+
```

## Data Contracts

Each data source has a contract defined in YAML:

- **Schema**: Types, required fields, constraints
- **Quality Rules**: Value ranges, uniqueness, referential integrity
- **SLAs**: Validation frequency, max resolution time
- **Owner**: Responsible party for that source's quality

## Usage

```bash
pip install -r requirements.txt

# Run full validation
python scripts/run_validation.py --suite transaction_suite

# Generate expectation suite from profiling
python scripts/generate_expectations.py --data ./data/sample.csv

# Validate contract
python scripts/run_validation.py --contract contracts/transaction_contract.yaml
```

## Quality Rules

| Rule | Type | Description |
|------|------|-------------|
| `expect_column_values_to_not_be_null` | Integrity | Required fields without nulls |
| `expect_column_values_to_be_unique` | Uniqueness | IDs without duplicates |
| `expect_column_values_to_be_between` | Range | Values within expected bounds |
| `expect_column_values_to_match_regex` | Format | Email, CPF with valid format |
| `expect_table_row_count_to_be_between` | Volume | Row count within expected range |

## Technical Decisions

**Why Great Expectations over Pandera?** GE has a more mature ecosystem: reusable expectation suites, automatic data docs, dbt/Airflow integration. Pandera is lighter but limited for governance at scale. GE allows versioning expectations alongside code.

**Why Data Contracts?** Contracts formalize responsibility for data quality. Instead of ad-hoc tests, each source has a contract defining: what is expected, who is responsible, and what happens on failure. This transforms data quality from reactive to proactive.

**Why versioned Expectation Suites?** Suites are versioned JSON files in git. Changes to data quality go through code review, just like code changes. The history of rule changes is auditable.

## Structure

```
data-quality-framework/
  expectations/              # Great Expectations suites (JSON)
    transaction_suite.json
    customer_suite.json
  contracts/                 # Data Contracts (YAML)
    transaction_contract.yaml
    customer_contract.yaml
  scripts/
    run_validation.py        # Run validations
    generate_expectations.py # Auto-generate suites
  src/
    validators/              # Custom validators
      base_validator.py
      transaction_validator.py
      customer_validator.py
    notifiers/               # Alerts
      slack_notifier.py
      email_notifier.py
    reports/
      quality_report.py      # HTML reports
  tests/
    test_validators.py
    test_contracts.py
  .github/
    workflows/
      quality-check.yml      # CI: validation on sample data
  docs/
    decisions.md             # Architecture Decision Records
```

---

Author: Diego Brito
