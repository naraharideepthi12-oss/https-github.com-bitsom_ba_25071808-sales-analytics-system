#!/usr/bin/env python
"""Quick test script to verify all modules work correctly"""

import sys
from utils.file_handler import read_sales_data, parse_transactions, validate_and_filter
from utils.data_processor import (
    calculate_total_revenue, region_wise_sales, top_selling_products,
    customer_analysis, daily_sales_trend, find_peak_sales_day,
    low_performing_products
)
from utils.api_handler import fetch_all_products
from utils.report_generator import generate_sales_report

print("=" * 60)
print("SALES ANALYTICS SYSTEM - QUICK TEST")
print("=" * 60)
print()

# Test 1: Read data
print("[1] Testing data reading...")
raw_lines = read_sales_data('data/sales_data.txt')
print(f"✓ Read {len(raw_lines)} lines")
print()

# Test 2: Parse data
print("[2] Testing data parsing...")
transactions = parse_transactions(raw_lines)
print(f"✓ Parsed {len(transactions)} transactions")
print()

# Test 3: Validate data
print("[3] Testing data validation...")
valid, invalid, summary = validate_and_filter(transactions)
print(f"✓ Valid: {len(valid)}, Invalid: {invalid}")
print()

# Test 4: Analytics
print("[4] Testing analytics functions...")
revenue = calculate_total_revenue(valid)
regions = region_wise_sales(valid)
top_prod = top_selling_products(valid, n=3)
customers = customer_analysis(valid)
daily = daily_sales_trend(valid)
peak = find_peak_sales_day(valid)
low = low_performing_products(valid, threshold=10)

print(f"✓ Total Revenue: ₹{revenue:,.2f}")
print(f"✓ Regions analyzed: {len(regions)}")
print(f"✓ Top product: {top_prod[0][0] if top_prod else 'None'}")
print(f"✓ Customers tracked: {len(customers)}")
print(f"✓ Daily records: {len(daily)}")
print(f"✓ Peak sales day: {peak[0]}")
print(f"✓ Low performers: {len(low)}")
print()

# Test 5: API (if available)
print("[5] Testing API connection...")
products = fetch_all_products()
print()

# Test 6: Report
print("[6] Testing report generation...")
from utils.api_handler import enrich_sales_data
enriched = enrich_sales_data(valid, products)
report_result = generate_sales_report(valid, enriched)
print()

print("=" * 60)
print("ALL TESTS COMPLETED SUCCESSFULLY!")
print("=" * 60)
print()
print("To run the full application with interactive mode:")
print("  python main.py")
