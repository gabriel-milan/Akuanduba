__all__ = ['StoreGateSvc']

# Mandatory imports
from Akuanduba.core import Logger, NotSet, AlgorithmSvc
from Akuanduba.core.messenger.macros import *
from Akuanduba.core.constants import *
from Akuanduba.core import StatusCode, StatusTool, StatusThread
import datetime
import time
import queue

class StoreGateSvc( AlgorithmSvc ):

  def __init__(self, name):
    # Mandatory stuff
    AlgorithmSvc.__init__(self, name)
    self._nsaves = 0

    import os
    if not os.path.exists(relative_save_dir):
        os.makedirs(relative_save_dir)


  def initialize(self):
    # Initialize thread
    super(StoreGateSvc, self).initialize()

    # Starting the thread.
    if self.start().isFailure():
      MSG_FATAL( self, "Impossible to initialize the %s service", self.name())
      return StatusCode.FAILURE

    # Lock the initialization. After that, this tool can not be initialized once again
    self.init_lock()
    return StatusCode.SUCCESS

  def execute( self, context ):
    return StatusCode.SUCCESS


  def finalize(self):
    super(StoreGateSvc,self).finalize()
    MSG_INFO( self, "Number of saved files : %d", self._nsaves )
    return StatusCode.SUCCESS



  def send( self, dobj ):
    ts=time.time()
    timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d-%H.%M.%S')
    self._put( (timestamp, dobj ) )


  def save( self, timestamp, dobj ):
    import json
    with open( relative_save_dir + timestamp+'.json', 'w') as fp:
      json.dump(dobj, fp)
      self._nsaves+=1



  def run( self ):
    while self.statusThread() is StatusThread.RUNNING:
      self.commit()
      if self._queue.qsize() > 0:
        MSG_INFO( self,  "Saving..." )
        # get the raw to be saved in json format
        timestamp, edm_list = self._get()
        d = {}
        for edm in edm_list:
          d.update(edm.toRawObj())
        self.save( timestamp, d )