from abc import ABC, abstractmethod
from typing import Any

import pandas as pd
import great_expectations as gx


class BaseValidator(ABC):
    def __init__(self, data: pd.DataFrame, suite_name: str):
        self.data = data
        self.suite_name = suite_name
        self.results = []

    @abstractmethod
    def get_expectations(self) -> list[dict[str, Any]]:
        pass

    def validate(self) -> dict:
        context = gx.get_context()
        data_source = context.data_sources.add_pandas(name=f"source_{self.suite_name}")
        data_asset = data_source.add_dataframe_asset(name=f"asset_{self.suite_name}")
        batch_definition = data_asset.add_batch_definition_whole_dataframe("batch")
        batch = batch_definition.get_batch(batch_parameters={"dataframe": self.data})

        expectations = self.get_expectations()
        self.results = []

        for exp in expectations:
            result = batch.validate_expectation(
                expectation_type=exp["expectation_type"],
                **exp["kwargs"],
            )
            self.results.append({
                "expectation": exp["expectation_type"],
                "success": result.success,
                "kwargs": exp["kwargs"],
            })

        passed = sum(1 for r in self.results if r["success"])
        return {
            "suite": self.suite_name,
            "total": len(self.results),
            "passed": passed,
            "failed": len(self.results) - passed,
        }
