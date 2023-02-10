import nidaqmx
import time
import nidaqmx.constants as constants

# Create a Task for reading voltage
task = nidaqmx.Task()

# Add a voltage channel to the task
task.ai_channels.add_ai_voltage_chan("cDAQ9185-1F56937Mod2/ai0")

task.timing.cfg_samp_clk_timing(
    rate=1000, sample_mode=constants.AcquisitionType.FINITE,
    samps_per_chan=100
)

#task.ai_channels.add_ai_current_chan("cDAQ9185-1F56937Mod3/ai0")
task.ai_channels.add_ai_voltage_chan("cDAQ9185-1F56937Mod1/ai0")

#task.ai_channels.add_ai_current_chan("cDAQ9185-1F56937Mod3/ai0", terminal_config=nidaqmx.constants.TerminalConfiguration.DEFAULT)



# Start the task
#task.start()
while True:
    task.start()
    voltage, currentVoltage = task.read()
    #voltage, currentVoltage, current = task.read()
    print("Voltage: {:.6f} V".format(voltage))
    print("CurrentVoltage: {:.6f} V".format(currentVoltage))
    print("Current: {:.6f} A".format(currentVoltage*12.5))
    #print("actual current: {:.6f} A".format(current))
    time.sleep(0.5)
    # Stop the task
    task.stop()


# Clear the task
task.close()
