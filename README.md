# Customer Profitability Dashboard

A data-driven dashboard to analyze customer and activity profitability using improved cost allocation methods.

## Problem Statement

Management currently allocates costs to customers based solely on revenue percentage. This approach results in nearly identical profit margins across all customers, making it difficult to identify which customers and activities are truly profitable. The business is experiencing revenue growth, but profitability is not improving at the same rate.

## Solution Overview

This project delivers a Customer Profitability Dashboard that provides a more accurate view of profitability. The solution calculates Cost to Serve for each customer by combining labour costs, space-related costs, and operational costs. Customers are then segmented into four categories based on revenue and real profit margins. The dashboard also identifies which activities create value and which activities destroy value.

## Key Features

- Improved Cost to Serve calculation using multiple data sources
- Customer segmentation into four categories based on profitability
- Identification of value-creating and value-destroying activities
- Interactive visualizations including Treemap and Scatter Matrix
- Clear comparison against the existing revenue-based allocation method

## Data Sources

- M1 Revenue
- M1 Activities
- M1 Labour
- M1 Inventory
- M1 Exceptions
- Cost Allocation Data

## Methodology

- Labour costs were calculated using available data and logical rate assumptions.
- Space-related costs (Rent and Equipment) were allocated using inventory holding data.
- Operational costs (Utilities and Warehouse Management) were allocated using activity volume.
- Customers were segmented using Revenue and Profit Margin thresholds.
- Activities were analyzed to determine their contribution to overall profitability.

## Key Findings

- Storage is the strongest value-creating activity with high profit and low cost per unit.
- Pick generates the highest volume but results in negative profit, making it a major value destroyer.
- Rework and Returns also destroy value due to high operational costs and low efficiency.
- Management’s current allocation method creates misleading flat profit margins across customers.
- A more accurate Cost to Serve reveals significant differences in customer profitability.

## Limitations

- Large portions of the labour dataset were corrupted with missing values.
- Significant mismatches existed between the Activities and Revenue datasets.
- Several cost components could not be fully allocated due to missing data.
- Product-level data was not available for deeper analysis.
- Full time-series analysis was limited due to data quality issues.

## Assumptions

- A standard labour rate of $47.50 per hour was applied where data was missing.
- Space-related costs were allocated proportionally based on average inventory holding.
- Operational costs were allocated based on total activity volume per customer.

## Future Improvements

- Improve data quality and recover missing labour records.
- Collect and integrate additional cost components for more accurate costing.
- Develop dynamic time-series analysis for daily and weekly trends.
- Add automated alerts for customers moving into unprofitable segments.
- Enhance the dashboard with forecasting and scenario analysis capabilities.
- Validate cost allocation models with operational teams.

## Tech Stack

- Python
- Streamlit
- Pandas
- Plotly

## How to Run

```bash
# Clone the repository
git clone <repository-link>

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run files/demo.py
