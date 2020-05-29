from coapthon.client.helperclient import HelperClient
from coapthon.client.coap import CoAP
from coapthon.messages.message import Message

host = "127.0.0.1"
port = 5683

clientHelper = HelperClient(server=(host, port))

try:
    path = "/basic"
    response = clientHelper.get(path)
    print(response)
    # print(response.payload)

except KeyboardInterrupt:
    print("Client Shutdown")
    clientHelper.close()
    print("Exiting...")
