# mongodb integration pack

> StackStorm intergratation for MongoDB. https://powerdns.com/
Carlos <nzlosh@yahoo.com>


## Configuration

The following options are required to be configured for the pack to work correctly.

| Option | Type | Required | Secret | Description |
|---|---|---|---|---|
| `api_key` | string | True | True | PowerDNS API Key |
| `api_url` | string | True | False | URL to PowerDNS API. |


## Actions


The pack provides the following actions:

### record_get
_Get record data_

| Parameter | Type | Required | Secret | Description |
|---|---|---|---|---|
| `record_name` | string | True | default | _Record name to be fetched._ |
| `zone_name` | string | True | default | _Zone name to fetch._ |
| `server_id` | string | True | default | _Server name to query._ |
| `response_timeout` | integer | True | default | _Time to wait for a response from PowerDNS._ |
### database_list
_Lists the avilable databases on a mongo server_

| Parameter | Type | Required | Secret | Description |
|---|---|---|---|---|
| `profile_name` | string | True | default | _The predefined mongodb profile to use._ |



## Sensors

There are no sensors available for this pack.



## Authentication

 * To be advised.


## Limitations

 * Records can only be created or enitrely updated.  No partial record updates are currently supported.

## References

  * This pack uses [python-powerdns](https://github.com/outini/python-powerdns).


## Thanks to
  * Antü Plasma Suite for the use of the mongodb icon under the CREATIVE COMMONS BY-SA 3.0. licence.

<sub>Documentation generated using [pack2md](https://github.com/nzlosh/pack2md)</sub>