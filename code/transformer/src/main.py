import os
import re
import time

from google.cloud import pubsub_v1, storage

import batch
import transformers
from common.logging import log

batch_id_regex = re.compile(r'/([A-Fa-f0-9\-]+)\.[A-Za-z]+$')
log.set(component="transformer")

def main(subscription_name):
    log.info(event="started")
    
    pubsub_client = pubsub_v1.SubscriberClient()
    storage_client = storage.Client()

    message_count = 0
    while True:
        response = pubsub_client.pull(subscription_name, max_messages=10)
        if (len(response.received_messages) == 0):
            log.info(
                event="finished",
                message_count=message_count
            )
            break

        message_count += len(response.received_messages)

        for message in response.received_messages:
            message_attributes = message.message.attributes
            object_id = message_attributes["objectId"]
            bucket_id = message_attributes["bucketId"]
            log.info(
                event="received_message",
                bucket=bucket_id,
                object=object_id
            )

            # Read batch from GCS
            bucket = storage_client.bucket(bucket_id)
            consumed_batch = batch.read(bucket, object_id)

            # Transform batch
            succeeded, failed = transform(consumed_batch, transformers.feature_to_concept_score)

            if(failed):
                log.warning(
                    event="transformation_failed",
                    bucket=bucket_id,
                    object=object_id,
                    record_count=len(failed)
                )

            # Write succeeded and failed batches to GCS
            batch_id = batch_id_regex.search(object_id).group(1)
            batch.store(failed, bucket, batch_id, 'failed')
            batch.store(succeeded, bucket, batch_id, 'succeeded')

            # Acknowledge message
            pubsub_client.acknowledge(subscription_name, [message.ack_id])
            log.info(
                event="processed_message",
                bucket=bucket_id,
                object=object_id,
                record_count=len(succeeded)
            )


def transform(batch, transform):
    failed = []
    succeeded = []
    for record in batch:
        try:
            concept_score = transform(record)
            concept_score['metadata'] = record['metadata']
            concept_score['metadata']['transformed_at'] = int(time.time()) * 1000
            succeeded.append(concept_score)
        except Exception as err:
            converted_message = {
                'input': record,
                'error': {
                    'exception': repr(err),
                    'transformed_at': int(time.time()) * 1000
                }
            }
            failed.append(converted_message)

    return succeeded, failed


if __name__ == "__main__":
    main(subscription_name=os.environ.get("SUBSCRIPTION", "projects/trv-hs-src-conceptstream-stage/subscriptions/rc5-raw-input"))