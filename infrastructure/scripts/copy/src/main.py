from sys import argv

from confluent_kafka import Consumer, Producer

default_max_message_count = 10
max_message_count = 10


def main(source_servers, source_topic, destination_servers, destination_topic, max_message_count=default_max_message_count):
	consumer_configuration = {
		'bootstrap.servers': source_servers,
		'group.id': 'kafka-copy',
		'auto.offset.reset': 'earliest',
		'enable.auto.commit': 'false'
	}

	producer_configuration = {
		'bootstrap.servers': destination_servers
	}

	try:
		consumer = Consumer(consumer_configuration)
		consumer.subscribe([source_topic])

		producer = Producer(producer_configuration)

		message_count = 0
		message = consumer.poll(timeout=10)
		while message is not None and message_count < max_message_count:
			if message.error():
				print("error " + message.error())
				continue

			producer.produce(destination_topic, message.value(), message.key())
			message_count += 1

			message = consumer.poll(timeout=0.5)
	finally:
		producer.flush()
		consumer.close()

	print(f'Copied {message_count} messages from {source_topic} to {destination_topic}.')


if __name__ == '__main__':
	if len(argv) < 5:
		print("Missing arguments. Required arguments are: source_servers, source_topic, destination_servers, destination_topic")
		exit()
	
	source_servers = argv[1]
	source_topic = argv[2]
	destination_servers = argv[3]
	destination_topic = argv[4]

	if len(argv) == 6:
		max_message_count = int(argv[5])
	else:
		max_message_count = default_max_message_count

	main(source_servers, source_topic, destination_servers, destination_topic, max_message_count)