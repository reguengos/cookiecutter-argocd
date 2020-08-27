# Consumer

Reads a Kafka topics and stores the contents in a GCS bucket.

## Setup

From the folder `accommodation-facility-consumer`, run:

```
pipenv install --dev
```

In a production environment, you should leave out `--dev`.

## Run

Make sure you're in the folder `accommodation-facility-consumer`. To run the consumer with default arguments, use:

```
pipenv run python src/main.py
```

You can pass arguments to the consumer using environment variables.

```
TOPIC=test MAX_BATCH_SIZE=100 pipenv run python src/main.py
```

Note that the default arguments were chosen to be convenient during development, so in most cases, you won't have to specify any parameters while developing. In production, you should specify all parameters.

Parameter | Description
----------|-------------
SERVERS   | A comma-separated list of Kafka brokers. Every entry in the list is of the form `host:port`, for example `kafka11.trivago.com:9092`.
TOPIC     | The name of the Kafka topic you want to read.
BUCKET    | The name of the GCS bucket where the consumer will store the data is has read.
MAX_BATCH_SIZE | The maximum number of records an output file may contain.
MAX_BATCH_TIME | The maximum duration in seconds the consumer may take to create a batch, measured from the moment the first message of the batch is consumed (so if it takes a while for the first message to arrive, that initial waiting time is not included in the batch time).
INITIAL_POLL_TIME | The maximum duration in seconds the consumer will wait for the first message to arrive. Only applies to the first batch. If the consumer doesn't receive a message within this time, it will quit.
SUBSEQUENT_POLL_TIME | The maximum duration in seconds the consumer will wait between batches. Applies to all batches except the first. This can usually be much shorter than the initial poll time.