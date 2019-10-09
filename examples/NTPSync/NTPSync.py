#
#   This is a sample script where a counter is controlled by the SampleTool and the SampleService prints it as
#   a warning message on every Akuanduba loop. The SampleTool is only triggered every 5 seconds. Besides
#   triggering this tool, the time trigger will also trigger the DataLog tool, which saves a JSON file with the
#   data from SampleDataframe.
#

# Akuanduba imports
from Akuanduba.core import Akuanduba, LoggingLevel
from Akuanduba.services import NTPSyncService
from Akuanduba import ServiceManager

# Creating Akuanduba
manager = Akuanduba("Akuanduba", level=LoggingLevel.INFO)

# The NTP sync service
ntp = NTPSyncService("Sample Service Name")

# Appending services
ServiceManager += ntp

# Initializing 
manager.initialize()
manager.execute()
manager.finalize()