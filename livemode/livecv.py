import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.template
import struct
import sys
from StringIO import StringIO
import threading
import cv2
import Queue
import signal
import numpy as np
import webbrowser

quit = False
class Common:
  """Common Handler"""
  def __init__(self):
    self.last = None
    self.lasthandler = None
    self.queue = Queue.Queue(1)
  def newcode(self,x,h):
    """New code x from the handler h. Store and push in queue"""
    self.last = x
    self.lasthandler = h
    if not self.queue.empty():
      self.queue.get()
    self.queue.put(x)
  def lastcode(self):
    """Last without queue"""
    r = self.last
    self.last = None
    return r
  def lastcodewait(self):
    """Last using queue and wait"""
    return self.queue.get()
  def sendback(self,msg):
    """Send back to the websocket"""
    self.lasthandler.write_message(msg,binary=False)

    
common = Common()

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
    common.newcode(message,self)
    #self.write_message("Ok " + buffer.getvalue(),binary=False)

  def check_origin(self,origin):
    print "check origin",origin
    return True
  def on_close(self):
    print 'connection closed...'

application = tornado.web.Application([
  (r'/x', WSHandler),
  (r"/", tornado.web.RedirectHandler, {"url": "/index.html"}),
  (r"/(.*)", tornado.web.StaticFileHandler, {"path": "."}),
])

#WebSocket connection to 'ws://127.0.0.1:8000/' failed: Error during WebSocket handshake: Sent non-empty 'Sec-WebSocket-Protocol' header but no response was received
#https://github.com/gdi2290/angular-websocket/issues/13
def _server_runner(app):
  global quit
  try:
    app.listen(8000)
  except:
    quit = True
  webbrowser.open("http://localhost:8000/index.html")
  tornado.ioloop.IOLoop.instance().start()
  
def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        sys.exit(0)

def imshow(x):
  cv2.imshow("live",x)
if __name__ == "__main__":
  th = threading.Thread(target = _server_runner, args = [application])
  th.daemon = True
  th.start()
  signal.signal(signal.SIGINT, signal_handler)

  cv2.namedWindow("live",cv2.WINDOW_NORMAL)
  cv2.resizeWindow("live",640,400)
  data = {} # for holding stuff safely
  while not quit:
    cc = common.lastcode()
    # Passive wait on Queue: 1) no SIGINT, 2) hourglass over window
    #cc = common.lastcodewait()
    if cc is not None:
      buffer = StringIO()
      sys.stdout = buffer
      good = True
      try:
        exec cc
      except Exception ,e:
        common.sendback(buffer.getvalue() + "\n" + "Exception " + str(e))
        good = False
      if good:
        common.sendback("Ok " + buffer.getvalue())
      sys.stdout = sys.__stdout__
    cv2.waitKey(1)
