__all__ = ['SampleService']

# Mandatory imports
from Akuanduba.core import Logger, NotSet, AkuandubaService
from Akuanduba.core.messenger.macros import *
from Akuanduba.core.constants import *
from Akuanduba.core import StatusCode, StatusTool, StatusThread
# Your own imports go here:
# import WhateverYouWant

#
# Your SERVICE must always have inheritance from AkuandubaService
#
class SampleService( AkuandubaService ):

  #
  # Here EDMs and other stuff will not be available yet, this is just for attributes initialization and superclass init
  #
  def __init__(self, name):

    # Mandatory stuff
    AkuandubaService.__init__(self, name)

    # Attributes initialization
    self.__thisCounter = 0

  #
  # At this point, the context will be set and all EDMs, services and tools will already be attached to it
  # If you need to get anything from context to set something on this service's initialization, this is the time
  #
  def initialize(self):

    # Initialize thread, as every service runs as a thread
    super(SampleService, self).initialize()
    if self.start().isFailure():
      MSG_FATAL( self, "Impossible to initialize the %s service", self.name())
      return StatusCode.FAILURE

    # Lock the initialization. After that, this tool can not be initialized once again
    self.init_lock()
    return StatusCode.SUCCESS

  #
  # This method will run once every Akuanduba loop only. Use this to get the data you want from context, process it
  # and store it on another dataframe or whatever you wanna do.
  #
  def execute( self, context ):

    # On this example, I'll only put a Warning message with the value of the counter I got from the context
    sampleDataframe = self.getContext().getHandler("SampleDataframe")
    MSG_WARNING(self, sampleDataframe.getCounter())

    # Always return SUCCESS
    return StatusCode.SUCCESS

  #
  # This will call finalization for this service
  #
  def finalize(self):

    super(SampleService,self).finalize()

    # Always return SUCCESS
    return StatusCode.SUCCESS

  #
  # The "run" method runs on separated threads, here you can get data and store it to the Akuanduba queue.
  # Access to context is not recommended here, since it could break the data for the "execute" loop.
  #
  def run( self ):

    # This is the main loop for the thread, do everything inside this
    while self.statusThread() is StatusThread.RUNNING:

      # Your code here (remove this pass after)
      pass