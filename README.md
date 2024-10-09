# AllWinRX: Pharmacy Data Optimization Project

### Team Members:
- **Adarsh Reddy** (Project Manager)
- **Steven Lo** (Data Engineer)
- **Yonathan Amare** (Software Engineer)

## Project Overview
AllWinRX aims to assist small independent pharmacies in calculating drug price comparisons and potential savings by joining the All Win Rx Group Purchasing Organization (GPO). We developed a comprehensive database and analytical tools to help these pharmacies quantify discounts and improve profitability by providing accurate cost analyses and strategic purchasing tools.

## Problem Addressed
Small pharmacies often face higher medicine costs due to limited bargaining power. Our project helps these pharmacies evaluate potential savings from GPO memberships by collecting relevant data, analyzing pricing information, and generating strategic recommendations.

## Solution
We created a robust **SQL database** to store drug prices and customer purchase data. To gather missing data, we developed a web scraper using **Selenium** (**webdriver.py**) that extracts pricing and drug information from an online pharmaceutical resource. Additionally, SQL queries were implemented in **calculations.py** to compute potential savings from GPO rebates, considering factors such as generic drug percentages and discount tiers. The **database.py** script connects to the SQL database to retrieve missing drug codes, ensuring complete and accurate data for further analysis.

## Technologies Used
- **Programming Languages**: Python, SQL, HTML
- **Data Storage**: MySQL (hosted on LMU Build)
- **Software/Tools**: DBeaver, Visual Studio Code, Selenium

---

## Key Features
- **Comprehensive Drug Price Database**: A SQL database containing drug prices, generic names, strength, size, form, and estimated rebates.
- **Automated Web Scraping**: A web scraper (**webdriver.py**) built with Selenium to gather missing data such as drug pricing and rebate information.
- **Analytical Tools**: SQL queries (**calculations.py**) to calculate savings from GPO rebates based on total drug purchases and generic drug percentages.
- **Data Completion**: The **database.py** script retrieves missing drug codes and updates the database to ensure complete data integrity for analysis.

---

## Code Files Overview

### 1. `webdriver.py`
- **Purpose**: This script uses Selenium to automate web scraping of drug pricing information from an online pharmaceutical resource. It gathers key data such as the trade name, generic name, strength, size, form, price, and estimated rebate.
- **Key Functionality**:
  - Logs into the pharmaceutical website.
  - Scrapes drug pricing and rebate data based on unique drug codes (CIN).
  - Updates the SQL database with the scraped information.

### 2. `calculations.py`
- **Purpose**: This script calculates potential savings for pharmacies by analyzing total purchase costs and applying relevant discounts from the GPO. It determines the percentage of generic drugs purchased and uses this to find applicable rebates.
- **Key Functionality**:
  - Fetches total purchase costs from the SQL database.
  - Calculates the percentage of generic drugs in the overall purchases.
  - Applies the GPO discount tiers based on purchase totals and generic percentages.

### 3. `database.py`
- **Purpose**: This script connects to the MySQL database and retrieves missing drug codes (CIN) from the `MasterSheet`. It ensures all necessary data is collected for further analysis.
- **Key Functionality**:
  - Connects to the MySQL database.
  - Queries for missing or incomplete drug data.
  - Outputs the missing drug codes for further web scraping or data entry.

---

## Future Improvements
- **Additional Supplier Data**: Integrating data from more supplier websites to provide a wider range of price comparisons.
- **Enhanced Database**: Expanding the database with more detailed drug information for more comprehensive analysis.
- **Improved Web Scraping**: Optimizing the web scraper for faster and more efficient data extraction.

## Contact
For more information, feel free to reach out to any of the project members or visit our [GitHub repository](#).
