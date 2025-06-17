import csv
import os
import re
from collections import defaultdict
from datetime import datetime

def parse_date(order_date):
    """Parse order_date with multiple formats, return datetime or None."""
    if not order_date:
        return None
    formats = [
        '%d-%m-%Y %H:%M',  # e.g., 27-05-2025 22:29
        '%Y-%m-%d',        # e.g., 2025-05-27
        '%Y-%m-%d %H:%M'   # e.g., 2025-05-27 22:29
    ]
    for fmt in formats:
        try:
            return datetime.strptime(order_date, fmt)
        except ValueError:
            continue
    return None

def format_date(dt):
    """Format datetime to YYYY-MM-DD, or return empty string if None."""
    return dt.strftime('%Y-%m-%d') if dt else ''

def is_test_row(row):
    """Check if any field contains 'test', 'TEST', 'donotfill', or 'DONOTFILL' as standalone words."""
    test_words = r'\b(test|TEST|donotfill|DONOTFILL)\b'
    for value in row.values():
        if value and re.search(test_words, str(value)):
            return True
    return False

def process_woocommerce_csv(input_file, customer_output='customers.csv', order_output='orders.csv', email_only_output='email_only_customers.csv', duplicates_output='duplicate_emails.csv', email_counts_output='email_order_counts.csv', test_output='test.csv'):
    # Initialize dictionaries and lists to store data
    customers_rows = defaultdict(list)  # Store all rows per email
    email_only_customers = {}
    email_counts = defaultdict(int)  # For duplicate email tracking
    order_counts = defaultdict(int)  # For order count per email
    duplicate_rows = []
    test_rows = []

    # Define fields
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

    email_only_fields = ['billing_email']

    duplicate_fields = [
        'billing_email', 'order_id', 'order_date',
        'billing_first_name', 'billing_last_name', 'billing_phone',
        'billing_address_1', 'billing_city', 'billing_state', 'billing_postcode', 'billing_country',
        'order_count'
    ]

    email_counts_fields = ['billing_email', 'order_count']

    # Try different encodings
    encodings = ['utf-8', 'latin1', 'iso-8859-1', 'cp1252']
    selected_encoding = None

    # Attempt to read the file with different encodings
    for encoding in encodings:
        try:
            with open(input_file, 'r', encoding=encoding) as infile:
                reader = csv.DictReader(infile)
                input_fieldnames = reader.fieldnames
                list(reader)
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
        input_fieldnames = reader.fieldnames
        line_number = 1

        # Process each row
        for line_number, row in enumerate(reader, start=2):  # Start from 2 to account for header
            try:
                # Check if row contains test words
                if is_test_row(row):
                    test_rows.append(row)
                    print(f"Warning: Row {line_number} moved to test.csv due to test words")
                    continue

                email = row.get('billing_email', '').strip().lower()  # Case-insensitive
                order_id = row.get('order_id', '').strip()
                if email:  # Only process if email exists
                    # Count email occurrences
                    email_counts[email] += 1

                    # Count orders if order_id exists
                    if order_id:
                        order_counts[email] += 1

                    # Replace 'NULL' with empty string for all fields
                    cleaned_row = {key: '' if str(row.get(key, '')).upper() == 'NULL' else row.get(key, '') for key in row}

                    # Store row for customers (all occurrences)
                    customers_rows[email].append(cleaned_row)
                else:
                    print(f"Warning: Skipping row {line_number} due to missing billing_email")
            except Exception as e:
                print(f"Warning: Skipping row {line_number} due to error: {str(e)}")
                continue

    # Process customers and duplicates
    customers = {}
    for email, rows in customers_rows.items():
        # Check if only billing_email has data
        other_fields_empty = all(
            all(row.get(field, '') == '' for field in customer_fields if field != 'billing_email')
            for row in rows
        )

        if other_fields_empty:
            # Store in email_only_customers
            email_only_customers[email] = {'billing_email': email}
        else:
            # Select the most recent row based on order_date
            latest_row = rows[0]  # Default to first row
            latest_date = None

            for row in rows:
                order_date = row.get('order_date', '').strip()
                current_date = parse_date(order_date)
                if current_date and (latest_date is None or current_date > latest_date):
                    latest_date = current_date
                    latest_row = row
                elif not current_date and order_date:
                    print(f"Warning: Invalid order_date '{order_date}' for email {email}, using first occurrence")

            # Store in customers
            customers[email] = {field: latest_row.get(field, '') for field in customer_fields}

        # Store rows for duplicates if order_count > 1
        if order_counts[email] > 1:
            for row in rows:
                if row.get('order_id', '').strip():  # Only include rows with orders
                    parsed_date = parse_date(row.get('order_date', ''))
                    duplicate_rows.append({
                        field: format_date(parsed_date) if field == 'order_date' else 
                              row.get(field, '') if field != 'order_count' else order_counts[email]
                        for field in duplicate_fields
                    })

    # Calculate email statistics
    unique_emails = sum(1 for count in email_counts.values() if count == 1)
    duplicate_emails = sum(1 for count in order_counts.values() if count > 1)
    unique_customers = len(email_counts)

    # Print statistics
    print(f"Test rows filtered: {len(test_rows)}")
    print(f"Unique email IDs: {unique_emails}")
    print(f"Duplicate emails: {duplicate_emails}")
    print(f"Unique customers: {unique_customers}")

    # Write customer data to CSV
    with open(customer_output, 'w', encoding='utf-8', newline='') as cust_file:
        writer = csv.DictWriter(cust_file, fieldnames=customer_fields)
        writer.writeheader()
        for customer in customers.values():
            writer.writerow(customer)

    # Write email-only customer data to CSV
    with open(email_only_output, 'w', encoding='utf-8', newline='') as email_file:
        writer = csv.DictWriter(email_file, fieldnames=email_only_fields)
        writer.writeheader()
        for customer in email_only_customers.values():
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
                    if is_test_row(row):
                        continue  # Skip test rows
                    if row.get('billing_email', '').strip():  # Only process if email exists
                        # Replace 'NULL' with empty string for all fields
                        cleaned_row = {key: '' if str(row.get(key, '')).upper() == 'NULL' else row.get(key, '') for key in row}
                        # Reformat order_date to YYYY-MM-DD
                        parsed_date = parse_date(cleaned_row.get('order_date', ''))
                        order_data = {
                            field: format_date(parsed_date) if field == 'order_date' else cleaned_row.get(field, '')
                            for field in order_fields
                        }
                        writer.writerow(order_data)
                except Exception as e:
                    print(f"Warning: Skipping row {line_number} in orders due to error: {str(e)}")
                    continue

    # Write duplicate emails to CSV
    with open(duplicates_output, 'w', encoding='utf-8', newline='') as dup_file:
        writer = csv.DictWriter(dup_file, fieldnames=duplicate_fields)
        writer.writeheader()
        for row in duplicate_rows:
            writer.writerow(row)

    # Write email order counts to CSV
    with open(email_counts_output, 'w', encoding='utf-8', newline='') as count_file:
        writer = csv.DictWriter(count_file, fieldnames=email_counts_fields)
        writer.writeheader()
        for email, count in order_counts.items():
            writer.writerow({'billing_email': email, 'order_count': count})

    # Write test rows to CSV
    with open(test_output, 'w', encoding='utf-8', newline='') as test_file:
        writer = csv.DictWriter(test_file, fieldnames=input_fieldnames)
        writer.writeheader()
        for row in test_rows:
            writer.writerow(row)

def main():
    input_file = 'woocommerce_export.csv'
    try:
        process_woocommerce_csv(input_file)
        print(f"Successfully created customers.csv, email_only_customers.csv, orders.csv, duplicate_emails.csv, email_order_counts.csv, and test.csv")
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found")
    except ValueError as ve:
        print(f"Error: {str(ve)}")
    except Exception as e:
        print(f"Unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    main()
