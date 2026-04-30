import argparse
import json

import pandas as pd
import great_expectations as gx


def generate_suite(data_path: str, suite_name: str) -> dict:
    df = pd.read_csv(data_path) if data_path.endswith(".csv") else pd.read_parquet(data_path)

    expectations = []
    for col in df.columns:
        expectations.append({
            "expectation_type": "expect_column_to_exist",
            "kwargs": {"column": col},
        })

        null_pct = df[col].isnull().mean()
        if null_pct == 0:
            expectations.append({
                "expectation_type": "expect_column_values_to_not_be_null",
                "kwargs": {"column": col},
            })

        if df[col].dtype in ["int64", "float64"]:
            expectations.append({
                "expectation_type": "expect_column_values_to_be_between",
                "kwargs": {
                    "column": col,
                    "min_value": float(df[col].min()),
                    "max_value": float(df[col].max()),
                },
            })

        if df[col].nunique() / len(df) == 1:
            expectations.append({
                "expectation_type": "expect_column_values_to_be_unique",
                "kwargs": {"column": col},
            })

    suite = {
        "expectation_suite_name": suite_name,
        "expectations": expectations,
    }
    return suite


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", required=True, help="Path to data file")
    parser.add_argument("--name", default="auto_generated_suite", help="Suite name")
    parser.add_argument("--output", default="expectations/auto_suite.json", help="Output path")
    args = parser.parse_args()

    suite = generate_suite(args.data, args.name)

    with open(args.output, "w") as f:
        json.dump(suite, f, indent=2)

    print(f"Generated {len(suite['expectations'])} expectations -> {args.output}")


if __name__ == "__main__":
    main()
