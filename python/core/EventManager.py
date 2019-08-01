__all__ = ['EventManager']

from Akuanduba.core import Logger, NotSet, LoggingLevel
from Akuanduba.core.messenger.macros import *
from Akuanduba.core import StatusCode
from Akuanduba.dataframe import *
import logging
# Time import (debug purposes)
from time import time

# get the unique identification
def uniqueid():
  import random
  seed = 0
  while True:
    yield seed
    seed += 1
unique_sequence = uniqueid()


# The main framework base class for SIM analysis.
# This class is responsible to build all containers object and
# manager the storegate and histogram services for all classes.
class EventManager( Logger ):


  def __init__(self, name, level = logging.INFO):
    Logger.__init__(self, level=level)
    import collections
    self._containers = {}
    self._context = NotSet
    self._name = name


  def initialize( self ):

    MSG_INFO( self, 'Initializing EventManager...')

    # create the event context. This will be used to hold all dataframes (EDMs)
    # produced during the execution loop. Its possible to attach the thread pointers
    from Akuanduba.core import EventContext
    self._context = EventContext("EventContext")

    from Akuanduba.dataframe import EventStatus

    # Create here all dataframes
    self._containers = {
        "EventStatus"     : EventStatus(),
        "SampleDataframe" : SampleDataframe(),
    }

    # Attach all EDMs into the event context
    for key, edm in self._containers.items():
      edm.setContext(self.getContext())
      self.getContext().setHandler(key, edm)

    # Getting all services (threads)
    from Akuanduba import ToolSvc
    ToolSvc.resume()

    # Loop over services (Threading mode)
    for tool in ToolSvc.getTools():
      if tool.isInitialized(): continue
      MSG_INFO( self, 'Initializing SERVICE with name: %s', tool.name())
      self.getContext().setHandler( tool.name() , tool )
      tool.setContext( self.getContext() )
      tool.level = self._level
      if tool.initialize().isFailure():
        MSG_FATAL(self, "Can not initialize SERVICE %s.", key)

    # Getting all tools
    from Akuanduba import ToolMgr
    ToolMgr.resume()

    # Loop over tools list.
    for tool in ToolMgr.getTools():
      if tool.isInitialized():continue
      MSG_INFO( self, 'Initializing TOOL with name: %s', tool.name())
      self.getContext().setHandler( tool.name() , tool )
      tool.setContext( self.getContext() )
      tool.level = self._level
      if tool.initialize().isFailure():
        MSG_FATAL(self, "Can not initialize TOOL %s.", tool.name())

    # Checks for error in the context
    if self.getContext().initialize().isFailure():
      MSG_FATAL(self, "Can not initialize Event Context.")

    # Initialization complete
    MSG_INFO( self, "Event manager initialization completed.")
    return StatusCode.SUCCESS


  def execute(self):

    MSG_INFO( self, 'Running...')
    status = self.getContext().getHandler("EventStatus")

    from Akuanduba import ToolMgr, ToolSvc

    # For any moment, any tool can call terminate to interrupt
    # the while loop and finalize the execute method
    while not status.terminate():
      initTime = time()

      # Services
      MSG_DEBUG( self, "Starting new loop")
      for tool in ToolSvc.getTools():

        MSG_DEBUG( self, "Execute SERVICE %s...",tool.name())
        if( tool.execute( self.getContext() ).isFailure() ):
          MSG_WARNING( self, "Impossible to execute SERVICE %s.", tool.name())

        # Use interrupt to stop the tool stack execution
        if status.stop():
          MSG_DEBUG( self, "Stop stack execution.")
          # stop tool loop and reset the stop flag inside of event
          status.resetStop()
          break

      # Tools
      for tool in ToolMgr.getTools():
        MSG_DEBUG( self, "Execute TOOL %s...",tool.name())
        if( tool.execute( self.getContext() ).isFailure() ):
          MSG_WARNING( self, "Impossible to execute TOOL %s.", tool.name())

        # Use interrupt to stop the tool stack execution
        if status.stop():
          MSG_DEBUG( self, "Stop stack execution.")
          # stop tool loop and reset the stop flag inside of event
          status.resetStop()
          break

      MSG_DEBUG( self, "=== Loop time (seconds): %f ===", time() - initTime)

    MSG_INFO( self, 'Stop execute...')

    return StatusCode.SUCCESS


  def finalize(self):

    from Akuanduba import ToolSvc, ToolMgr

    # Services
    for tool in ToolSvc.getTools():
      if( tool.finalize().isFailure() ):
        MSG_WARNING( self, "Impossible to execute SERVICE %s.", tool.name())
        return StatusCode.FAILURE

    # Tools
    for tool in ToolMgr.getTools():
      if( tool.finalize().isFailure() ):
        MSG_WARNING( self, "Impossible to execute TOOL %s.", tool.name())
        return StatusCode.FAILURE

    return StatusCode.SUCCESS

  def getContext(self):
    return self._context

  def setContext(self, context):
    self._context = context