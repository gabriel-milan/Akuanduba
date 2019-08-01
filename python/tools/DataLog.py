__all__ = ["DataLog"]

from Akuanduba.core import Algorithm, StatusCode, NotSet, retrieve_kw

class DataLog(Algorithm):

  def __init__(self, name, **kw):
    Algorithm.__init__(self, name)


  def initialize(self):
    self.init_lock()
    return StatusCode.SUCCESS


  def execute(self,context):

    # Getting the dataframe you want to save
    sampleDataframe = self.getContext().getHandler("SampleDataframe")

    # Getting the storage service
    storage = context.getHandler("StoreGateSvc")
    if not storage:
      MSG_ERROR(self, "There is no StoreGate into the context")
    storage.send( [sampleDataframe] )

    return StatusCode.SUCCESS

  def finalize(self):
    self.fina_lock()
    return StatusCode.SUCCESS