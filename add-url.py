import boto3
import requests
import json
import os

DYNAMODB = boto3.client('dynamodb')
SUCCESS = "SUCCESS"
FAILED = "FAILED"


def put_target_url(event, table_name: str =os.environ['URL_LIST']) -> None:
    # access to dynamodb
    try:
        response = DYNAMODB.put_item(
            TableName = table_name,
            Item={
                "urls": {
                    "S": event['ResourceProperties']['Item']['urls']
                },
                "url-aliases": {
                    "S": event['ResourceProperties']['Item']['url-aliases']
                },
                "ruby": {
                    "S": event['ResourceProperties']['Item']['ruby']
                },
                "enabled": {
                    "BOOL": bool(int(event['ResourceProperties']['Item']['enabled']))
                }
            }
        )
        print(response)
    except KeyError as e:
        print("ERROR: Not exists " + str(e) + " in key list.")

    except ValueError as e:
        print("ERROR: " + str(e))
    


 
def send(event, context, responseStatus, noEcho=False):
    responseUrl = event['ResponseURL']
 
    print(responseUrl)
 
    responseBody = {}
    responseBody['Status'] = responseStatus
    responseBody['Reason'] = 'See the details in CloudWatch Log Stream: ' + context.log_stream_name
    responseBody['PhysicalResourceId'] = context.log_stream_name
    responseBody['StackId'] = event['StackId']
    responseBody['RequestId'] = event['RequestId']
    responseBody['LogicalResourceId'] = event['LogicalResourceId']
    responseBody['NoEcho'] = noEcho
 
    json_responseBody = json.dumps(responseBody)
 
    print("Response body:\n" + json_responseBody)
 
    headers = {
        'content-type' : '',
        'content-length' : str(len(json_responseBody))
    }
 
    try:
        response = requests.put(responseUrl,
                                data=json_responseBody,
                                headers=headers)
        print("Status code: " + response.reason)
    except Exception as e:
        print("send(..) failed executing requests.put(..): " + str(e))

    
    
def lambda_handler(event: dict, context: dict) -> None:
    put_target_url(event)
    send(event, context, responseStatus=SUCCESS)

