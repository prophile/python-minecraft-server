#!/usr/bin/env python3
"""
Copyright (C) 2011 Michael Daffin

  This software is provided 'as-is', without any express or implied
  warranty.  In no event will the authors be held liable for any damages
  arising from the use of this software.

  Permission is granted to anyone to use this software for any purpose,
  including commercial applications, and to alter it and redistribute it
  freely, subject to the following restrictions:

  1. The origin of this software must not be misrepresented; you must not
     claim that you wrote the original software. If you use this software
     in a product, an acknowledgment in the product documentation would be
     appreciated but is not required.
  2. Altered source versions must be plainly marked as such, and must not be
     misrepresented as being the original software.
  3. This notice may not be removed or altered from any source distribution.
"""
import socket
import sys
import mcprocess

class Server:
    host = 'localhost'
    port = 54545
    buf  = 1024
    addr = (host,port)

    def __init__( self, daemon = True ):
        self.sock = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )

        if daemon:
            self.daemonize()
        else:
            self.clientize()

        self.sock.close()
    
    def daemonize( self ):
        self.sock.bind(self.addr)
        self.mcprocess = mcprocess.MCProcess()

        while True:
            data,self.addr = self.sock.recvfrom( self.buf )
            data = data.decode( 'utf-8' )
            print( "Data: " + data )
            if data:
                self.mcprocess.process_input( data )
            if data == "quit":
                break

    def clientize( self ):
        while True:
            data = input( '>> ' )
            if self.sock.sendto( data.encode( 'utf-8' ), self.addr ):
                print( "Sending message" )
            else:
                print( "Failed to send" )


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "-d":
        s = Server()
    else:
        s = Server( False )
