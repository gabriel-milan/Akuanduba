# All list
__all__ = ["SampleDataframe"]

#
# Imports
#
# Mandatory imports
from Akuanduba.core.messenger.macros import *
from Akuanduba.core.constants import *
from Akuanduba.core import NotSet, AkuandubaDataframe
# Your imports go here:
# import WhateverYouWant

#
# Your DATAFRAME must always have inheritance from AkuandubaDataframe
#
class SampleDataframe (AkuandubaDataframe):

  #
  # Here EDMs and other stuff will not be available yet, this is just for attributes initialization and superclass init
  #
  def __init__(self, name):

    # Mandatory stuff
    AkuandubaDataframe.__init__(self, name)

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
