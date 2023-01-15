#  coding: utf-8 
import socketserver
import os

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

HTTP_200 = "HTTP/1.1 200 OK\n"
HTTP_301 = "HTTP/1.1 301 MOVED PERMANENTLY\n"
HTTP_400 = "HTTP/1.1 400 BAD REQUEST\n"
HTTP_404 = "HTTP/1.1 404 NOT FOUND\n"
HTTP_405 = "HTTP/1.1 405 METHOD NOT ALLOWED\n"

HTTP_mime = "Content-Type: text/html; UTF-8\n"
CSS_mime = "Content-Type: text/css; UTF-8\n"

class MyWebServer(socketserver.BaseRequestHandler):
	
	def handle(self):
		self.data = self.request.recv(1024).strip()

		if(len(self.data.split(b"\n")) == 0): #no actual request
			self.handle_400()
			return

		start_line = self.data.split(b"\n", 1)[0].strip()
		if(start_line.startswith(b"GET")):
			path = start_line[3:len(start_line) - len(" HTTP/1.1")].strip()
			directory_path = b"./www"

			if(path.startswith(b"http://")):
				path_noscheme = path[len("http://"):]
				if(path_noscheme.find("/") > 0):
					path= path[path_noscheme.find("/"):]
				else:
					self.handle_400()

			elif(path.startswith(b"/")):
				#Check if the path ends inside /www/ directory
				os.path.abspath(directory_path + path)
				if(not os.path.abspath(directory_path + path).startswith(os.path.abspath(directory_path))):				
					self.handle_404()
					return
				
				if(path.endswith(b"/")):
					try:
						file = open(directory_path + path + b"index.html", "r")
						self.request.sendall(bytearray(HTTP_200 + HTTP_mime + "\n" + file.read(), 'utf-8'))
					except:
						self.handle_404()
					return
				elif(os.path.isdir(directory_path + path)):
					location = (b"Location: " + path + b"/\n").decode('utf-8')
					self.request.sendall(bytearray(HTTP_301 + location, 'utf-8'))
				else:
					try:
						file = open(directory_path + path, "r")
						if(path.endswith(b".css")):
							self.request.sendall(bytearray(HTTP_200 + CSS_mime + "\n" + file.read(), 'utf-8'))
						elif(path.endswith(b".html")):
							self.request.sendall(bytearray(HTTP_200 + HTTP_mime + "\n" + file.read(), 'utf-8'))
						else:
							self.request.sendall(bytearray(HTTP_200 + "\n" + file.read(), 'utf-8'))
					except OSError:
						self.handle_404()
					return
			else:
				self.handle_400()	
		elif(start_line.startswith((b"HEAD", b"POST", b"PUT", b"DELETE", b"CONNECT", b"OPTIONS", b"TRACE", b"PATCH"))):
			#Throw 405 error
			self.handle_405()
		else:
			#Throw 400 error
			self.handle_400()
		#Make sure it's a proper url

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
