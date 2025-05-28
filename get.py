import json
import boto3
import os

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('DYNAMODB_TABLE', 'CustomerDB')
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    try:
        # Fetch all customer records
        response = table.scan()
        items = response.get('Items', [])

        # Optional: sort by customerName or timestamp if desired
        # items.sort(key=lambda x: x.get('customerName', ''))

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET,OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({'customers': items})
        }

    except Exception as e:
        print(f"Error scanning DynamoDB table: {str(e)}")  # Server-side logs

        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET,OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({'error': 'Internal server error'})
        }

