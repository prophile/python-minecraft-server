#!/usr/bin/python3

from pycraft import server
import sys

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        if sys.argv[1] == "-d":
            s = server.Server()
        else:
            s = server.Server( message = sys.argv[1] )
    else:
        print( "That's not how you use this program!!" )
