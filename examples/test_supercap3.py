from supercap import SuperCapacitorModel
import datetime as dtt
from matplotlib import pyplot as plt


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
	# mysupercap2 = {
		# 'leakcurrent' : 0.0002, #in A
		# 'capacitance' : 150, # in F
		# 'ratedcurrent' : 113, # in A
		# 'initialvoltage' : 0, # in V
		# 'ratedvoltage' : 3, # in V
		# 'esr' : 0.0065 # in ohms
		# }

	#The following lines allow to generate a test charge and discharge process for the supercapacitor2
	testsc = SuperCapacitorModel(mysupercap1)
	 
	testsc.set_timedelta(dtt.timedelta(seconds=10))
	
	t_charge_cp=1000
	t_selfdischarge_cp=300
	t_discharge_cp=1200
	t_charge_cc=800
	t_selfdischarge_cc=200
	t_discharge_cc=1000
	for i in range(0,t_charge_cp):
		testsc.charge_ctP(100)
	for i in range(0,t_selfdischarge_cp):
		testsc.selfdischarge()
	for i in range(0,t_discharge_cp):
		testsc.discharge_ctP(150) 
	for i in range(0,t_charge_cc):
		testsc.charge_ctI(2)
	for i in range(0,t_selfdischarge_cc):
		testsc.selfdischarge()
	for i in range(0,t_discharge_cc):
		testsc.discharge_ctI(3) 
		   
	plt.plot(testsc.voltageseries,label='Capacitor-1')

	
	#The following lines allow to generate a test charge and discharge process for the supercapacitor1
	# testsc2 = SuperCapacitorModel(mysupercap2)
	 
	# testsc2.set_timedelta(dtt.timedelta(seconds=1))
	 
	# for i in range(0,1000):
		# testsc2.charge_ctP(100)
	# for i in range(0,200):
		# testsc2.selfdischarge()
	# for i in range(0,800):
		# testsc2.discharge_ctP(100) 
	# for i in range(0,1000):
		# testsc2.charge_ctI(2)
	# for i in range(0,200):
		# testsc2.selfdischarge()
	# for i in range(0,800):
		# testsc2.discharge_ctI(3) 
		   
	# plt.plot(testsc2.voltageseries,label='Capacitor-2')
	plt.axvspan(0, t_charge_cp, color='red', alpha=0.1)
	plt.axvspan(t_charge_cp, t_charge_cp+t_selfdischarge_cp, color='green', alpha=0.1)
	plt.axvspan(t_charge_cp+t_selfdischarge_cp, t_charge_cp+t_selfdischarge_cp+t_discharge_cp, color='blue', alpha=0.1)
	plt.axvspan(t_charge_cp+t_selfdischarge_cp+t_discharge_cp, t_charge_cp+t_selfdischarge_cp+t_discharge_cp+t_charge_cc, color='red', alpha=0.1)
	plt.axvspan(t_charge_cp+t_selfdischarge_cp+t_discharge_cp+t_charge_cc, t_charge_cp+t_selfdischarge_cp+t_discharge_cp+t_charge_cc+t_selfdischarge_cc, color='green', alpha=0.1)
	plt.axvspan(t_charge_cp+t_selfdischarge_cp+t_discharge_cp+t_charge_cc+t_selfdischarge_cc, t_charge_cp+t_selfdischarge_cp+t_discharge_cp+t_charge_cc+t_selfdischarge_cc+t_discharge_cc, color='blue', alpha=0.1)
	plt.legend(loc="best")
	plt.xlabel('Time [s]')
	plt.ylabel('Voltage [V]')
	plt.show(block=True)  
	
main()

