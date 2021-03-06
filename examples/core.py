## Copyright (c) 2010, Coptix, Inc.  All rights reserved.
## See the LICENSE file for license terms and warranty disclaimer.

"""core -- an example CoreInterface implementation

This example demonstrates how to implement a simple XMPP Core
interface.  Normally the higher-level Application/Plugin abstraction
is used.  The server waits for a <ping> from the client and responds
with a pong.  This is done until the client closes the stream.
"""

import xmpp

class Pong(xmpp.CoreInterface):

    def __init__(self, addr, stream):
        self.address = addr
        self.parser = xmpp.xml.Parser(xmpp.XMPPTarget(self))
        self.stream = stream.read(self.parser.feed)
        self.pings = 0

        print 'Waiting for some pings from %s.' % (addr[0])

    def is_stanza(self, name):
        return name == '{jabber:client}ping'

    def handle_open_stream(self, attrs):
        self.stream.write(
            '<stream:stream xmlns="jabber:client"'
            ' from="server@example.net" xml:lang="en"'
            ' xmlns:stream="http://etherx.jabber.org/streams">'
        )

    def handle_stanza(self, ping):
        self.pings += 1
        self.stream.write('<pong/>')

    def handle_close_stream(self):
        self.stream.write('</stream:stream>', self.close)

    def close(self):
        print 'Got %d ping(s) from %s.' % (self.pings, self.address[0])
        self.stream.close()

if __name__ == '__main__':
    server = xmpp.TCPServer(xmpp.XMPPHandler(Pong)).bind('127.0.0.1', 9000)
    xmpp.start([server])
