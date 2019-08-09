#
#   This is a sample script where a counter is controlled by the SampleTool and the SampleService prints it as
#   a warning message on every Akuanduba loop. The SampleTool is only triggered every 5 seconds. Besides
#   triggering this tool, the time trigger will also trigger the DataLog tool, which saves a JSON file with the
#   data from SampleDataframe.
#

# Akuanduba imports
from Akuanduba.core import Akuanduba, LoggingLevel, AkuandubaTrigger
from Akuanduba.services import StoreGateSvc
from Akuanduba.tools import DataLog
from Akuanduba import ServiceManager, ToolManager, DataframeManager
from Akuanduba.core.constants import Second
from Akuanduba.triggers import TimerCondition
from Akuanduba.core.Watchdog import Watchdog

# This sample's imports
from dataframes.SampleDataframe import *
from services.SampleService import *
from tools.SampleTool import *

# Creating services
svc = SampleService("Sample Service Name")
storage = StoreGateSvc( "StoreGateSvc" )

# Creating tools
tool = SampleTool ("Sample Tool Name")
tool_params = {
    "execute" : {
            "timeout" : 5,
            "action" : 'terminate',
    },
}
Watchdog += tool, tool_params
Watchdog.enable()

# Creating file saver (it's also a tool)
save_file = DataLog( "File saver" )

# Creating dataframes
sampleDataframe = SampleDataframe ("SampleDataframe")

# Creating time trigger
trigger  = AkuandubaTrigger("Sample Trigger Name", triggerType = 'or')

# Append conditions and tools to trigger just adding them
# Tools appended to the trigger will only run when trigger is StatusTrigger.TRIGGERED,
# and will run in the order they've been appended
trigger += TimerCondition( "5-second condition", 5 * Second )
trigger += tool
trigger += save_file

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
ToolManager += trigger

# Apprending dataframes
DataframeManager += sampleDataframe

# Initializing 
manager.initialize()
manager.execute()
manager.finalize()