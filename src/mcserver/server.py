import os, errno
import sys
import subprocess

class Server:
    
    """
    Starts the minecraft server
    """
    def start( self ):
        self.first_run()

        subprocess.Popen( 'sleep 20 && echo done', shell=True )
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

    """
    Stops the minecraft server
    """
    def stop( self, value=0 ):
        sys.stdout.write( 'Shutting down server...' )
        sys.exit( value )

    """
    Sends a command to the minecraft server
    """
    def send( self, message ):
        sys.stdout.write( message )

if __name__ == "__main__":
    server = Server()
    server.start()
