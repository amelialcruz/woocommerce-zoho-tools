# WooCommerce to Zoho CRM Tools

This repository contains Python scripts to process WooCommerce export CSV files, generating customer and order data optimized for Zoho CRM imports. The primary script, `process_woocommerce_csv.py`, splits a WooCommerce export into two CSV files: one for unique customer records and another for order details with associated customer information.

## Features

- **Customer Extraction**: Deduplicates customer data using `billing_email` as the unique identifier.
- **Order Details**: Includes customer details (first name, last name, phone) in the orders CSV for seamless Zoho CRM integration.
- **Data Cleaning**: Replaces 'NULL' values with empty strings for cleaner imports.
- **Encoding Support**: Handles multiple input CSV encodings (UTF-8, Latin1, ISO-8859-1, CP1252).
- **Error Handling**: Skips problematic rows with detailed error logging for debugging.

## Prerequisites

- **Python 3.6+**: The script uses standard libraries (`csv`, `os`, `collections`), so no additional dependencies are required.
- **WooCommerce Export CSV**: Must include the following headers:
  ```
  order_id,order_date,billing_first_name,billing_last_name,billing_email,billing_phone,
  billing_address_1,billing_address_2,billing_city,billing_state,billing_postcode,
  billing_country,shipping_first_name,shipping_last_name,shipping_address_1,
  shipping_address_2,shipping_city,shipping_state,shipping_postcode,shipping_country,
  order_total,payment_method,order_status
  ```

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/woocommerce-zoho-tools.git
   cd woocommerce-zoho-tools
   ```
2. **Verify Python Version**:
   ```bash
   python3 --version
   ```
   Ensure Python 3.6 or higher is installed. No additional dependencies are needed.

## Usage

1. Place your WooCommerce export CSV file (e.g., `woocommerce_export.csv`) in the `scripts/` directory.
2. Run the script:
   ```bash
   python3 scripts/process_woocommerce_csv.py
   ```
3. **Output Files**:
   - `customers.csv`: Unique customer records with billing and shipping details.
   - `orders.csv`: Order details with billing email, first name, last name, and phone.

## Input File Format

The input CSV must include the headers listed in the **Prerequisites** section. Example row:
```
order_id,order_date,billing_first_name,billing_last_name,billing_email,billing_phone,...
123,2025-01-01,John,Doe,john.doe@example.com,123-456-7890,...
```

## Output Files

- **customers.csv**:
  - **Fields**: `billing_email`, `billing_first_name`, `billing_last_name`, `billing_phone`, `billing_address_1`, `billing_address_2`, `billing_city`, `billing_state`, `billing_postcode`, `billing_country`, `shipping_first_name`, `shipping_last_name`, `shipping_address_1`, `shipping_address_2`, `shipping_city`, `shipping_state`, `shipping_postcode`, `shipping_country`
  - **Notes**: Deduplicated by `billing_email`; 'NULL' values replaced with empty strings.

- **orders.csv**:
  - **Fields**: `order_id`, `order_date`, `billing_email`, `billing_first_name`, `billing_last_name`, `billing_phone`, `order_total`, `payment_method`, `order_status`
  - **Notes**: Includes customer details for Zoho CRM compatibility; 'NULL' values replaced with empty strings.

## Troubleshooting

- **Encoding Errors**: The script tries UTF-8, Latin1, ISO-8859-1, and CP1252 encodings. If errors persist, save your CSV as UTF-8 in a text editor (e.g., Notepad++ or VS Code).
- **Skipped Rows**: Check console output for line numbers and errors if rows are skipped. Inspect those lines in the input CSV for invalid data.
- **Zoho CRM Import**: Map output CSV fields to Zoho CRM fields during import, as Zoho may use different field names.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For issues or suggestions, open an issue on GitHub or contact [amelialcruz01@gmail.com].
