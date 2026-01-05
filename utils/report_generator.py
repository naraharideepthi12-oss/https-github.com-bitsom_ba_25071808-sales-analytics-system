"""
Report Generator Module - Task 4: Report Generation
Generates comprehensive formatted sales reports.
"""

from datetime import datetime
from utils.data_processor import (
    calculate_total_revenue, region_wise_sales, top_selling_products,
    customer_analysis, daily_sales_trend, find_peak_sales_day, 
    low_performing_products
)


def generate_sales_report(transactions, enriched_transactions, 
                         output_file='output/sales_report.txt'):
    """
    Generates a comprehensive formatted text report
    
    Args:
        transactions (list): List of validated transaction dictionaries
        enriched_transactions (list): List of enriched transaction dictionaries
        output_file (str): Path to output report file
    """
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            # ===== 1. HEADER =====
            f.write("="*60 + "\n")
            f.write(" "*15 + "SALES ANALYTICS REPORT\n")
            f.write(" "*10 + f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(" "*10 + f"Records Processed: {len(transactions)}\n")
            f.write("="*60 + "\n\n")
            
            # ===== 2. OVERALL SUMMARY =====
            f.write("OVERALL SUMMARY\n")
            f.write("-"*60 + "\n")
            
            total_revenue = calculate_total_revenue(transactions)
            total_transactions = len(transactions)
            avg_order_value = total_revenue / total_transactions if total_transactions > 0 else 0
            
            # Get date range
            dates = [t['Date'] for t in transactions]
            min_date = min(dates) if dates else "N/A"
            max_date = max(dates) if dates else "N/A"
            
            f.write(f"Total Revenue:         ₹{total_revenue:,.2f}\n")
            f.write(f"Total Transactions:    {total_transactions}\n")
            f.write(f"Average Order Value:   ₹{avg_order_value:,.2f}\n")
            f.write(f"Date Range:            {min_date} to {max_date}\n")
            f.write("\n")
            
            # ===== 3. REGION-WISE PERFORMANCE =====
            f.write("REGION-WISE PERFORMANCE\n")
            f.write("-"*60 + "\n")
            f.write(f"{'Region':<15} {'Sales':<18} {'% of Total':<12} {'Transactions':<10}\n")
            f.write("-"*60 + "\n")
            
            region_stats = region_wise_sales(transactions)
            for region, stats in region_stats.items():
                f.write(f"{region:<15} ₹{stats['total_sales']:>15,.2f} "
                       f"{stats['percentage']:>10.2f}% {stats['transaction_count']:>10}\n")
            
            f.write("\n")
            
            # ===== 4. TOP 5 PRODUCTS =====
            f.write("TOP 5 SELLING PRODUCTS\n")
            f.write("-"*60 + "\n")
            f.write(f"{'Rank':<6} {'Product Name':<25} {'Qty':<8} {'Revenue':<15}\n")
            f.write("-"*60 + "\n")
            
            top_products = top_selling_products(transactions, n=5)
            for rank, (product, qty, revenue) in enumerate(top_products, 1):
                f.write(f"{rank:<6} {product:<25} {qty:<8} ₹{revenue:>13,.2f}\n")
            
            f.write("\n")
            
            # ===== 5. TOP 5 CUSTOMERS =====
            f.write("TOP 5 CUSTOMERS\n")
            f.write("-"*60 + "\n")
            f.write(f"{'Rank':<6} {'Customer ID':<15} {'Total Spent':<18} {'Orders':<10}\n")
            f.write("-"*60 + "\n")
            
            customer_stats = customer_analysis(transactions)
            top_customers = list(customer_stats.items())[:5]
            for rank, (customer_id, stats) in enumerate(top_customers, 1):
                f.write(f"{rank:<6} {customer_id:<15} ₹{stats['total_spent']:>15,.2f} "
                       f"{stats['purchase_count']:>10}\n")
            
            f.write("\n")
            
            # ===== 6. DAILY SALES TREND =====
            f.write("DAILY SALES TREND\n")
            f.write("-"*60 + "\n")
            f.write(f"{'Date':<12} {'Revenue':<18} {'Transactions':<15} {'Unique Customers':<15}\n")
            f.write("-"*60 + "\n")
            
            daily_trend = daily_sales_trend(transactions)
            for date, stats in daily_trend.items():
                f.write(f"{date:<12} ₹{stats['revenue']:>15,.2f} "
                       f"{stats['transaction_count']:>14} {stats['unique_customers']:>16}\n")
            
            f.write("\n")
            
            # ===== 7. PRODUCT PERFORMANCE ANALYSIS =====
            f.write("PRODUCT PERFORMANCE ANALYSIS\n")
            f.write("-"*60 + "\n")
            
            peak_date, peak_revenue, peak_count = find_peak_sales_day(transactions)
            f.write(f"Peak Sales Day:        {peak_date}\n")
            f.write(f"Peak Revenue:          ₹{peak_revenue:,.2f}\n")
            f.write(f"Transactions on Peak:  {peak_count}\n\n")
            
            low_products = low_performing_products(transactions, threshold=10)
            if low_products:
                f.write("Low Performing Products (Qty < 10):\n")
                f.write(f"{'Product Name':<25} {'Qty':<8} {'Revenue':<15}\n")
                f.write("-"*60 + "\n")
                for product, qty, revenue in low_products:
                    f.write(f"{product:<25} {qty:<8} ₹{revenue:>13,.2f}\n")
            else:
                f.write("Low Performing Products: None\n")
            
            # Average transaction value per region
            f.write("\nAverage Transaction Value per Region:\n")
            f.write("-"*60 + "\n")
            for region, stats in region_stats.items():
                avg_trans = stats['total_sales'] / stats['transaction_count'] if stats['transaction_count'] > 0 else 0
                f.write(f"{region:<20} ₹{avg_trans:>15,.2f}\n")
            
            f.write("\n")
            
            # ===== 8. API ENRICHMENT SUMMARY =====
            f.write("API ENRICHMENT SUMMARY\n")
            f.write("-"*60 + "\n")
            
            matched_count = sum(1 for t in enriched_transactions if t.get('API_Match', False))
            total_enriched = len(enriched_transactions)
            success_rate = (matched_count / total_enriched * 100) if total_enriched > 0 else 0
            
            f.write(f"Total Products Enriched:  {matched_count}/{total_enriched}\n")
            f.write(f"Success Rate:             {success_rate:.1f}%\n")
            
            # Find non-matched products
            non_matched = []
            for t in enriched_transactions:
                if not t.get('API_Match', False) and t['ProductID'] not in non_matched:
                    non_matched.append(t['ProductID'])
            
            if non_matched:
                f.write(f"\nProducts Not Enriched ({len(non_matched)}):\n")
                for product_id in non_matched[:10]:  # Show first 10
                    f.write(f"  - {product_id}\n")
                if len(non_matched) > 10:
                    f.write(f"  ... and {len(non_matched) - 10} more\n")
            
            f.write("\n")
            f.write("="*60 + "\n")
            f.write(" "*15 + "END OF REPORT\n")
            f.write("="*60 + "\n")
        
        print(f"✓ Report saved to: {output_file}")
        return True
        
    except IOError as e:
        print(f"ERROR: Failed to write report file: {e}")
        return False
    except Exception as e:
        print(f"ERROR: Error generating report: {e}")
        return False
