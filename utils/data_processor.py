"""
Data Processor Module - Task 2: Data Processing
Performs comprehensive analysis on sales transactions.
"""

from datetime import datetime
from collections import defaultdict


def calculate_total_revenue(transactions):
    """
    Calculates total revenue from all transactions
    
    Args:
        transactions (list): List of transaction dictionaries
        
    Returns:
        float: Total revenue (sum of Quantity * UnitPrice)
    """
    total_revenue = 0.0
    for transaction in transactions:
        total_revenue += transaction['Quantity'] * transaction['UnitPrice']
    
    return total_revenue


def region_wise_sales(transactions):
    """
    Analyzes sales by region
    
    Args:
        transactions (list): List of transaction dictionaries
        
    Returns:
        dict: Dictionary with region statistics
        
    Expected Output Format:
    {
        'North': {
            'total_sales': 450000.0,
            'transaction_count': 15,
            'percentage': 29.13
        },
        'South': {...},
        ...
    }
    """
    total_revenue = calculate_total_revenue(transactions)
    
    region_data = defaultdict(lambda: {'total_sales': 0.0, 'transaction_count': 0})
    
    for transaction in transactions:
        region = transaction['Region']
        amount = transaction['Quantity'] * transaction['UnitPrice']
        region_data[region]['total_sales'] += amount
        region_data[region]['transaction_count'] += 1
    
    # Calculate percentages and sort by total_sales
    result = {}
    for region, data in sorted(region_data.items(), 
                               key=lambda x: x[1]['total_sales'], 
                               reverse=True):
        percentage = (data['total_sales'] / total_revenue * 100) if total_revenue > 0 else 0
        result[region] = {
            'total_sales': data['total_sales'],
            'transaction_count': data['transaction_count'],
            'percentage': round(percentage, 2)
        }
    
    return result


def top_selling_products(transactions, n=5):
    """
    Finds top n products by total quantity sold
    
    Args:
        transactions (list): List of transaction dictionaries
        n (int): Number of top products to return (default: 5)
        
    Returns:
        list: List of tuples (ProductName, TotalQuantity, TotalRevenue)
        
    Expected Output Format:
    [
        ('Laptop', 45, 2250000.0),
        ('Mouse', 38, 19000.0),
        ...
    ]
    """
    product_data = defaultdict(lambda: {'quantity': 0, 'revenue': 0.0})
    
    for transaction in transactions:
        product_name = transaction['ProductName']
        quantity = transaction['Quantity']
        amount = transaction['Quantity'] * transaction['UnitPrice']
        
        product_data[product_name]['quantity'] += quantity
        product_data[product_name]['revenue'] += amount
    
    # Sort by quantity descending and get top n
    sorted_products = sorted(product_data.items(),
                            key=lambda x: x[1]['quantity'],
                            reverse=True)[:n]
    
    result = [(product, data['quantity'], data['revenue']) 
              for product, data in sorted_products]
    
    return result


def customer_analysis(transactions):
    """
    Analyzes customer purchase patterns
    
    Args:
        transactions (list): List of transaction dictionaries
        
    Returns:
        dict: Dictionary of customer statistics
        
    Expected Output Format:
    {
        'C001': {
            'total_spent': 95000.0,
            'purchase_count': 3,
            'avg_order_value': 31666.67,
            'products_bought': ['Laptop', 'Mouse', 'Keyboard']
        },
        'C002': {...},
        ...
    }
    """
    customer_data = defaultdict(lambda: {
        'total_spent': 0.0,
        'purchase_count': 0,
        'products': set()
    })
    
    for transaction in transactions:
        customer_id = transaction['CustomerID']
        amount = transaction['Quantity'] * transaction['UnitPrice']
        
        customer_data[customer_id]['total_spent'] += amount
        customer_data[customer_id]['purchase_count'] += 1
        customer_data[customer_id]['products'].add(transaction['ProductName'])
    
    # Convert to final format and sort by total_spent descending
    result = {}
    for customer_id, data in sorted(customer_data.items(),
                                   key=lambda x: x[1]['total_spent'],
                                   reverse=True):
        avg_order_value = data['total_spent'] / data['purchase_count'] if data['purchase_count'] > 0 else 0
        result[customer_id] = {
            'total_spent': data['total_spent'],
            'purchase_count': data['purchase_count'],
            'avg_order_value': round(avg_order_value, 2),
            'products_bought': sorted(list(data['products']))
        }
    
    return result


def daily_sales_trend(transactions):
    """
    Analyzes sales trends by date
    
    Args:
        transactions (list): List of transaction dictionaries
        
    Returns:
        dict: Dictionary sorted by date
        
    Expected Output Format:
    {
        '2024-12-01': {
            'revenue': 125000.0,
            'transaction_count': 8,
            'unique_customers': 6
        },
        '2024-12-02': {...},
        ...
    }
    """
    daily_data = defaultdict(lambda: {
        'revenue': 0.0,
        'transaction_count': 0,
        'customers': set()
    })
    
    for transaction in transactions:
        date = transaction['Date']
        amount = transaction['Quantity'] * transaction['UnitPrice']
        
        daily_data[date]['revenue'] += amount
        daily_data[date]['transaction_count'] += 1
        daily_data[date]['customers'].add(transaction['CustomerID'])
    
    # Convert to final format and sort chronologically
    result = {}
    for date in sorted(daily_data.keys()):
        data = daily_data[date]
        result[date] = {
            'revenue': data['revenue'],
            'transaction_count': data['transaction_count'],
            'unique_customers': len(data['customers'])
        }
    
    return result


def find_peak_sales_day(transactions):
    """
    Identifies the date with highest revenue
    
    Args:
        transactions (list): List of transaction dictionaries
        
    Returns:
        tuple: (date, revenue, transaction_count)
    """
    daily_trend = daily_sales_trend(transactions)
    
    if not daily_trend:
        return None, 0, 0
    
    peak_date = max(daily_trend.items(), key=lambda x: x[1]['revenue'])
    date = peak_date[0]
    data = peak_date[1]
    
    return (date, data['revenue'], data['transaction_count'])


def low_performing_products(transactions, threshold=10):
    """
    Identifies products with low sales
    
    Args:
        transactions (list): List of transaction dictionaries
        threshold (int): Minimum quantity threshold (default: 10)
        
    Returns:
        list: List of tuples (ProductName, TotalQuantity, TotalRevenue)
        
    Expected Output Format:
    [
        ('Webcam', 4, 12000.0),
        ('Headphones', 7, 10500.0),
        ...
    ]
    """
    product_data = defaultdict(lambda: {'quantity': 0, 'revenue': 0.0})
    
    for transaction in transactions:
        product_name = transaction['ProductName']
        quantity = transaction['Quantity']
        amount = transaction['Quantity'] * transaction['UnitPrice']
        
        product_data[product_name]['quantity'] += quantity
        product_data[product_name]['revenue'] += amount
    
    # Filter products below threshold and sort by quantity ascending
    low_performers = [(product, data['quantity'], data['revenue'])
                      for product, data in product_data.items()
                      if data['quantity'] < threshold]
    
    low_performers.sort(key=lambda x: x[1])
    
    return low_performers
