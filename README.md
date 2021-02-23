# Socket Server for IOT device

## Category

- [Notice](#notice)
- [API Document](#api-document)
  - [PING/PONG](#ping_pong)
  - [Send Request to Server](#send-request-to-server)
  - [Get Response from Server](#get-response-from-server)
  - [Status Code](#status-code)
- [Links](#links)
- [To-do List](#to-do-list)

## Notice

**NOT every Request will get a Response. Server will filter out the duplicate Request.**

## API Document

### PING/PONG

**Send**

```
PING
```

**Get**

```
PONG
```

### Send Request to Server

**Format**

```
<request_type>_<request_id>_<container_id>
```

**Regex**

```
^(RTN|RLD)_\w{4}_\d{6}$
```

**Example**

_Return a container #2020_

```
RTN_AB12_002020
```

**Detail**

| column       | description                                                                  | length | type              | accept         |
| ------------ | ---------------------------------------------------------------------------- | ------ | ----------------- | -------------- |
| request_type | -                                                                            | 3      | string            | `RTN` or `RLD` |
| request_id   | You should set an random 4 digit ID for a request to let you track response. | 4      | string or integer | -              |
| container_id | You should pad this column to 6 digit.                                       | 6      | integer           | -              |

### Get Response from Server

**Format**

```
<response_type>_<status_code>_<request_id>
```

**Regex**

```
^(SUC|ERR)_\d{3}_\w{4}$
```

**Example**

_Request #AB12 success_

```
SUC_001_AB12
```

**Detail**

| column        | description                                                          | length | type              | expect         |
| ------------- | -------------------------------------------------------------------- | ------ | ----------------- | -------------- |
| response_type | -                                                                    | 3      | string            | `SUC` or `ERR` |
| status_code   | Describe response status. Check [Status Code](#status-code) section. | 3      | integer           | -              |
| request_id    | The request ID you set.                                              | 4      | string or integer | -              |

### Status Code

**Success**

- `001` **Success**

**Error**

- `101` **Format of the Request is invalid**
- `102` **Encoding of the Request is invalid**
- `201` **Can't Find the Container**
- `202` **Container's State is Not Ready For that Action**
- `400` **API return Fail Result**
- `901` **Connection Closed by Server**
- `998` **INTERNAL Server Error**
- `999` **Unknown Server Error**

## Links

- Recommended Socket Server/Client for Testing: [SocketTest](http://sockettest.sourceforge.net/)

## To-do List

All done. Well done!
