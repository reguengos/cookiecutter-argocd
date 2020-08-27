import json
import base64

import pytest
from confluent_kafka import Producer
from google.cloud import storage

import accommodation_feature_pb2
import converters
from main import main

storage_client = storage.Client()

@pytest.fixture
def topic_name():
    return "test-topic"

@pytest.fixture
def prefix(topic_name):
    return f"raw-input/{topic_name}"

@pytest.fixture
def bucket(prefix):
    bucket = storage_client.bucket("sstolk-test-rc5-concept-scores")
    clean_bucket(bucket, prefix=prefix)
    yield bucket
    clean_bucket(bucket, prefix=prefix)


def test_when_message_succeed(kafka_service, topic_name, prefix, bucket):
    key = {
        "accommodation_feature_id": 200,
        "accommodation_feature_ns": 300,
        "accommodation_id": 400,
        "accommodation_ns": 500 
        }
    value = {
        "key": key,
        "score": 10000
        }

    accommodation_feature = accommodation_feature_pb2.accommodation_feature()
    accommodation_feature.key.accommodation_feature_id = value['key']['accommodation_feature_id']
    accommodation_feature.key.accommodation_feature_ns = value['key']['accommodation_feature_ns']
    accommodation_feature.key.accommodation_id = value['key']['accommodation_id']
    accommodation_feature.key.accommodation_ns = value['key']['accommodation_ns']
    accommodation_feature.score = value['score']
    value_pb = accommodation_feature.SerializeToString()

    accommodation_feature_key = accommodation_feature_pb2.accommodation_feature.PK()
    accommodation_feature_key.accommodation_feature_id = key['accommodation_feature_id']
    accommodation_feature_key.accommodation_feature_ns = key['accommodation_feature_ns']
    accommodation_feature_key.accommodation_id = key['accommodation_id']
    accommodation_feature_key.accommodation_ns = key['accommodation_ns']
    key_pb = accommodation_feature_key.SerializeToString()

    produce_message(kafka_service, topic_name, key_pb, value_pb)
    main(
        servers=kafka_service,
        bucket_name=bucket.name,
        converter=converters.feature_to_json,
        topic=topic_name,
        max_batch_size = 10,
        max_batch_time = 5,
        initial_poll_time = 15,
        subsequent_poll_time = 0.5
    )

    # Read from GCS. Check only one file got saved
    blobs = storage_client.list_blobs(bucket, prefix=prefix)
    blobs = list(blobs)

    assert len(blobs) == 1
    blob = blobs[0]
    assert "succeeded" in blob.name

    # Compare input with output file.
    saved_message = json.loads(blob.download_as_string())
    assert saved_message["key"] == key
    assert saved_message["value"] == value


def test_when_message_failed(kafka_service, topic_name, prefix, bucket):
    key = b'{"key": 42}'
    value = b'{"accommodation_feature_id": "error"}'

    produce_message(kafka_service, topic_name, key, value)

    main(
        servers=kafka_service,
        bucket_name=bucket.name,
        converter=converters.feature_to_json,
        topic=topic_name,
        max_batch_size = 10,
        max_batch_time = 5,
        initial_poll_time = 15,
        subsequent_poll_time = 0.5
    )

    # Read from GCS. Check only one file got saved
    blobs = storage_client.list_blobs(bucket, prefix=prefix)
    blobs = list(blobs)
    assert len(blobs) == 1
    blob = blobs[0]
    assert "failed" in blob.name

    # Compare input with output file.
    saved_message = json.loads(blob.download_as_string())
    assert base64.decodebytes(saved_message["key"].encode('utf-8')) == key
    assert base64.decodebytes(saved_message["value"].encode('utf-8')) == value


def test_when_no_message(kafka_service, topic_name, prefix, bucket):
    main(
        servers=kafka_service,
        bucket_name=bucket.name,
        converter=converters.feature_to_json,
        topic=topic_name,
        max_batch_size = 10,
        max_batch_time = 5,
        initial_poll_time = 15,
        subsequent_poll_time = 0.5
    )

    # Read from GCS. Check only one file got saved
    blobs = storage_client.list_blobs(bucket, prefix=prefix)
    blobs = list(blobs)
    assert len(blobs) == 0


def clean_bucket(bucket, prefix):
    blobs = storage_client.list_blobs(bucket, prefix=prefix)
    bucket.delete_blobs(blobs)


def produce_message(kafka_service, topic, key, value):
    configuration = {"bootstrap.servers": kafka_service}
    producer = Producer(configuration)

    producer.produce(topic, value, key)
    producer.flush()