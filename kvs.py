#!/usr/bin/python

# Copyright 2016 Shakir James. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =============================================================================

"""Key-Value Stores"""

import shelve

from boto3 import resource
from collections import defaultdict
from botocore.exceptions import ClientError


class _KVS(object):
    """KVS interface."""

    def __contains__(self, key):
        raise NotImplementedError

    def get(self, key):
        raise NotImplementedError

    def put(self, key, value):
        raise NotImplementedError

    def delete(self, key):
        raise NotImplementedError

    def close(self):
        pass


class Dict(_KVS):
    """In memory key-value store: dictionary"""
    def __init__(self, table_name=''):
        self._kvs = defaultdict(set)

    def __contains__(self, key):
        return key in self._kvs

    def put(self, key, value):
        self._kvs[key].add(value)

    def get(self, key):
        if key not in self._kvs:
            raise KeyError
        return self._kvs[key]

    def delete(self, key):
        del self._kvs[key]


class Shelf(_KVS):
    """Local key-value store: shelve adapter."""
    # gdbm key must be string, not unicode
    def __init__(self, table_name):
        self.table_name = table_name
        self._kvs = shelve.open(self.table_name, flag='c')

    def __contains__(self, key):
        return str(key) in self._kvs

    def put(self, key, value):
        key = str(key)
        values = self._kvs.get(key, set())
        values.add(value)
        self._kvs[key] = values

    def get(self, key):
        return self._kvs[str(key)]

    def delete(self, key):
        del self._kvs[str(key)]

    def close(self):
        self._kvs.close()


class DynamoDB(_KVS):
    """DynamoDB adapter."""

    def __init__(self, name, **kwargs):
        self.table_name = name
        dynamodb_resource = resource('dynamodb', **kwargs)
        self._kvs = dynamodb_resource.Table(self.table_name)

    def __contains__(self, key):
        try:
            self.get(key)
            return True
        except KeyError:
            return False

    def get(self, key):
        response = self._kvs.get_item(Key={'kvs_key': key})
        return response['Item']['kvs_values']

    def put(self, key, value):
        self._kvs.update_item(
            Key={'kvs_key': key},
            UpdateExpression=(
                "add #attrName :attrValue"),
            ExpressionAttributeNames={'#attrName': 'kvs_values'},
            ExpressionAttributeValues={':attrValue': set([value])},
            ReturnValues='NONE')

    def delete(self, key):
        try:
            self._kvs.delete_item(
                Key={'kvs_key': key},
                ConditionExpression="attribute_exists(kvs_key)",)
        except ClientError as e:
            if e.response['Error']['Code'] == "ConditionalCheckFailedException":
                raise KeyError(e.response['Error']['Message'])
