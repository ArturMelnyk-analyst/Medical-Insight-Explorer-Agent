from typing import Dict, List, Optional

import pandas as pd


class HealthcareAnalyticsEngine:
    """
    Deterministic analytics engine for cleaned Medicare healthcare claims data.
    """

    def __init__(self, tables: Dict[str, pd.DataFrame]) -> None:
        self.tables = tables

    def get_table_shapes(self) -> pd.DataFrame:
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
        if claim_type not in {"inpatient", "outpatient"}:
            raise ValueError("claim_type must be either 'inpatient' or 'outpatient'.")

        table_name = f"train_{claim_type}"
        claims = self.tables[table_name]

        if "Provider" not in claims.columns:
            raise ValueError(f"Provider column not found in {table_name}.")

        result = claims["Provider"].value_counts().head(top_n).reset_index()
        result.columns = ["Provider", "claim_count"]

        return result

    def average_inpatient_cost_by_chronic_condition(
        self,
        condition_col: str,
    ) -> pd.DataFrame:
        """
        Calculate inpatient reimbursement statistics by chronic-condition flag.

        Handles both raw Medicare numeric indicators and cleaned text labels.
        """
        beneficiary = self.tables["train_beneficiary"]
        inpatient = self.tables["train_inpatient"]

        if condition_col not in beneficiary.columns:
            raise ValueError(f"Column not found in beneficiary table: {condition_col}")

        if "BeneID" not in beneficiary.columns:
            raise ValueError("BeneID missing from beneficiary table.")

        if "BeneID" not in inpatient.columns:
            raise ValueError("BeneID missing from inpatient table.")

        if "InscClaimAmtReimbursed" not in inpatient.columns:
            raise ValueError("InscClaimAmtReimbursed missing from inpatient table.")

        merged = inpatient.merge(
            beneficiary[["BeneID", condition_col]],
            on="BeneID",
            how="left",
        )

        label_map = {
            "1": "Diabetes",
            "1.0": "Diabetes",
            "diabetes": "Diabetes",
            "yes": "Diabetes",
            "true": "Diabetes",
            "2": "No Diabetes",
            "2.0": "No Diabetes",
            "no diabetes": "No Diabetes",
            "no_diabetes": "No Diabetes",
            "no": "No Diabetes",
            "false": "No Diabetes",
        }

        merged["ConditionLabel"] = (
            merged[condition_col]
            .astype(str)
            .str.strip()
            .str.lower()
            .map(label_map)
        )

        merged = merged.dropna(
            subset=["ConditionLabel", "InscClaimAmtReimbursed"]
        ).copy()

        result = (
            merged.groupby("ConditionLabel", observed=True)["InscClaimAmtReimbursed"]
            .agg(["count", "mean", "median", "sum"])
            .reset_index()
            .rename(columns={"ConditionLabel": condition_col})
        )

        result[condition_col] = pd.Categorical(
            result[condition_col],
            categories=["No Diabetes", "Diabetes"],
            ordered=True,
        )

        return result.sort_values(condition_col).reset_index(drop=True)

    def inpatient_reimbursement_by_diabetes_status(self) -> pd.DataFrame:
        """
        Return claim-level reimbursement values by diabetes status.

        Used for distribution visualization because box plots are more informative
        than mean-only bar charts for skewed reimbursement data.
        """
        beneficiary = self.tables["train_beneficiary"]
        inpatient = self.tables["train_inpatient"]

        condition_col = "ChronicCond_Diabetes"

        required_beneficiary_cols = ["BeneID", condition_col]
        required_inpatient_cols = ["BeneID", "InscClaimAmtReimbursed"]

        for col in required_beneficiary_cols:
            if col not in beneficiary.columns:
                raise ValueError(f"Column not found in beneficiary table: {col}")

        for col in required_inpatient_cols:
            if col not in inpatient.columns:
                raise ValueError(f"Column not found in inpatient table: {col}")

        merged = inpatient.merge(
            beneficiary[required_beneficiary_cols],
            on="BeneID",
            how="left",
        )

        label_map = {
            "1": "Diabetes",
            "1.0": "Diabetes",
            "diabetes": "Diabetes",
            "yes": "Diabetes",
            "true": "Diabetes",
            "2": "No Diabetes",
            "2.0": "No Diabetes",
            "no diabetes": "No Diabetes",
            "no_diabetes": "No Diabetes",
            "no": "No Diabetes",
            "false": "No Diabetes",
        }

        merged["DiabetesStatus"] = (
            merged[condition_col]
            .astype(str)
            .str.strip()
            .str.lower()
            .map(label_map)
        )

        result = (
            merged[["DiabetesStatus", "InscClaimAmtReimbursed"]]
            .dropna()
            .copy()
        )

        result["DiabetesStatus"] = pd.Categorical(
            result["DiabetesStatus"],
            categories=["No Diabetes", "Diabetes"],
            ordered=True,
        )

        return result.sort_values("DiabetesStatus").reset_index(drop=True)

    def claim_distribution_by_state(
        self,
        claim_type: str = "inpatient",
    ) -> pd.DataFrame:
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
        return self.tables["train_beneficiary"].columns.tolist()