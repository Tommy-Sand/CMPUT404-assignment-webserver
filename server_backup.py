#  coding: utf-8 
import socketserver

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/

HTTP_200 = """HTTP/1.1 200 OK

HELLO WORLD!"""
HTTP_301 = "HTTP/1.1 301 MOVED PERMANENTLY\n"
HTTP_404 = "HTTP/1.1 404 NOT FOUND\n"
HTTP_405 = "HTTP/1.1 405 METHOD NOT ALLOWED\n"

class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
		#Make sure it's a get request
        if(len(self.data.split(b"\n")) == 0): 
            #Send 404 error
            print("404 error")
        start_line = self.data.split(b"\n", 1)[0].strip()
        if(start_line.startswith(b"GET")):
            #Can proceed
            print("Can proceed")
        elif(start_line.startswith((b"HEAD", b"POST", b"PUT", b"DELETE", b"CONNECT", b"OPTIONS", b"TRACE", b"PATCH"))):
            #Throw 405 error
            print("Cannot proceed")
            ERROR = "\nAllow: GET"
            self.request.sendall(bytearray(HTTP_405 + ERROR, 'utf-8'))
        else:
            #Throw 404 error
            print("404 Error")
        #Make sure it's a proper url
            #If the url is http://127.0.0.1:8080/
        self.request.sendall(bytearray(HTTP_200,'utf-8'))

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
