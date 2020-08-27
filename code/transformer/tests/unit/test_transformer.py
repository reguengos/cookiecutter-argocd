import math
import transformers

def test_it_converts_a_valid_value():
    feature = {
        'metadata': dummy_metadata,
        'key': dummy_key,
        'value': {
            'key': {
                'accommodation_id': 1029,
                'accommodation_ns': 100,
                'accommodation_feature_id': 3847,
                'accommodation_feature_ns': 300,
            },
            'score': 3333
        }
    }

    concept_score = transformers.feature_to_concept_score(feature)

    assert concept_score['value']['key']['concept_id'] == 3847
    assert concept_score['value']['key']['concept_ns'] == 300
    assert concept_score['value']['key']['accommodation_id'] == 1029
    assert concept_score['value']['key']['accommodation_ns'] == 100
    assert concept_score['value']['score'] == 3333

def test_it_converts_a_valid_key():
    feature = {
        'metadata': dummy_metadata,
        'key': {
            'accommodation_id': 5678,
            'accommodation_ns': 100,
            'accommodation_feature_id': 4321,
            'accommodation_feature_ns': 300,
        },
        'value': None
    }

    concept_score = transformers.feature_to_concept_score(feature)

    assert concept_score['key']['concept_id'] == 4321
    assert concept_score['key']['concept_ns'] == 300
    assert concept_score['key']['accommodation_id'] == 5678
    assert concept_score['key']['accommodation_ns'] == 100

def test_it_converts_a_none_value():
    feature = {
        'metadata': dummy_metadata,
        'key': dummy_key,
        'value': None
    }

    concept_score = transformers.feature_to_concept_score(feature)

    assert concept_score['value'] == None

def test_it_adds_a_timestamp_in_milliseconds_to_metadata():
    feature = {
        'metadata': {
            'consumed_at': 1593388800021,
            'partition': 0,
            'offset': 0
        },
        'key': dummy_key,
        'value': None
    }

    concept_score = transformers.feature_to_concept_score(feature)

    assert concept_score['metadata']['consumed_at'] == 1593388800021
    assert concept_score['metadata']['transformed_at'] > concept_score['metadata']['consumed_at']
    assert math.log10(concept_score['metadata']['transformed_at']) > 12
    assert math.log10(concept_score['metadata']['transformed_at']) < 13
    assert isinstance(concept_score['metadata']['transformed_at'], int)


dummy_key = {
    'accommodation_id': 0,
    'accommodation_ns': 0,
    'accommodation_feature_id': 0,
    'accommodation_feature_ns': 0,
}

dummy_metadata = {
    'consumed_at': 0,
    'partition': 0,
    'offset': 0
}
