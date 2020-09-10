import yaml
import boto3

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
                'data': {'S': yaml.dump(bet)}
            })
        self.logger.info(res)
        return result
