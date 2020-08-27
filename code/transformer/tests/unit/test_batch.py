import math

from main import transform

def test_it_returns_an_empty_list_if_the_batch_is_empty():
    batch = []
    succeeded, failed = transform(batch, stub_transformer)

    assert succeeded == []
    assert failed == []

def test_it_transforms_all_records():
    batch = [{
        "key": 1,
        "value": None,
        "metadata": {}
    },{
        "key": 2,
        "value": None,
        "metadata": {}
    }]
    succeeded, _ = transform(batch, stub_transformer)

    assert len(succeeded) == len(batch)
    assert succeeded[0]['value'] == 'Transformed'
    assert succeeded[1]['value'] == 'Transformed'

def test_it_separates_out_records_that_fail_transformation():
    batch = [{
        "value": "I am broken, I have no key",
        "metadata": {}
    },{
        "key": 2,
        "value": None,
        "metadata": {}
    }]
    succeeded, failed = transform(batch, stub_transformer)

    assert len(succeeded) == 1
    assert len(failed) == 1
    assert succeeded[0]['value'] == 'Transformed'
    assert failed[0]['input']['value'] == 'I am broken, I have no key'

def test_it_adds_transformation_time_to_metadata_for_transformed_records():
    batch = [{
        "key": 1, "value": None,
        "metadata": {}
    },{
        "value": None,
        "metadata": {}
    }]

    succeeded, failed = transform(batch, stub_transformer)
    assert math.log10(succeeded[0]['metadata']['transformed_at']) >= 12
    assert math.log10(succeeded[0]['metadata']['transformed_at']) < 13
    assert isinstance(succeeded[0]['metadata']['transformed_at'], int)
    assert math.log10(failed[0]['error']['transformed_at']) >= 12
    assert math.log10(failed[0]['error']['transformed_at']) < 13
    assert isinstance(failed[0]['error']['transformed_at'], int)

def test_it_carries_over_all_metadata_from_the_incoming_record():
    batch = [{
        "key": 1,
        "value": None,
        "metadata": {
            "partition": 0,
            "offset": 15,
            "consumed_at": "consumption_time_in_ms"
        }
    }]

    succeeded, failed = transform(batch, stub_transformer)
    assert succeeded[0]['metadata']['partition'] == 0
    assert succeeded[0]['metadata']['offset'] == 15
    assert succeeded[0]['metadata']['consumed_at'] == 'consumption_time_in_ms'

def test_it_stores_the_input_message_if_transformation_fails():
    batch = [{
        "value": "I am broken, I have no key",
        "metadata": {
            "partition": 0,
            "offset": 16,
            "consumed_at": "consumption_time_in_ms"
        }
    }]

    succeeded, failed = transform(batch, stub_transformer)
    assert failed[0]['input']['value'] == "I am broken, I have no key"
    assert failed[0]['input']['metadata']['partition'] == 0
    assert failed[0]['input']['metadata']['offset'] == 16
    assert failed[0]['input']['metadata']['consumed_at'] == 'consumption_time_in_ms'

def test_if_the_record_has_no_metadata_transformation_is_considered_failed():
    batch = [
        {
            "key": 1,
            "value": "I miss my metadata!"
        }
    ]

    _, failed = transform(batch, stub_transformer)
    assert failed[0]['input']['value'] == "I miss my metadata!"
    assert failed[0]['input']['key'] == 1

def test_it_adds_the_exception_to_failed_records():
    batch = [
        {
            "value": "I'm corrupted, I have no key",
            "metadata": {}
        },
        {
            "key": 1,
            "value": "Please process me",
            "metadata": {}
        }
    ]

    succeeded, failed = transform(batch, stub_transformer)
    assert 'exception' not in succeeded[0]
    assert 'exception' in failed[0]['error']
    assert failed[0]['error']['exception'] == "KeyError('key')"

def stub_transformer(record):
    return {
        'key' : record['key'],
        'value' : 'Transformed'
    }