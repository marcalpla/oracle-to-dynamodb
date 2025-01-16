import click
import oracledb
import boto3
import json


@click.command()
@click.option(
    '--oracle-dsn', 
    required=True, 
    help='Oracle DSN')
@click.option(
    '--oracle-user', 
    required=True, 
    help='Oracle user')
@click.option(
    '--oracle-password', 
    required=True, 
    help='Oracle password')
@click.option(
    '--select-query', 
    required=True, 
    help='Select query')
@click.option(
    '--dynamodb-table-name',
    required=True, 
    help='DynamoDB table name')
@click.option(
    '--dynamodb-attributes', 
    required=True, 
    help='DynamoDB attributes, e.g. ["id", "name", "age"]')
@click.option(
    '--delete-mode',
    is_flag=True,
    help='Enable delete mode based on keys from the select query')
@click.option(
    '--aws-access-key',
    required=False,
    help='AWS Access Key ID')
@click.option(
    '--aws-secret-key',
    required=False, 
    help='AWS Secret Access Key')
@click.option(
    '--aws-session-token',
    required=False, 
    help='AWS Session Token')
@click.option(
    '--aws-region',
    required=False, 
    help='AWS Region')
def main(
        oracle_dsn, 
        oracle_user, 
        oracle_password, 
        select_query, 
        dynamodb_table_name, 
        dynamodb_attributes,
        delete_mode=False,
        aws_access_key=None,
        aws_secret_key=None,
        aws_session_token=None,
        aws_region=None
    ):
    connection = oracledb.connect(
                    user=oracle_user, 
                    password=oracle_password, 
                    dsn=oracle_dsn)
    cursor = connection.cursor()
    cursor.execute(select_query)

    dynamodb = boto3.resource('dynamodb',
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        aws_session_token=aws_session_token,
        region_name=aws_region)
    table = dynamodb.Table(dynamodb_table_name)

    dynamodb_attributes_list = json.loads(dynamodb_attributes)
    if (not isinstance(dynamodb_attributes_list, list) 
        or len(dynamodb_attributes_list) == 0):
        raise click.BadParameter('dynamodb-attributes must be '
                                 'a non-empty JSON array.')

    rows_processed = 0

    if delete_mode:
        hash_key = dynamodb_attributes_list[0]
        range_key = (dynamodb_attributes_list[1] 
                     if len(dynamodb_attributes_list) > 1 
                     else None)

        with table.batch_writer() as batch:
            for row in cursor:
                key = {hash_key: row[0]}
                if range_key and len(row) > 1:
                    key[range_key] = row[1]
                batch.delete_item(Key=key)
                rows_processed += 1
                if rows_processed % 1000 == 0:
                    print(f'{rows_processed} rows processed and deleted '
                          f'from DynamoDB table {dynamodb_table_name}')
    else:
        with table.batch_writer() as batch:
            for row in cursor:
                item = {dynamodb_attributes_list[i]: (
                            True if str(value).lower() == 'true' else 
                            False if str(value).lower() == 'false' else
                            value)
                        for i, value in enumerate(row)}
                batch.put_item(Item=item)
                rows_processed += 1
                if rows_processed % 1000 == 0:
                    print(f'{rows_processed} rows processed and inserted '
                        f'into DynamoDB table {dynamodb_table_name}')

    cursor.close()
    connection.close()

    print(f'Finished: {rows_processed} rows processed and '
          f'{'deleted' if delete_mode else 'inserted'} '
          f'into DynamoDB table {dynamodb_table_name}')


if __name__ == '__main__':
    main()