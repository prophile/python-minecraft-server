import os, errno
import sys
import subprocess

class Server:

    def __init__( self ):
        self.arguments = 'nogui'
        self.server_jar = 'minecraft_server.jar'
        self.running = False
    
    """
    Starts the minecraft server
    """
    def start( self ):
        if self.running:
            sys.stderr.write( 'Error: Server already running' )
            return

        self.first_run()

        if !check_jar():
            return

        self._mcp = subprocess.Popen( 'java ' + self.arguments + ' -jar ' + self.server_jar, shell=True )
        self.running = True
        while True:
            try:
                input = sys.stdin.readline()
                if input:
                    self.send(input)
            except KeyboardInterrupt:
                self.stop()

    """
    Checks for the first run and sets up anything that needs to be set up
    """
    def first_run( self ):
        directory = os.getcwd() + '/minecraft'

        try:
            os.mkdir( directory )
        except OSError, e:
            if e.errno != errno.EEXIST:
                raise

        os.chdir( directory )

        if not os.path.exists( 'server.propertities' ):
            print "First run"
        else:
            print "Not first run"

    """
    Stops the minecraft server
    """
    def stop( self ):
        sys.stdout.write( 'Shutting down server...' )
        self._mcp.communicate( 'stop' )
        self._mcp.wait()
        self.running = False

    """
    Stops the minecraft server then exits
    """
    def quit( self, value=0):
        stop()
        sys.exit( value )

    """
    Sends a command to the minecraft server
    """
    def send( self, message ):
        self._mcp.communicate( message )

    def check_jar():
        if !os.path.exists( self.server_jar ):
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
