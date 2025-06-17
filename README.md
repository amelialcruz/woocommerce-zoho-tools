# WooCommerce to Zoho CRM Tools

This repository contains Python scripts to process WooCommerce export CSV files, generating customer and order data optimized for Zoho CRM imports. The primary script, `process_woocommerce_csv.py`, splits a WooCommerce export into two CSV files: one for unique customer records and another for order details with associated customer information.

## process_woocommerce_csv.py

This Python script is designed to process exported WooCommerce order CSV files, cleaning and transforming the data into separate, structured CSV files for customer information, order details, email-only customer records, duplicate email analysis, and email order counts. It's particularly useful for preparing WooCommerce data for CRM imports, marketing segmentation, or analytical purposes.

---

## Features

* **Flexible CSV Encoding**: Automatically attempts to decode input CSVs using common encodings (`utf-8`, `latin1`, `iso-8859-1`, `cp1252`) to prevent decoding errors.
* **Data Cleaning**: Replaces `'NULL'` string values with empty strings across all fields for cleaner data.
* **Test Data Filtering**: Identifies and segregates rows containing "test", "TEST", "donotfill", or "DONOTFILL" (case-insensitive, as whole words) into a separate `test.csv` file, preventing erroneous data from contaminating main outputs.
* **Customer Segmentation**:
    * Generates a `customers.csv` containing unique customer records. For customers with multiple orders, it intelligently selects the most recent order's details to represent the customer's latest information.
    * Creates an `email_only_customers.csv` for records where only an email address is provided, indicating incomplete customer data.
* **Order Extraction**: Produces an `orders.csv` with core order details, including a reformatted `order_date` (`YYYY-MM-DD`).
* **Duplicate Analysis**:
    * Identifies and lists `duplicate_emails.csv` for emails associated with more than one order, helping to spot repeat customers or potential data entry issues.
    * Generates `email_order_counts.csv` summarizing the total number of orders per unique email address.
* **Robust Date Parsing**: Handles multiple date formats (`DD-MM-YYYY HH:MM`, `YYYY-MM-DD`, `YYYY-MM-DD HH:MM`) for the `order_date` field.

---

## How It Works

The script reads your main WooCommerce export CSV. It iterates through each row, performs data cleaning, and checks for test-related keywords. Based on the `billing_email`, it categorizes and consolidates customer and order information. For customers with multiple entries, it intelligently picks the most recent order's data for the main customer record. Finally, it writes the processed data into five distinct CSV files.

---

## Installation

This script requires **Python 3.x**. No external libraries beyond Python's standard library are needed.

1.  **Save the script**: Save the provided code as a Python file (e.g., `woo_processor.py`).
2.  **Prepare your input CSV**: Ensure your WooCommerce export CSV is named `woocommerce_export.csv` and placed in the same directory as the script. If your file has a different name, you'll need to update the `input_file` variable in the `main()` function of the script.

---

## Usage

To run the script, open your terminal or command prompt, navigate to the directory where you saved `woo_processor.py` and your `woocommerce_export.csv`, and execute the following command:

```bash
python woo_processor.py
````

Upon successful execution, you will find the following new CSV files generated in the same directory:

-----

## Output Files

  * **`customers.csv`**: Contains a unique record for each customer with their latest billing and shipping information.
      * **Fields**: `billing_email`, `billing_first_name`, `billing_last_name`, `billing_phone`, `billing_address_1`, `billing_address_2`, `billing_city`, `billing_state`, `billing_postcode`, `billing_country`, `shipping_first_name`, `shipping_last_name`, `shipping_address_1`, `shipping_address_2`, `shipping_city`, `shipping_state`, `shipping_postcode`, `shipping_country`.
  * **`orders.csv`**: Lists all valid order entries with key details.
      * **Fields**: `order_id`, `order_date`, `billing_email`, `billing_first_name`, `billing_last_name`, `billing_phone`, `order_total`, `payment_method`, `order_status`.
  * **`email_only_customers.csv`**: Contains records where only the `billing_email` was populated in the original data, indicating incomplete customer profiles.
      * **Fields**: `billing_email`.
  * **`duplicate_emails.csv`**: Captures all order entries for email addresses that appear more than once (i.e., customers with multiple orders). Includes the `order_count` for that specific email.
      * **Fields**: `billing_email`, `order_id`, `order_date`, `billing_first_name`, `billing_last_name`, `billing_phone`, `billing_address_1`, `billing_city`, `billing_state`, `billing_postcode`, `billing_country`, `order_count`.
  * **`email_order_counts.csv`**: Provides a summary of how many orders are associated with each unique `billing_email`.
      * **Fields**: `billing_email`, `order_count`.
  * **`test.csv`**: Contains all original rows that were identified as containing test data. This file preserves the full original structure of the input CSV.

-----

## Date Formats

The `parse_date` function is designed to handle the following `order_date` formats from your input CSV:

  * `DD-MM-YYYY HH:MM` (e.g., `27-05-2025 22:29`)
  * `YYYY-MM-DD` (e.g., `2025-05-27`)
  * `YYYY-MM-DD HH:MM` (e.g., `2025-05-27 22:29`)

All `order_date` values in the output CSVs (`orders.csv`, `duplicate_emails.csv`) will be formatted as `YYYY-MM-DD`.

-----

## Test Data Handling

The `is_test_row` function performs a case-insensitive search for the exact words "test", "donotfill", "TEST", or "DONOTFILL" in any field within a row. Rows identified as containing these words will be moved to `test.csv` and excluded from all other output files.

-----

## Error Handling & Warnings

The script includes basic `try-except` blocks to handle common issues like `FileNotFoundError` for the input CSV and `UnicodeDecodeError` during file reading (by attempting multiple encodings). It also provides warnings in the console for:

  * Rows skipped due to a missing `billing_email`.
  * Rows skipped due to general processing errors.
  * Rows moved to `test.csv` because they contain test words.
  * Invalid `order_date` formats, which will default to using the first occurrence of the customer's data if a valid date isn't found for selection.

-----

## Contributing

Contributions are welcome\! If you have suggestions for improvements, new features, or bug fixes, please feel free to open an [issue](https://www.google.com/search?q=https://github.com/amelialcruz/woocommerce-zoho-tools/issues) or submit a [pull request](https://www.google.com/search?q=https://github.com/amelialcruz/woocommerce-zoho-tools/pulls).

-----

```
```

