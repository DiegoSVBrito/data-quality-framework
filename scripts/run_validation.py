import argparse
import json
import sys
from pathlib import Path

import great_expectations as gx
import pandas as pd
import yaml


def load_contract(contract_path: str) -> dict:
    with open(contract_path) as f:
        return yaml.safe_load(f)


def run_suite_validation(data_path: str, suite_path: str) -> dict:
    with open(suite_path) as f:
        suite = json.load(f)

    df = pd.read_csv(data_path) if data_path.endswith(".csv") else pd.read_parquet(data_path)

    context = gx.get_context()
    data_source = context.data_sources.add_pandas(name="validation_source")
    data_asset = data_source.add_dataframe_asset(name="data_asset")
    batch_definition = data_asset.add_batch_definition_whole_dataframe("batch")
    batch = batch_definition.get_batch(batch_parameters={"dataframe": df})

    results = []
    for exp in suite["expectations"]:
        result = batch.validate_expectation(
            expectation_type=exp["expectation_type"],
            **exp["kwargs"],
        )
        results.append({
            "expectation": exp["expectation_type"],
            "success": result.success,
            "kwargs": exp["kwargs"],
        })

    passed = sum(1 for r in results if r["success"])
    failed = len(results) - passed

    return {
        "suite": suite["expectation_suite_name"],
        "total": len(results),
        "passed": passed,
        "failed": failed,
        "success_rate": passed / len(results) * 100 if results else 0,
        "results": results,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--suite", required=True, help="Path to expectation suite JSON")
    parser.add_argument("--data", required=True, help="Path to data file (CSV/Parquet)")
    parser.add_argument("--contract", help="Path to data contract YAML")
    args = parser.parse_args()

    result = run_suite_validation(args.data, args.suite)

    print(f"\nSuite: {result['suite']}")
    print(f"Total: {result['total']} | Passed: {result['passed']} | Failed: {result['failed']}")
    print(f"Success rate: {result['success_rate']:.1f}%\n")

    if result["failed"] > 0:
        print("Failed expectations:")
        for r in result["results"]:
            if not r["success"]:
                print(f"  - {r['expectation']}: {r['kwargs']}")
        sys.exit(1)


if __name__ == "__main__":
    main()
