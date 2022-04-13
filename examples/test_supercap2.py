from supercap import SuperCapacitorModel
import datetime as dtt
from matplotlib import pyplot as plt
import numpy as np

def main():
	#initialize capacitor-1 with its nameplate details
	mysupercap1 = {
		'leakcurrent' : 500e-4*3, #in A
		'capacitance' : 300, # in F
		'ratedcurrent' : 30, # in A
		'initialvoltage' : 0, # in V
		'ratedvoltage' : 70, # in V
		'esr' : 0.55*3 # in ohms
		}
	#initialize capacitor-2 with its nameplate details	
	mysupercap2 = {
		'leakcurrent' : 500e-4*3, #in A
		'capacitance' : 300, # in F
		'ratedcurrent' : 30, # in A
		'initialvoltage' : 20, # in V
		'ratedvoltage' : 70, # in V
		'esr' : 0.55*3 # in ohms
		}
	#initialize capacitor-2 with its nameplate details	
	mysupercap3 = {
		'leakcurrent' : 500e-4*3, #in A
		'capacitance' : 300, # in F
		'ratedcurrent' : 30, # in A
		'initialvoltage' : 10, # in V
		'ratedvoltage' : 70, # in V
		'esr' : 0.55*3 # in ohms
		}

	#The following lines allow to generate a test charge and discharge process for the supercapacitor2
	testsc = SuperCapacitorModel(mysupercap1)
	 
	testsc.set_timedelta(dtt.timedelta(seconds=1))
	 
	for i in range(0,250):
		testsc.charge_ctI(2)
	#for i in range(0,50):
	#	testsc.selfdischarge()
	#for i in range(0,250):
	#	testsc.discharge_ctI(3) 
		   
	plt.plot(testsc.voltageseries,label='Python',linewidth=2)

	x, y = np.loadtxt('2A_charge.csv', delimiter=',', unpack=True)
	plt.plot(x,y,label='Matlab')
	ymin, ymax = min(y), max(y)
	plt.ylim(0, 1.3 * ymax)
	plt.legend(loc="best")
	plt.xlabel('Time [s]')
	plt.ylabel('Voltage [V]')
	plt.show(block=True)
	
	#The following lines allow to generate a test charge and discharge process for the supercapacitor1
	testsc2 = SuperCapacitorModel(mysupercap2)
	 
	testsc2.set_timedelta(dtt.timedelta(seconds=1))
	 
	for i in range(0,1):
		testsc2.charge_ctI(2)
	#for i in range(0,50):
	#	testsc2.selfdischarge()
	for i in range(0,200):
		testsc2.discharge_ctI(3) 
		   
	plt.plot(testsc2.voltageseries,label='Python',linewidth=3)
	x, y = np.loadtxt('3A_discharge.csv', delimiter=',', unpack=True)
	plt.plot(x,y,label='Matlab')
	ymin, ymax = min(y), max(y)
	plt.ylim(0, 1.05 * ymax)
	plt.legend(loc="best")
	plt.xlabel('Time [s]')
	plt.ylabel('Voltage [V]')
	plt.show(block=True)  
	
	#The following lines allow to generate a test charge and discharge process for the supercapacitor1
	testsc3 = SuperCapacitorModel(mysupercap3)
	 
	testsc3.set_timedelta(dtt.timedelta(seconds=1))
	 
	#for i in range(0,250):
	#	testsc2.charge_ctI(2)
	for i in range(0,50):
		testsc3.selfdischarge()
	#for i in range(0,200):
	#	testsc2.discharge_ctI(3) 
		   
	plt.plot(testsc3.voltageseries,label='Python',linewidth=3)
	x, y = np.loadtxt('Selfdischarge.csv', delimiter=',', unpack=True)
	plt.plot(x,y,label='Matlab')
	ymin, ymax = min(y), max(y)
	plt.ylim(4, 1.1 * ymax)
	plt.legend(loc="best")
	plt.xlabel('Time [s]')
	plt.ylabel('Voltage [V]')
	plt.show(block=True)  
	
main()

