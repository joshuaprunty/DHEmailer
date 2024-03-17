import json
import boto3

def Scrape():

    # JSON Wireframe for output.
    output = {
        'allison': {
            'breakfast': ['tester', 'placeholder'],
            'lunch': [],
            'dinner': []
        },
        'elder': {
            'breakfast': [],
            'lunch': [],
            'dinner': []
        },
        'plexWest': {
            'breakfast': ['tester', 'placeholder'],
            'lunch': [],
            'dinner': ['tester', 'placeholder']
        },
        'plexEast': {
            'breakfast': [],
            'lunch': [],
            'dinner': ['tester', 'placeholder']
        },
        'sargent': {
            'breakfast': [],
            'lunch': ['tester', 'placeholder'],
            'dinner': []
        }
    }

    # Output now holds our full scraped data - write it as-is to meals.json.
    json_data = json.dumps(output)

    s3_client = boto3.client('s3')

    bucket_name = 'diningscraper'
    key = 'usrmeal/meals.json'  

    # Write the JSON data to meals.json in your S3 bucket
    s3_client.put_object(Bucket=bucket_name, Key=key, Body=json_data, ContentType='application/json')

def lambda_handler(event, context):
    Scrape()
    return {
        'statusCode': 200,
        'body': json.dumps('Scrape Successful!')
    }
