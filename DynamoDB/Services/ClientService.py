from boto3.dynamodb.conditions import Key
from datetime import datetime
from config import *
import boto3
import uuid

class ClientService:
    def __init__(self):
        dynamodb = boto3.resource(
            'dynamodb',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name='us-east-1'
        )

        self.table = dynamodb.Table('mecanica_rubio')

    def create_element_with_uuid(self, data: dict) -> str:
        uuid = str(uuid.uuid4())

        self.table.put_item(
            Item={
                'pk': uuid,
                'sk': datetime.now().isoformat(),
                'data': data
            }
        )

        return uuid
    
    def create_row(self, pk: str, entity: str, data: dict) -> dict:
        return self.table.put_item(
            Item={
                'pk': pk,
                'sk': datetime.now().isoformat(),
                'identifier': entity,
                'data': data
            }
        )

    def get_element_by_uuid(self, uuid: str) -> dict:
        response = self.table.query(
            KeyConditionExpression=Key('pk').eq(uuid),
            Limit=1
        )

        items = response.get('Items', [])

        return items[0] if items else None
    
    def get_row(self, pk: str, sk: str) -> dict:
        return self.table.get_item(
            Key={
                'pk': pk,
                'sk': sk
            }
        )

    def query(self, userid: str) -> dict:
        params = {
            'KeyConditionExpression': Key('pk').eq(userid),
            'ScanIndexForward': False,
            'Limit': 20
        }

        response = self.table.query(**params)

        items = response['Items']

        return items