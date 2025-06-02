import csv
import os
from collections import defaultdict

def process_woocommerce_csv(input_file, customer_output='customers.csv', order_output='orders.csv'):
    # Initialize dictionaries to store unique customer data
    customers = {}

    # Define customer and order fields
    customer_fields = [
        'billing_email', 'billing_first_name', 'billing_last_name', 
        'billing_phone', 'billing_address_1', 'billing_address_2',
        'billing_city', 'billing_state', 'billing_postcode', 'billing_country',
        'shipping_first_name', 'shipping_last_name', 'shipping_address_1',
        'shipping_address_2', 'shipping_city', 'shipping_state',
        'shipping_postcode', 'shipping_country'
    ]

    order_fields = [
        'order_id', 'order_date', 'billing_email', 
        'billing_first_name', 'billing_last_name', 'billing_phone',
        'order_total', 'payment_method', 'order_status'
    ]

    # Try different encodings
    encodings = ['utf-8', 'latin1', 'iso-8859-1', 'cp1252']
    selected_encoding = None

    # Attempt to read the entire file with different encodings
    for encoding in encodings:
        try:
            with open(input_file, 'r', encoding=encoding) as infile:
                reader = csv.DictReader(infile)
                # Test read the entire file to ensure encoding works
                list(reader)  # This will read all rows and catch encoding errors
                selected_encoding = encoding
                break
        except UnicodeDecodeError:
            continue

    if not selected_encoding:
        raise ValueError("Could not decode file with any supported encoding (utf-8, latin1, iso-8859-1, cp1252)")

    print(f"Using encoding: {selected_encoding}")

    # Read input CSV
    with open(input_file, 'r', encoding=selected_encoding) as infile:
        reader = csv.DictReader(infile)
        line_number = 1

        # Process each row
        for line_number, row in enumerate(reader, start=2):  # Start from 2 to account for header
            try:
                email = row.get('billing_email', '').strip()
                if email:  # Only process if email exists
                    # Replace 'NULL' with empty string for all fields
                    cleaned_row = {key: '' if str(row.get(key, '')).upper() == 'NULL' else row.get(key, '') for key in row}
                    # Store customer data (using email as unique identifier)
                    customers[email] = {field: cleaned_row.get(field, '') for field in customer_fields}
            except Exception as e:
                print(f"Warning: Skipping row {line_number} due to error: {str(e)}")
                continue

    # Write customer data to CSV
    with open(customer_output, 'w', encoding='utf-8', newline='') as cust_file:
        writer = csv.DictWriter(cust_file, fieldnames=customer_fields)
        writer.writeheader()
        for customer in customers.values():
            writer.writerow(customer)

    # Write order data to CSV
    with open(order_output, 'w', encoding='utf-8', newline='') as order_file:
        writer = csv.DictWriter(order_file, fieldnames=order_fields)
        writer.writeheader()

        # Re-read input file to write orders
        with open(input_file, 'r', encoding=selected_encoding) as infile:
            reader = csv.DictReader(infile)
            for line_number, row in enumerate(reader, start=2):
                try:
                    if row.get('billing_email', '').strip():  # Only process if email exists
                        # Replace 'NULL' with empty string for all fields
                        cleaned_row = {key: '' if str(row.get(key, '')).upper() == 'NULL' else row.get(key, '') for key in row}
                        order_data = {field: cleaned_row.get(field, '') for field in order_fields}
                        writer.writerow(order_data)
                except Exception as e:
                    print(f"Warning: Skipping row {line_number} in orders due to error: {str(e)}")
                    continue

def main():
    input_file = 'woocommerce_export.csv'  # Update with your input file name
    try:
        process_woocommerce_csv(input_file)
        print(f"Successfully created customers.csv and orders.csv")
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found")
    except ValueError as ve:
        print(f"Error: {str(ve)}")
    except Exception as e:
        print(f"Unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    main()