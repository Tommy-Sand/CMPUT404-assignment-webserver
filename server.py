#  coding: utf-8 
import socketserver

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#	 http://www.apache.org/licenses/LICENSE-2.0
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

HTTP_200 = """HTTP/1.1 200 OK\n\n"""
HTTP_301 = "HTTP/1.1 301 MOVED PERMANENTLY\n"
HTTP_400 = "HTTP/1.1 400 BAD REQUEST\n"
HTTP_404 = "HTTP/1.1 404 NOT FOUND\n"
HTTP_405 = "HTTP/1.1 405 METHOD NOT ALLOWED\n"

class MyWebServer(socketserver.BaseRequestHandler):
	
	def handle(self):
		self.data = self.request.recv(1024).strip()
		print ("Got a request of: %s\n" % self.data)
		if(len(self.data.split(b"\n")) == 0): 
			#Throw 400 error
			self.handle_400()
			return
		start_line = self.data.split(b"\n", 1)[0].strip()
		if(start_line.startswith(b"GET")):
			#Can proceed
			path = start_line[3:len(start_line) - 9].strip()
			print(path)
			directory_path = b"./www"
			print("Can proceed")
			#absolute path
			if(path.startswith(b"/")):
				if(path == b"/" or path == b"/index.html"):
					#Serve ./www/index.html
					file = open("./www/index.html", "r")
					self.request.sendall(bytearray(HTTP_200 + file.read(), 'utf-8'))
				elif(path == b"/base.css"):
					#Serve ./www/base.css
					directory_path += path 
					file = open(directory_path, "r")
					self.request.sendall(bytearray(HTTP_200 + file.read(), 'utf-8'))
				elif(path == b"/deep/" or path == b"/deep/index.html"):
					#Serve ./www/deep/index.html
					directory_path += path
					file = open("./www/deep/index.html", "r")
					self.request.sendall(bytearray(HTTP_200 + file.read(), 'utf-8'))
				elif(path == b"/deep/deep.css"):
					#Serve ./www/deep/base.css
					file = open("./www/deep/deep.css", "r")
					self.request.sendall(bytearray(HTTP_200 + file.read(), 'utf-8'))
				else:
					self.handle_404()
			#complete URL
			elif(path.startswith(b"http://")):
				pass
		elif(start_line.startswith((b"HEAD", b"POST", b"PUT", b"DELETE", b"CONNECT", b"OPTIONS", b"TRACE", b"PATCH"))):
			#Throw 405 error
			self.handle_405()
		else:
			#Throw 400 error
			self.handle_400()
		#Make sure it's a proper url
			#If the url is http://127.0.0.1:8080/
		#self.request.sendall(bytearray(HTTP_200,'utf-8'))

	def handle_400(self):
		ERROR = "\nBad Request\n"
		self.request.sendall(bytearray(HTTP_400 + ERROR, 'utf-8'))

	def handle_404(self):
		ERROR = "\nNo such page exists\n"
		self.request.sendall(bytearray(HTTP_404 + ERROR, 'utf-8'))

	def handle_405(self):
		ERROR = "\nAllow: GET\n"
		self.request.sendall(bytearray(HTTP_405 + ERROR, 'utf-8'))

if __name__ == "__main__":
	HOST, PORT = "localhost", 8080

	socketserver.TCPServer.allow_reuse_address = True
	# Create the server, binding to localhost on port 8080
	server = socketserver.TCPServer((HOST, PORT), MyWebServer)

	# Activate the server; this will keep running until you
	# interrupt the program with Ctrl-C
	server.serve_forever()
