# Verint Migration Toolkit

The Verint Migration Toolkit is a Python-based application that extracts configuration data (such as Organizations, Groups, Employees, Roles, and Access Rights) from a legacy Verint instance via authenticated API calls. It outputs the processed data into an Excel workbook for audit, analysis, and use in migration workflows.

---

## Project Structure

```
verint_migration_toolkit/
│
├── main.py                     # Entrypoint script to trigger all extractors
├── config.py                   # Loads API credentials and base URL from .env
├── verint_client.py            # Wrapper for API authentication and requests
├── hmac_auth.py                # Custom Verint HMAC authentication logic
│
├── extractors/
│   ├── organization_extractor.py
│   ├── group_extractor.py
│   ├── employee_extractor.py
│   ├── access_rights_extractor.py
│   └── role_extractor.py
│
├── output/                     # Folder where final Excel output is written
│   └── verint_full_export.xlsx
│
└── json_dump/                  # Timestamped raw API responses (for audit/debug)
```

---

## How to Run

### 1. Install Dependencies

Make sure you have Python 3.8+ and pip installed. Then:

```bash
pip install -r requirements.txt
```

### 2. Set Environment Variables

Create a `.env` file in the root directory and define the following:

```
VERINT_BASE_URL=https://your-verint-instance.com
VERINT_API_KEY_ID=your_api_key_id
VERINT_API_KEY_SECRET=your_base64_encoded_secret
```

> Make sure your secret is base64url-encoded.

### 3. Execute the Script

You can run the extractors individually or all together via:

```bash
python main.py
```

---

## Output Files

- The primary output file is: `output/verint_full_export.xlsx`
  - Sheets include:
    - Organization Hierarchy
    - Group Hierarchy
    - Employees
    - Access Rights
    - Roles

- Raw JSON responses are stored in `json_dump/` with timestamps.

---

## Status

This toolkit is intended to support auditing and preparation for migrating Verint configurations from legacy systems to new instances in a structured, trackable manner.

---

