# Sales Analytics System

A comprehensive Python-based Sales Data Analytics System that processes sales data, integrates with external APIs, performs detailed analysis, and generates comprehensive reports.

## Overview

This system is designed to:

- Read and clean messy sales transaction files
- Parse complex and malformed data with multiple encoding formats
- Validate transactions according to business rules
- Fetch real-time product information from APIs
- Perform sophisticated sales pattern and customer behavior analysis
- Generate comprehensive formatted reports
- Enrich sales data with external API information

## Project Structure

```
sales-analytics-system/
├── README.md                      # This file
├── main.py                        # Main execution script
├── requirements.txt               # Python dependencies
├── utils/
│   ├── __init__.py
│   ├── file_handler.py           # Data reading and parsing (Part 1)
│   ├── data_processor.py         # Sales analysis functions (Part 2)
│   ├── api_handler.py            # API integration (Part 3)
│   └── report_generator.py       # Report generation (Part 4)
├── data/
│   ├── sales_data.txt            # Input sales data file
│   └── enriched_sales_data.txt   # Generated enriched data output
└── output/
    └── sales_report.txt          # Generated comprehensive report
```

## Features

### Part 1: Data File Handler & Preprocessing

- **Multi-encoding Support**: Automatically handles UTF-8, Latin-1, CP1252 encoding
- **Robust Parsing**: Splits pipe-delimited data with error handling
- **Data Cleaning**:
  - Removes commas from product names and numeric fields
  - Handles missing fields and extra fields
  - Converts data to proper types (int, float)
- **Validation**: Filters invalid records based on:
  - Quantity > 0
  - Unit Price > 0
  - Valid transaction/product/customer IDs
  - Required fields present
  - Valid regions
- **User Filtering**: Optional filtering by region and transaction amount range

### Part 2: Data Processing & Analysis

Comprehensive sales analytics including:

- **Revenue Analysis**
  - Total revenue calculation
  - Region-wise sales breakdown
  - Revenue by percentage of total
- **Product Analysis**
  - Top 5 selling products by quantity
  - Low performing products (below threshold)
  - Revenue per product
- **Customer Analysis**
  - Top customers by total spent
  - Purchase count per customer
  - Average order value
  - Products bought by customer
- **Temporal Analysis**
  - Daily sales trends
  - Peak sales day identification
  - Unique customer count per day
  - Transaction count per day

### Part 3: API Integration

- **DummyJSON API Integration**: Fetches product data from https://dummyjson.com/products
- **Product Mapping**: Maps local product IDs to API product information
- **Data Enrichment**: Adds category, brand, and rating information to sales data
- **Error Handling**: Gracefully handles API failures with fallback options
- **Data Export**: Saves enriched data to file with all original and new fields

### Part 4: Report Generation

Generates formatted text reports including:

- **Header Section**: Report title, generation timestamp, record count
- **Overall Summary**: Total revenue, transaction count, average order value, date range
- **Region Performance**: Sales by region with percentages and transaction counts
- **Top Products**: Top 5 selling products with revenue
- **Top Customers**: Top 5 customers by spending
- **Daily Trends**: Day-by-day revenue, transaction, and customer metrics
- **Product Performance**: Peak sales day, low performers, regional averages
- **API Enrichment**: Success rate and unmatched products

### Part 5: Main Application

Complete workflow with:

- Interactive user prompts for filtering options
- Step-by-step progress indicators
- Comprehensive error handling
- User-friendly console output
- File creation confirmations

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Setup Steps

1. **Clone or download the repository**

   ```bash
   cd sales-analytics-system
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Verify directory structure**
   Ensure the following directories exist:
   - `data/` (contains sales_data.txt)
   - `output/` (will contain generated reports)
   - `utils/` (contains module files)

## Usage

### Basic Execution

Run the main script:

```bash
python main.py
```

### Interactive Features

The program will prompt you with options:

1. **Data Loading**: Automatically reads and parses sales data from `data/sales_data.txt`
2. **Filter Options**: Choose to filter data by:
   - Region (North, South, East, West)
   - Transaction amount range
   - Both filters combined
3. **Automatic Analysis**: Performs all analyses on selected data
4. **Report Generation**: Creates detailed report in `output/sales_report.txt`
5. **Data Enrichment**: Fetches API data and saves enriched transactions

### Example Session

```
============================================================
                SALES ANALYTICS SYSTEM
============================================================

[1/13] Reading sales data...
✓ Successfully read 80 transaction lines

[2/13] Parsing and cleaning data...
✓ Parsed 80 records

[3/13] Displaying filter options...
==================================================
FILTER OPTIONS AVAILABLE
==================================================
Available Regions: East, North, South, West
Transaction Amount Range: ₹173.00 - ₹818,960.00
==================================================

Do you want to filter data? (y/n): n

[4/13] Validating transactions...
✓ Valid Records: 70
✓ Invalid Records Removed: 10
✓ Final Count: 70

[5/13] Analyzing sales data...
✓ Analysis complete
  - Total Revenue: ₹1,545,000.00
  - Regions Analyzed: 4
  - Top Product: Laptop
  - Peak Sales Day: 2024-12-15

[6/13] Fetching product data from API...
✓ Successfully fetched 30 products from API

[7/13] Enriching sales data...
✓ Enriched 65/70 transactions (92.9%)

[8/13] Saving enriched data...
✓ Saved to: data/enriched_sales_data.txt

[9/13] Generating comprehensive report...
✓ Report saved to: output/sales_report.txt

[10/13] Process Complete!

============================================================
SUMMARY
============================================================
✓ Data processed successfully!
✓ Valid transactions: 70
✓ Output files created:
  - Enriched data: data/enriched_sales_data.txt
  - Report: output/sales_report.txt
============================================================
```

## Output Files

### 1. enriched_sales_data.txt

Pipe-delimited file containing all transactions with enriched API data:

```
TransactionID|Date|ProductID|ProductName|Quantity|UnitPrice|CustomerID|Region|API_Category|API_Brand|API_Rating|API_Match
T001|2024-12-01|P101|Laptop|2|59328.0|C008|North|laptops|HP|4.5|True
T002|2024-12-01|P102|Mouse|5|801.0|C008|South|computer accessories||0|False
```

### 2. sales_report.txt

Comprehensive formatted text report with:

- Summary statistics
- Regional breakdown
- Top products and customers
- Daily sales trends
- Performance analysis
- API enrichment summary

## Data Validation Rules

Records are REMOVED (Invalid) if:

- Missing CustomerID or Region
- Quantity ≤ 0
- UnitPrice ≤ 0
- TransactionID doesn't start with 'T'
- ProductID doesn't start with 'P'
- CustomerID doesn't start with 'C'

Records are CLEANED and KEPT (Valid) if:

- Have commas in ProductName → commas removed
- Have commas in numbers → commas removed, converted to int/float
- All required fields present
- Pass validation rules above

## Error Handling

The system includes comprehensive error handling for:

- **File I/O Errors**: FileNotFoundError, encoding issues, write failures
- **API Errors**: Connection timeouts, HTTP errors, JSON parsing errors
- **Data Errors**: Invalid data types, missing fields, malformed records
- **User Input**: Invalid filter options, incorrect format
- **Processing Errors**: Division by zero, missing data

All errors are caught and displayed with user-friendly messages without crashing the program.

## Data Statistics

Expected from sample dataset (80 raw records):

- Total records in file: 80
- Invalid records to remove: 10
- Valid records after cleaning: 70
- Expected regions: North, South, East, West
- Expected products: ~10 different products
- Date range: December 2024

## Dependencies

- **requests** (2.31.0): For API integration with DummyJSON

Install with:

```bash
pip install -r requirements.txt
```

## Module Documentation

### utils/file_handler.py

- `read_sales_data(filename)`: Reads file with encoding handling
- `parse_transactions(raw_lines)`: Parses and cleans transaction data
- `validate_and_filter(transactions, region, min_amount, max_amount)`: Validates and filters data

### utils/data_processor.py

- `calculate_total_revenue(transactions)`: Computes total revenue
- `region_wise_sales(transactions)`: Analyzes sales by region
- `top_selling_products(transactions, n)`: Finds top n products
- `customer_analysis(transactions)`: Analyzes customer patterns
- `daily_sales_trend(transactions)`: Daily sales breakdown
- `find_peak_sales_day(transactions)`: Identifies highest revenue day
- `low_performing_products(transactions, threshold)`: Finds underperforming products

### utils/api_handler.py

- `fetch_all_products()`: Fetches products from DummyJSON API
- `create_product_mapping(api_products)`: Creates ID-to-product mapping
- `enrich_sales_data(transactions, api_products)`: Enriches with API data
- `save_enriched_data(enriched_transactions, filename)`: Saves enriched data

### utils/report_generator.py

- `generate_sales_report(transactions, enriched_transactions, output_file)`: Generates comprehensive report

## Troubleshooting

### Issue: "File not found" error

- **Solution**: Ensure `data/sales_data.txt` exists in the data folder

### Issue: API connection error

- **Solution**: Check internet connection; system will continue without API enrichment

### Issue: Permission denied when writing files

- **Solution**: Ensure you have write permissions for the project directory

### Issue: Encoding errors when reading file

- **Solution**: System automatically tries multiple encodings; if still failing, verify file format

### Issue: No valid transactions after filtering

- **Solution**: Adjust filter criteria or use no filters to process all valid records

## Performance

- Processes 100+ transaction records in under 1 second
- Fetches API data in 1-3 seconds (depending on connection)
- Generates reports in under 100ms
- Memory efficient with streaming file operations where possible

## Future Enhancements

- Export reports to PDF/Excel formats
- Dashboard web interface
- Real-time data monitoring
- Advanced analytics with charts/visualizations
- Database integration
- Automated scheduling

## License

This project is provided as-is for educational purposes.

## Support

For issues or questions, please refer to the inline code documentation and error messages provided by the system.
