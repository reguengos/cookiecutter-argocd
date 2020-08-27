import json
import time
from accommodation_feature_pb2 import accommodation_feature
from google.protobuf.message import DecodeError
import base64

def feature_to_json(message):
    error = message.key() is None
    key = None
    value = None

    try:
        key = feature_key_to_dict(message.key()) if message.key() else None
    except DecodeError:
        error = True
        key = base64.b64encode(message.key()).decode('ascii')

    try:
        value = feature_to_dict(message.value()) if message.value() else None
    except DecodeError:
        error = True
        value = base64.b64encode(message.value()).decode('ascii')

    converted_message = {
        'metadata': {
            'consumed_at': now_in_milliseconds(),
            'partition': message.partition(),
            'offset': message.offset()
        },
        'key': key,
        'value': value
    }

    return json.dumps(converted_message), error
 

def feature_to_dict(feature):
    feature = accommodation_feature.FromString(feature)
    return {
        'key': {
            'accommodation_id': feature.key.accommodation_id,
            'accommodation_ns': feature.key.accommodation_ns,
            'accommodation_feature_id': feature.key.accommodation_feature_id,
            'accommodation_feature_ns': feature.key.accommodation_feature_ns
        },
        'score': feature.score
    }


def feature_key_to_dict(key):
    key = accommodation_feature.PK.FromString(key)
    return {
        'accommodation_id': key.accommodation_id,
        'accommodation_ns': key.accommodation_ns,
        'accommodation_feature_id': key.accommodation_feature_id,
        'accommodation_feature_ns': key.accommodation_feature_ns
    }


def now_in_milliseconds():
    return int(time.time() * 1000)