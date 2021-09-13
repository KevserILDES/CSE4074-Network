from socket import *
import datetime
from sys import argv
from threading import Thread
import os,time

class RequestThread(Thread):
    def __init__(self, threadNo, connection, PORT, HOST, request_method, requesting_file):
        Thread.__init__(self)
        self.threadNo = threadNo
        self.connection = connection
        self.PORT = PORT
        self.HOST = HOST
        self.requested_method = request_method
        self.requesting_file = requesting_file
        self.header = " "
        self.response = " "
        print("New Thread created to handle a request %s at %s:%s" % (requesting_file, HOST, PORT), "\n")

    def run(self):
        type = "text/html"
        print(self.requested_method)
        if 'GET' in self.requested_method:  # check whether method equals GET
            if self.requesting_file.isdigit(): #check whether requested file is digit
                file_length = int(self.requesting_file)
                if 200000 >= file_length >= 100: #size of the requested file is between 100 and 20000 bytes
                    text = create_document(file_length)
                    self.response = "<HTML>\n<HEAD>\n<TITLE> I am " + str(file_length) + " bytes long </TITLE>\n</HEAD>\n<BODY>\n"
                    self.response += text
                    self.response += "\n</BODY>\n</HTML>\n"
                    ok_req(self, type, len(self.response)) #call ok request function for craete header for request
                else:
                    bad_req(self, type) #call bad request method if file size outside the desired size
            else:
                bad_req(self, type)  #call bad request method if requested file is not an digit
        else:
            not_impl(self, type) #call not impl method if requested method not GET

        self.header += 'Date: ' + str(datetime.datetime.now()) + '\n\n'
        # After checking all factors send the header to notify client
        final_response = self.header.encode()
        if 'HEAD' in self.requested_method: #If requested method is HEAD there is no body
            self.connection.send(final_response)
            self.connection.close()
        else:
            if isinstance(self.response, str):
                self.response = self.response.encode()
            final_response += self.response
            self.connection.send(final_response)
            self.connection.close()


#Write Bad request header
def bad_req(self, type):
    self.header = "HTTP/1.1 400 Bad Request\r\n"
    self.header += "Content-Type: %s\r\n" % type
    self.header += "Content-Length: %d\r\n" % len(str("400 Bad Request"))
    self.header += "Server: HTTPServer/1.1\r\n"
    self.response = "400 Bad Request"
    print(self.header)
    print("Thread No:", self.threadNo, "\n")
    print("----------------------------------------------------------")


#Write Ok request header
def ok_req(self, type, size):
    self.header = "HTTP/1.1 200 OK\r\n"
    self.header += "Content-Type: %s\r\n" % type
    self.header += 'Content-Length: ' + str(size) + '\r\n'
    self.header += "Server: HTTPServer/1.1\r\n"
    print(self.header)
    print("Thread No:", self.threadNo, "\n")
    print("----------------------------------------------------------")


#Write header for not implemented request method
def not_impl(self, type):
    self.header = "HTTP/1.1 501 Not Implemented\r\n"
    self.header += "Content-Type: %s\r\n" % type
    self.header += "Content-Length: %d\r\n" % len(str("501 Not Implemented"))
    self.header += "Server: HTTPServer/1.1\r\n"
    self.response = "501 Not Implemented"
    print(self.header)
    print("Thread No:", self.threadNo, "\n")
    print("----------------------------------------------------------")


#create requested document that size is determined by the requested URI
def create_document(size):
    text = ""
    filename = "./" + str(size) + ".html"
    file = open(filename, 'w+')
    content = "<HTML>\n<HEAD>\n"
    content += "<TITLE>I am " + str(size) + " bytes long</TITLE>\n</HEAD>\n<BODY>"
    text_size = size - 80 - len(str(size)) #subtract constant bytes from total size
    while text_size > 0:
        text += "a"  #fil the remaining bits with the letter 'a'
        text_size -= 1
    body = list(text)
    new_text = ""
    for i in body:
        content += i
        new_text += i
    content += "</BODY>\n</HTML>"
    file.write(content)
    file.close()
    return new_text


# Define host and take port argument
HOST_s = '127.0.0.1'
PORT_s = int(argv[1])
    
def server():
    # Setup a socket connection with client, bind it to the port and host
    my_socket = socket(AF_INET, SOCK_STREAM)
    my_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    my_socket.bind((HOST_s, PORT_s))
    my_socket.listen(5)
    requestList = []
    header = ''
    response = ''
    final_response = ''
    print("************************ HTTP Server ************************")
    print("HTTP Server running on %s using port" % HOST_s, PORT_s, "\n")
    print("----------------------------------------------------------")
    try:
        # Forever loop to accept client requests
        while True:
            connection, address = my_socket.accept()
            """print("******************** Client Details ********************")
            print("Client host name: " + str(address[0]) + "\nClient port number: " + str(address[1]))
            print("Client Host Name:", (gethostbyaddr(connection.getpeername()[0]))[0])
            print("Socket family: ",connection.family)
            print("Socket type: " , connection.type)
            print("Socket protocol: ", connection.proto)
            print("Timeout: " + str(connection.gettimeout()))
            print("********************************************************")"""
    
            request = connection.recv(1024).decode()  # get client request as 1024 bytes
            string_list = request.split('\r\n')  # Split request from lines
            request_method = string_list[0]  # get first line
            requesting_file = request_method.split()[1].lstrip('/') #leading slash from this line and reach the requested file
    
            newRequest = RequestThread(len(requestList), connection, PORT_s, HOST_s, request_method, requesting_file) #create new thread for every request
            newRequest.start() #start new request
            requestList.append(newRequest) # add every new request to request list
    
            for t in requestList:
                t.join()
    
    except KeyboardInterrupt:
        # Close socket
        my_socket.close()
        print("\nFinish")

path = "D:/Kevser/eng/sene4_dönem1/netw/project/cache"  #cache path       

#thread for proxy
class RequestThreadPr(Thread):
    def __init__(self,request, threadNo, connection, PORT_PR, HOST_PR, request_method, requesting_file,host):
        Thread.__init__(self)
        self.request=request
        self.host=host
        self.threadNo = threadNo
        self.connection = connection
        self.PORT_PR = PORT_PR
        self.HOST_PR = HOST_PR
        self.requested_method = request_method
        self.requesting_file = requesting_file
        self.header = " "
        self.response = " "
        print("New thread is created in proxy side\n")

    def run(self):
        type = "text/html"
        if 'GET' in self.requested_method:  # check whether method equals GET
            if self.requesting_file.isdigit(): #check whether requested file is digit
                file_length = int(self.requesting_file)
                if 9999<file_length:
                    long_req(self, type)
                    self.header += 'Date: ' + str(datetime.datetime.now()) + '\n\n'
                    final_response = self.header.encode()
                    if isinstance(self.response, str):
                        self.response = self.response.encode()                
                    final_response += self.response
                    self.connection.send(final_response)    #send response to client
                    self.connection.close()
                    return
        try:    #try - except to return not found when server unavailable
            server_socket = socket(AF_INET, SOCK_STREAM)    #to connnect server

            cacheTimer = time.time() - 300  #cache expire time                      
            os.chdir(path)                                     

            for cachefile in os.listdir(path):  #check time passed and remove accordingly
                st=os.stat(cachefile)
                mtime=st.st_mtime
                if mtime < cacheTimer:
                    print ("File removed: ", cachefile)
                    os.unlink(cachefile)   
                    
            odd=1
            if self.requesting_file.isdigit() and os.path.isfile(self.requesting_file):
                if int(self.requesting_file)%2==0:
                    print("The cached version is old, so receive modified response from server")
                    odd=0
            #check cache and if exists send
            if os.path.isfile(self.requesting_file) and odd==1: #for Conditional Get --if odd length not modified take from cache--
                fr = open(self.requesting_file, "r")   #open file to read                      
                cacheResponse = fr.read()   #take cached response
                self.response=cacheResponse     
                if isinstance(self.response, str):
                    self.response = self.response.encode() 
                final_response=self.response
                print("Send from cache: ",self.requesting_file,"\n")    #print info
                fr.close()
            else:   #if not in cache or modified --even length--, receive from server and add to cache 
                server_socket.connect((HOST_s,PORT_s))   #connect to server
                server_socket.send(self.request)    #send request
                response_data = server_socket.recv(4096)   #receive response
                self.response =response_data  
                final_response = self.response
                print("Received from server and added to cache: ",self.requesting_file,"\n")    #print info
                fw = open(self.requesting_file, "wb")  #add response to cache
                fw.write(final_response)
                fw.close()
            server_socket.close()
            
        except error:   #if server currently not working
            not_found(self,type)
            self.header += 'Date: ' + str(datetime.datetime.now()) + '\n\n'
            final_response = self.header.encode()
            if isinstance(self.response, str):
                self.response = self.response.encode()                
            final_response += self.response
      
        self.connection.send(final_response)    #send response to client
        self.connection.close()
        
#for proxy long request
def long_req(self,type):
    self.header = "HTTP/1.0 414 Request-URI Too Long\r\n"
    self.header += "Content-Type: %s\r\n" % type
    self.header += "Content-Length: %d\r\n" % len(str("414 Request-URI Too Long"))
    self.response = "414 Request-URI Too Long"
    print(self.header)  
    
def not_found(self,type):
    self.header = "HTTP/1.0 404 Not Found\r\n"
    self.header += "Content-Type: %s\r\n" % type
    self.header += "Content-Length: %d\r\n" % len(str("404 Not Found"))
    self.response = "404 Not Found"
    print(self.header) 
    
def proxy():

    #Define host and port 
    HOST_PR='127.0.0.1'
    PORT_PR=8888
    
    # Setup a socket connection with client, bind it to the port and host
    pr_cli_socket=socket(AF_INET, SOCK_STREAM)
    pr_cli_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    pr_cli_socket.bind((HOST_PR,PORT_PR))
    pr_cli_socket.listen(5)
    requestList = []
    print("Proxy Server running on %s using port" % HOST_PR, PORT_PR)
    try:
        # Forever loop to accept client requests
        while True:
            connection_pr, address = pr_cli_socket.accept()
            """print("******************** Proxy Client Details ********************")
            print("Client host name: " + str(address[0]) + "\nClient port number: " + str(address[1]))
            print("Client Host Name:", (gethostbyaddr(connection_pr.getpeername()[0]))[0])
            print("Socket family: ",connection_pr.family)
            print("Socket type: " , connection_pr.type)
            print("Socket protocol: ", connection_pr.proto)
            print("Timeout: " + str(connection_pr.gettimeout()))
            print("********************************************************")
            """
            try:                
                request = connection_pr.recv(4096)  # get client request
                string_list = request.decode().split('\r\n')  # Split request from lines
                request_method = string_list[0]  # get first line
                if str(PORT_s) in request_method:
                    
                    method=request_method.split(' ')[0] #get method --GET--
                    hostName=request_method.split('/')[2]   #get hostname
                    host=hostName.split(':')[0] #et host --localhost--
                    requesting_file = request_method.split('/')[3]  #get size 
                    length=requesting_file.split(' ')[0]
        
                    real_req=method+' '+'/'+requesting_file+'/'+request_method.split('/')[4]+'\r\n'   #constructing final reqeust to be send to server --URI to URL--
                    real_req+= request.decode()[request.decode().index('\n')+1:]
                    real_req=real_req.encode()
                else:   #Request is already in URL format
                    string_list = request.decode().split('\r\n')  # Split request from lines
                    request_method = string_list[0]  # get first line
                    length = request_method.split('/')[1].split(' ') [0] #get size 
        
                    real_req=request
                
                newRequest = RequestThreadPr(real_req,len(requestList), connection_pr, PORT_PR, HOST_PR, request_method, length,host)   #new thread for every request
                newRequest.start()
                requestList.append(newRequest)
    
                for request in requestList:
                    request.join()
            except:
                continue

    except KeyboardInterrupt:
        # Close socket
        pr_cli_socket.close()
        print("\nFinish")    

if __name__=='__main__':
    t1=Thread(target=proxy)
    t2=Thread(target=server)
    t1.start()
    t2.start()
     