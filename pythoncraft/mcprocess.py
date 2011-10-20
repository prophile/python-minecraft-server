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
from urllib.error import HTTPError, URLError
from pythoncraft import config
import threading
import re

class MCProcess:

    def help( self ):
        msg = "Version: DEVELOPMENT PREVIEW\n"
        msg += "help    - Displays this message\n"
        msg += "help mc - Displays minecrafts help\n"
        msg += "start   - Starts the minecraft server\n"
        msg += "stop    - Stops the minecraft server\n"
        msg += "upgrade - Upgrades the minecraft server"
        return msg

    def __init__( self ):
        self.server_jar = 'minecraft_server.jar'
        self._mcp = None

        print( "Welcome to the minecraft python wrapper" )
        print( "Type 'help' for help" )

        self.first_run()

    def main_loop( self ):
        while True:
            sys.stdout.write( '\r>' )
            sys.stdout.flush()
            try:
                input = sys.stdin.readline()
                if input:
                    #self.process_input( input )
                    print( "Feature removed" )
            except KeyboardInterrupt:
                self.stop()
                sys.exit(1)

    def _mc_output_loop( self ):
        while self._mcp:
            line = self._mcp.stdout.readline()
            string = line.decode( "utf-8" )
            if re.search( "^>\\r", string ):
                # Remoeve >\r
                string = string.lstrip( ">" )
                string = string.rstrip( "\r" )
                string = string.rstrip( "\n" )
                print( string )

    """
    Starts the minecraft server
    """
    def start( self ):
        if self._mcp != None:
            sys.stderr.write( 'Error: Server already running\n' )
            return 'Server already running'

        if not self.check_jar():
            return 'Could not fund jar'

        self._mcp = subprocess.Popen( config.java_exec + " " + config.java_flags + ' -jar ' + self.server_jar + " nogui", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT )

        self._mcp_reader = threading.Thread( target=self._mc_output_loop )
        self._mcp_reader.start()
        print( "Starting minecraft server" )
        return 'Starting minecraft server'

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

        if os.path.exists( 'server.propertities' ):
            print( "First run" )
        else:
            print( "Not first run" )

    """
    Stops the minecraft server
    """
    def stop( self ):
        print( self._mcp )
        if self._mcp == None:
            print( 'Server not running' )
            return 'Server not running'
        self.send( 'stop' )
        self._mcp.wait()
        self._mcp = None
        self._mcp_reader.join()
        self._mcp_reader = None
        print( "Server stopped" )
        return 'Server stopped'

    """
    Sends a command to the minecraft server
    """
    def send( self, message ):
        if self._mcp == None:
            print( 'Minecraft server not started' )
            return 'Minecraft server not started'
        message += '\n'
        self._mcp.stdin.write( message.encode('latin-1') )
        self._mcp.stdin.flush()
        print( message + " send to minecraft server" )
        return message + " sent to minecraft server"

    def check_jar( self ):
        print ( "Current dir: ", os.getcwd() )
        if not os.path.exists( self.server_jar ):
            sys.stderr.write( 'Error: ' + self.server_jar + ' does not exist\n' )
            return False
        return True


    def upgrade( self ):
        url = config.url[ config.server_type ]
        local = None
        try:
            sys.stdout.write( "Downloading minecraft server from " + url + "..." )
            sys.stdout.flush()
            f = urllib.request.urlopen( url )

            newjar = self.server_jar + ".new"
            local = open( newjar, "wb" )
            local.write( f.read() )
            os.rename( newjar, self.server_jar )

            print( " done" )
            retmsg = "Download completed. "
            if self._mcp:
                retmsg += "Restart the minecraft sever to use the new version"
            return retmsg
        
        #handle errors
        except HTTPError as e:
            retmsg = "HTTP Error:", e.reason, url
        except URLError as e:
            retmsg = "URL Error:", e.reason, url
        finally:
            if local:
                local.close()
            return retmsg

if __name__ == "__main__":
    p = MCProcess()
    p.main_loop()
