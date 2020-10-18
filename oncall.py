import boto3
import os


CONNECT = boto3.client('connect')
DYNAMODB = boto3.client('dynamodb')


def get_phone_number(calling_order: str, table_name: str =os.environ['PHONE_BOOK']) -> str:
    # access to dynamodb
    response = DYNAMODB.get_item(
        TableName = table_name,
        Key={
            "calling-order": {
                "S": calling_order
            }
        }
    )
    
    print(calling_order)
    return response['Item']['phone-no']['S']


def get_url_ruby(target_url: str, table_name: str =os.environ['URL_LIST']) -> str:
    # access to dynamodb
    response = DYNAMODB.get_item(
        TableName = table_name,
        Key={
            "url-aliases": {
                "S": target_url
            }
        }
    )
    print(response['Item']['ruby']['S'])
    return response['Item']['ruby']['S']



def call_message(
    destination_phone_number: str,
    alarm_name: str,
    token: str,
    contact_flow_id: str =os.environ['CONTACT_FLOW_ID'], 
    instance_id: str =os.environ['CONNECT_INSTANCE_ID'], 
    source_phone_number: str =os.environ['SOURCE_PHONE_NUMBER']
    ) -> None:
    CONNECT.start_outbound_voice_contact(
        DestinationPhoneNumber = destination_phone_number,
        ContactFlowId = contact_flow_id,
        InstanceId = instance_id,
        SourcePhoneNumber = source_phone_number,
        Attributes={
            'alarmName': alarm_name,
            'Token': token
        }
    )
    
    
def lambda_handler(event: dict, context: dict) -> None:
    alarm_name = event['ExecutionContext']['Execution']['Input']['detail']['alarmName']
    open_bracket_pos=alarm_name.rfind("[") + 1
    close_bracket_pos=alarm_name.rfind("]")
    target_url = alarm_name[open_bracket_pos:close_bracket_pos]
    target_url_jpn = get_url_ruby(target_url=target_url)
    
    token = event['ExecutionContext']['Task']['Token']
    calling_order = event['ExecutionContext']['State']['Name']
    destination_phone_number = get_phone_number(calling_order=calling_order)
    
    call_message(
        destination_phone_number = destination_phone_number,
        alarm_name = target_url_jpn,
        token = token
    )

