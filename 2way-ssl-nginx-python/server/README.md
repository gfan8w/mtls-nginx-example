# `demoapiserver`

A Flask application to demonstrate how 2-way SSL works from a Server's perspective.

To run `demoapiserver`, simply following the step mentioned [here](../README.md#running-the-environment). 


## Additional notes about security

For added security, other then using Client Certificate to verify the Client's identity by the Server, the Client
should also supply a "shared secret" for every call to the Server's "secure routes".

The "shared secret" will be included in the header of the Client's HTTP Request. The Server should validate this token. In
this `demoapiserver`, the token parameter name will be `X-CLIENT-SERVER-TOKEN` (see [server/demoapiserver/lib/conf/app_settings.py](./demoapiserver/lib/conf/app_settings.py)).

If the Client's HTTP Request to the "secure routes" is successfully served, the Server should reply with another
"shared secret". This other "shared secret" will be included in the header of the Server's HTTP Response. In this
`demoapiserver`, the token parameter name will be `X-SERVER-CLIENT-TOKEN`.


<img src="../resources/2way-ssl-ref-implementation-demoapiserver.png" />