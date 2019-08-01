# All list
__all__ = ["SampleDataframe"]

#
# Imports
#
# Mandatory imports
from Akuanduba.dataframe import EDM
from Akuanduba.core.messenger.macros import *
from Akuanduba.core.constants import *
from Akuanduba.core import NotSet
# Your imports go here:
# import WhateverYouWant

#
# Your DATAFRAME must always have inheritance from EDM
#
class SampleDataframe (EDM):

  #
  # Here EDMs and other stuff will not be available yet, this is just for attributes initialization and superclass init
  #
  def __init__(self):

    # Mandatory stuff
    EDM.__init__(self)

    # Initializing counter
    self.__counter = 0

  #
  # Getters and setters
  #
  def getCounter (self):
    return self.__counter

  def incrementCounter (self):
    self.__counter += 1

  #
  # "toRawObj" method is a mandatory method that delivers a dict with the desired data
  # for file saving
  #
  def toRawObj(self):
    d = {
          "CounterValue" : self.getCounter(),
          }
    return d
