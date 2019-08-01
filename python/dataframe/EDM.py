__all__ = ['EDM']

from Akuanduba.core import StatusCode, Logger, NotSet
from Akuanduba.core.messenger.macros import *

class EDM(Logger):

  def __init__(self):
    Logger.__init__(self)
    self._decoration = dict()
    self._context = NotSet

  def setContext( self, context):
    self._context=context

  def getContext(self):
    return self._context

  def initialize(self):
    return StatusCode.SUCCESS

  def execute(self):
    return StatusCode.SUCCESS

  def finalize(self):
    return StatusCode.SUCCESS

  def setDecor(self, key, v):
    self._decoration[key] = v

  def getDecor(self,key):
    try:
      return self._decoration[key]
    except KeyError:
      MSG_WARNING( self, 'Decoration %s not found',key)

  def clearDecorations(self):
    self._decoration = dict()

  def decorations(self):
    return self._decoration.keys()