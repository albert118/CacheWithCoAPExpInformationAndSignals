import sys
import threading

from coapthon.layers import cachelayer
from coapthon.server.coap import CoAP
from coapthon.reverse_proxy.coap import CoAP as RevProxy

from coapthon import defines
from coapthon.resources.resource import Resource

def shutdown(server):
    print("Client Shutdown")
    server.close()
    print("Exiting...")

# dummy resource for testing.
class TestResource(Resource):
    def __init__(self, name="TestResource", coap_server=None):
        super(TestResource, self).__init__(name, coap_server, visible=True,
                                            observable=True, allow_children=True)
        self.payload = "A test resource"
        self.resource_type = "rt1"
        self.content_type = "text/plain"
        self.interface_type = "if1"

    def render_GET(self, request):
        return self

    def render_PUT(self, request):
        self.edit_resource(request)
        return self

    def render_POST(self, request):
        res = self.init_resource(request, TestResource())
        return res

    def render_DELETE(self, request):
        return True

 # dummy resource for testing.
class AnotherTestResource(Resource):
    def __init__(self, name="AnotherTestResource", coap_server=None):
        super(AnotherTestResource, self).__init__(name, coap_server, visible=True,
                                            observable=True, allow_children=True)
        self.payload = "Another test resource"
        self.resource_type = "rt1"
        self.content_type = "text/plain"
        self.interface_type = "if1"

    def render_GET(self, request):
        return self

    def render_PUT(self, request):
        self.edit_resource(request)
        return self

    def render_POST(self, request):
        res = self.init_resource(request, AnotherTestResource())
        return res

    def render_DELETE(self, request):
        return True

 # dummy resource for testing.
class BasicResource(Resource):
    def __init__(self, name="AnotherTestResource", coap_server=None):
        super(BasicResource, self).__init__(name, coap_server, visible=True,
                                            observable=True, allow_children=True)
        self.payload = "A basic test resource"
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

# working! 
class CoAPServer(CoAP):
    def __init__(self, server_address, multicast=False):
        CoAP.__init__(self, server_address, multicast)
        self.add_resource('/basic', BasicResource())

        print(("CoAP Server started on " + str(server_address[0]) + ":" + str(server_address[1])))

class RevProxyServer(RevProxy):
    def __init__(self, server_address, xml_file, multicast=False, cache=False, starting_mid=False):
        RevProxy.__init__(self, server_address, xml_file=xml_file, multicast=multicast,
                        cache=cache, starting_mid=starting_mid)

        print(("CoAP Reverse Proxy Caching Server started on " + str(server_address[0]) + ":" + str(server_address[1])))

def main():  # pragma: no cover
    server_address1 = ("127.0.0.1", 5684)
    server_address2 = ("127.0.0.1", 5685)
    server_address3 = ("127.0.0.1", 5686)
    ProxyServer_address = ("127.0.0.1", 5683)

    multicast    = False
    cache        = True
    starting_mid = False
    xml_file = "reverse_proxy.xml"

    server1 = CoAPServer(server_address1, multicast)
    server2 = CoAPServer(server_address2, multicast)
    server3 = CoAPServer(server_address3, multicast)

    ProxyServer = RevProxyServer(ProxyServer_address, xml_file, multicast=multicast,
                            cache=cache, starting_mid=starting_mid)

    server_thread1 = threading.Thread(target=server1.listen, args=(10,))
    server_thread2 = threading.Thread(target=server2.listen, args=(10,))
    server_thread3 = threading.Thread(target=server3.listen, args=(10,))

    ProxyServer_thread = threading.Thread(target=ProxyServer.listen, args=(10,))

    try:
        server_thread1.start()
        server_thread2.start()
        server_thread3.start()

        ProxyServer_thread.start()

    except KeyboardInterrupt:
        shutdown(server1)
        server_thread1.join(timeout=10)
        shutdown(server2)
        server_thread2.join(timeout=10)
        shutdown(server3)
        server_thread3.join(timeout=10)
        shutdown(ProxyServer)
        ProxyServer_thread.join(timeout=10)

main()
