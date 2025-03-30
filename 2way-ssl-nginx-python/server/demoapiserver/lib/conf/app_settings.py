#######################################
# Identity
#######################################
VALID_CLIENT_CNS = [
    "web.client.com"
    # we only accept the client with this CN, not the middle nginx cert
    # "middle.nginx1.ddl.com",
    # "backend.nginx2.ddl.com"
]

#######################################
# Shared secret
#######################################
# server to client
SHARED_SECRET_SERVER2CLIENT_PARAM = "X-SERVER-CLIENT-TOKEN"  # replace me
SHARED_SECRET_SERVER2CLIENT_VALUE = "this is a shared secret from server to client"  # replace me

# client to server
SHARED_SECRET_CLIENT2SERVER_PARAM = "X-CLIENT-SERVER-TOKEN"  # replace me
SHARED_SECRET_CLIENT2SERVER_VALUE = "this is a shared secret from client to server"  # replace me
