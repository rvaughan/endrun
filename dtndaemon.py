#!/usr/bin/env python

import dtn
import threading
import sys
import os
import errno
import time

logfile = '/var/log/dtn_transfer.log'
incoming_pipe = '/tmp/received'

logout = open(logfile, 'a')

pipeinfd = os.open(incoming_pipe, os.O_RDONLY | os.O_NONBLOCK)

def logthis(data):
  logout.write("["+time.ctime()+"] " + data + "\n");
  logout.flush()

def processBundle(filename):
  print "doing the thing!"
  logthis("Opened file " + filename +  " for processing by Natasha.")  
  dtn.receive(filename)

def listen():
  
    while 1:
      incoming = os.read(pipeinfd, 1024*10)
      
      if len(incoming) > 0:
        filename = incoming
        if ".data" in filename:
          processBundle(filename)
      else:
        time.sleep(1)

logthis("Starting up.")

listenthread = threading.Thread(target=listen)
listenthread.daemon = True
listenthread.start()