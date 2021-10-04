# mongodb integration pack

> StackStorm integration for MongoDB administration.
Carlos <nzlosh@yahoo.com>


## Configuration

The following options are required to be configured for the pack to work correctly.

| Option | Type | Required | Secret | Description |
|---|---|---|---|---|
| `default_profile` | string | True |  | The name of the default profile to use in actions. |
| `profiles` | array | True |  | MongoDB cluster/server profiles |



### High available setups

Mongo databases using replication must have the replica set in the packs configuration otherwise the action will not automatically switch to the PRIMARY server and will fail.

## Actions


The pack provides the following actions:

### collection_list
_List the available collections for a database._

| Parameter | Type | Required | Secret | Description |
|---|---|---|---|---|
| `profile_name` | string | False | default | _Mongodb profile to be used for the action._ |
| `db_name` | string | True | default | _The name of database to list collections._ |
### collection_list
_Create a collection in a database._

| Parameter | Type | Required | Secret | Description |
|---|---|---|---|---|
| `profile_name` | string | False | default | _Mongodb profile to be used for the action._ |
| `db_name` | string | True | default | _The name of database to create the collection on._ |
| `name` | string | True | default | _The name of collection to created._ |
### user_create
_Create a database user._

| Parameter | Type | Required | Secret | Description |
|---|---|---|---|---|
| `profile_name` | string | False | default | _Mongodb profile to be used for the action._ |
| `username` | string | True | default | _Name of the user to be created._ |
| `password` | string | True | True | _Password of the user to be created._ |
| `roles` | array | True | default | _The list of Mongo roles to applied to the user._ |
| `db_name` | string | True | default | _The name of database to create the collection on._ |
### user_list
_List users in a database._

| Parameter | Type | Required | Secret | Description |
|---|---|---|---|---|
| `profile_name` | string | False | default | _Mongodb profile to be used for the action._ |
| `db_name` | string | True | default | _The name of database to create the collection on._ |
### collection_delete
_Delete a collection in a database._

| Parameter | Type | Required | Secret | Description |
|---|---|---|---|---|
| `profile_name` | string | False | default | _Mongodb profile to be used for the action._ |
| `db_name` | string | True | default | _The name of database to delete the collection on._ |
| `name` | string | True | default | _The name of collection to deleted._ |
### database_list
_List the available databases in a mongo server_

| Parameter | Type | Required | Secret | Description |
|---|---|---|---|---|
| `profile_name` | string | False | default | _Mongodb profile to be used for the action._ |
### user_update
_Update an existing database user._

| Parameter | Type | Required | Secret | Description |
|---|---|---|---|---|
| `profile_name` | string | False | default | _Mongodb profile to be used for the action._ |
| `username` | string | True | default | _Name of the user to be created._ |
| `password` | string | True | True | _Password of the user to be created._ |
| `roles` | array | True | default | _The list of Mongo roles to applied to the user._ |
| `db_name` | string | True | default | _The name of database to create the collection on._ |
| `mode` | string | True | default | _Mode of update. 'replace' or 'merge'._ |
### user_delete
_Delete an existing database user._

| Parameter | Type | Required | Secret | Description |
|---|---|---|---|---|
| `profile_name` | string | False | default | _Mongodb profile to be used for the action._ |
| `username` | string | True | default | _Name of the user to be created._ |
| `db_name` | string | True | default | _The name of database to create the collection on._ |
### database_delete
_Delete a database._

| Parameter | Type | Required | Secret | Description |
|---|---|---|---|---|
| `profile_name` | string | False | default | _Mongodb profile to be used for the action._ |
| `db_name` | string | True | default | _The name of database to be dropped._ |
### database_create
_Create a database on a mongo server_

| Parameter | Type | Required | Secret | Description |
|---|---|---|---|---|
| `profile_name` | string | False | default | _Mongodb profile to be used for the action._ |
| `db_name` | string | True | default | _The name of the database to be created._ |



## Sensors

There are no sensors available for this pack.



## Authentication

 * To be able to administer MongoDB using this pack, a user account that has the privileges to manipulate databases, collections, documents is required.

   For simlicity sakes, the `root` role has above and beyond the required access to preform any actions in this pack.  However, it is not recommended to use such a role in production.  The exact permissions to grant to the user will depend on the security policies of the organisation operating MongoDB.

   As an example of creating a root user account:
   ```
   db.createUser("<db_admin_account>", { roles: [{role: "root", db: "admin"}], pwd: "<db_admin_password>"})
   ```

   For more information on authentication and authorisation, seek help from the Mongo manual:
   - https://docs.mongodb.com/manual/core/authentication/
   - https://docs.mongodb.com/manual/core/authorization/
   - https://docs.mongodb.com/manual/core/security-transport-encryption/


## Limitations

 * This pack is intended for MongoDB administration only and does not provide any data querying functionality.


## References

  * [pymongo](https://pymongo.readthedocs.io/en/stable/index.html) Python module is used in this pack.


## Acknowledgements
  * Antü Plasma Suite for the use of the mongodb icon under the CREATIVE COMMONS BY-SA 3.0. licence.

<sub>Documentation generated using [pack2md](https://github.com/nzlosh/pack2md)</sub>