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

# Calculate the average transparency score for each site, which will allow us to evaluate and compare the overall transparency of pricing information across different platforms. This analysis can help identify which sites provide clearer and more accessible information about drug prices, dosages, quantities, and other relevant details that contribute to a higher transparency score. A higher average transparency score may indicate that a site is more user-friendly and provides better information for consumers
transparency = (
    df.groupby("site")["transparency_score"]
    .mean()
    .reset_index(name="average_transparency_score")
)

transparency["average_transparency_score"] = transparency["average_transparency_score"].round(2)

transparency_file = os.path.join(OUTPUT_FOLDER, "transparency_scores_by_site.csv")
transparency.to_csv(transparency_file, index=False)

print("Average transparency score by site:")
print(transparency)
print()


# Calculate the price difference from TrumpRx for each drug, which will allow us to compare the listed prices on other platforms to the prices offered by TrumpRx. This analysis can help identify how much more expensive or cheaper other sites are compared to TrumpRx for the same drugs, providing insights into potential cost savings or price disparities across different platforms.
trumprx_prices = (
    df[df["site"] == "TrumpRx"][["drug_name", "listed_price"]]
    .rename(columns={"listed_price": "trumprx_price"})
)

price_compare = listed_df.merge(trumprx_prices, on="drug_name", how="left")

price_compare["price_difference_from_trumprx"] = (
    price_compare["listed_price"] - price_compare["trumprx_price"]
).round(2)

price_compare_file = os.path.join(OUTPUT_FOLDER, "price_difference_from_trumprx.csv")
price_compare.to_csv(price_compare_file, index=False)

print("Price difference from TrumpRx:")
print(price_compare[["drug_name", "site", "listed_price", "trumprx_price", "price_difference_from_trumprx"]])
print()

# Create a bar chart to visualize the average listed price for each site, which will allow us to easily compare the pricing across different platforms. This visual representation can help highlight any significant differences in average prices and make it easier for consumers to identify which sites tend to have higher or lower prices on average. By sorting the bars in ascending order, we can quickly see which sites are more affordable and which may be more expensive for consumers looking to purchase their medications. This chart can serve as a useful tool for consumers to make informed decisions about where to buy their drugs based on cost.
avg_price_chart = average_price.sort_values("average_price")

plt.figure(figsize=(8, 5))
plt.bar(avg_price_chart["site"], avg_price_chart["average_price"])
plt.title("Average Listed Price by Site")
plt.xlabel("Site")
plt.ylabel("Average Listed Price")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(CHARTS_FOLDER, "average_price_by_site.png"))
plt.close()


# Create a bar chart to visualize the number of drugs listed on each site, which will allow us to compare the availability of medications across different platforms. This visual representation can help highlight which sites have the most comprehensive listings and how they compare to each other in terms of drug availability. By sorting the bars in descending order, we can quickly see which sites offer the widest selection of drugs and which may have more limited offerings for consumers looking to purchase their medications. This chart can serve as a useful tool for consumers to make informed decisions about where to buy their drugs based on the availability of the medications they need.
availability_chart = availability.sort_values("drugs_listed", ascending=False)

plt.figure(figsize=(8, 5))
plt.bar(availability_chart["site"], availability_chart["drugs_listed"])
plt.title("Number of Drugs Listed by Site")
plt.xlabel("Site")
plt.ylabel("Drugs Listed")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(CHARTS_FOLDER, "availability_by_site.png"))
plt.close()


# Create a bar chart to visualize the average transparency score for each site, which will allow us to compare the overall transparency of pricing information across different platforms. This visual representation can help highlight which sites provide clearer and more accessible information about drug prices, dosages, quantities, and other relevant details that contribute to a higher transparency score. By sorting the bars in descending order, we can quickly see which sites are more user-friendly and provide better information for consumers, making it easier for them to make informed decisions about where to purchase their medications based on the quality of information provided.
transparency_chart = transparency.sort_values("average_transparency_score", ascending=False)

plt.figure(figsize=(8, 5))
plt.bar(transparency_chart["site"], transparency_chart["average_transparency_score"])
plt.title("Average Transparency Score by Site")
plt.xlabel("Site")
plt.ylabel("Average Transparency Score")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(CHARTS_FOLDER, "transparency_scores_by_site.png"))
plt.close()


# Create a bar chart to visualize the listed price for each drug across different sites, which will allow us to compare the pricing for specific medications across various platforms. This visual representation can help highlight any significant price differences for the same drug across different sites and make it easier for consumers to identify which platforms offer the best prices for the medications they need. By grouping the bars by drug and coloring them by site, we can quickly see how the prices vary for each drug across different platforms, providing valuable insights for consumers looking to make informed purchasing decisions based on cost.
pivot_prices = listed_df.pivot(index="drug_name", columns="site", values="listed_price")

pivot_prices.plot(kind="bar", figsize=(10, 6))
plt.title("Listed Price by Drug and Site")
plt.xlabel("Drug")
plt.ylabel("Listed Price")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig(os.path.join(CHARTS_FOLDER, "price_by_drug_and_site.png"))
plt.close()


# Save the output tables and charts for further use and reference. The tables are saved in the "outputs" folder, while the charts are saved in the "charts" folder. This organization allows for easy access to the results of the analysis and provides a clear separation between the data outputs and visualizations. By saving these files, we can ensure that the insights gained from the analysis are preserved and can be easily shared or revisited in the future.
print("Analysis complete.")
print(f"Output tables saved in: {OUTPUT_FOLDER}")
print(f"Charts saved in: {CHARTS_FOLDER}")