import socket
import sys
from thread import *

class SocketServer(object):
  """A SocketServer that appends Mark Galloway to each received message"""
  
  def __init__(self, sock=None):
    if sock is None:
      self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    else:
      self.sock = sock
    print 'Socket created'


  def bind(self, host='', port=8888):
    try:
      self.sock.bind((host, port))
    except socket.error , msg:
      print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
      sys.exit()


  def listen(self, numClients=5):
    self.sock.listen(numClients)
    print 'Socket now listening'


  def serve(self):
    #now keep talking with the client
    while 1:
      # Wait to accept a connection - blocking call
      conn, addr = self.sock.accept()
      # Display client info
      print('Connected with ' + addr[0] + ':' + str(addr[1]))

      #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
      start_new_thread(self.clientthread, (conn,))

  #Function for handling connections. This will be used to create threads
  def clientthread(self, conn):
    #Sending message to connected client
    conn.send('Welcome to the server. Type something and hit enter\n') #send only takes string
     
    #infinite loop so that function do not terminate and thread does not end.
    while True:
        #Receiving from client
        data = conn.recv(1024)

        if ord(str(data).strip()[0]) == 27:
          conn.sendall("Yo, closing\n")
          conn.close()

        if data[-1] == '\n':
          data = data[:-2] # Get rid of annoying new line
        reply = data + " Mark Galloway\n"
        if not data:
          break

        conn.sendall(reply)
     

server = SocketServer()
server.bind('', 8887)
server.listen(5)
server.serve()
