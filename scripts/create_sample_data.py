from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
SAMPLE_DIR = PROJECT_ROOT / "data" / "sample"

RANDOM_STATE = 42


TABLE_FILES = {
    "train_beneficiary": "train_beneficiary_clean.parquet",
    "test_beneficiary": "test_beneficiary_clean.parquet",
    "train_inpatient": "train_inpatient_clean.parquet",
    "test_inpatient": "test_inpatient_clean.parquet",
    "train_outpatient": "train_outpatient_clean.parquet",
    "test_outpatient": "test_outpatient_clean.parquet",
    "train_labels": "train_labels_clean.parquet",
    "test_labels": "test_labels_clean.parquet",
}


CLAIM_SAMPLE_SIZES = {
    "train_inpatient": 3000,
    "test_inpatient": 1000,
    "train_outpatient": 5000,
    "test_outpatient": 1000,
}


LABEL_SAMPLE_SIZES = {
    "train_labels": 1000,
    "test_labels": 1000,
}


def load_table(filename: str) -> pd.DataFrame:
    path = PROCESSED_DIR / filename

    if not path.exists():
        raise FileNotFoundError(f"Missing processed file: {path}")

    return pd.read_parquet(path)


def safe_sample(df: pd.DataFrame, n_rows: int) -> pd.DataFrame:
    if len(df) <= n_rows:
        return df.copy().reset_index(drop=True)

    return df.sample(n=n_rows, random_state=RANDOM_STATE).reset_index(drop=True)


def clean_demo_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    if "State" in df.columns:
        df["State"] = (
            df["State"]
            .fillna("Unknown")
            .astype(str)
            .str.replace(".0", "", regex=False)
            .replace({"nan": "Unknown", "None": "Unknown", "<NA>": "Unknown"})
        )

    if "ChronicCond_Diabetes" in df.columns:
        df["ChronicCond_Diabetes"] = (
            df["ChronicCond_Diabetes"]
            .fillna("Unknown")
            .replace({
                1: "Diabetes",
                1.0: "Diabetes",
                "1": "Diabetes",
                "1.0": "Diabetes",
                2: "No Diabetes",
                2.0: "No Diabetes",
                "2": "No Diabetes",
                "2.0": "No Diabetes",
            })
            .astype(str)
            .replace({"nan": "Unknown", "None": "Unknown", "<NA>": "Unknown"})
        )

    return df


def sample_claims(claims: pd.DataFrame, n_rows: int) -> pd.DataFrame:
    claims = claims.copy()

    if "BeneID" in claims.columns:
        claims = claims.dropna(subset=["BeneID"])

    if "Provider" in claims.columns:
        claims = claims.dropna(subset=["Provider"])

    if "InscClaimAmtReimbursed" in claims.columns:
        claims = claims.dropna(subset=["InscClaimAmtReimbursed"])

    return safe_sample(claims, n_rows)


def build_beneficiary_sample(
    beneficiary: pd.DataFrame,
    sampled_claims: list[pd.DataFrame],
) -> pd.DataFrame:
    beneficiary = clean_demo_columns(beneficiary)

    required_bene_ids = set()

    for claims in sampled_claims:
        if "BeneID" in claims.columns:
            required_bene_ids.update(claims["BeneID"].dropna().unique())

    matched = beneficiary[beneficiary["BeneID"].isin(required_bene_ids)].copy()

    # Keep only rows useful for demo analytics.
    if "State" in matched.columns:
        matched = matched[matched["State"] != "Unknown"]

    # If strict filtering removes too much, fall back to all matched rows.
    if matched.empty:
        matched = beneficiary[beneficiary["BeneID"].isin(required_bene_ids)].copy()

    return matched.reset_index(drop=True)


def build_label_sample(
    labels: pd.DataFrame,
    sampled_claims: list[pd.DataFrame],
    n_rows: int,
) -> pd.DataFrame:
    labels = labels.copy()

    if "Provider" not in labels.columns:
        return safe_sample(labels, n_rows)

    required_providers = set()

    for claims in sampled_claims:
        if "Provider" in claims.columns:
            required_providers.update(claims["Provider"].dropna().unique())

    matched = labels[labels["Provider"].isin(required_providers)].copy()

    if matched.empty:
        return safe_sample(labels, n_rows)

    return safe_sample(matched, n_rows)


def save_sample(df: pd.DataFrame, filename: str) -> None:
    output_path = SAMPLE_DIR / filename
    df.to_parquet(output_path, index=False)

    print(
        f"Created sample: {output_path} "
        f"rows={df.shape[0]} columns={df.shape[1]}"
    )


def main() -> None:
    SAMPLE_DIR.mkdir(parents=True, exist_ok=True)

    train_inpatient = sample_claims(
        load_table(TABLE_FILES["train_inpatient"]),
        CLAIM_SAMPLE_SIZES["train_inpatient"],
    )

    test_inpatient = sample_claims(
        load_table(TABLE_FILES["test_inpatient"]),
        CLAIM_SAMPLE_SIZES["test_inpatient"],
    )

    train_outpatient = sample_claims(
        load_table(TABLE_FILES["train_outpatient"]),
        CLAIM_SAMPLE_SIZES["train_outpatient"],
    )

    test_outpatient = sample_claims(
        load_table(TABLE_FILES["test_outpatient"]),
        CLAIM_SAMPLE_SIZES["test_outpatient"],
    )

    train_beneficiary = build_beneficiary_sample(
        load_table(TABLE_FILES["train_beneficiary"]),
        [train_inpatient, train_outpatient],
    )

    test_beneficiary = build_beneficiary_sample(
        load_table(TABLE_FILES["test_beneficiary"]),
        [test_inpatient, test_outpatient],
    )

    train_labels = build_label_sample(
        load_table(TABLE_FILES["train_labels"]),
        [train_inpatient, train_outpatient],
        LABEL_SAMPLE_SIZES["train_labels"],
    )

    test_labels = build_label_sample(
        load_table(TABLE_FILES["test_labels"]),
        [test_inpatient, test_outpatient],
        LABEL_SAMPLE_SIZES["test_labels"],
    )

    save_sample(train_beneficiary, TABLE_FILES["train_beneficiary"])
    save_sample(test_beneficiary, TABLE_FILES["test_beneficiary"])
    save_sample(train_inpatient, TABLE_FILES["train_inpatient"])
    save_sample(test_inpatient, TABLE_FILES["test_inpatient"])
    save_sample(train_outpatient, TABLE_FILES["train_outpatient"])
    save_sample(test_outpatient, TABLE_FILES["test_outpatient"])
    save_sample(train_labels, TABLE_FILES["train_labels"])
    save_sample(test_labels, TABLE_FILES["test_labels"])


if __name__ == "__main__":
    main()