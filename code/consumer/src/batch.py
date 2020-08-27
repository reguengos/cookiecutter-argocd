import uuid
import logging
import time


def create(consumer, convert_message, max_batch_size, countdown_timer, poll_timeout):
    succeeded = []
    failed = []

    poller = MessagePoller(consumer)
    received_message = poller.wait_for_message(timeout=poll_timeout)
    if not received_message:
        return succeeded, failed

    countdown_timer.start()

    while len(succeeded) < max_batch_size and not countdown_timer.has_elapsed():
        message = poller.next_message(timeout=countdown_timer.time_remaining())
        if message is None:
            break

        converted_message, conversion_failed = convert_message(message)
        if message.error() is not None or conversion_failed:
            failed.append((converted_message, message))
        else:
            succeeded.append((converted_message, message))

    return succeeded, failed


def store(batch, bucket, topic, folder):
    if not batch:
        return

    contents = '\n'.join((record[0] for record in batch))
    file_name = f'raw-input/{topic}/{folder}/{now_in_milliseconds()}-{uuid.uuid4()}.json'

    logging.info(f'Writing batch to gs://{bucket.name}/{file_name}.')
    blob = bucket.blob(file_name)
    blob.upload_from_string(contents)
    return file_name


def commit(batch, consumer):
    for message in (record[1] for record in batch):
        consumer.commit(message)


def now_in_milliseconds():
    return int(time.time() * 1000)


class MessagePoller:
    def __init__(self, consumer):
        self._consumer = consumer
        self._message = None

    def wait_for_message(self, timeout):
        """
        Waits for a message to arrive until the timeout is reached.
        Returns whether it received a message.
        """
        self._message = self._consumer.poll(timeout)
        return self._message is not None

    def next_message(self, timeout):
        if self._message is None:
            self._message = self._consumer.poll(timeout)

        message = self._message
        self._message = None
        return message
