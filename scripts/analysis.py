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

# Find the average listed price for each site, which will allow us to compare the pricing across different platforms and identify any significant differences in cost for the same drugs. This analysis can reveal which sites tend to have higher or lower prices on average, providing insights into potential cost savings for consumers.
average_price = (
    listed_df.groupby("site")["listed_price"]
    .mean()
    .reset_index(name="average_price")
)

average_price["average_price"] = average_price["average_price"].round(2)

average_price_file = os.path.join(OUTPUT_FOLDER, "average_price_by_site.csv")
average_price.to_csv(average_price_file, index=False)

print("Average price by site:")
print(average_price)
print()


# Calculate the median listed price for each site, which will provide a more robust measure of central tendency for the prices on each platform, especially if there are outliers or skewed distributions. This analysis can help identify which sites have more consistent pricing and which may have extreme values that affect the average price.
median_price = (
    listed_df.groupby("site")["listed_price"]
    .median()
    .reset_index(name="median_price")
)

median_price["median_price"] = median_price["median_price"].round(2)

median_price_file = os.path.join(OUTPUT_FOLDER, "median_price_by_site.csv")
median_price.to_csv(median_price_file, index=False)

print("Median price by site:")
print(median_price)
print()


# Identify the cheapest site for each drug, which will allow us to determine which platform offers the lowest price for each specific medication. This analysis can help consumers make informed decisions about where to purchase their drugs based on cost and can also highlight any significant price differences for the same drug across different sites.
cheapest_by_drug = (
    listed_df.loc[listed_df.groupby("drug_name")["listed_price"].idxmin()]
    .sort_values("drug_name")
    [["drug_name", "site", "listed_price"]]
    .reset_index(drop=True)
)

cheapest_file = os.path.join(OUTPUT_FOLDER, "cheapest_site_per_drug.csv")
cheapest_by_drug.to_csv(cheapest_file, index=False)

print("Cheapest site for each drug:")
print(cheapest_by_drug)
print()


# Count how many times each site is the cheapest for a drug, which will provide insights into which platforms consistently offer the lowest prices for medications. This analysis can help identify which sites are more likely to be the most cost-effective options for consumers and can reveal any trends in pricing across different platforms.
cheapest_counts = (
    cheapest_by_drug["site"]
    .value_counts()
    .reset_index()
)

cheapest_counts.columns = ["site", "times_cheapest"]

cheapest_counts_file = os.path.join(OUTPUT_FOLDER, "times_cheapest_by_site.csv")
cheapest_counts.to_csv(cheapest_counts_file, index=False)

print("How many times each site was cheapest:")
print(cheapest_counts)
print()