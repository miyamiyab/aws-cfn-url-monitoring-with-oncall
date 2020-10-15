import requests
import boto3
import os

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
HEADERS = {'User-Agent': USER_AGENT}

DYNAMODB = boto3.client('dynamodb')

def scan_assign_target(table_name: str =os.environ['URL_LIST']):
    response = DYNAMODB.scan(
        TableName=table_name,
        AttributesToGet=[
            'urls'
            ],
        ScanFilter={
            'enabled': {
                'AttributeValueList': [
                    {
                        'BOOL': True
                    }
                ],
                'ComparisonOperator': 'EQ'
            }
        }
    )
    
    return response


def lambda_handler(event, context):

    try:
        scan_result = scan_assign_target()
        for urls in scan_result['Items']:
            url = urls['urls']['S']
            response = requests.get(url, headers=HEADERS)
            code = response.status_code
            exec_time = response.elapsed.total_seconds()
            
            if os.environ['TEST_URL'] != "None":
                if os.environ['TEST_URL'] == url:
                    print(url + " " + str(444) + " " + str(exec_time))
                else:
                    print(url + " " + str(code) + " " + str(exec_time))
            else:
                print(url + " " + str(code) + " " + str(exec_time))
            
    except Exception as e:
        print(e)
