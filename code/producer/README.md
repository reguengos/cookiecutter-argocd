# Concept score producer

Reads concept score from a GCS bucket and write them to a Kafka topic.

## Setup

From the folder `concept_score_producer`, run:

```
pipenv install --dev
```

In a production environment, you should leave out `--dev`.

## Run

Make sure you're in the folder `concept_score_producer`. To run the producer with default arguments, use:

```
pipenv run python src/main.py
```

You can pass arguments to the producer using environment variables.

```
TOPIC=test BUCKET=test pipenv run python src/main.py
```

Note that the default arguments were chosen to be convenient during development, so in most cases, you won't have to specify any parameters while developing. In production, you should specify all parameters.

Parameter | Description
----------|-------------
SERVERS   | A comma-separated list of Kafka brokers. Every entry in the list is of the form `host:port`, for example `kafka11.trivago.com:9092`.
TOPIC     | The name of the Kafka topic you want to write to.
BUCKET    | The name of the GCS bucket where the producer will read the concept scores from.