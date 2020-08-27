import batch
import base64

def test_it_consumes_all_messages():
    consumer = ConsumerStub([
        ( 'key', 'value' ),
        ( 'this', 'that' )
    ])


    succeeded, _ = batch.create(consumer, stub_convert, max_batch_size=2, countdown_timer=CountdownTimerStub(), poll_timeout=4)

    assert len(succeeded) == 2
    assert succeeded[0][0].key() == 'key'
    assert succeeded[0][0].value() == 'value'
    assert succeeded[1][0].key() == 'this'
    assert succeeded[1][0].value() == 'that'


def test_it_does_not_consume_messages_beyond_the_maximum():
    consumer = ConsumerStub([
        ( 'key', 'value' ),
        ( 'this', 'that' ),
        ( 'not', 'relevant' )
    ])

    succeeded, _ = batch.create(consumer, stub_convert, max_batch_size=2, countdown_timer=CountdownTimerStub(), poll_timeout=4)

    assert len(succeeded) == 2
 
def test_it_picks_up_where_it_left_off():
    consumer = ConsumerStub([
        ( 'key', 'value' ),
        ( 'this', 'that' ),
        ( 'not', 'relevant' ),
        ( 'fixed', 'it!'),
        ( 'no', 'more' )
    ])

    batch.create(consumer, stub_convert, max_batch_size=2, countdown_timer=CountdownTimerStub(), poll_timeout=4)
    succeeded, _ = batch.create(consumer, stub_convert, max_batch_size=2, countdown_timer=CountdownTimerStub(), poll_timeout=4)

    assert len(succeeded) == 2
    assert succeeded[0][0].key() == 'not'
    assert succeeded[0][0].value() == 'relevant'
    assert succeeded[1][0].key() == 'fixed'
    assert succeeded[1][0].value() == 'it!'

def test_it_separates_failed_messages():
    consumer = ConsumerStub([
        ( 'key', 'value' ),
        ( 'this', 'that', True ),
        ( 'not', 'relevant' )
    ])

    succeeded, failed = batch.create(consumer, stub_convert, max_batch_size=2, countdown_timer=CountdownTimerStub(), poll_timeout=4)

    assert len(succeeded) == 2
    assert len(failed) == 1
    assert succeeded[0][0].key() == 'key'
    assert succeeded[1][0].key() == 'not'
    assert failed[0][0].key() == 'this'

def test_it_treats_message_that_dont_convert_as_failed():
    consumer = ConsumerStub([
        ( 'fail conversion', 'd'),
        ( 'a', 'b' )
    ])

    succeeded, failed = batch.create(consumer, stub_convert, max_batch_size=1, countdown_timer=CountdownTimerStub(), poll_timeout=4)

    assert len(succeeded) == 1
    assert len(failed) == 1
    assert succeeded[0][0].key() == 'a'
    assert failed[0][0].key() == 'fail conversion'


def test_it_exits_when_there_are_no_messages():
    consumer = ConsumerStub([])

    succeeded, failed = batch.create(consumer, stub_convert, max_batch_size=1, countdown_timer=CountdownTimerStub(), poll_timeout=4)

    assert len(succeeded) == 0
    assert len(failed) == 0

def test_it_stops_consuming_when_time_runs_out():
    consumer = ConsumerStub([
        ( '1', 'one' ),
        ( '2', 'two' ),
        ( '3', 'three' ),
        ( '4', 'four' ),
    ])
    timer = CountdownTimerStub(3)

    succeeded, _ = batch.create(consumer, stub_convert, max_batch_size=999, countdown_timer=timer, poll_timeout=4)

    assert len(succeeded) == 3

def test_it_picks_up_where_it_left_off_after_a_timeout():
    consumer = ConsumerStub([
        ( '1', 'one' ),
        ( '2', 'two' ),
        ( '3', 'three' ),
        ( '4', 'four' ),

    ])
    timer = CountdownTimerStub(2)

    batch.create(consumer, stub_convert, max_batch_size=999, countdown_timer=timer, poll_timeout=4)
    succeeded, _ = batch.create(consumer, stub_convert, max_batch_size=2, countdown_timer=CountdownTimerStub(), poll_timeout=4)

    assert len(succeeded) == 2
    assert succeeded[0][0].key() == '3'
    assert succeeded[1][0].key() == '4'

def test_it_times_out_while_waiting_for_more_messages():
    consumer = ConsumerStub([
        ( '1', 'one' ),
        None,
        ( '2', 'two' )
    ])
    timer = CountdownTimerStub(2)

    succeeded, _ = batch.create(consumer, stub_convert, max_batch_size=2, countdown_timer=timer, poll_timeout=4)

    assert len(succeeded) == 1

def test_it_includes_the_original_kafka_message():
    consumer = ConsumerStub([
        ( '1', 'one' ),
        ( '2', 'two', True ),
        ( '3', 'three' )
    ])
    
    succeeded, failed = batch.create(consumer, stub_convert, max_batch_size=2, countdown_timer=CountdownTimerStub(), poll_timeout=4)

    assert succeeded[0][1] == consumer._messages[0]
    assert succeeded[1][1] == consumer._messages[2]
    assert failed[0][1] == consumer._messages[1]


def stub_convert(message):
    return message, message.key() == 'fail conversion'


class CountdownTimerStub:
    def __init__(self, ticks=9999):
        self._ticks = ticks
    
    def has_elapsed(self):
        self._ticks -= 1
        return self._ticks < 0
    
    def start(self):
        pass
    
    def time_remaining(self):
        return self._ticks

class Message:
    def __init__(self, key, value, is_error):
        self._key = key
        self._value = value
        self._is_error  = is_error == True
    
    def key(self):
        return self._key
    
    def value(self):
        return self._value
    
    def error(self):
        return None if not self._is_error else ()


class ConsumerStub():
    def __init__(self, messages=None):
        messages = messages or []
        self._messages = [
            Message(message[0], message[1], len(message) > 2) if message is not None else None
            for message in messages
        ]
        self._index = -1
    
    def poll(self, timeout):
        self._index += 1
        return self._messages[self._index] if self._index < len(self._messages) else None