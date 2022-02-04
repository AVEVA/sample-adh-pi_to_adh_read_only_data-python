"""This sample script demonstrates how to invoke the Sequential Data Store REST API for read only clients"""

import json
import datetime

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

def main(test=False):
    """This function is the main body of the SDS sample script"""
    exception = None
    try:
        print('Step 1. Authenticate against OCS')
        appsettings = get_appsettings()

        # Step 1
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
        endIndex = datetime.datetime.utcnow()
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

        print('Step 3. Show verbosity')
        # Step 3 Show Verbosity with Last Value
        # Create ADH client with verbose
        print('Let\'s first use accept-verbose as True to see the PI point property columns included:')
        print()
        sds_client.acceptverbosity = True

        print('Getting latest event of the stream, note how we can see the properties included:')
        if community_id:
            values = sds_client.SharedStreams.getLastValue(community_tenant_id, community_namespace_id, community_id, stream.Id)
        else:
            values = sds_client.Streams.getLastValue(namespace_id, stream.Id)
        
        print(values)
        print()
        print('Now let\'s use accept-verbosity as False to see the difference:')
        sds_client.acceptverbosity = False

        if community_id:
            values = sds_client.SharedStreams.getLastValue(community_tenant_id, community_namespace_id, community_id, stream.Id)
        else:
            values = sds_client.Streams.getLastValue(namespace_id, stream.Id)
        
        print(values)
        print()

        # Step 4 Get Window Events
        # Get events from the last day using verbose
        sds_client.acceptverbosity = True

        if community_id:
            values = sds_client.SharedStreams.getWindowValues(community_tenant_id, community_namespace_id, community_id, stream.Id, start=startIndex, end=endIndex)        
        else:
            values = sds_client.Streams.getWindowValues(namespace_id, stream.Id, start=startIndex, end=endIndex)
        
        print('Step 4. Retrieve Window events')
        print('Getting window events with verbosity accepted:')
        print(f'Total events found: {str(len(values))}')
        for val in values:
            print(val)
        print()

        # Get events from the last day using non-verbose
        sds_client.acceptverbosity = False

        if community_id:
            values = sds_client.SharedStreams.getWindowValues(community_tenant_id, community_namespace_id, community_id, stream.Id, start=startIndex, end=endIndex)
        else:
            values = sds_client.Streams.getWindowValues(namespace_id, stream.Id, start=startIndex, end=endIndex)
        
        print('Getting window events with verbosity not accepted:')
        print(f'Total events found: {str(len(values))}')
        for val in values:
            print(val)
        print()

        # Get events from the last day including headers
        sds_client.acceptverbosity = True

        if community_id:
            values = sds_client.SharedStreams.getWindowValuesForm(
                community_tenant_id, community_namespace_id, community_id, stream.Id, start=startIndex, end=endIndex, form='tableh')
        else:
            values = sds_client.Streams.getWindowValuesForm(namespace_id, stream.Id, None, start=startIndex, end=endIndex, form='tableh')

        print('Step 5. Retrieve Window events in table form')
        print('Getting window events as a table with headers:')
        for val in values['Rows']:
            print(val)
        print()    

        # Step 5 Get Range Events
        if community_id:
            values = sds_client.SharedStreams.getRangeValues(
                community_tenant_id, community_namespace_id, community_id, stream.Id, start=startIndex, value_class=None, skip=0, count=10, 
                reversed=False, boundary_type=0)
        else:
            values = sds_client.Streams.getRangeValues(
                namespace_id, stream.Id, start=startIndex, value_class=None, skip=0, count=10, 
                reversed=False, boundary_type=0)

        print('Step 6. Retrieve Range events')
        print('Getting range events with verbosity accepted:')
        print(f'Total events found: {str(len(values))}')
        for val in values:
            print(val)
        print()

        # Step 6 Get Interpolated Events
        sds_client.acceptverbosity = False

        if community_id:
            retrieved_interpolated = sds_client.SharedStreams.getRangeValuesInterpolated(
                community_tenant_id, community_namespace_id, community_id, stream.Id, start=startIndex, end=endIndex, count=10)
        else:
            retrieved_interpolated = sds_client.Streams.getRangeValuesInterpolated(
                namespace_id, stream.Id, None, start=startIndex, end=endIndex, count=10)

        print('Step 7. Retrieve Interpolated events')
        print('Sds can interpolate or extrapolate data at an index location '
              'where data does not explicitly exist:')
        print('Getting interpolated events with non-verbose client:')
        for val in retrieved_interpolated:
            print(val)
        print()

        # Step 7 Get Filtered Events
        if values:
            values_only = [value['Value'] for value in retrieved_interpolated]
            average_value = sum(values_only) / len(values_only)
        else:
            average_value = 0

        print('Step 8. Retrieve Filtered events')
        print(f'To show the filter functionality, we will use the less than operator. Based on the data that we have received, {average_value} is the average value, we will use this as a threshold.')
        print(f'Getting filtered events for values less than {average_value}:')
        if community_id:
            filtered_events = sds_client.SharedStreams.getWindowValues(
                community_tenant_id, community_namespace_id, community_id, stream.Id, start=startIndex, end=endIndex, value_class=None, filter=f'Value lt {average_value}')
        else:
            filtered_events = sds_client.Streams.getWindowValues(
                namespace_id, stream.Id, start=startIndex, end=endIndex, value_class=None, filter=f'Value lt {average_value}')

        print(f'Total events found: {str(len(filtered_events))}')
        for val in filtered_events:
            print(val)
        print()
    finally:
        if test and exception is not None:
            raise exception
    print('Complete!')

if __name__ == '__main__':
    main()
