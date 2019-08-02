#
#   This is a sample script where a counter is controlled by the SampleTool and the SampleService prints it as
#   a warning message on every Akuanduba loop. The SampleTool is only triggered every 5 seconds. Besides
#   triggering this tool, the time trigger will also trigger the DataLog tool, which saves a JSON file with the
#   data from SampleDataframe.
#

# Akuanduba imports
from Akuanduba.core import Akuanduba, LoggingLevel, Trigger
from Akuanduba.services import StoreGateSvc
from Akuanduba.tools import DataLog
from Akuanduba import ServiceManager, ToolManager, DataframeManager
from Akuanduba.core.constants import Second
from Akuanduba.triggers import Clock

# This sample's imports
from dataframes.SampleDataframe import *
from services.SampleService import *
from tools.SampleTool import *

# Creating services
svc = SampleService("Sample Service Name")
storage = StoreGateSvc( "StoreGateSvc" )

# Creating tools
tool = SampleTool ("Sample Tool Name")

# Creating dataframes
sampleDataframe = SampleDataframe ("SampleDataframe")

# Creating time trigger
trigger  = Trigger("5-second trigger")
trigger += Clock( "5-second trigger", 5 * Second )

# Creating file saver
save_file = DataLog( "File saver" )

# Creating Akuanduba
manager = Akuanduba("Akuanduba", level=LoggingLevel.INFO)

# Appending services
ServiceManager += svc
ServiceManager += storage

# Appending tools
#
# ToolManager += TOOL_1
# ToolManager += TOOL_2
#
# Every tool appended after this trigger, will only run after it
ToolManager += trigger
ToolManager += tool
ToolManager += save_file

# Apprending dataframes
DataframeManager += sampleDataframe

# Initializing 
manager.initialize()
manager.execute()
manager.finalize()