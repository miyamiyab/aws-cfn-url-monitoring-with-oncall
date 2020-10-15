import boto3
import json

STF = boto3.client('stepfunctions')

def lambda_handler(event: dict, context: dict) -> dict:
    output_dict ={
        "status": 200
    }
    output = json.dumps(output_dict)
    
    response = STF.send_task_success(
        taskToken = event['Details']['ContactData']['Attributes']['Token'],
        output = output
    )
    
    return output_dict
