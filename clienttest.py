from coapthon.client.helperclient import HelperClient
from coapthon.messages.message import Message
from coapthon.messages.request import Request
from coapthon.messages.response import Response
from coapthon import defines

host = "127.0.0.1"
port = 5686

clientHelper = HelperClient(server=(host, port))

def shutdown():
    print("Client Shutdown")
    clientHelper.close()
    print("Exiting...")

try:
    req = Request()
    req.code = defines.Codes.GET.number
    req.uri_path = "/basic"
    req.type = defines.Types["CON"]
    req._mid = 2
    req.destination = (host, port)

    response = clientHelper.send_request(req)
    # response = clientHelper.get(path)

    print(response)         # print the entire response.
    print(response.payload) # print the payload attribute.
    shutdown()

except KeyboardInterrupt:
    shutdown()
