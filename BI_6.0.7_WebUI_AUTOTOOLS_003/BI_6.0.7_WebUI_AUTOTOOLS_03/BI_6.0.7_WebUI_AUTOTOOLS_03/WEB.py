__author__ = "luxu"


parm = {"number": 0}

from http.server import *
import os

def main():

    HTTPServer(("0.0.0.0", 1234), CGIHTTPRequestHandler).serve_forever()

if __name__ == "__main__":
    main()
