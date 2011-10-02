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
