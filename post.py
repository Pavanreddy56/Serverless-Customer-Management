import json 
import boto3
import os
import uuid
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('DYNAMODB_TABLE', 'CustomerDB')
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    try:
        data = json.loads(event['body'])

        # Validate required fields
        if not all(k in data for k in ('customerName', 'email', 'phone')):
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'Missing required fields'})
            }

        customer_item = {
            'Customerid': str(uuid.uuid4()),  # ✅ Partition key
            'customerName': data['customerName'],
            'email': data['email'],
            'phone': data['phone'],
            'timestamp': datetime.utcnow().isoformat()
        }

        # Save to DynamoDB
        table.put_item(Item=customer_item)

        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'message': 'Customer saved successfully'})
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': str(e)})
        }
