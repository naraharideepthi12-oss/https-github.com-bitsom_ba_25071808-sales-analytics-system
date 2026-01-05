"""
Sales Analytics System - Main Application
Complete execution flow for sales data processing and analysis.
"""

import sys
from utils.file_handler import read_sales_data, parse_transactions, validate_and_filter
from utils.data_processor import (
    calculate_total_revenue, region_wise_sales, top_selling_products,
    customer_analysis, daily_sales_trend, find_peak_sales_day,
    low_performing_products
)
from utils.api_handler import fetch_all_products, enrich_sales_data, save_enriched_data
from utils.report_generator import generate_sales_report


def print_header():
    """Print welcome header"""
    print("\n" + "="*60)
    print(" "*12 + "SALES ANALYTICS SYSTEM")
    print("="*60)
    print()


def print_step(step_num, total_steps, message):
    """Print formatted step message"""
    print(f"[{step_num}/{total_steps}] {message}")


def main():
    """
    Main execution function
    
    Workflow:
    1. Print welcome message
    2. Read sales data file (handle encoding)
    3. Parse and clean transactions
    4. Display filter options to user
    5. Ask if user wants to filter
    6. Validate transactions
    7. Display validation summary
    8. Perform all data analyses
    9. Fetch products from API
    10. Enrich sales data with API info
    11. Save enriched data to file
    12. Generate comprehensive report
    13. Print success message with file locations
    """
    
    try:
        print_header()
        
        # Step 1: Read sales data
        print_step(1, 13, "Reading sales data...")
        raw_lines = read_sales_data('data/sales_data.txt')
        
        if not raw_lines:
            print("ERROR: No data to process. Exiting.")
            return
        
        print(f"✓ Successfully read {len(raw_lines)} transaction lines\n")
        
        # Step 2: Parse and clean transactions
        print_step(2, 13, "Parsing and cleaning data...")
        parsed_transactions = parse_transactions(raw_lines)
        
        if not parsed_transactions:
            print("ERROR: No valid transactions parsed. Exiting.")
            return
        
        print(f"✓ Parsed {len(parsed_transactions)} records\n")
        
        # Step 3: Display filter options
        print_step(3, 13, "Displaying filter options...")
        all_transactions, invalid_count, summary = validate_and_filter(parsed_transactions)
        print()
        
        # Step 4: Ask user for filtering
        filtered_transactions = all_transactions
        user_filter = input("Do you want to filter data? (y/n): ").strip().lower()
        
        if user_filter == 'y':
            print("\nAvailable filters:")
            print("1. Filter by Region")
            print("2. Filter by Amount Range")
            print("3. Filter by Both")
            
            filter_choice = input("Select filter option (1-3): ").strip()
            
            region_filter = None
            min_amount = None
            max_amount = None
            
            if filter_choice in ['1', '3']:
                # Get regions from all transactions
                regions = set(t['Region'] for t in all_transactions if t.get('Region'))
                print(f"Available regions: {', '.join(sorted(regions))}")
                region_filter = input("Enter region: ").strip()
            
            if filter_choice in ['2', '3']:
                try:
                    min_amount_str = input("Enter minimum amount (or press Enter to skip): ").strip()
                    max_amount_str = input("Enter maximum amount (or press Enter to skip): ").strip()
                    
                    min_amount = float(min_amount_str) if min_amount_str else None
                    max_amount = float(max_amount_str) if max_amount_str else None
                except ValueError:
                    print("Invalid amount entered. Skipping amount filter.")
            
            # Re-validate with filters
            filtered_transactions, invalid_count, summary = validate_and_filter(
                parsed_transactions, 
                region=region_filter, 
                min_amount=min_amount, 
                max_amount=max_amount
            )
        
        print()
        
        # Step 5: Validate transactions
        print_step(4, 13, "Validating transactions...")
        print(f"✓ Valid Records: {len(filtered_transactions)}")
        print(f"✓ Invalid Records Removed: {summary['invalid']}")
        print(f"✓ Final Count: {summary['final_count']}\n")
        
        if len(filtered_transactions) == 0:
            print("ERROR: No valid transactions after filtering. Exiting.")
            return
        
        # Step 6: Perform data analysis
        print_step(5, 13, "Analyzing sales data...")
        
        total_revenue = calculate_total_revenue(filtered_transactions)
        region_stats = region_wise_sales(filtered_transactions)
        top_products = top_selling_products(filtered_transactions, n=5)
        customer_stats = customer_analysis(filtered_transactions)
        daily_trend = daily_sales_trend(filtered_transactions)
        peak_day = find_peak_sales_day(filtered_transactions)
        low_products = low_performing_products(filtered_transactions, threshold=10)
        
        print(f"✓ Analysis complete")
        print(f"  - Total Revenue: ₹{total_revenue:,.2f}")
        print(f"  - Regions Analyzed: {len(region_stats)}")
        print(f"  - Top Product: {top_products[0][0] if top_products else 'N/A'}")
        print(f"  - Peak Sales Day: {peak_day[0] if peak_day[0] else 'N/A'}\n")
        
        # Step 7: Fetch product data from API
        print_step(6, 13, "Fetching product data from API...")
        api_products = fetch_all_products()
        print()
        
        # Step 8: Enrich sales data
        print_step(7, 13, "Enriching sales data with API information...")
        enriched_transactions = enrich_sales_data(filtered_transactions, api_products)
        print()
        
        # Step 9: Save enriched data
        print_step(8, 13, "Saving enriched data...")
        save_enriched_data(enriched_transactions)
        print()
        
        # Step 10: Generate report
        print_step(9, 13, "Generating comprehensive report...")
        generate_sales_report(filtered_transactions, enriched_transactions)
        print()
        
        # Step 11: Success message
        print_step(10, 13, "Process Complete!")
        print()
        
        print("="*60)
        print("SUMMARY")
        print("="*60)
        print(f"✓ Data processed successfully!")
        print(f"✓ Valid transactions: {len(filtered_transactions)}")
        print(f"✓ Output files created:")
        print(f"  - Enriched data: data/enriched_sales_data.txt")
        print(f"  - Report: output/sales_report.txt")
        print("="*60 + "\n")
        
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
    except Exception as e:
        print(f"\n\nERROR: An unexpected error occurred: {e}")
        print("Please check your input and try again.")
        return


if __name__ == "__main__":
    main()
