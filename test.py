"""This script tests the SDS Python sample script"""

import json
from typing import List
import unittest
import random
from ocs_sample_library_preview import (ADHClient, SdsStream, SdsType, SdsTypeProperty, SdsTypeCode, SdsError)
from PIToOcsEvent import PIToOcsEvent
from program import main
from time import sleep


class SDSPythonSampleTests(unittest.TestCase):
    """Tests for the SDS Python sample"""

    @classmethod
    def test_main(cls):
        """Tests the SDS Python main sample script"""
        main(True)


def get_appsettings():
    """Open and parse the appsettings.json file"""

    # Try to open the configuration file
    try:
        with open(
            'appsettings.json',
            'r',
        ) as f:
            appsettings = json.load(f)
    except Exception as error:
        print(f'Error: {str(error)}')
        print(f'Could not open/read appsettings.json')
        exit()

    return appsettings


def create_type(sds_client: ADHClient, type_id: str) -> SdsType:
    # Create types to be used in type properties
    datetime_type = SdsType('Datetime', SdsTypeCode.DateTime)
    nullable_type = SdsType('NullableSingle', SdsTypeCode.NullableSingle)
    boolean_type = SdsType('Boolean', SdsTypeCode.Boolean)
    string_type = SdsType('String', SdsTypeCode.String)
    nullable_int32_type = SdsType('NullableInt32', SdsTypeCode.NullableInt32)

    # Create type properties
    timestamp = SdsTypeProperty(id='Timestamp', name='Timestamp', is_key=True, sds_type=datetime_type)
    value = SdsTypeProperty(id='Value', name='Value', is_key=False, sds_type= nullable_type)
    is_questionable = SdsTypeProperty(id='IsQuestionable', name='IsQuestionable', is_key=False, sds_type=boolean_type)
    is_substituted = SdsTypeProperty(id='IsSubstituted', name='IsSubstituted', is_key=False, sds_type=boolean_type)
    is_annotated = SdsTypeProperty(id='IsAnnotated', name='IsAnnotated', is_key=False, sds_type=boolean_type)
    systemstate_code = SdsTypeProperty(id='SystemStateCode', name='SystemStateCode', is_key=False, sds_type=nullable_int32_type)
    digitalstate_name = SdsTypeProperty(id='DigitalStateName', name='DigitalStateName', is_key=False, sds_type=string_type)
    typeProperties = [timestamp, value, is_questionable, is_substituted, is_annotated, systemstate_code, digitalstate_name]

    # Create type
    testType = SdsType(id=type_id, name=type_id, sds_type_code=SdsTypeCode.Object, properties=typeProperties)
    return sds_client.Types.getOrCreateType(namespace_id=namespace_id, type=testType)
    

def create_stream(sds_client: ADHClient, stream_id: str, type_id: str) -> SdsStream:
    testStream = SdsStream(id=stream_id, type_id=type_id)
    sds_client.Streams.createOrUpdateStream(namespace_id=namespace_id, stream=testStream)


def create_test_values() -> List[PIToOcsEvent]:
    # Normal event with positive Value
    event_value = PIToOcsEvent()
    event_value.value = random.uniform(0, 100)

    # Normal event with negative Value
    # Sleep to avoid identical timestamps
    sleep(1)
    event_negative_value = PIToOcsEvent()
    event_negative_value.value = random.uniform(0, -100)

    # Event with IsQuestionable as true
    sleep(1)
    event_questionable = PIToOcsEvent()
    event_questionable.IsQuestionable = True
    event_questionable.value = random.uniform(0, 100)

    # Event with SystemStateCode and no Value
    sleep(1)
    eventSystemCode = PIToOcsEvent()
    eventSystemCode.SystemStateCode = '246'
    eventSystemCode.DigitalStateName = 'I/O Timeout'

    return [event_value, event_negative_value, event_questionable, eventSystemCode]

def cleanup(namespace_id: str, type_id: str, stream_id: str):
    try:
        print('Deleting created Type and Stream')
        sds_client.Streams.deleteStream(namespace_id=namespace_id, stream_id=stream_id)
        sds_client.Types.deleteType(namespace_id=namespace_id, type_id=type_id)
    except SdsError as err:
        print('Failed Deletion with message: ' + err.value)

if __name__ == '__main__':
    appsettings = get_appsettings()
    namespace_id = appsettings.get('NamespaceId')
    stream_id = appsettings.get('StreamId')
    type_id = appsettings.get('TypeId')

    sds_client = ADHClient(
        appsettings.get('ApiVersion'),
        appsettings.get('TenantId'),
        appsettings.get('Resource'),
        appsettings.get('ClientId'),
        appsettings.get('ClientSecret'))

    print('Get or create SDS Type and Stream to use') 
    type = create_type(sds_client, type_id=type_id)
    stream = create_stream(sds_client=sds_client, stream_id=stream_id, type_id=type.Id)

    print('Create and upload test values, sleeping 1 second in between creation to avoid identical timestamps')
    values = create_test_values()
    sds_client.Streams.insertValues(namespace_id=namespace_id, stream_id=stream_id, values=values)
    
    try:
        # Run test on seeded data
        unittest.main(exit=False)
    finally:
        # Remove created SDS Stream and Type
        cleanup(namespace_id, type_id, stream_id)


