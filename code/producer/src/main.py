import json
import os

import concept_score_pb2
from confluent_kafka import Producer
from google.cloud import pubsub_v1, storage, datastore

from common.logging import log
import batch

log.set(component="producer")


def main(project, subscription, servers, kafka_topic):
    configuration = {
        'bootstrap.servers': servers
    }
    producer = Producer(configuration)

    pubsub_client = pubsub_v1.SubscriberClient()
    datastore_client = datastore.Client(project=project)
    storage_client = storage.Client(project=project)

    message_count = 0
    while True:
        response = pubsub_client.pull(subscription, max_messages=10)
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
            concept_scores_batch = batch.read(bucket, object_id)
            try:
                for record in concept_scores_batch:
                    # Check in State Buffer if this is the latest version of the concept score
                    state_buffer_id = f"{record['key']['concept_id']}#{record['key']['concept_ns']}#{record['key']['accommodation_id']}#{record['key']['accommodation_ns']}"
                    state_buffer_key = datastore_client.key(
                        'ConceptScore', state_buffer_id)
                    record_state = datastore_client.get(state_buffer_key)

                    if (record_state is not None) and (record_state['sequence_number'] >= record['metadata']['offset']):
                        log.info(
                            event='dropped_record',
                            key=state_buffer_id,
                            offset=record['metadata']['offset']
                        )
                        continue

                    if record['value'] is None:
                        value = None
                    else:
                        concept_score = concept_score_pb2.concept_score()
                        concept_score.key.concept_id = record['value']['key']['concept_id']
                        concept_score.key.concept_ns = record['value']['key']['concept_ns']
                        concept_score.key.accommodation_id = record['value']['key']['accommodation_id']
                        concept_score.key.accommodation_ns = record['value']['key']['accommodation_ns']
                        concept_score.score = record['value']['score']
                        value = concept_score.SerializeToString()

                    concept_score_key = concept_score_pb2.concept_score.PK()
                    concept_score_key.concept_id = record['key']['concept_id']
                    concept_score_key.concept_ns = record['key']['concept_ns']
                    concept_score_key.accommodation_id = record['key']['accommodation_id']
                    concept_score_key.accommodation_ns = record['key']['accommodation_ns']
                    key = concept_score_key.SerializeToString()

                    # producer.produce(kafka_topic, value, key)
                    log.debug(
                        event="published_concept_score",
                        concept_id=record['key']['concept_id'],
                        concept_ns=record['key']['concept_ns'],
                        accommodation_id=record['key']['accommodation_id'],
                        accommodation_ns=record['key']['accommodation_ns']
                    )

                    # Update the state buffer
                    entity = datastore.Entity(key=state_buffer_key)
                    entity['sequence_number'] = record['metadata']['offset']
                    datastore_client.put(entity)

                # Acknowledge message
                pubsub_client.acknowledge(subscription, [message.ack_id])
                log.info(
                    event="processed_message",
                    bucket=bucket_id,
                    object=object_id,
                    message=message.ack_id
                )

                # producer.poll()

            finally:
                # producer.flush()
                pass


if __name__ == "__main__":
    main(
        project=os.environ.get("PROJECT", "trv-hs-src-conceptstream-stage"),
        subscription=os.environ.get(
            "SUBSCRIPTION", "projects/trv-hs-src-conceptstream-stage/subscriptions/rc5-concept-scores"),
        servers=os.environ.get("SERVERS", "localhost:9092"),
        kafka_topic=os.environ.get("TOPIC", "concept_score")
    )
