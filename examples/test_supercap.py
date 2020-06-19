from supercap import SuperCapacitorModel
import datetime as dtt
from matplotlib import pyplot as plt


def main():
	#initialize capacitor-1 with its nameplate details
	mysupercap1 = {
		'leakcurrent' : 500e-4*3, #in A
		'capacitance' : 40*3, # in F
		'ratedcurrent' : 10*3, # in A
		'initialvoltage' : 70*3, # in V
		'ratedvoltage' : 70*3, # in V
		'esr' : 0.55*3 # in ohms
		}
	#initialize capacitor-2 with its nameplate details	
	mysupercap2 = {
		'leakcurrent' : 400e-4*3, #in A
		'capacitance' : 60*3, # in F
		'ratedcurrent' : 15*3, # in A
		'initialvoltage' : 40*3, # in V
		'ratedvoltage' : 75*3, # in V
		'esr' : 0.55*3 # in ohms
		}

	#The following lines allow to generate a test charge and discharge process for the supercapacitor2
	testsc = SuperCapacitorModel(mysupercap2)
	 
	testsc.set_timedelta(dtt.timedelta(seconds=1))
	 
	for i in range(0,1000):
		testsc.charge_ctP(100)
	for i in range(0,500):
		testsc.selfdischarge()
	for i in range(0,1500):
		testsc.discharge_ctP(100) 
	for i in range(0,1000):
		testsc.charge_ctI(2)
	for i in range(0,75):
		testsc.selfdischarge()
	for i in range(0,1000):
		testsc.discharge_ctI(3) 
		   
	plt.plot(testsc.voltageseries)
	plt.xlabel('Time [s]')
	plt.ylabel('Voltage [V]')
	#plt.show(block=True)  
	
	#The following lines allow to generate a test charge and discharge process for the supercapacitor1
	testsc2 = SuperCapacitorModel(mysupercap2)
	 
	testsc2.set_timedelta(dtt.timedelta(seconds=1))
	 
	for i in range(0,1000):
		testsc2.charge_ctP(100)
	for i in range(0,70):
		testsc2.selfdischarge()
	for i in range(0,1200):
		testsc2.discharge_ctP(100) 
	for i in range(0,1000):
		testsc2.charge_ctI(2)
	for i in range(0,70):
		testsc2.selfdischarge()
	for i in range(0,1000):
		testsc2.discharge_ctI(3) 
		   
	plt.plot(testsc2.voltageseries)
	plt.xlabel('Time [s]')
	plt.ylabel('Voltage [V]')
	plt.show(block=True)  
	
main()

