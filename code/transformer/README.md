# Transformer

Transforms the input data from its native data schema to the data schema of the concept score stream.

## Setup

From the folder `transformer`, run:

```
pipenv install --dev
```

In a production environment, you should leave out `--dev`.

## Run

Make sure you're in the folder `transformer`. To run the transformer with default arguments, use:

```
PYTHONPATH=.. pipenv run python src/main.py
```

Note that you need to specify the PYTHONPATH in order for the code in `/common` to be reachable. You can pass arguments to the transformer using environment variables.

```
PYTHONPATH=.. SUBSCRIPTION=projects/test/subscriptions/test pipenv run python src/main.py
```

Parameter | Description
----------|------------
SUBSCRIPTION | The name of the Pub/Sub subscription the transformer reads from to learn about new raw input data.

Note that the transformer gets the name of the input bucket from the messages in Pub/Sub and uses the same bucket for its output.