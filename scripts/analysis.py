import os
import pandas as pd
import matplotlib.pyplot as plt


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_FILE = os.path.join(BASE_DIR, "data", "drug_price_comparison.csv")
OUTPUT_FOLDER = os.path.join(BASE_DIR, "outputs")
CHARTS_FOLDER = os.path.join(BASE_DIR, "charts")

# Create output directories if they don't exist
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
os.makedirs(CHARTS_FOLDER, exist_ok=True)


# Loading the data
df = pd.read_csv(INPUT_FILE)

print("Data loaded successfully.")
print()
print("First 5 rows:")
print(df.head())
print()


# Cleaning and preprocessing the data
# Replace empty strings with missing values
df = df.replace("", pd.NA)

# Clean text columns
df["drug_name"] = df["drug_name"].astype(str).str.strip()
df["site"] = df["site"].astype(str).str.strip()

# Convert numeric columns
numeric_columns = [
    "listed",
    "listed_price",
    "number_of_clicks_to_access_price",
    "price_clear",
    "dosage_clear",
    "quantity_clear",
    "price_type_clear",
    "pharmacy_variation_note",
    "restrictions_visible",
    "easy_access",
    "transparency_score",
]

for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Fill missing 0/1 fields with 0
binary_columns = [
    "listed",
    "price_clear",
    "dosage_clear",
    "quantity_clear",
    "price_type_clear",
    "pharmacy_variation_note",
    "restrictions_visible",
    "easy_access",
    "transparency_score",
]

for col in binary_columns:
    df[col] = df[col].fillna(0)

# Recalculate transparency score so it is always correct
score_columns = [
    "price_clear",
    "dosage_clear",
    "quantity_clear",
    "price_type_clear",
    "pharmacy_variation_note",
    "restrictions_visible",
    "easy_access",
]

df["transparency_score"] = df[score_columns].sum(axis=1)

# Save cleaned dataset
cleaned_file = os.path.join(OUTPUT_FOLDER, "cleaned_drug_data.csv")
df.to_csv(cleaned_file, index=False)

print(f"Cleaned data saved to: {cleaned_file}")
print()

# Create a subset of the data for listed drugs only from all of the websites
listed_df = df[df["listed"] == 1].copy()

print("Number of total rows:", len(df))
print("Number of listed rows:", len(listed_df))
print()


# Calculate how many drugs are listed on each site and the percentage of total possible drugs, analyzing the availability of drugs across the different sites. This will help us understand which sites have the most comprehensive listings and how they compare to each other in terms of drug availability.
availability = (
    df.groupby("site")["listed"]
    .sum()
    .reset_index(name="drugs_listed")
)

availability["total_possible_drugs"] = df.groupby("site")["drug_name"].count().values
availability["availability_percent"] = (
    availability["drugs_listed"] / availability["total_possible_drugs"] * 100
).round(2)

availability_file = os.path.join(OUTPUT_FOLDER, "availability_by_site.csv")
availability.to_csv(availability_file, index=False)

print("Availability by site:")
print(availability)
print()
