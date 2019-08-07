__all__ = ['Trigger', 'TAccept', 'TriggerCondition', 'AkuandubaTrigger']

from Akuanduba.core import Logger, EnumStringification, NotSet
from Akuanduba.core.messenger.macros import *
from Akuanduba.core import StatusCode, StatusTool, StatusTrigger, AkuandubaTool


class TAccept(object):

  def __init__(self):
    import collections
    self._accept = collections.OrderedDict()

  def setResult( self, key, result ):
    self._accept[key] = result

  def getResult(self, key):
    return self._accept[key]

  def getResultOrdered(self):
    return self._accept

  def passedOR(self):
    return any( [ answer for _, answer in self._accept.items() ])

  def passedAND(self):
    return all( [ answer for _, answer in self._accept.items() ])

  def clear(self):
    self._accept.clear()



class Trigger( AkuandubaTool ):

  def __init__(self, name):
    AkuandubaTool.__init__(self, name)
    import collections
    self._hypos = collections.OrderedDict()

  def __add__(self, hypo):
      self._hypos[hypo.name()] = hypo
      return self

  def initialize( self ):
    # Loop over hypos
    for key, hypo in self._hypos.items():

      if hypo.isInitialized(): continue
      MSG_INFO( self, 'Initializing hypothesis test with name: %s', key)
      hypo.setContext( self.getContext() )
      hypo.level = self._level

      if hypo.initialize().isFailure():
        MSG_FATAL( self, "Can not initialize hypothesis %s.", key)

    MSG_WARNING(self, "WARNING: This is deprecated and will be removed in the future.")

    MSG_INFO( self, "Trigger %s initialization completed.",self.name())

    self.init_lock()
    return StatusCode.SUCCESS


  def execute(self, context):

    MSG_DEBUG(self, 'Running trigger...')

    # get the system flags
    status = self.getContext().getHandler("EventStatus")

    # create the trigger object
    accept = TAccept()

    # Tools
    for key, hypo in self._hypos.items():

      MSG_DEBUG( self, "Execute hypo %s", hypo.name())

      if( hypo.execute_r( self.getContext(), accept ).isFailure() ):
        MSG_WARNING( self, "Impossible to execute %s.", tool.name())


    if not accept.passedOR():
      # stop the tool stack execution.
      MSG_DEBUG( self, "Sending stop signal for the tools stack.")
      status.forceStop()
    else:
      MSG_INFO( self, '%s triggered!',self.name())


    return StatusCode.SUCCESS


  def finalize(self):
    # Services
    for key, hypo in self._hypos.items():
      if( hypo.finalize().isFailure() ):
        MSG_WARNING( self, "Impossible to execute %s.", hypo.name())
        return StatusCode.FAILURE
    self.fina_lock()
    return StatusCode.SUCCESS

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

#
# Base class for trigger conditions
#
class TriggerCondition ( Logger ):

  # Init
  def __init__ (self, name):
    Logger.__init__(self)
    self._name = name

  # Get name
  def name (self):
    return self._name

  # Ordinary methods
  def initialize (self):
    return StatusCode.SUCCESS

  def execute (self):
    return StatusTrigger.NOT_TRIGGERED
  
  def finalize (self):
    return StatusCode.SUCCESS

#
# Main trigger class
#
class AkuandubaTrigger ( AkuandubaTool ):

  # Init
  def __init__(self, name, triggerType = 'or'):
    accepted_triggerTypes = ['or', 'and', 'xor']
    AkuandubaTool.__init__(self, name)

    import collections
    self._conditions = collections.OrderedDict()
    self._activities = collections.OrderedDict()

    if (triggerType not in accepted_triggerTypes):
      MSG_FATAL (self, "The trigger type {} is not allowed. Please change it.".format(triggerType))
    else:
      self._triggerType = triggerType

  # Redefining the __add__ method in order to ease manipulation
  def __add__(self, stuff):

    if issubclass(type(stuff), AkuandubaTool):
      self._activities[stuff.name()] = stuff
    elif issubclass(type(stuff), TriggerCondition):
      self._conditions[stuff.name()] = stuff
    else:
      MSG_ERROR(self, "Anything you add to a AkuandubaTrigger object must inherit either from AkuandubaTool or TriggerCondition")
    return self

  # Method for the "or" triggerType
  def make_or (self, answers):
    return any(answers)

  # Method for the "and" triggerType
  def make_and (self, answers):
    return all(answers)
  
  # Method for the "xor" triggerType
  def make_xor (self, answers):
    from functools import reduce
    return reduce(lambda i, j: i ^ j, answers)

  def initialize (self):

    # Initializing all activities
    for tool in [tool for _, tool in self._activities.items()]:
      if tool.isInitialized():continue
      MSG_INFO( self, 'Initializing TriggerActivity with name %s', tool.name())
      self.getContext().setHandler( tool.name() , tool )
      tool.setContext( self.getContext() )
      tool.level = self._level
      if not (tool.initialize() is StatusCode.SUCCESS):
        MSG_FATAL(self, "Couldn't initialize TriggerActivity %s.", tool.name())

    # Initializing all conditions
    for condition in [condition for _, condition in self._conditions.items()]:
      try:
        MSG_INFO (self, 'Initializing TriggerCondition with name %s', condition.name())
        if not (condition.initialize() is StatusCode.SUCCESS):
          MSG_FATAL (self, "Initialization of TriggerCondition %s didn't return SUCCESS", condition.name())
      except:
        MSG_FATAL (self, "Couldn't initialize TriggerCondition %s", condition.name())
    
    return StatusCode.SUCCESS
  
  def execute (self, context):

    # Computes answers from conditions
    answers = []
    conditions = [condition for _, condition in self._conditions.items()]
    for condition in conditions:
      answers.append(condition.execute())
    
    result = NotSet

    # Check if triggers
    if (self._triggerType == 'or'):
      result = self.make_or(answers)
    elif (self._triggerType == 'and'):
      result = self.make_and(answers)
    elif (self._triggerType == 'xor'):
      result = self.make_xor (answers)
    
    # If it triggers, than run own stack
    if (result == StatusTrigger.TRIGGERED):
      MSG_INFO (self, "{} triggered!".format(self._name))
      for tool in [tool for _, tool in self._activities.items()]:
        MSG_INFO (self, "- Executing tool {}...".format(tool.name()))
        if (tool.execute (self.getContext()).isFailure()):
          MSG_ERROR (self, "-- Failed to execute tool {}".format(tool.name()))
        
    return StatusCode.SUCCESS

  def finalize (self):

    for tool in [tool for _, tool in self._activities.items()]:
      if (tool.finalize().isFailure()):
        MSG_ERROR ( self, "Impossible to finalize tool %s.", tool.name())
        return StatusCode.FAILURE
    
    return StatusCode.SUCCESS