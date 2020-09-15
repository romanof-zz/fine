import json
import boto3
from .models import Bet

class BetDataAccess:
    def __init__(self, logger):
        self.logger = logger

        # db
        self.client = boto3.client('dynamodb', region_name='us-east-2')
        self.table_name = 'bets'

    def put(self, bet):
        res = self.client.put_item(
            TableName = self.table_name,
            Item = {
                'id': {'S': bet.id },
                'data': {'S': json.dumps(bet.__dict__, indent=4, sort_keys=True, default=str)}
            })
        self.logger.info(res)
        return res

    def load_all(self):
        response = self.client.scan(TableName = self.table_name)
        return [json.loads(item['data']['S']) for item in response['Items']]
