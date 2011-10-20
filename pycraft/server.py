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
from pycraft import mcprocess
import re

class Server:
    """
    Handles running the server as a daemon and sending messages to the daemon
    and sending messages to the daemon as a client.
    """

    host = 'localhost'
    port = 54545
    buf  = 1024
    addr = (host,port)

    def __init__( self, message = None ):
        """
        Starts the server in daemon mode or sends a message to the server.

        @message: the message to send to the server, if None then start the
                  server as a daemon
        """
        self.sock = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )

        if not message:
            self.daemonize()
        else:
            self.sendmessage( message )

        self.sock.close()
    
    def daemonize( self ):
        """
        Starts the daemon and waits for the client to tell it what to do.
        Acts as a layer between the client and the mcprocess passing messages
        back and forth.
        """
        self.sock.bind(self.addr)
        self.mcprocess = mcprocess.MCProcess()

        try:
            while True:
                data,self.returnaddr = self.sock.recvfrom( self.buf )
                data = data.decode( 'utf-8' )

                if not data:
                    print( "No data received from connection from", self.returnaddr )
                    continue

                self.process_input( data )
        except KeyboardInterrupt:
            print( "^C caught, stopping..." )
            self.mcprocess.stop()
            sys.exit(1)

    def sendmessage( self, message ):
        """
        Send a message to the server.

        @message: the message to send to the server
        """
        if not self.sock.sendto( message.encode( 'utf-8' ), self.addr ):
            print( "Error, could not send message" )
            return
        self.sock.settimeout(20)
        while True:
            message,self.addr = self.sock.recvfrom( self.buf )
            message = message.decode( 'utf-8' )
            if message == "DONE":
                break
            if re.search( "^SET", message ):
                s = message.split()
                if s[1] == "TIMEOUT":
                    self.sock.settimeout( int(s[2]) )
                continue
            print( message )

    def reply( self, message ):
        if not self.sock.sendto( message.encode( 'utf-8' ), self.returnaddr ):
            print( "Error, could not send message" )

    def process_input( self, user_input ):
        user_input = user_input.strip()
        if user_input == 'start':
            self.reply( self.mcprocess.start() )
        elif user_input == 'stop':
            self.reply( self.mcprocess.stop() )
        elif user_input == 'restart':
            self.reply( self.mcprocess.stop() )
            self.reply( self.mcprocess.start() )
        elif user_input == 'quit':
            self.reply( self.mcprocess.stop() )
            self.reply( "Server terminating" )
            self.reply( "DONE" )
            sys.exit()
        elif user_input == 'upgrade':
            self.reply( "Downloading upgrade" )
            self.reply( "SET TIMEOUT 120" )
            self.reply( self.mcprocess.upgrade() )
        elif user_input == 'help':
            self.reply( self.mcprocess.help() )
        elif user_input == 'help mc':
            if not self.mcprocess._mcp:
                self.reply( 'Server must be running to display help' )
            else:
                self.reply( self.mcprocess.send( 'help' ) )
        else:
            self.reply( self.mcprocess.send( user_input ) )
        self.reply( "DONE" )



if __name__ == "__main__":
    if len(sys.argv) >= 2:
        if sys.argv[1] == "-d":
            s = Server()
        else:
            s = Server( message = sys.argv[1] )
    else:
        print( "That's not how you use this program!!" )
