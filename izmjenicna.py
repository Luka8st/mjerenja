import nidaqmx
import time
import numpy as np
import nidaqmx.constants as constants
from matplotlib import pyplot as plt

# Create a Task for reading voltage
task = nidaqmx.Task()

# Add a voltage channel to the task
task.ai_channels.add_ai_voltage_chan("cDAQ9185-1F56937Mod2/ai0")
#task.ai_channels.add_ai_voltage_chan("cDAQ9185-1F56937Mod1/ai0")
task.ai_channels.add_ai_voltage_chan("cDAQ9185-1F56937Mod2/ai1")
task.ai_channels.add_ai_voltage_chan("cDAQ9185-1F56937Mod2/ai2")


signal_freq = 50
samples_per_period = 40
number_of_periods = 5
samples_per_ch = samples_per_period * number_of_periods
sample_rate = signal_freq * samples_per_period

if sample_rate < 2000 or sample_rate > 50000:
    print(1 / 0)

task.timing.cfg_samp_clk_timing(
    rate=sample_rate, sample_mode=constants.AcquisitionType.FINITE,
    samps_per_chan=samples_per_ch
)

# def phase_difference_for_single_values(voltage, current):
#     # Calculate the cross power spectral density (CPSD)
#     CPSD = np.mean(voltage * np.conj(current))
#     # Calculate the phase difference in radians
#     phase_diff = np.angle(CPSD)
#     return phase_diff


def phase_difference(voltage, current):
    # Ensure that voltage and current have the same length
    if len(voltage) != len(current):
        raise ValueError("Voltage and current arrays must have the same length.")

    # Calculate the cross power spectral density (CPSD)
    CPSD = np.sum(voltage * np.conj(current))/len(voltage)
    #print(f'cpsd={CPSD}')
    
    # Calculate the phase difference in radians
    #phase_diff = np.angle(CPSD)
    phase_diff = np.deg2rad(CPSD)
    #print(f'phase={phase_diff/np.pi} pi')
    
    return phase_diff

def convert(list):
    returnList = []
    for i in list:
        returnList.append(i * 12.5)
    print(returnList)
    return returnList

def subtract(list1, list2):
    returnList = []

    print(len(list1))

    for i in range(samples_per_ch):
        returnList.append(list1[i] - list2[i])
    print(returnList)
    return returnList


voltage_data = []
current_data = []


while True:
    task.start()

    voltage, currentVoltage1, currentVoltage2 = task.read(number_of_samples_per_channel=samples_per_ch)

    currentVoltage = subtract(currentVoltage1, currentVoltage2)

    current = convert(currentVoltage)
    print(f'voltage:{voltage}')
    print(f'currentV:{currentVoltage}')
    voltage_data.extend(voltage)
    current_data.extend(current)

    voltageSqr = [a**2 for a in voltage]
    currentSqr = [a**2 for a in current]
    effVolt = np.sqrt(sum(voltageSqr) / len(voltage))
    effCurrent = np.sqrt(sum(currentSqr) / len(current))
    print("================================================================")
    print("Struja: {:.6f} A".format(effCurrent))
    print("Napon: {:.6f} V".format(effVolt))

    # volt_zero_crossings = np.where(np.diff(np.sign(voltage)))[0]
    # curr_zero_crossings = np.where(np.diff(np.sign(current)))[0]
    # print(volt_zero_crossings)
    # print(curr_zero_crossings)
    phi = phase_difference(voltage, current)
    print(f'Phase diff: {phi} rad')

    djelatna = effVolt * effCurrent * np.cos(phi)
    jalova = effVolt * effCurrent * np.sin(phi)
    ukupnaSnaga = effVolt * effCurrent
    faktorSnage = np.cos(phi)

    print(f'Djelatna snaga (P): {djelatna} W')
    print(f'Jalova snaga (Q): {jalova} VAR')
    print(f'Ukupna snaga (S): {ukupnaSnaga} VA')
    print(f'Faktor snage: {faktorSnage}')
    print(f'Frekvencija signala: {signal_freq} Hz')


    plt.clf()
    plt.title('Acquired Data')
    plt.plot(voltage, label="Napon")
    plt.plot(current, label="Struja")
    # plt.plot(djelatna, label="Djelatna snaga")
    # plt.plot(jalova, label="Jalova snaga")
    # plt.plot(ukupnaSnaga, label="Ukupna snaga")
    # plt.plot(faktorSnage, label="Faktor snage")
    plt.legend()
    plt.pause(1)

    task.stop()

# Clear the task
task.close()






