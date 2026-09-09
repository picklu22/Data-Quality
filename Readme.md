# Data Quality Framework

A comprehensive Python-based data quality validation framework designed for Snowflake data warehouses. This framework provides automated testing and validation of data quality metrics including null checks, duplicate detection, pattern matching, data type validation, and outlier detection.

## 📋 Overview

The Data Quality Framework is a modular testing suite that validates data quality requirements against Snowflake databases. It reads quality rules from Excel configuration files and executes comprehensive validation tests to ensure data integrity and consistency.

**Key Capabilities:**
- Automated null value detection
- Duplicate record identification
- Pattern and format validation
- Data type verification
- Outlier detection and analysis
- Configurable quality rules via Excel
- HTML test report generation
- Snowflake integration with connection pooling

## 📁 Project Structure

```
DataQuality/
├── Config/
│   ├── __init__.py
│   ├── config.py              # Configuration module loading from config.yml
│   └── config.yml             # Snowflake connection settings
├── Connector/
│   └── Snowflake_Connection.py # Database connection utilities
├── Src/
│   ├── __init__.py
│   ├── Snowflake_Connection.py # Snowflake connector wrapper
│   ├── excel_reader.py         # Excel configuration file reader
│   ├── query_executor.py       # SQL query execution layer
│   └── validator.py            # Data quality validation functions
├── tests/
│   ├── test_data_type_check.py    # Data type validation tests
│   ├── test_duplicate_check.py    # Duplicate detection tests
│   ├── test_null_check.py         # Null value validation tests
│   ├── test_outlier_check.py      # Outlier detection tests
│   └── test_patteren_check.py     # Pattern matching tests
├── test_data/
│   └── data_quality_requirements.xlsx  # Quality rules configuration
├── Report/                     # Generated HTML test reports
├── conftest.py                 # Pytest fixtures and configuration
├── pytest.ini                  # Pytest settings
├── requirements.txt            # Python dependencies
└── Readme.md                   # This file
```

## 🛠️ Technology Stack

- **Python 3.10+** - Core programming language
- **Snowflake** - Cloud data warehouse
- **Pytest** - Testing framework
- **Pandas** - Data manipulation and Excel reading
- **NumPy** - Numerical computations
- **PyYAML** - Configuration management
- **Python-dotenv** - Environment variable handling
- **ReportLab** - Report generation
- **Pytest-HTML** - HTML test reporting

## 🚀 Setup Instructions

### Prerequisites
- Python 3.10 or higher
- Snowflake account with appropriate access
- pip package manager

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd DataQuality
   ```

2. **Create virtual environment (optional but recommended):**
   ```bash
   python -m venv .venv
   # On Windows:
   .venv\Scripts\activate
   # On macOS/Linux: 
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Snowflake connection:**
   - Edit `Config/config.yml` with your Snowflake credentials:
   ```yaml
   snowflake:
     account: "YOUR_ACCOUNT_ID"
     user: "YOUR_USERNAME"
     password: "YOUR_PASSWORD"
     warehouse: "YOUR_WAREHOUSE"
     database: "YOUR_DATABASE"
     schema: "YOUR_SCHEMA"
     role: "YOUR_ROLE"
   ```

## 📊 Core Modules

### Config Module (`Config/`)
Manages application configuration and Snowflake connection settings loaded from `config.yml`.

**Key exports:**
- `SNOWFLAKE_USER` - Database user
- `SNOWFLAKE_PASSWORD` - Authentication password
- `SNOWFLAKE_ACCOUNT` - Snowflake account identifier
- `SNOWFLAKE_WAREHOUSE` - Compute warehouse
- `SNOWFLAKE_DATABASE` - Target database
- `SNOWFLAKE_SCHEMA` - Target schema

### Connection Module (`Connector/` & `Src/`)
Provides Snowflake database connection management.

**Functions:**
- `get_connection()` - Returns active Snowflake connection

### Validation Module (`Src/validator.py`)
Core validation functions for data quality checks.

**Key Functions:**
- `check_null(connection, table_name, field_name)` - Validates no null values exist
- `check_duplicate(connection, table_name, field_name)` - Detects duplicate records
- `check_pattern(connection, table_name, field_name, pattern)` - Validates pattern compliance
- `check_data_type(connection, table_name, field_name, expected_type)` - Type validation
- `check_outliers(connection, table_name, field_name)` - Identifies statistical outliers

### Data Reader Module (`Src/excel_reader.py`)
Reads data quality requirements from Excel files.

**Functions:**
- `read_rules(file_path)` - Loads validation rules from XLSX file

### Query Executor Module (`Src/query_executor.py`)
Executes SQL queries against Snowflake.

**Functions:**
- `execute_query(connection, query)` - Executes SQL and returns results

## 🧪 Running Tests

### Run all tests:
```bash
pytest
```

### Run specific test file:
```bash
pytest tests/test_null_check.py -v
```

### Run with HTML report:
```bash
pytest --html=Report/report.html
```

### Run tests verbosely:
```bash
pytest -v
```

### Run specific test by marker:
```bash
pytest -k "null" -v
```

## 📋 Test Suite Overview

| Test File | Purpose |
|-----------|---------|
| `test_null_check.py` | Validates required fields contain no null values |
| `test_duplicate_check.py` | Detects and reports duplicate records |
| `test_data_type_check.py` | Verifies column data types match expectations |
| `test_patteren_check.py` | Validates data format and pattern compliance |
| `test_outlier_check.py` | Identifies statistical outliers in numeric data |

## 🔧 Configuration Files

### `Config/config.yml`
Main configuration file for Snowflake connection:
```yaml
snowflake:
  account: "ACCOUNT_ID"
  user: "username"
  password: "password"
  warehouse: "WAREHOUSE_NAME"
  database: "DATABASE_NAME"
  schema: "SCHEMA_NAME"
  role: "ROLE_NAME"
```

### `test_data/data_quality_requirements.xlsx`
Excel file containing quality validation rules with columns:
- `TABLE_NAME` - Target table
- `COLUMN_NAME` - Target column
- `RULE_TYPE` - Type of validation (NULL, DUPLICATE, PATTERN, TYPE, OUTLIER)
- `RULE_VALUE` - Validation parameter/pattern
- `SEVERITY` - Error severity level

### `pytest.ini`
Pytest configuration:
```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_functions = test_*
addopts = -v
```

## 💡 Usage Examples

### Basic Null Check
```python
from Src.Snowflake_Connection import get_connection
from Src.validator import check_null

connection = get_connection()
is_valid, null_count = check_null(connection, "CUSTOMERS", "EMAIL")
print(f"Valid: {is_valid}, Nulls Found: {null_count}")
connection.close()
```

### Pattern Validation
```python
from Src.validator import check_pattern

is_valid, violations = check_pattern(
    connection, 
    "ORDERS", 
    "ORDER_ID", 
    "^ORD-[0-9]{6}$"
)
```

### Reading Quality Rules
```python
from Src.excel_reader import read_rules

rules = read_rules("test_data/data_quality_requirements.xlsx")
for rule in rules:
    print(f"Table: {rule['TABLE_NAME']}, Column: {rule['COLUMN_NAME']}")
```

## 📈 Reports

Generated test reports are saved in the `Report/` directory as HTML files. These reports include:
- Test execution summary
- Pass/fail statistics
- Detailed test results
- Execution timestamps
- Performance metrics

View reports by opening HTML files in a web browser.

## 🔐 Security Notes

⚠️ **Important:** Never commit `Config/config.yml` with real credentials to version control. Use environment variables instead:

```python
import os
user = os.getenv('SNOWFLAKE_USER')
password = os.getenv('SNOWFLAKE_PASSWORD')
```

## 🐛 Troubleshooting

### Import Errors
If you encounter import errors, ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### Connection Issues
- Verify Snowflake credentials in `Config/config.yml`
- Check network connectivity to Snowflake
- Ensure your IP is whitelisted in Snowflake network policies

### Test Failures
- Review generated HTML reports in `Report/` directory
- Check test logs for detailed error messages
- Verify data quality requirements in Excel file

## 📝 Contributing

1. Create a new branch for features
2. Add tests for new validation types
3. Update documentation
4. Submit pull request with detailed description

---


