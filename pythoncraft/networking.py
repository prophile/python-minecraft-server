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
import socketserver
import socket
import sys
from pythoncraft import mcprocess

port = 55242
host = 'localhost'

class Server:
    def __init__( self ):
        try:
            server = ThreaddedServer( (host, port), ServerHandler )
        except socket.error as e:
            if e.errno == 98:
                print( "Server is already running" )
            sys.exit(1)
        server.mcp = mcprocess.MCProcess()
        server.serve_forever()

class ThreaddedServer( socketserver.ThreadingMixIn, socketserver.TCPServer ):
    allow_reuse_address = True

class ServerHandler( socketserver.StreamRequestHandler ):
    
    def handle( self ):
        self.data = self.rfile.readline().strip()
        print( "%s wrote:" % self.client_address[0] )
        print( self.data )
        self.process_input( self.data.decode( "utf8" ) )

    def write( self, msg ):
        self.wfile.write( bytes( str(msg) + "\n", "utf8" ) )

    def process_input( self, user_input ):
        user_input = user_input.strip()
        if user_input == 'start':
            self.write( self.server.mcp.start() )
        elif user_input.startswith( 'stop' ):
            self.write( self.server.mcp.stop() )
        elif user_input == 'restart':
            self.write( self.server.mcp.stop() )
            self.write( self.server.mcp.start() )
        elif user_input == 'quit':
            self.write( self.server.mcp.stop() )
            self.write( "Server terminating" )
            self.write( "DONE" )
            self.server.shutdown()
        elif user_input == 'upgrade':
            self.write( "Downloading upgrade" )
            self.write( self.server.mcp.upgrade() )
        elif user_input == 'status':
            self.write( 'Pycraft server is running' )
            self.write( self.server.mcp.status() )
        elif user_input == 'help':
            self.write( self.server.mcp.help() )
        elif user_input == 'help mc':
            if not self.server.mcp._mcp:
                self.write( 'Server must be running to display help' )
            else:
                self.write( self.server.mcp.send( 'help' ) )
        else:
            self.write( self.server.mcp.send( user_input ) )
        self.write( "DONE" )

class Client:
    def __init__( self, message ):
        data = " ".join( sys.argv[1:] )

        self.sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )

        try:
            self.sock.connect( ( host, port ) )
        except socket.error as e:
            if e.errno == 111:
                if data == "status":
                    print( "Pycraft server is not running" )
                else:
                    print( "Could not connect to daemon." )
                    print( "Run pycraft -d to start pycraft as a daemon first." )
                sys.exit(1)
            raise e
        self.write( data )
        self.cfile = self.sock.makefile()

        while True:
            msg = self.read()
            if msg == "DONE":
                break
            print( "Got: %s" % msg )


        self.sock.close()

    def write( self, message ):
        self.sock.send( bytes( message + "\n", "utf8" ) )

    def read( self ):
        return self.cfile.readline().strip()
