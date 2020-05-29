import getopt
import sys
from coapthon.layers import cachelayer
from coapthon.server.coap import CoAP
from coapthon.reverse_proxy.coap import CoAP as RevProxy

from coapthon import defines
from coapthon.resources.resource import Resource

class BasicResource(Resource):
    def __init__(self, name="BasicResource", coap_server=None):
        super(BasicResource, self).__init__(name, coap_server, visible=True,
                                            observable=True, allow_children=True)
        self.payload = "TEST TEST TEST TEST TEST"
        self.resource_type = "rt1"
        self.content_type = "text/plain"
        self.interface_type = "if1"

    def render_GET(self, request):
        return self

    def render_PUT(self, request):
        self.edit_resource(request)
        return self

    def render_POST(self, request):
        res = self.init_resource(request, BasicResource())
        return res

    def render_DELETE(self, request):
        return True
        
class CoAPServer(CoAP):
    def __init__(self, host, port, multicast=False):
        CoAP.__init__(self, (host, port), multicast)
        self.add_resource('basic/', BasicResource())

        print(("CoAP Server started on " + host + ":" + str(port)))
        print((self.root.dump()))

class RevProxyServer(CoAP):
    def __init__(self, host, port, multicast=False):
        RevProxy.__init__(self, (host, port), multicast, cache=True)
        self.add_resource('basic/', BasicResource())
        
        print(("CoAP Reverse Proxy Caching Server started on " + host + ":" + str(port)))
        print((self.root.dump()))

def usage():  # pragma: no cover
    print("coapserver.py -i <ip address> -p <port>")


def main():  # pragma: no cover
    ip = "127.0.0.1"
    port = 5683
    multicast = False

    server = CoAPServer(ip, port, multicast)
    try:
        server.listen(10)
    except KeyboardInterrupt:
        print("Server Shutdown")
        server.close()
        print("Exiting...")

main()
