import yaml
import os

# Load configuration from config.yml
config_path = os.path.join(os.path.dirname(__file__), 'config.yml')

with open(config_path, 'r') as file:
    config_data = yaml.safe_load(file)

# Extract snowflake configuration
snowflake_config = config_data.get('snowflake', {})

# Export constants
SNOWFLAKE_USER = snowflake_config.get('user')
SNOWFLAKE_PASSWORD = snowflake_config.get('password')
SNOWFLAKE_ACCOUNT = snowflake_config.get('account')
SNOWFLAKE_WAREHOUSE = snowflake_config.get('warehouse')
SNOWFLAKE_DATABASE = snowflake_config.get('database')
SNOWFLAKE_SCHEMA = snowflake_config.get('schema')
