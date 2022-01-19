# Reading PI to OCS Values from Sequential Data Store Python Sample

**Version:** 1.0

[![Build Status](https://dev.azure.com/osieng/engineering/_apis/build/status/product-readiness/OCS/osisoft.sample-pi-to-ocs-read-only-data-python?repoName=osisoft%2Fsample-pi-to-ocs-read-only-data-python&branchName=main)](https://dev.azure.com/osieng/engineering/_build/latest?definitionId=4498&repoName=osisoft%2Fsample-pi-to-ocs-read-only-data-python&branchName=main)

## Building a Python client to make REST API calls to the SDS Service

The sample code in this topic demonstrates how to invoke SDS REST APIs using Python to read values from a stream in SDS created from a PI to OCS transfer. By examining the code, you will see how to establish a connection to SDS, obtain an authorization token, and query SDS for values.

The sections that follow provide a brief description of the process from beginning to end.

`Note: This sample requires an Id of a PI to OCS stream already created in SDS.`

Developed against Python 3.10.1

## To Run this Sample

1. Clone the GitHub repository
1. Install required modules: `pip install -r requirements.txt`
1. Open the folder with your favorite IDE
1. Configure the sample using the file [appsettings.placeholder.json](appsettings.placeholder.json). Before editing, rename this file to `appsettings.json`. This repository's `.gitignore` rules should prevent the file from ever being checked in to any fork or branch, to ensure credentials are not compromised.
1. Update `appsettings.json` with the credentials provided by OSIsoft
1. Run `program.py`

To Test the sample:

1. Run `python test.py`

or

1. Install pytest `pip install pytest`
1. Run `pytest program.py`

## PI Tag Name to OCS Stream Id

Streams in SDS are referred to by their Id rather than by their name as is common with PI tags. To find the PI to OCS stream corresponding to your PI tag name in SDS, you can search in the portal using the following format:

ID:PI_<YOUR_SERVER_NAME>_* AND Name:<PI_TAG_NAME>

The SDS portal can found by navigating to the [Cloud Portal](http://cloud.osisoft.com) and visiting the *Sequential Data Store* option under the *Data Management* tab on the left hand menu, where you can find the search bar in the top center.

To do this programatically you can use the `getStreams` method, for more information see the [Retrieve Streams by Query](#retreive-streams-by-query) section below.
## Establish a Connection

The sample code uses the samples library which uses the `requests` module, which exposes simple methods for specifying request types to a given destination address. This library automatically adds the `Accept-Encoding` header to requests and decompresses encoded responses before returning them to the user, so no special handling is required to support compression. The client calls the requests method by passing a destination URL, payload, and headers. The server's response is stored.

```python
response = requests.post(url, data=payload, headers=client_headers)
```

- _url_ is the service endpoint (for example:
  `https://dat-a.osisoft.com`). The connection is used by the `SdsClient` class.

Each call to the SDS REST API consists of an HTTP request along with a specific URL and HTTP method. The URL consists of the server name plus the extension that is specific to the call. Like all REST APIs, the SDS REST API maps HTTP methods to CRUD operations as shown in the following table:

| HTTP Method | CRUD Operation | Content Found In |
| ----------- | -------------- | ---------------- |
| POST        | Create         | message body     |
| GET         | Retrieve       | URL parameters   |
| PUT         | Update         | message body     |
| DELETE      | Delete         | URL parameters   |

Note: Only the GET method will be used in this sample as it targets clients limited to read permissions, the [OCS waveform sample](https://github.com/osisoft/OSI-Samples-OCS/blob/main/docs/SDS_WAVEFORM.md) is available and more in depth to cover every HTTP method.

## Configure the Sample

Included in the sample there is a configuration file with placeholders that need to be replaced with the proper values. They include information for authentication, connecting to the SDS Service, pointing to a namespace, and retrieving stream data.

### OSIsoft Cloud Services

First, a valid namespace Id for the tenant must be given. In SDS, a namespace provides isolation within a Tenant. Each namespace has its own collection of Streams, Types, and Stream Views. It is not possible to programmatically create or delete a namespace. If you are a new user, be sure to go to the [Cloud Portal](http://cloud.osisoft.com) and create a namespace using your tenant login credentials provided by OSIsoft. You must provide the namespace Id of a valid namespace in `appsettings.json` for the sample to function properly.

The SDS Service is secured using Azure Active Directory. The sample application is an example of a _credential client_. Credential clients provide a client Id and secret that are authenticated against the directory and are associated with a given tenant. They are created through the tenant's Security portal. The steps necessary to create a new client Id and secret are described below.

Log on to the [Cloud Portal](https://cloud.osisoft.com) and navigate to the `Clients` page under the `Security` tab, which is situated along left of the webpage. This sample program covers data retrieval, so the client provided needs to have access to said data. 

To create a new client, click `Add Client` in the top pane of the page and follow the prompts, ensuring that the appropriate roles are assigned to allow the client to read values from PI to OCS stream to be used. 

To create a new secret for a client, select the client and click the `Add Secret` button under the client details pane then follow the prompts. Note that the secret is only displayed at the time of creation and cannot be retrieved at a later time.

Finally, a query string to retrieve the stream to read from must be given. For more information on how to define this see [Search in SDS](https://docs.osisoft.com/bundle/ocs/page/developer-guide/sequential-data-store-dev/sds-search.html)

### Config Schema

The values to be replaced are in `appsettings.json`:

```json
{
  "Resource": "https://dat-b.osisoft.com",
  "ApiVersion": "v1",
  "TenantId": "PLACEHOLDER_REPLACE_WITH_TENANT_ID",
  "NamespaceId": "PLACEHOLDER_REPLACE_WITH_NAMESPACE_ID",
  "CommunityId": null,
  "ClientId": "PLACEHOLDER_REPLACE_WITH_APPLICATION_IDENTIFIER",
  "ClientSecret": "PLACEHOLDER_REPLACE_WITH_APPLICATION_SECRET",
  "StreamId": "PLACEHOLDER_REPLACE_WITH_STREAM_ID"
}
```

### Community

If you are accessing a stream shared in an OCS community, enter the community Id in the `CommunityId` and owning field of the configuration. Make sure to also grant the appropriate "Community Member" role to the Client-Credentials Client used by the sample. 

If you are not using OCS communities, leave the `CommunityId` field blank.

## Obtain an Authentication Token

Within each request to SDS, the headers are provided by a function that is also responsible for refreshing the token. An authentication context is created and a token is acquired from that context.

```python
tokenInformation = requests.post(
tokenEndpoint,
data = {"client_id" : self.clientId,
        "client_secret" : self.clientSecret,
        "grant_type" : "client_credentials"})

token = json.loads(tokenInformation.content)
```

This is handled by the python library.

## Retrieve Stream

To run this sample we will need to first retrieve the PI to OCS stream to read values from. This is done by calling the `getStream` method providing the Id of the stream to retrieve. The stream Id is configured in the `appsettings.json` file as `StreamId`.

`getStream` is used for retrieving a stream and its information. This is the function definition:

```python
getStream(self, namespace_id, stream_id):
```

- **namespace_id** is the Id of the namespace to query against.
- **stream_id** is the Id of the stream to retrieve.

- A JSON object containing the stream is returned.

The method is called as shown:

```python
stream = client.Streams.getStream(self, namespace_id, stream_id)
```

## Retreive Streams by Query

If you would like to query SDS for multiple streams we can use the `getStreams` method providing a query parameter. This could be used to find PI to OCS streams given your PI tag and PI Server names as shown earlier by providing the same query format, ID:PI_<YOUR_SERVER_NAME>_* AND Name:<PI_TAG_NAME>. Following is the function definition:

```python
streams = getStreams(self, namespace_id, query, skip, count):
```

**namespace_id**: is the Id of the namespace to query against.
**query**: is the query to use.
**skip**: is the number of streams to skip for paging
**count**: is the number of streams to limit to

- A JSON object containing an array of streams is returned.

## Retrieve Values from a Stream

The SDS read API features different methods of reading values, in this sample we will demonstrate reading Window, Range, and Filtered values, as well as using Interpolation.

When ingressing data using PI to OCS, the resulting stream types contain a certain set of PI point attributes as stream type properties to give more information about the data:

| Column         | Description     | 
|--------------|-----------|
| IsQuestionable | The event value is unreliable or the circumstances under which it was recorded are suspect |
| IsSubstituted | The event value has been changed from the original archived value |
| IsAnnotated | An annotation has been made to the event to include further information or commentary |
| SystemStateCode | The system digital state code |
| DigitalStateName | The digital state name |

The amount of information included can be managed by setting the verbosity, which we will show in more detail below.

#### Verbosity

SDS read APIs supports an accept-verbosity header that will set whether verbose output should be excluded. A value is considered verbose if it is the default value for its type, such as false for a boolean, None for a string, etc. The following example output demonstrates responses for the same call using verbose and non-verbose values:

accept-verbosity = verbose
{
  'Timestamp': '2021-12-15T01:39:05Z',
  'Value': 98.30506,
  'IsQuestionable': False,
  'IsSubstituted': True,
  'IsAnnotated': False,
  'SystemStateCode': None,
  'DigitalStateName': None
}

accept-verbosity = none-verbose
{
  'Timestamp': '2021-12-15T01:39:05Z',
  'Value': 98.30506,
  'IsSubstituted': True,
}

Note that since `IsSubstituted` is True it is still included in both responses while the other values are excluded when not accepting verbose values.

When using the python sample library, this option is configurable when creating the `OCSClient` object by providing True or False for the `accept_verbosity` constructor parameter.

### Get Window Values

`getWindowValues` is used for retrieving events over a specific index range. This is the function definition:

```python
def getWindowValues(self, namespace_id, stream_id, value_class, start, end):
```

- **start** and **end** (inclusive) represent the indices for the retrieval.
- The **namespace Id** and **stream Id** must be provided to the function call.
- A JSON object containing a list of the found values is returned.

The method is called as shown :

```python
values = client.Streams.getWindowValues(namespaceId, stream.Id, None, 0, 40)
```

You can also retrieve the values in the form of a table (in this case with headers). Here is how to use it:

```python
def getWindowValuesForm(self, namespace_id, stream_id, value_class, start, end, form)
```

- **start** and **end** (inclusive) represent the indices for the retrieval.
- The **namespace Id** and **stream Id** must be provided to the function call.
- **form** specifies the organization of a table, the two available formats are table and header table

Here is how it is called:

```python
values = sdsClient.Streams.getWindowValuesForm(namespaceId, stream.Id, None, 0, 180,"tableh")
```

### Get Range Values

`getRangeValues` is used for retrieving a specified number of events from a starting index. The starting index is the Id of the `SdsTypeProperty` that corresponds to the key value of the type. Here is the request:

```python
def getRangeValues(self, namespace_id, stream_id, value_class, start, skip, count, reversed, boundary, streamView_id=""):
```

- **start** is the increment by which the retrieval will happen.
- **count** is how many values you wish to have returned.
- **reversed** is a boolean that when `true` causes the retrieval to work backwards from the starting point.
- **boundary** is a `SdsBoundaryType` value that determines the behavior if the starting index cannot be found. Refer the to the [SDS documentation](https://ocs-docs.osisoft.com/Content_Portal/Documentation/SequentialDataStore/Data_Store_and_SDS.html) for more information about SdsBoundaryTypes.

The `getRangeValues` method is called as shown :

```python
values = sdsClient.Streams.getRangeValues(namespaceId, stream.Id, None, "1", 0, 3, False, SdsBoundaryType.ExactOrCalculated)
```

## Additional Methods

Note that there are more methods provided in the SdsClient than are discussed in this document, for a complete list of HTTP request URLs refer to the [SDS documentation](https://ocs-docs.osisoft.com/Content_Portal/Documentation/SequentialDataStore/Data_Store_and_SDS.html).

---

Automated test uses Python 3.9.1 x64

For the main PI to OCS read only stream samples page [ReadMe](https://github.com/osisoft/OSI-Samples-OCS/blob/main/docs/PI_TO_OCS.md)  
For the main OCS samples page [ReadMe](https://github.com/osisoft/OSI-Samples-OCS)
For the main OSIsoft samples page [ReadMe](https://github.com/osisoft/OSI-Samples)