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
import os, errno
import sys
import subprocess
import urllib.request

class Server:

    def __init__( self ):
        self.arguments = 'nogui'
        self.server_jar = 'minecraft_server.jar'
        self._mcp = None

    def main_loop( self ):
        while True:
            try:
                input = sys.stdin.readline()
                if input:
                    self.process_input( input )
            except KeyboardInterrupt:
                self.quit()

    
    """
    Starts the minecraft server
    """
    def start( self ):
        if self._mcp != None:
            sys.stderr.write( 'Error: Server already running' )
            return

        self.first_run()

        if not self.check_jar():
            return

        self._mcp = subprocess.Popen( 'java ' + self.arguments + ' -jar ' + self.server_jar, shell=True )

    """
    Checks for the first run and sets up anything that needs to be set up
    """
    def first_run( self ):
        directory = os.getcwd() + '/minecraft'

        try:
            os.mkdir( directory )
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        os.chdir( directory )

        if not os.path.exists( 'server.propertities' ):
            print( "First run" )
        else:
            print( "Not first run" )

    """
    Stops the minecraft server
    """
    def stop( self ):
        print( self._mcp )
        if self._mcp == None:
            sys.stderr.write( 'Server not running' )
            return
        sys.stdout.write( 'Shutting down server...' )
        self._mcp.communicate( 'stop' )
        self._mcp.wait()
        self._mcp = None

    """
    Stops the minecraft server then exits
    """
    def quit( self, value=0):
        self.stop()
        sys.exit( value )

    """
    Sends a command to the minecraft server
    """
    def send( self, message ):
        if self._mcp == None:
            return
        self._mcp.communicate( message )

    def check_jar( self ):
        print ( "Current dir: ", os.getcwd() )
        if not os.path.exists( self.server_jar ):
            sys.stderr.write( 'Error: ' + self.server_jar + ' does not exist' )
            return false
        return true

    def process_input( input ):
        if input == 'stop':
            stop()
        elif input == 'quit':
            quit()
        else:
            send( input )

if __name__ == "__main__":
    server = Server()
    server.start()
