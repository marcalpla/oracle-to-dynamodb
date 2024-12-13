# Oracle to DynamoDB

Transfer data from an Oracle database to an AWS DynamoDB table. It also supports a mode for deleting items.

## Installation

Install dependencies using [Poetry](https://python-poetry.org/):

```bash
poetry install
```

## Usage

```bash
poetry run oracle-to-dynamodb \
  --oracle-dsn <ORACLE_DSN> \
  --oracle-user <ORACLE_USER> \
  --oracle-password <ORACLE_PASSWORD> \
  --select-query <SELECT_QUERY> \
  --dynamodb-table-name <DYNAMODB_TABLE_NAME> \
  --dynamodb-attributes '["attr1", "attr2"]' \
  [--delete-mode] \
  [--aws-access-key <AWS_ACCESS_KEY>] \
  [--aws-secret-key <AWS_SECRET_KEY>] \
  [--aws-session-token <AWS_SESSION_TOKEN>] \
  [--aws-region <AWS_REGION>]
```

### Options
- `--oracle-dsn`: Oracle Data Source Name (DSN).
- `--oracle-user`: Oracle username.
- `--oracle-password`: Oracle password.
- `--select-query`: SQL SELECT query to fetch data.
- `--dynamodb-table-name`: Target DynamoDB table name.
- `--dynamodb-attributes`: JSON array of DynamoDB attribute names. The order of attributes should match the order of columns in the SELECT query.
- `--delete-mode`: Deletes items in DynamoDB instead of inserting them.
- `--aws-access-key`: AWS Access Key ID (optional).
- `--aws-secret-key`: AWS Secret Access Key (optional).
- `--aws-session-token`: AWS Session Token (optional).
- `--aws-region`: AWS Region (optional).
