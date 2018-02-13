from mongoengine import connect
from realtimeapp.models import SensorReading, return_all, return_all_by_date
from nose.tools import assert_equal, assert_raises
import datetime

connect(is_mock=True)
readings_sample = {
    'bedroom20181815170112298831': 
    {'date': '2018-01-15 17:18:12.298831', 'room': 'bedroom', 'temperature': 20, 'humidity': 60},
    'bedroom20181815170113326091': 
    {'date': '2018-01-15 17:18:13.326091', 'room': 'bedroom', 'temperature': 11, 'humidity': 61}, 
    'bedroom20181815170114343102':
    {'date': '2018-01-15 17:18:14.343102', 'room': 'bedroom', 'temperature': 17, 'humidity': 57}
}


def test_sensor_reading_save():
    '''
    Test models using MongoDB
    Create and Read data
    '''

    # Saving Documents
    reading_1 = SensorReading(
        room='backyard_test',
        temperature=15,
        humidity=99,
        date=datetime.datetime.now().isoformat(),
        readingid = 'backyard_test_1201801051548'
    )
    reading_1_doc = reading_1.save()       # This will perform an insert

    reading_2 = SensorReading(
        room='backyard_test_2',
        temperature=11.1,
        humidity=51.5,
        date=datetime.datetime.now().isoformat(),
        readingid = 'backyard_test_220180105165021'
    )
    reading_2_doc = reading_2.save()


    assert_equal(reading_1_doc.room, 'backyard_test')
    assert_equal(reading_1_doc.temperature, 15)
    assert_equal(reading_1_doc.humidity, 99)
    assert_equal(reading_1_doc.date, reading_1.date)

    assert_equal(reading_2_doc.room, 'backyard_test_2')
    assert_equal(reading_2_doc.temperature, 11.1)
    assert_equal(reading_2_doc.humidity, 51.5)
    assert_equal(reading_2_doc.date, reading_2.date)

def test_sensor_reading_validation_error():
    '''
    Test validation, validation should be triggered and save command fail
    '''
    reading_3 = SensorReading(
        room='backyard_test_3',
        temperature='string',
        humidity=51.5,
        date='2018-01-05T16:50:21.114721',
        readingid = 'backyard_test_3201801051650'
    )
    
    with assert_raises(Exception) as e:
        reading_3.save()

    assert_equal(e.exception._message,'ValidationError (SensorReading:backyard_test_3201801051650) ') 


def test_return_all():
    '''
    Creates a database dump, used for numpy
    Check that the structure returned by this method is equal to:
    readings = {
        'bedroom20181815170112298831': 
        {'date': '2018-01-15 17:18:12.298831', 'room': 'bedroom', 'temperature': 20, 'humidity': 60},
        'bedroom20181815170113326091': 
        {'date': '2018-01-15 17:18:13.326091', 'room': 'bedroom', 'temperature': 11, 'humidity': 61}, 
        'bedroom20181815170114343102':
        {'date': '2018-01-15 17:18:14.343102', 'room': 'bedroom', 'temperature': 17, 'humidity': 57},
        readingid : {reading._data}
    }
    '''

    reading_4 = SensorReading(
        room='backyard_test_2',
        temperature=11.1,
        humidity=51.5,
        date='2018-01-05T16:50:21.114721',
        readingid = 'backyard_test_220180105165023'
    )
    reading_4.save()

    readings = return_all()
    
    assert_equal(type(readings), type(readings_sample))
    assert_equal(readings.get('backyard_test_220180105165021')['humidity'],51.5) 


def test_return_all_by_date():
    test_sensor_reading_save()
    readings = return_all_by_date(days=1)
    
    # Make sure we get the readings are already serialized as a dictionary
    assert_equal(type(readings), type(readings_sample))
    # Verify that the data is in the results set
    assert_equal(readings.get('backyard_test_220180105165021')['humidity'],51.5) 
