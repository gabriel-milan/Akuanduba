#
#   This is a sample script where a counter is controlled by the SampleTool and the SampleService prints it as
#   a warning message on every EventManager loop. The SampleTool is only triggered every 5 seconds. Besides
#   triggering this tool, the time trigger will also trigger the DataLog tool, which saves a JSON file with the
#   data from SampleDataframe.
#

# Imports
from Akuanduba.core import EventManager, LoggingLevel, Trigger
from Akuanduba.services import SampleService, StoreGateSvc
from Akuanduba.tools import SampleTool, DataLog
from Akuanduba import ToolSvc, ToolMgr
from Akuanduba.core.constants import Second
from Akuanduba.triggers import Clock
import logging

# Creating services
svc = SampleService("Sample Service Name")
storage = StoreGateSvc( "StoreGateSvc" )

# Creating tools
tool = SampleTool ("Sample Tool Name")

# Creating time trigger
trigger  = Trigger("5-second trigger")
trigger += Clock( "5-second trigger", 5 * Second )

# Creating file saver
save_file = DataLog( "File saver" )

# Creating EventManager
manager = EventManager("Akuanduba", level=logging.INFO)

# Appending services
ToolSvc += svc
ToolSvc += storage

# Appending tools
#
# ToolMgr += TOOL_1
# ToolMgr += TOOL_2
#
# Every tool appended after this trigger, will only run after it
ToolMgr += trigger
ToolMgr += tool
ToolMgr += save_file

# Initializing 
manager.initialize()
manager.execute()
manager.finalize()