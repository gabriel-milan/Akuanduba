__all__ = ["ToolSvc", "ToolMgr"]

from Akuanduba.core.messenger import Logger
from Akuanduba.core.messenger.macros import *
from Akuanduba.core import Algorithm, AlgorithmSvc

class Service( Logger ):

  def __init__(self, name, isMgr=False):
    Logger.__init__(self)
    import collections
    self._name = name
    self._isMgr = isMgr
    self._tools = collections.OrderedDict()
    MSG_INFO( self, "Creating %s as Service...", name)

  def name(self):
    return self._name

  def get(self, name):
    return self._tools[name]

  def put(self, tool):
    self._tools[ tool.name() ] =  tool

  def __iter__(self):
    for name, tool in self._tools.iteritems():
      yield tool

  def disable(self):
    for name, tool in self._tools.iteritems():
      MSG_DEBUG( self, "Disable %s tool", name)
      tool.disable()

  def enable(self):
    for name, tool in self._tools.iteritems():
      MSG_DEBUG( self, "Enable %s tool", name)
      tool.enable()

  def push_back(self, tool):
    if self._isMgr:
      if not issubclass(type(tool),Algorithm):
        MSG_FATAL( self, "This tool must have inheritance from Algorithm. Is this a service?")
    else: # is service (in thread mode)
     if not issubclass(type(tool),AlgorithmSvc):
      MSG_FATAL( self, "This tool must have inheritance from AlgorithmSvc. Is this a service?")
    if not tool.name() in self._tools.keys():
      self._tools[tool.name()] = tool
    else:
      MSG_FATAL(self, "Tool %s already exist into the tool service list. Please include this tool with another name...")

  def __add__(self, tool):
    self.push_back( tool )
    return self

  def clear(self):
    self._tools.clear()

  def resume(self):
    MSG_INFO( self, "Service: %s", self.name())
    for name, tool in self._tools.items():
      MSG_INFO( self, " * %s as tool", tool.name())

  def getTools(self):
    return [ tool for _, tool in self._tools.items() ]

  def retrieve( self, key ):
    if key in self._tools.keys():
      return self._tools[key]
    else:
      MSG_ERROR( self, "Tool with name %s not found in the tool service", key)


# Use this to attach all tools
ToolSvc = Service("ToolSvc")

# Use this to attach all event loop manager
ToolMgr = Service("ToolMgr", True)