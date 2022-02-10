"""This sample script demonstrates how to invoke the Sequential Data Store REST API for read only clients"""

import json

from datetime import datetime
from ocs_sample_library_preview import (ADHClient)

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

def print_data(data:list):
    """Print values of the data list to the console"""
    print(f'Total events found: {str(len(data))}')
    for val in data:
        print(val)
    print()

def main(test=False):
    """This function is the main body of the SDS sample script"""
    exception = None
    try:
        print('Step 1. Authenticate against OCS')
        appsettings = get_appsettings()

        # Step 1 Try to open the configuration file
        namespace_id = appsettings.get('NamespaceId')
        community_id = appsettings.get('CommunityId')
        stream_id = appsettings.get('StreamId')

        sds_client = ADHClient(
            appsettings.get('ApiVersion'),
            appsettings.get('TenantId'),
            appsettings.get('Resource'),
            appsettings.get('ClientId'),
            appsettings.get('ClientSecret'))
     
        print(r'-------------------------------------------------------')
        print(r' _____ _____ _         ____   _____  _____ _____       ')
        print(r'|  __ \_   _| |       / __ \ / ____|/ ____|  __ \      ')
        print(r'| |__) || | | |_ ___ | |  | | |    | (___ | |__) |   _ ')
        print(r'|  ___/ | | | __/ _ \| |  | | |     \___ \|  ___/ | | |')
        print(r'| |    _| |_| || (_) | |__| | |____ ____) | |   | |_| |')
        print(r'|_|   |_____|\__\___/ \____/ \_____|_____/|_|    \__, |')
        print(r'                                                  __/ |')
        print(r'                                                 |___/ ')
        print(r'-------------------------------------------------------')
        
        print(f'Sds endpoint at {sds_client.uri}')
        print()

        # Create start and end indices for the past day
        currentTime = datetime.utcnow()
        endIndex = currentTime
        startIndex = endIndex - datetime.timedelta(days=1)

        # Get PI to ADH Stream
        print('Step 2. Retrieve stream')
        if community_id:
            stream = next(iter(sds_client.Communities.getCommunityStreams(community_id, f'id:{stream_id}')), None)
            if stream:
                community_tenant_id = stream.TenantId
                community_namespace_id = stream.NamespaceId
            else:
                print(f'Stream with Id {stream_id} not found!')
                raise Exception(f'Stream with Id {stream_id} not found!') 
        else:
            stream = sds_client.Streams.getStream(namespace_id, stream_id)

        print(f'Stream found: {stream.Id}')
        print()

        print('Step 3. Retrieve Window events')
        if community_id:
            values = sds_client.SharedStreams.getWindowValues(community_tenant_id, community_namespace_id, community_id, stream.Id, start=startIndex, end=endIndex)        
        else:
            values = sds_client.Streams.getWindowValues(namespace_id, stream.Id, start=startIndex, end=endIndex)
        
        print_data(values)

        print('Step 4. Retrieve Window events in table form')
        if community_id:
            values = sds_client.SharedStreams.getWindowValuesForm(
                community_tenant_id, community_namespace_id, community_id, stream.Id, start=startIndex, end=endIndex, form='tableh')
        else:
            values = sds_client.Streams.getWindowValuesForm(namespace_id, stream.Id, None, start=startIndex, end=endIndex, form='tableh')

        print_data(values['Rows'])

        print('Step 5. Retrieve Range events')
        if community_id:
            values = sds_client.SharedStreams.getRangeValues(
                community_tenant_id, community_namespace_id, community_id, stream.Id, start=startIndex, value_class=None, skip=0, count=10, 
                reversed=False, boundary_type=0)
        else:
            values = sds_client.Streams.getRangeValues(
                namespace_id, stream.Id, start=startIndex, value_class=None, skip=0, count=10, 
                reversed=False, boundary_type=0)

        print_data(values)

        print('Step 6. Retrieve Interpolated events')
        print('Sds can interpolate or extrapolate data at an index location where data does not explicitly exist:')
        if community_id:
            retrieved_interpolated = sds_client.SharedStreams.getRangeValuesInterpolated(
                community_tenant_id, community_namespace_id, community_id, stream.Id, start=startIndex, end=endIndex, count=10)
        else:
            retrieved_interpolated = sds_client.Streams.getRangeValuesInterpolated(
                namespace_id, stream.Id, None, start=startIndex, end=endIndex, count=10)

        print_data(retrieved_interpolated)

        print('Step 7. Retrieve Filtered events')
        print(f'To show the filter functionality, we will use the less than operator to show values less than 0. (This value can be updated in filter statement below to better fit the data set)')
        if community_id:
            filtered_events = sds_client.SharedStreams.getWindowValues(
                community_tenant_id, community_namespace_id, community_id, stream.Id, start=startIndex, end=endIndex, value_class=None, filter=f'Value lt 0')
        else:
            filtered_events = sds_client.Streams.getWindowValues(
                namespace_id, stream.Id, start=startIndex, end=endIndex, value_class=None, filter=f'Value lt 0')

        print_data(filtered_events)
    finally:
        if test and exception is not None:
            raise exception
    print('Complete!')

if __name__ == '__main__':
    main()