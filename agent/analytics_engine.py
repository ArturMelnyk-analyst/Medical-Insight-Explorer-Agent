from typing import Dict, List, Optional

import pandas as pd


class HealthcareAnalyticsEngine:
    """
    Deterministic analytics engine for cleaned Medicare healthcare claims data.

    This class performs controlled pandas-based computations over the relational
    Parquet tables loaded by HealthcareDataLoader.

    The goal is to compute real metrics first. Later, an LLM can explain these
    computed results instead of inventing answers.
    """

    def __init__(self, tables: Dict[str, pd.DataFrame]) -> None:
        self.tables = tables

    def get_table_shapes(self) -> pd.DataFrame:
        """
        Return row and column counts for all loaded tables.
        """
        rows = []

        for table_name, dataframe in self.tables.items():
            rows.append(
                {
                    "table_name": table_name,
                    "rows": dataframe.shape[0],
                    "columns": dataframe.shape[1],
                }
            )

        return pd.DataFrame(rows).sort_values("table_name").reset_index(drop=True)

    def inpatient_claim_summary(self) -> Dict[str, Optional[float]]:
        """
        Return basic summary statistics for training inpatient claims.
        """
        inpatient = self.tables["train_inpatient"]

        summary = {
            "total_claims": int(len(inpatient)),
            "unique_beneficiaries": int(inpatient["BeneID"].nunique())
            if "BeneID" in inpatient.columns
            else None,
            "unique_claims": int(inpatient["ClaimID"].nunique())
            if "ClaimID" in inpatient.columns
            else None,
            "unique_providers": int(inpatient["Provider"].nunique())
            if "Provider" in inpatient.columns
            else None,
        }

        if "InscClaimAmtReimbursed" in inpatient.columns:
            claim_amount = inpatient["InscClaimAmtReimbursed"].dropna()

            summary.update(
                {
                    "mean_reimbursement": float(claim_amount.mean()),
                    "median_reimbursement": float(claim_amount.median()),
                    "total_reimbursement": float(claim_amount.sum()),
                }
            )

        return summary

    def outpatient_claim_summary(self) -> Dict[str, Optional[float]]:
        """
        Return basic summary statistics for training outpatient claims.
        """
        outpatient = self.tables["train_outpatient"]

        summary = {
            "total_claims": int(len(outpatient)),
            "unique_beneficiaries": int(outpatient["BeneID"].nunique())
            if "BeneID" in outpatient.columns
            else None,
            "unique_claims": int(outpatient["ClaimID"].nunique())
            if "ClaimID" in outpatient.columns
            else None,
            "unique_providers": int(outpatient["Provider"].nunique())
            if "Provider" in outpatient.columns
            else None,
        }

        if "InscClaimAmtReimbursed" in outpatient.columns:
            claim_amount = outpatient["InscClaimAmtReimbursed"].dropna()

            summary.update(
                {
                    "mean_reimbursement": float(claim_amount.mean()),
                    "median_reimbursement": float(claim_amount.median()),
                    "total_reimbursement": float(claim_amount.sum()),
                }
            )

        return summary

    def beneficiary_age_summary(self) -> Dict[str, Optional[float]]:
        """
        Return summary statistics for beneficiary age.
        """
        beneficiary = self.tables["train_beneficiary"]

        if "AgeAtDeathOrLastClaim" not in beneficiary.columns:
            return {"error": "AgeAtDeathOrLastClaim column not found."}

        age = beneficiary["AgeAtDeathOrLastClaim"].dropna()

        return {
            "count": int(age.count()),
            "mean_age": float(age.mean()),
            "median_age": float(age.median()),
            "min_age": float(age.min()),
            "max_age": float(age.max()),
        }

    def top_providers_by_claim_count(
        self,
        claim_type: str = "inpatient",
        top_n: int = 10,
    ) -> pd.DataFrame:
        """
        Return top providers by claim count for inpatient or outpatient claims.
        """
        if claim_type not in {"inpatient", "outpatient"}:
            raise ValueError("claim_type must be either 'inpatient' or 'outpatient'.")

        table_name = f"train_{claim_type}"
        claims = self.tables[table_name]

        if "Provider" not in claims.columns:
            raise ValueError(f"Provider column not found in {table_name}.")

        result = (
            claims["Provider"]
            .value_counts()
            .head(top_n)
            .reset_index()
        )

        result.columns = ["Provider", "claim_count"]

        return result

    def average_inpatient_cost_by_chronic_condition(
        self,
        condition_col: str,
    ) -> pd.DataFrame:
        """
        Calculate inpatient reimbursement statistics by chronic-condition flag.

        Example condition columns may include chronic disease indicators from
        the beneficiary table.
        """
        beneficiary = self.tables["train_beneficiary"]
        inpatient = self.tables["train_inpatient"]

        if condition_col not in beneficiary.columns:
            raise ValueError(f"Column not found in beneficiary table: {condition_col}")

        if "BeneID" not in beneficiary.columns or "BeneID" not in inpatient.columns:
            raise ValueError("BeneID must exist in both beneficiary and inpatient tables.")

        if "InscClaimAmtReimbursed" not in inpatient.columns:
            raise ValueError("InscClaimAmtReimbursed column not found in inpatient table.")

        merged = inpatient.merge(
            beneficiary[["BeneID", condition_col]],
            on="BeneID",
            how="left",
        )

        result = (
            merged.groupby(condition_col, dropna=False)["InscClaimAmtReimbursed"]
            .agg(["count", "mean", "median", "sum"])
            .reset_index()
            .sort_values("mean", ascending=False)
        )

        return result

    def claim_distribution_by_state(
        self,
        claim_type: str = "inpatient",
    ) -> pd.DataFrame:
        """
        Return claim counts by beneficiary state for inpatient or outpatient claims.
        """
        if claim_type not in {"inpatient", "outpatient"}:
            raise ValueError("claim_type must be either 'inpatient' or 'outpatient'.")

        claims = self.tables[f"train_{claim_type}"]
        beneficiary = self.tables["train_beneficiary"]

        if "BeneID" not in claims.columns or "BeneID" not in beneficiary.columns:
            raise ValueError("BeneID must exist in both claims and beneficiary tables.")

        if "State" not in beneficiary.columns:
            raise ValueError("State column not found in beneficiary table.")

        merged = claims.merge(
            beneficiary[["BeneID", "State"]],
            on="BeneID",
            how="left",
        )

        result = (
            merged.groupby("State", dropna=False)
            .size()
            .reset_index(name="claim_count")
            .sort_values("claim_count", ascending=False)
        )

        return result

    def available_beneficiary_columns(self) -> List[str]:
        """
        Return available columns from the training beneficiary table.
        Useful for discovering chronic-condition columns.
        """
        return self.tables["train_beneficiary"].columns.tolist()