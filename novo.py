import nidaqmx
import time
import nidaqmx.constants as constants
import matplotlib.pyplot as plt

# Create a Task for reading voltage
task = nidaqmx.Task()

# Add a voltage channel to the task
task.ai_channels.add_ai_voltage_chan("cDAQ9185-1F56937Mod2/ai0")

task.timing.cfg_samp_clk_timing(
    rate=1000, sample_mode=constants.AcquisitionType.FINITE,
    samps_per_chan=100
)

task.ai_channels.add_ai_voltage_chan("cDAQ9185-1F56937Mod1/ai0")

voltages = []
currents = []
powers = []

# Start the task
while True:
    task.start()
    voltage, currentVoltage = task.read()
    current = currentVoltage * 12.5
    power = voltage * current
    voltages.append(voltage)
    currents.append(current)
    powers.append(power)
    print("Voltage: {:.6f} V".format(voltage))
    print("CurrentVoltage: {:.6f} V".format(currentVoltage))
    print("Current: {:.6f} A".format(current))
    print("Power: {:.6f} W".format(power))
    time.sleep(0.1)
    task.stop()

    plt.clf()
    plt.plot(voltages, label='Voltage')
    plt.plot(currents, label='Current')
    plt.plot(powers, label='Power')
    plt.legend()
    plt.pause(0.01)

# Clear the task
task.close()
