import base64
import json
import logging
import os
import time
import uuid

from confluent_kafka import Consumer
from google.cloud import storage
from google.protobuf.message import DecodeError

import batch
import converters
from countdown_timer import CountdownTimer
import sys


def main(servers, topic, bucket_name, converter, max_batch_size, max_batch_time, initial_poll_time, subsequent_poll_time):
    logging.basicConfig(level="INFO")

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    configuration = {
        "bootstrap.servers": servers,
        "group.id": "rc5_consumer",
        "auto.offset.reset": "earliest",
        "enable.auto.commit": "false",
        "error_cb": on_kafka_error,
    }

    consumer = Consumer(configuration)
    try:
        consumer.subscribe([topic])

        # Give the MessagePoller some more time to connect to the cluster.
        poll_timeout = initial_poll_time
        while True:
            succeeded, failed = batch.create(
                consumer,
                converter,
                max_batch_size,
                CountdownTimer(max_batch_time),
                poll_timeout
            )
            if (not succeeded and not failed):
                break
            batch.store(failed, bucket, topic, folder="failed")
            batch.commit(failed, consumer)
            batch.store(succeeded, bucket, topic, folder="succeeded")
            batch.commit(succeeded, consumer)
            
            # Remaining messages will come in faster now that we're connected to the cluster
            poll_timeout = subsequent_poll_time

    finally:
        consumer.close()


def on_kafka_error(error):
    logging.info(error)


if __name__ == "__main__":
    main(
        servers=os.environ.get("SERVERS", "localhost:9092"),
        topic=os.environ.get("TOPIC","accommodation_feature"),
        bucket_name=os.environ.get("BUCKET", "test-rc5-concept-scores"),
        converter=converters.feature_to_json,
        max_batch_size=int(os.environ.get("MAX_BATCH_SIZE", 10)),
        max_batch_time=float(os.environ.get("MAX_BATCH_TIME", 5)),
        initial_poll_time=float(os.environ.get("INITIAL_POLL_TIME", 15)),
        subsequent_poll_time=float(os.environ.get("SUBSEQUENT_POLL_TIME", 1))
    )

