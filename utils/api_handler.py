"""
API Handler Module - Task 3: API Integration
Handles fetching product data from DummyJSON API and enriching sales data.
"""

import requests
import json


def fetch_all_products():
    """
    Fetches all products from DummyJSON API
    
    Returns:
        list: List of product dictionaries
        
    Expected Output Format:
    [
        {
            'id': 1,
            'title': 'iPhone 9',
            'category': 'smartphones',
            'brand': 'Apple',
            'price': 549,
            'rating': 4.69
        },
        ...
    ]
    
    Requirements:
    - Fetch all available products (use limit=100)
    - Handle connection errors with try-except
    - Return empty list if API fails
    - Print status message (success/failure)
    """
    try:
        url = "https://dummyjson.com/products?limit=100"
        print(f"Fetching products from API: {url}")
        
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        products = data.get('products', [])
        
        # Extract only needed fields
        simplified_products = []
        for product in products:
            simplified_products.append({
                'id': product.get('id'),
                'title': product.get('title'),
                'category': product.get('category'),
                'brand': product.get('brand'),
                'price': product.get('price'),
                'rating': product.get('rating')
            })
        
        print(f"✓ Successfully fetched {len(simplified_products)} products from API")
        return simplified_products
        
    except requests.exceptions.Timeout:
        print("ERROR: API request timed out")
        return []
    except requests.exceptions.ConnectionError:
        print("ERROR: Could not connect to API")
        return []
    except requests.exceptions.HTTPError as e:
        print(f"ERROR: HTTP error occurred: {e}")
        return []
    except (json.JSONDecodeError, KeyError) as e:
        print(f"ERROR: Invalid response format from API: {e}")
        return []
    except Exception as e:
        print(f"ERROR: Failed to fetch products: {e}")
        return []


def create_product_mapping(api_products):
    """
    Creates a mapping of product IDs to product info
    
    Args:
        api_products (list): List of products from fetch_all_products()
        
    Returns:
        dict: Dictionary mapping product IDs to info
        
    Expected Output Format:
    {
        1: {'title': 'iPhone 9', 'category': 'smartphones', 'brand': 'Apple', 'rating': 4.69},
        2: {'title': 'iPhone X', 'category': 'smartphones', 'brand': 'Apple', 'rating': 4.44},
        ...
    }
    """
    product_mapping = {}
    
    for product in api_products:
        product_id = product.get('id')
        if product_id:
            product_mapping[product_id] = {
                'title': product.get('title'),
                'category': product.get('category'),
                'brand': product.get('brand'),
                'rating': product.get('rating')
            }
    
    return product_mapping


def enrich_sales_data(transactions, api_products):
    """
    Enriches sales transactions with API product data
    
    Args:
        transactions (list): List of transaction dictionaries
        api_products (list): List of products from API
        
    Returns:
        list: List of enriched transaction dictionaries
    """
    # Create product mapping
    product_mapping = create_product_mapping(api_products)
    
    enriched_transactions = []
    enriched_count = 0
    
    for transaction in transactions:
        enriched_transaction = transaction.copy()
        
        # Try to extract numeric ID from ProductID (e.g., P101 -> 101)
        product_id_str = transaction['ProductID']
        try:
            numeric_id = int(product_id_str[1:]) if product_id_str.startswith('P') else None
        except (ValueError, IndexError):
            numeric_id = None
        
        # Look up in API data
        if numeric_id and numeric_id in product_mapping:
            api_product = product_mapping[numeric_id]
            enriched_transaction['API_Category'] = api_product.get('category')
            enriched_transaction['API_Brand'] = api_product.get('brand')
            enriched_transaction['API_Rating'] = api_product.get('rating')
            enriched_transaction['API_Match'] = True
            enriched_count += 1
        else:
            enriched_transaction['API_Category'] = None
            enriched_transaction['API_Brand'] = None
            enriched_transaction['API_Rating'] = None
            enriched_transaction['API_Match'] = False
        
        enriched_transactions.append(enriched_transaction)
    
    enrichment_rate = (enriched_count / len(transactions) * 100) if transactions else 0
    print(f"✓ Enriched {enriched_count}/{len(transactions)} transactions ({enrichment_rate:.1f}%)")
    
    return enriched_transactions


def save_enriched_data(enriched_transactions, filename='output/enriched_sales_data.txt'):
    """
    Saves enriched transactions back to file
    
    Args:
        enriched_transactions (list): List of enriched transaction dictionaries
        filename (str): Output file path
        
    Expected File Format:
    TransactionID|Date|ProductID|ProductName|Quantity|UnitPrice|CustomerID|Region|API_Category|API_Brand|API_Rating|API_Match
    T001|2024-12-01|P101|Laptop|2|45000.0|C001|North|laptops|Apple|4.7|True
    
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            # Write header
            header = "TransactionID|Date|ProductID|ProductName|Quantity|UnitPrice|CustomerID|Region|API_Category|API_Brand|API_Rating|API_Match\n"
            f.write(header)
            
            # Write data rows
            for transaction in enriched_transactions:
                # Handle None values
                api_category = transaction.get('API_Category', '')
                api_brand = transaction.get('API_Brand', '')
                api_rating = transaction.get('API_Rating', '')
                api_match = transaction.get('API_Match', False)
                
                row = (f"{transaction['TransactionID']}|"
                       f"{transaction['Date']}|"
                       f"{transaction['ProductID']}|"
                       f"{transaction['ProductName']}|"
                       f"{transaction['Quantity']}|"
                       f"{transaction['UnitPrice']}|"
                       f"{transaction['CustomerID']}|"
                       f"{transaction['Region']}|"
                       f"{api_category}|"
                       f"{api_brand}|"
                       f"{api_rating}|"
                       f"{api_match}\n")
                
                f.write(row)
        
        print(f"✓ Saved enriched data to: {filename}")
        return True
        
    except IOError as e:
        print(f"ERROR: Failed to save enriched data: {e}")
        return False
    except Exception as e:
        print(f"ERROR: Unexpected error while saving: {e}")
        return False
