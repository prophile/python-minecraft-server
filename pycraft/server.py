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
    """
    Handels running the server as a deamon and sending messages to the deamon
    and sending messages to the deamon as a client.
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

        while True:
            data,addr = self.sock.recvfrom( self.buf )
            data = data.decode( 'utf-8' )

            if not data:
                print( "No data recieved from connection from", addr )
                continue

            self.process_input( data )
            if not self.sock.sendto( "reieved".encode( 'utf-8' ), addr ):
                print( "Error, could not send message" )
            if data == "quit":
                break

    def sendmessage( self, message ):
        """
        Send a message to the server.

        @message: the message to send to the server
        """
        if not self.sock.sendto( message.encode( 'utf-8' ), self.addr ):
            print( "Error, could not send message" )
            return
        data,self.addr = self.sock.recvfrom( self.buf ) #TODO timeout
        data = data.decode( 'utf-8' )
        print( data )

    def process_input( self, user_input ):
        user_input = user_input.strip()
        if user_input == 'start':
            self.mcprocess.start()
        elif user_input == 'stop':
            print("Stopppign")
            self.mcprocess.stop()
        elif user_input == 'quit':
            self.mcprocess.quit()
        elif user_input == 'upgrade':
            self.mcprocess.upgrade()
        elif user_input == 'help':
            print( self.mcprocess.help() )
        elif user_input == 'help mc':
            if not self.mcprocess._mcp:
                sys.stderr.write( 'Server must be running to display help\n' )
            else:
                self.mcprocess.send( 'help' )
        else:
            print( "Command not reconised, sending to mincraft server" )
            self.mcprocess.send( user_input )


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        if sys.argv[1] == "-d":
            s = Server()
        else:
            s = Server( message = sys.argv[1] )
    else:
        print( "Thats not how you use this program!!" )
