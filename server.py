#  coding: utf-8 
import socketserver
import os
import mimetypes

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

NEWLINE = "\r\n"


class MyWebServer(socketserver.BaseRequestHandler):

    def handle(self):
        self.data = self.request.recv(1024).strip()
        
        # PROCESS DATA TO HEADERS
        # retrieve method, path, protocol from the first line
        method,path,protocol = [part.strip() for part in self.data.splitlines()[0].decode().split()]
        if (method =="GET"):
            self.processRequest(path)
        else:
            # 405
            code = 'HTTP/1.1 405 Method not allowed' + NEWLINE
            self.request.sendall(bytearray(code,'utf-8'))
            self.request.sendall(bytearray("Connection: closed"+NEWLINE+NEWLINE,'utf-8'))
    
    def processRequest(self,path):
        ppath = "www"+path
        # header = {}

        # check unsecured path:
        if (".." not in ppath):
            if (os.path.isdir(ppath) or os.path.isfile(ppath)):
                # print("200 OK")
                if ("." not in ppath):
                    filetype ="html"
                else:
                    filetype = ppath.split(".")[-1]
                #PROCESS APPROPRIATE HEADER AND CONTENT
                code = 'HTTP/1.1 200 OK' + NEWLINE
                content_type = 'Content-Type: text/'+filetype + NEWLINE
                self.request.sendall(bytearray(code,'utf-8'))
                self.request.sendall(bytearray(content_type,'utf-8'))
                self.request.sendall(bytearray("Connection: closed"+NEWLINE+NEWLINE,'utf-8'))
            else:
                code = 'HTTP/1.1 404 Not found' + NEWLINE
                self.request.sendall(bytearray(code,'utf-8'))
                self.request.sendall(bytearray("Connection: closed"+NEWLINE+NEWLINE,'utf-8'))
        else:
            code = 'HTTP/1.1 404 Not Found' + NEWLINE
            self.request.sendall(bytearray(code,'utf-8'))
            self.request.sendall(bytearray("Connection: closed"+NEWLINE+NEWLINE,'utf-8'))

        # self.request.sendall(bytearray("OK",'utf-8'))
        

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
