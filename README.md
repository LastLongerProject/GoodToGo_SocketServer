# Socket Server for IOT device

## API Document

### Request to API

**Format**

```
<request_type>_<request_id>_<container_id>
```

**Regex**

```
^(RTN|RLD)_\w{4}_\d{6}$
```

|              | description                                                                  | length | type              | accept         |
| ------------ | ---------------------------------------------------------------------------- | ------ | ----------------- | -------------- |
| request_type | -                                                                            | 3      | string            | ["RTN", "RLD"] |
| request_id   | You should set an random 4 digit ID for a request to let you track response. | 4      | string or integer | -              |
| container_id | You should pad this column to 6 digit.                                       | 6      | integer           | -              |

**Example**

_Return a container #2020_

```
RTN_AB12_002020
```

### Response from API

**Format**

```
<response_type>_<status_code>_<request_id>
```

**Regex**

```
^(SUC|ERR)_\d{3}_\w{4}$
```

|               | description                                                          | length | type              | expect         |
| ------------- | -------------------------------------------------------------------- | ------ | ----------------- | -------------- |
| response_type | -                                                                    | 3      | string            | ["SUC", "ERR"] |
| status_code   | Describe response status. Check [Status Code](#status-code) section. | 3      | integer           | -              |
| request_id    | The request ID you set.                                              | 4      | string or integer | -              |

**Example**

_Request #AB12 success_

```
SUC_001_AB12
```

### Status Code

**Success**

- 001 **Success**

**Error**

- 101 **Format of the Request is invalid**
- 201 **Can't Find the Container**
- 202 **Container's State is Not Ready For that Action**
- 901 **Connection Closed by Server**
- 998 **INTERNAL Server Error**
- 999 **Unknown Server Error**

## TODO

- Response System
- Api Binding
- Threading
