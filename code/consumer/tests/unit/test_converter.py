import converters
from accommodation_feature_pb2 import accommodation_feature
import json
import math
import pytest
import base64


def test_it_adds_a_timestamp_in_milliseconds():
    message = Message(None, None)

    result, _ = converters.feature_to_json(message)
    result = json.loads(result)

    assert math.log10(result['metadata']['consumed_at']) >= 12
    assert math.log10(result['metadata']['consumed_at']) < 13
    assert isinstance(result['metadata']['consumed_at'], int)

def test_it_converts_an_empty_key_and_an_empty_value_to_null():
    message = Message(None, None)
    
    result, _ = converters.feature_to_json(message)
    result = json.loads(result)

    assert result['key'] is None
    assert result['value'] is None

def test_it_reports_an_error_if_the_key_is_empty():
    message = Message(None, None)

    _, error = converters.feature_to_json(message)

    assert error

def test_it_parses_a_feature_key(key):
    message = Message(key, None)

    result, error = converters.feature_to_json(message)
    result = json.loads(result)

    assert not error
    assert result['key']['accommodation_id'] == 1234
    assert result['key']['accommodation_ns'] == 100
    assert result['key']['accommodation_feature_id'] == 9876
    assert result['key']['accommodation_feature_ns'] == 300

def test_it_parses_a_feature(key, feature):
    message = Message(key, feature)

    result, error = converters.feature_to_json(message)
    result = json.loads(result)

    assert not error
    assert result['value']['key']['accommodation_id'] == 1234
    assert result['value']['key']['accommodation_ns'] == 100
    assert result['value']['key']['accommodation_feature_id'] == 9876
    assert result['value']['key']['accommodation_feature_ns'] == 300
    assert result['value']['score'] == 5000

def test_it_reports_an_error_when_parsing_a_key_fails():
    message = Message(b'invalid', None)

    result, error = converters.feature_to_json(message)
    result = json.loads(result)

    assert error

def test_it_stores_a_faulty_key_in_base64():
    message = Message(b'invalid', None)

    result, error = converters.feature_to_json(message)
    result = json.loads(result)
    
    assert error
    assert result['key'] == 'aW52YWxpZA=='

def test_it_reports_an_error_when_parsing_a_feature_fails(key):
    message = Message(key, b'invalid')

    result, error = converters.feature_to_json(message)
    result = json.loads(result)

    assert error
 
def test_it_stores_a_faulty_feature_in_base64():
    message = Message(None, b'invalid')

    result, error = converters.feature_to_json(message)
    result = json.loads(result)
    
    assert error
    assert result['value'] == 'aW52YWxpZA=='

def test_it_stores_the_partition_and_offset():
    message = Message(None, None, partition=18, offset=92)

    result, _ = converters.feature_to_json(message)
    result = json.loads(result)

    assert result['metadata']['partition'] == 18
    assert result['metadata']['offset'] == 92


@pytest.fixture
def feature():
    feature = accommodation_feature()
    feature.key.accommodation_id = 1234
    feature.key.accommodation_ns = 100
    feature.key.accommodation_feature_id = 9876
    feature.key.accommodation_feature_ns = 300
    feature.score = 5000

    return feature.SerializeToString()

@pytest.fixture
def key():
    key = accommodation_feature.PK()
    key.accommodation_id = 1234
    key.accommodation_ns = 100
    key.accommodation_feature_id = 9876
    key.accommodation_feature_ns = 300
    
    return key.SerializeToString()


class Message:
    def __init__(self, key, value, partition=0, offset=0):
        self._key = key
        self._value = value
        self._partition = partition
        self._offset = offset
    
    def key(self):
        return self._key
    
    def value(self):
        return self._value
    
    def partition(self):
        return self._partition
    
    def offset(self):
        return self._offset