# Customer Segmentation Dashboard

## Overview
Interactive Power BI dashboard for customer segmentation analysis enabling data-driven marketing strategies. This project combines SQL-based data extraction, Python preprocessing, and Power BI visualization to identify and analyze customer segments based on purchasing behavior, demographics, and engagement metrics.

## Skills Demonstrated
- Business Intelligence & Data Visualization
- SQL Query Development
- Data Preprocessing & Feature Engineering
- Customer Analytics & RFM Analysis
- Dashboard Design & Storytelling
- Power BI Development

## Tech Stack
- **Visualization**: Power BI Desktop
- **Database**: SQL Server / PostgreSQL
- **Data Processing**: Python (pandas, numpy)
- **Database Connectivity**: pyodbc
- **Analysis**: Customer segmentation algorithms (RFM, K-means)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/TejaVamshidharReddy/Customer-Segmentation-Dashboard.git
cd Customer-Segmentation-Dashboard
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Set up database connection:
   - Update connection strings in `src/data_preparation.py`
   - Ensure SQL Server/PostgreSQL is accessible

4. Run data preparation:
```bash
python src/data_preparation.py
```

5. Open Power BI:
   - Install Power BI Desktop from Microsoft Store
   - Load the prepared data
   - Connect to data source using credentials

## Usage

### 1. Data Extraction
Run SQL queries to extract customer data:
```bash
# Execute segmentation queries
python src/run_segmentation.py
```

### 2. Data Preparation
Preprocess and prepare data for visualization:
```bash
python src/data_preparation.py
```

### 3. Power BI Dashboard
- Open Power BI Desktop
- Import prepared datasets
- Refresh data connections
- Explore interactive visualizations

## Input/Output Examples

### Input:
- **Customer Transactions**: CustomerID, TransactionDate, Amount, ProductCategory
- **Customer Demographics**: CustomerID, Age, Gender, Location, JoinDate
- **Engagement Metrics**: CustomerID, EmailOpens, WebsiteVisits, LastPurchaseDate

### Output:
- **Customer Segments**: High-Value, Medium-Value, Low-Value, At-Risk, New Customers
- **RFM Scores**: Recency, Frequency, Monetary values per customer
- **Visualizations**: 
  - Segment distribution charts
  - Revenue by segment
  - Customer lifecycle analysis
  - Geographic distribution maps
  - Trend analysis over time

## Business Impact

- **Targeted Marketing**: Identify high-value customer segments for personalized campaigns
- **Retention Strategies**: Detect at-risk customers and implement retention programs
- **Revenue Optimization**: Focus resources on segments with highest ROI potential
- **Product Development**: Understand segment-specific preferences and needs
- **Executive Insights**: Real-time dashboards for data-driven decision making
- **Cost Efficiency**: Reduce marketing spend by targeting right customer groups

## Project Structure
```
Customer-Segmentation-Dashboard/
│
├── data/
│   └── sample_customer_data.csv
│
├── src/
│   ├── segmentation_query.sql
│   └── data_preparation.py
│
├── notebooks/
│   └── dashboard_exploration.ipynb
│
├── README.md
└── requirements.txt
```

## Contributing
Feel free to fork this repository and submit pull requests for any improvements.

## License
This project is open source and available under the MIT License.

## Contact
For questions or collaboration opportunities, reach out via GitHub.
