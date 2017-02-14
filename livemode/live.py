import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.template
import struct
import sys
from StringIO import StringIO
import threading

    
class WSHandler(tornado.websocket.WebSocketHandler):
  def open(self):
    self.set_nodelay(True)
    self.write_message("The server says: 'Hello'. Connection was accepted.")

  def select_subprotocol(self,protocols):
    print "protocols",len(protocols),protocols
    if len(protocols) > 0:
      return protocols[0]
    else:
      return 
  def on_message(self, message):
    # FUTURE:
    #  push in main thread queue
    #  let it execute
    #  respond with error once
    print "got<",message,">"
    buffer = StringIO()
    sys.stdout = buffer
    try:
      exec message
    except Exception ,e:
      self.write_message("Exception " + str(e),binary=False)
      return
    sys.stdout = sys.__stdout__
    self.write_message("Ok " + buffer.getvalue(),binary=False)

  def check_origin(self,origin):
    print "check origin",origin
    return True
  def on_close(self):
    print 'connection closed...'

application = tornado.web.Application([
  (r'/x', WSHandler),
  (r"/", web.RedirectHandler, {"url": "/index.html"}),
  (r"/(.*)", tornado.web.StaticFileHandler, {"path": "."}),
])

#WebSocket connection to 'ws://127.0.0.1:8000/' failed: Error during WebSocket handshake: Sent non-empty 'Sec-WebSocket-Protocol' header but no response was received
#https://github.com/gdi2290/angular-websocket/issues/13
def _server_runner(app):
  print "started"
  app.listen(8000)
  tornado.ioloop.IOLoop.instance().start()
  
if __name__ == "__main__":
  th = threading.Thread(target = _server_runner, args = [application])
  th.daemon = True
  th.start()

  ev = threading.Event()
  ev.clear()
  try:
      # some non-blocking looping in main thread
      while not ev.isSet():
          print "Main loop"
          ev.wait(30)
  except KeyboardInterrupt:
      pass

  print "good bye"
