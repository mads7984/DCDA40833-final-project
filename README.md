# DCDA40833-final-project
# Drug Price Comparison & Transparency Analysis

---

## About This Project

This project evaluates how prescription discount platforms compare in terms of:

- Drug availability  
- Listed prices  
- Pricing transparency  

The analysis focuses on **Type 2 diabetes medications**, a category chosen due to its high cost burden, widespread use, and strong representation across multiple platforms.

This project was developed as part of a data analysis capstone and emphasizes **clear methodology, reproducible analysis, and practical insights for consumers**.

---

## Research Question

How does TrumpRx compare to other prescription discount platforms—specifically GoodRx, SingleCare, and Cost Plus Drugs—for selected Type 2 diabetes medications in terms of listed price, drug availability, and pricing transparency?

---

## Project Overview

The project uses a **small-sample comparative approach** to evaluate a selected set of high-cost and commonly prescribed diabetes medications.

Rather than attempting large-scale web scraping (which proved unreliable due to site protections and inconsistent structures), this project uses:

- Targeted data collection  
- Manual verification for accuracy  
- Python-based analysis and visualization  

This approach ensures that results are both **accurate and reproducible**.

---

## Dataset

### Primary Dataset File

data/drug_price_comparison.csv

### Dataset Description

This dataset contains structured information for each drug across multiple platforms.

Each row represents:
> one drug × one platform

---

### Variables Explained

| Column | Description |
|------|-------------|
| drug_name | Name of the medication |
| site | Platform (TrumpRx, GoodRx, SingleCare, CostPlus) |
| listed | 1 = drug is listed, 0 = not listed |
| listed_price | Price shown on the website (numeric) |
| price_type | Type of price (starting, coupon, cash, etc.) |
| dosage | Drug strength (e.g., 10 mg, 1 mg injection) |
| quantity | Number of units (e.g., 30 tablets, 1 pen) |
| price_clear | Price clearly displayed (0/1) |
| dosage_clear | Dosage clearly shown (0/1) |
| quantity_clear | Quantity clearly shown (0/1) |
| price_type_clear | Price type explained (0/1) |
| pharmacy_variation_note | Price variability explained (0/1) |
| restrictions_visible | Coupons/conditions disclosed (0/1) |
| easy_access | Price accessible in ≤ 2 clicks (0/1) |
| transparency_score | Sum of transparency indicators (0–7) |
| notes | Additional observations |

---

## Pricing Transparency Framework

A key contribution of this project is the creation of a **quantitative transparency scoring system**.

Each platform is evaluated based on whether it clearly communicates:

1. Price visibility  
2. Dosage information  
3. Quantity information  
4. Price type explanation  
5. Pharmacy variability  
6. Restrictions or requirements  
7. Ease of accessing pricing  

Each indicator is scored:

0 = not present  
1 = present  

### Transparency Score Calculation

transparency_score = sum of all indicators (0–7)

This allows for:
- direct comparison across platforms  
- statistical analysis  
- visualization of usability differences  

---

## Methodology

### Data Collection

- A set of 5–10 Type 2 diabetes drugs was selected from TrumpRx  
- Each drug was searched across:
  - TrumpRx  
  - GoodRx  
  - SingleCare  
  - Cost Plus Drugs  

### Collection Approach

Due to scraping challenges (e.g., 403 errors, dynamic content, inconsistent HTML structures), a **hybrid approach** was used:

- limited automated scraping where feasible  
- manual data entry and verification  

This ensures **accuracy over automation**.

---

## Analysis Workflow

All analysis is conducted using Python.

### Tools Used
- pandas → data manipulation  
- matplotlib → visualization  

### Key Analyses

- Average price by platform  
- Drug availability by platform  
- Lowest price per drug  
- Price differences relative to TrumpRx  
- Average transparency score by platform  

---

## Project Structure

project_folder/

├── data/  
│   ├── drug_price_comparison.csv  
│   ├── cleaned_drug_data.csv  

├── scripts/  
│   ├── analysis.py  

├── notebooks/  
│   ├── analysis.ipynb  

├── outputs/  
│   ├── average_price_by_site.csv  
│   ├── cheapest_site_per_drug.csv  

├── charts/  
│   ├── avg_price_by_site.png  
│   ├── availability_by_site.png  
│   ├── transparency_scores.png  

├── docs/  
│   ├── project_proposal.docx  
│   ├── final_paper.docx  

└── README.md  

---

## How to Run This Project

### 1. Install Required Packages

pip install pandas matplotlib

### 2. Run Analysis Script

python scripts/analysis.py

### 3. Optional: Use Notebook

Open:
notebooks/analysis.ipynb

---

## Key Outputs

The project produces:

- Cleaned datasets  
- Summary statistics  
- Comparison tables  
- Visualizations (charts)  

These outputs support conclusions about:
- pricing differences  
- availability gaps  
- transparency quality  

---

## Limitations

- Small sample size (intentional for accuracy)  
- Prices vary by location and pharmacy  
- Some platforms use estimates rather than exact prices  
- Manual data entry may introduce minor inconsistencies  

---

## Future Improvements

- Expand to additional drug categories  
- Automate more reliable data collection  
- Include geographic pricing variation  
- Add more platforms  

---

## Connection to Course Objectives

This project demonstrates:

- Data collection and structuring  
- Data cleaning and transformation  
- Quantitative analysis using Python  
- Data visualization  
- Critical evaluation of digital systems  

It reflects iterative development and refinement throughout the course.

---

## Author

Madeline Gordy  
Texas Christian University  
Addran College of Liberal Arts  

---

## Final Summary

This project provides a focused, data-driven comparison of prescription discount platforms. By combining structured data collection with Python-based analysis, it offers meaningful insights into drug pricing and transparency while remaining manageable and reproducible.