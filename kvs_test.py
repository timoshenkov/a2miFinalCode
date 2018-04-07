import os
import tempfile
import test

from boto3 import resource
from kvs import Shelf, Dict, DynamoDB
from unittest import skipUnless


class CommonTestCase(object):
    def test_put_get(self):
        self.kvs.put('key', 'value')
        self.assertItemsEqual(self.kvs.get('key'), ['value'])

    def test_put_same_key(self):
        self.kvs.put('key', 'value1')
        self.kvs.put('key', 'value2')
        self.kvs.put('key', 'value2')
        self.assertItemsEqual(self.kvs.get('key'), ['value1', 'value2'])

    def test_contains(self):
        self.kvs.put('key', 'value')
        self.assertTrue('key' in self.kvs)
        self.assertFalse('ke' in self.kvs)

    def test_get_nokey(self):
        with self.assertRaises(KeyError):
            print(self.kvs.get('key'))
            self.kvs.get('key')

    def test_delete(self):
        self.kvs.put('key', 'value')
        self.kvs.delete('key')
        with self.assertRaises(KeyError):
            self.kvs.delete('key')

    def test_delete_nokey(self):
        with self.assertRaises(KeyError):
            self.kvs.delete('key')


class ShelfTestCase(test.TestCase, CommonTestCase):
    def setUp(self):
        self.table_name = next(tempfile._get_candidate_names())
        self.kvs = Shelf(self.table_name)

    def tearDown(self):
        os.unlink(self.table_name)


class DictTestCase(test.TestCase, CommonTestCase):
    def setUp(self):
        self.kvs = Dict()


@skipUnless(test.TEST_DYNAMODB_LOCAL, 'requires dynamodb local')
# Running DynamoDB on Your Computer:
# docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.html
class DynamoDBTestCase(test.TestCase, CommonTestCase):
    def setUp(self):
        self.table_name = 'test'
        self.endpoint_url = 'http://localhost:8000'
        self.region_name = 'us-east-1'
        self.dynamodb = resource(
            'dynamodb', region_name=self.region_name,
            endpoint_url=self.endpoint_url)
        self.table = self.dynamodb.create_table(
            TableName=self.table_name,
            KeySchema=[
                {
                    'AttributeName': 'kvs_key',
                    'KeyType': 'HASH'  # Partition key
                },
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'kvs_key',
                    'AttributeType': 'S'
                },
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        self.kvs = DynamoDB(
            self.table_name, region_name=self.region_name,
            endpoint_url=self.endpoint_url)

    def tearDown(self):
        self.table.delete()


if __name__ == '__main__':
    test.main()
