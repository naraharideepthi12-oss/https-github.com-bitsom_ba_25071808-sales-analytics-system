"""
File Handler Module - Task 1: Data File Handler & Preprocessing
Handles reading, parsing, and validating sales data with error handling.
"""


def read_sales_data(filename):
    """
    Reads sales data from file handling encoding issues
    
    Args:
        filename (str): Path to the sales data file
        
    Returns:
        list: Raw lines (strings) from the file
        
    Expected Output Format:
    ['T001|2024-12-01|P101|Laptop|2|45000|C001|North', ...]
    
    Requirements:
    - Use 'with' statement
    - Handle different encodings (try 'utf-8', 'latin-1', 'cp1252')
    - Handle FileNotFoundError with appropriate error message
    - Skip the header row
    - Remove empty lines
    """
    encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
    lines = []
    
    for encoding in encodings:
        try:
            with open(filename, 'r', encoding=encoding) as f:
                lines = f.readlines()
            print(f"✓ Successfully read file with {encoding} encoding")
            break
        except UnicodeDecodeError:
            continue
        except FileNotFoundError:
            print(f"ERROR: File not found at {filename}")
            return []
        except Exception as e:
            print(f"ERROR: Problem reading file: {e}")
            return []
    
    if not lines:
        print("ERROR: Could not read file with any encoding")
        return []
    
    # Skip header row and remove empty lines
    raw_lines = []
    for i, line in enumerate(lines):
        if i == 0:  # Skip header
            continue
        line = line.strip()
        if line:  # Skip empty lines
            raw_lines.append(line)
    
    return raw_lines


def parse_transactions(raw_lines):
    """
    Parses raw lines into clean list of dictionaries
    
    Args:
        raw_lines (list): List of raw transaction strings
        
    Returns:
        list: List of dictionaries with transaction data
        
    Expected Output Format:
    [
        {
            'TransactionID': 'T001',
            'Date': '2024-12-01',
            'ProductID': 'P101',
            'ProductName': 'Laptop',
            'Quantity': 2,           # int type
            'UnitPrice': 45000.0,    # float type
            'CustomerID': 'C001',
            'Region': 'North'
        },
        ...
    ]
    
    Requirements:
    - Split by pipe delimiter '|'
    - Handle commas within ProductName (remove or replace)
    - Remove commas from numeric fields and convert to proper types
    - Convert Quantity to int
    - Convert UnitPrice to float
    - Skip rows with incorrect number of fields
    """
    transactions = []
    
    for line in raw_lines:
        try:
            fields = line.split('|')
            
            # Check if we have the correct number of fields
            if len(fields) < 8:
                continue
            
            # Extract fields
            transaction_id = fields[0].strip()
            date = fields[1].strip()
            product_id = fields[2].strip()
            product_name = fields[3].strip()
            quantity_str = fields[4].strip()
            unit_price_str = fields[5].strip()
            customer_id = fields[6].strip()
            region = fields[7].strip()
            
            # Handle commas in ProductName - remove them
            product_name = product_name.replace(',', '')
            
            # Remove commas from numeric fields
            quantity_str = quantity_str.replace(',', '')
            unit_price_str = unit_price_str.replace(',', '')
            
            # Convert to proper types
            try:
                quantity = int(quantity_str)
                unit_price = float(unit_price_str)
            except ValueError:
                continue
            
            transaction = {
                'TransactionID': transaction_id,
                'Date': date,
                'ProductID': product_id,
                'ProductName': product_name,
                'Quantity': quantity,
                'UnitPrice': unit_price,
                'CustomerID': customer_id,
                'Region': region
            }
            
            transactions.append(transaction)
            
        except Exception as e:
            # Skip malformed rows
            continue
    
    return transactions


def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    """
    Validates transactions and applies optional filters
    
    Args:
        transactions (list): List of transaction dictionaries
        region (str, optional): Filter by specific region
        min_amount (float, optional): Minimum transaction amount (Quantity * UnitPrice)
        max_amount (float, optional): Maximum transaction amount
        
    Returns:
        tuple: (valid_transactions, invalid_count, filter_summary)
        
    Expected Output Format:
    (
        [list of valid filtered transactions],
        5,  # count of invalid transactions
        {
            'total_input': 100,
            'invalid': 5,
            'filtered_by_region': 20,
            'filtered_by_amount': 10,
            'final_count': 65
        }
    )
    
    Validation Rules:
    - Quantity must be > 0
    - UnitPrice must be > 0
    - All required fields must be present
    - TransactionID must start with 'T'
    - ProductID must start with 'P'
    - CustomerID must start with 'C'
    """
    valid_transactions = []
    invalid_count = 0
    filtered_by_region = 0
    filtered_by_amount = 0
    
    # Get available regions and amount range for display
    all_amounts = [t['Quantity'] * t['UnitPrice'] for t in transactions 
                   if t['Quantity'] > 0 and t['UnitPrice'] > 0]
    
    if all_amounts:
        min_trans_amount = min(all_amounts)
        max_trans_amount = max(all_amounts)
    else:
        min_trans_amount = 0
        max_trans_amount = 0
    
    available_regions = set()
    
    for transaction in transactions:
        # Validate required fields
        required_fields = ['TransactionID', 'Date', 'ProductID', 'ProductName', 
                          'Quantity', 'UnitPrice', 'CustomerID', 'Region']
        
        if not all(field in transaction for field in required_fields):
            invalid_count += 1
            continue
        
        # Validation rules
        if transaction['Quantity'] <= 0:
            invalid_count += 1
            continue
        
        if transaction['UnitPrice'] <= 0:
            invalid_count += 1
            continue
        
        if not transaction['TransactionID'].startswith('T'):
            invalid_count += 1
            continue
        
        if not transaction['ProductID'].startswith('P'):
            invalid_count += 1
            continue
        
        if not transaction['CustomerID'].startswith('C'):
            invalid_count += 1
            continue
        
        if not transaction['Region']:
            invalid_count += 1
            continue
        
        # Track available regions
        available_regions.add(transaction['Region'])
        
        # Calculate transaction amount
        transaction_amount = transaction['Quantity'] * transaction['UnitPrice']
        
        # Apply region filter
        if region and transaction['Region'] != region:
            filtered_by_region += 1
            continue
        
        # Apply amount filters
        if min_amount and transaction_amount < min_amount:
            filtered_by_amount += 1
            continue
        
        if max_amount and transaction_amount > max_amount:
            filtered_by_amount += 1
            continue
        
        valid_transactions.append(transaction)
    
    # Display available options to user
    print("\n" + "="*50)
    print("FILTER OPTIONS AVAILABLE")
    print("="*50)
    print(f"Available Regions: {', '.join(sorted(available_regions))}")
    print(f"Transaction Amount Range: ₹{min_trans_amount:,.2f} - ₹{max_trans_amount:,.2f}")
    print("="*50)
    
    # Create summary dictionary
    filter_summary = {
        'total_input': len(transactions),
        'invalid': invalid_count,
        'filtered_by_region': filtered_by_region,
        'filtered_by_amount': filtered_by_amount,
        'final_count': len(valid_transactions)
    }
    
    return valid_transactions, invalid_count, filter_summary
