
import logging
import pandas as pd
import numpy as np
import math
from prompt_toolkit.key_binding.bindings.named_commands import self_insert
class SuperCapacitorModel():

    def __init__(self, supercapmodel):    
        self.leak_I = supercapmodel.get('leakcurrent')
        self.capacitance = supercapmodel.get('capacitance')
        self.actual_U = supercapmodel.get('initialvoltage')
        self.rated_U = supercapmodel.get('ratedvoltage')
        self.rated_I = supercapmodel.get('ratedcurrent')
        self.esr = supercapmodel.get('esr')
        self.status = SCStatus.IDLE
        ##########################################
        #do some checks on the inital parameters
        ##########################################
        if supercapmodel.get('initialvoltage') > supercapmodel.get('ratedvoltage'):
            logging.warn('Initial supercap voltage higher than allowed, defaulting to maximum voltage...')
            self.actual_U = self.rated_U
        if 'minvoltage' in supercapmodel:
            self.set_min_U(supercapmodel.get('minvoltage'))
        else:
            self.set_min_U(0.0)
        if self.actual_U < self.min_U:
            logging.warn('Initial supercap voltage lower than allowed, defaulting to minimum voltage...')
            self.actual_U = self.min_U
        ##########################################
        #initiate the voltage evolution dataframe
        ##########################################
        self.voltageseries = pd.DataFrame(columns=['Voltage'])
        self.voltageseries = self.voltageseries.append({'Voltage' : self.actual_U},ignore_index = True) # first value of the voltage series is the initial voltage
        if(self.actual_U == self.rated_U):
            self.status = SCStatus.FCHGD
        if(self.actual_U == self.min_U):
            self.status = SCStatus.FDCHGD
        ##########################################
        #calculate maximum power output
        ##########################################
        self.max_ch_P = self.rated_U * self.rated_I
        self.max_dchP = (self.rated_U ** 2) / (4*self.esr)  
        ##########################################
        # define the time resolution for the operation of the supercapacitor
        # all calculations will be done with this
        ##########################################
        self.timedelta = None        
            
    def set_timedelta(self,timedelta):
        self.timedelta = timedelta        
            
    def charge_ctP(self,ch_power):
        if ch_power > self.max_ch_P: #if the required charge current is higher than the rated current
            if self.status in {SCStatus.DCHG,SCStatus.FDCHGD,SCStatus.SFDCHG}: # if you were previously discharging or fully discharged
                self.actual_U = self.actual_U + (self.rated_I * self.esr) #do the voltage jump related to the ESR
            else: #otherwise
                self.actual_U = math.sqrt(self.actual_U **2 + (2 * self.max_dchP * self.timedelta.total_seconds() / self.capacitance)) #do a normal charge step with the maximum power
            self.status = SCStatus.CHG #and change your status to charging
        else: #if the required charge current is lower than the rated current
            if self.status in {SCStatus.DCHG,SCStatus.FDCHGD,SCStatus.SFDCHG}: #if you were previously discharging or fully discharged
                ch_I = ch_power / self.rated_U # controller always provides rated U when charging
                self.actual_U = self.actual_U + (ch_I * self.esr) # do the voltage jump related to the ESR
            else: #otherwise
                self.actual_U = math.sqrt(self.actual_U **2 + (2 * ch_power * self.timedelta.total_seconds() / self.capacitance)) #do a normal charge step with the provided power
            self.status = SCStatus.CHG #and change your status to charging
        if self.actual_U >= self.rated_U: #if the voltage at the end of the step is higher than your maximum allowed voltage
            self.actual_U =  self.rated_U #set to maximum voltage
            self.status = SCStatus.FCHGD #and set the status to fully charged
        self.voltageseries = self.voltageseries.append({'Voltage' : self.actual_U},ignore_index = True)      
    
    def charge_ctI(self, ch_I): # supercap will charge at a constant current
        if ch_I > self.rated_I: #if the required charge current is higher than the rated current
            if self.status in {SCStatus.DCHG,SCStatus.FDCHGD,SCStatus.SFDCHG}: # if you were previously discharging or fully discharged
                self.actual_U = self.actual_U + (self.rated_I * self.esr) #do the voltage jump related to the ESR
            else: #otherwise
                self.actual_U = self.actual_U + (self.rated_I * self.timedelta.total_seconds() / self.capacitance) #do a normal charge step with the maximum current
            self.status = SCStatus.CHG #and change your status to charging
        else: #if the required charge current is lower than the rated current
            if self.status in {SCStatus.DCHG,SCStatus.FDCHGD,SCStatus.SFDCHG}: #if you were previously discharging or fully discharged
                self.actual_U = self.actual_U + (ch_I * self.esr) # do the voltage jump related to the ESR
            else: #otherwise
                self.actual_U = self.actual_U + (ch_I * self.timedelta.total_seconds() / self.capacitance) #do a normal charge step with the calculated current
            self.status = SCStatus.CHG #and change your status to charging
        if self.actual_U >= self.rated_U: #if the voltage at the end of the step is higher than your maximum allowed voltage
            self.actual_U =  self.rated_U #set to maximum voltage
            self.status = SCStatus.FCHGD #and set the status to fully charged
        self.voltageseries = self.voltageseries.append({'Voltage' : self.actual_U},ignore_index = True)
    
    """
    discharge_ctP:
    will try to discharge the supercapacitor according to a certain solicited power
    If in order to output this power the supercapacitor needs to output a current HIGHER
    than it's recommended operating current, then it will discharge using this maximum current
    in order to prevent extremely high energy losses. 
    
    If it is able to output a current which is equal to or smaller than the recommended 
    operating current, then it will do so.
    
    It returns whatever power it was actually able to output, which depends on whether it uses
    the solicited power (And thus the calculated current) or the maximum current.
    """
    
    def discharge_ctP(self, try_dch_power):
        if try_dch_power > self.max_dchP: #if the calculated discharge current is higher than the supercap's recommended operational current
            if self.next_is_discharge_limit(self.max_dchP): #if the supercapacitor would be discharged by the next timestep
                true_dch_power = (self.actual_U **2 - self.min_U **2) * (self.capacitance/ (2 * self.timedelta.total_seconds())) #then calculate the maximum power you can give in this moment
                self.actual_U = self.min_U #discharging at this voltage ensures min voltage is reached by next timestep
                self.status = SCStatus.FDCHGD
            else: #if not
                if self.status in {SCStatus.CHG,SCStatus.FCHGD,SCStatus.SFDCHG}: #if previously charging, fully charged, or self-discharging
                    print("JUMPING")
                    self.actual_U = self.actual_U - (self.rated_I * self.esr) #do the voltage drop related to the ESR
                else:
                    self.actual_U = math.sqrt(self.actual_U **2 - (2 * self.max_dchP * self.timedelta.total_seconds() / self.capacitance)) #discharge using the maximum recommended current
                true_dch_power = self.max_dchP #calculate the feasible discharge power                
                self.status = SCStatus.DCHG #change status to discharging
        else: #if the discharge current is less than the maximum recommended current
            if self.next_is_discharge_limit(try_dch_power): #check again for this
                true_dch_power = (self.actual_U **2 - self.min_U **2) * (self.capacitance/ (2 * self.timedelta.total_seconds())) #*t_delta #then calculate the maximum power you can give in this moment
                self.actual_U = self.min_U # discharging at this power ensures next voltage is min voltage             
                self.status = SCStatus.FDCHGD
            else: # if not
                if self.status in {SCStatus.CHG,SCStatus.FCHGD,SCStatus.SFDCHG}: #if previously charging, fully charged, or self-discharging
                    dch_I = try_dch_power / self.actual_U
                    self.actual_U = self.actual_U - (dch_I * self.esr) #do the voltage drop related to the ESR                
                else:
                    self.actual_U = math.sqrt(self.actual_U **2 - (2 * try_dch_power * self.timedelta.total_seconds() / self.capacitance)) #discharge with the calculated current
                true_dch_power = try_dch_power #calculate the feasible discharge power, in this case equal to the "try_dch_power" solicited
                self.status = SCStatus.DCHG # change status to discharging
        if self.actual_U < self.min_U:
            self.actual_U = self.min_U
        self.voltageseries = self.voltageseries.append({'Voltage' : self.actual_U},ignore_index = True)          
        return true_dch_power    
        
    def discharge_ctI(self, dch_current):
        if dch_current > self.rated_I: #if the calculated discharge current is higher than the supercap's recommended operational current
            if self.next_is_discharge_limit(self.rated_I): #if the supercapacitor would be discharged by the next timestep
                true_dch_power = 0 #then don't discharge!
                self.status = SCStatus.FDCHGD
            else: #if not
                if self.status in {SCStatus.CHG,SCStatus.FCHGD,SCStatus.SFDCHG}: #if you were previously charging or were fully charged,
                    self.actual_U = self.actual_U - (self.rated_I * self.esr) #do the voltage drop related to the ESR
                else:
                    self.actual_U = self.actual_U - (self.rated_I * self.timedelta.total_seconds() / self.capacitance) #discharge using the maximum recommended current
                true_dch_power = self.actual_U * self.rated_I #calculate the feasible discharge power                
                self.status = SCStatus.DCHG #change status to discharging
        else: #if the discharge current is less than the maximum recommended current
            if self.next_is_discharge_limit(dch_current): #check again for this
                true_dch_power = 0 #then don't discharge!
                self.status = SCStatus.FDCHGD
            else: # if not
                if self.status in {SCStatus.CHG,SCStatus.FCHGD,SCStatus.SFDCHG}: #if you were previously charging or were fully charged,
                    self.actual_U = self.actual_U - (dch_current * self.esr) #do the voltage drop related to the ESR                
                else:
                    self.actual_U = self.actual_U - (dch_current * self.timedelta.total_seconds() / self.capacitance) #discharge with the calculated current
                true_dch_power = self.actual_U * dch_current #calculate the feasible discharge power, in this case equal to the "try_dch_power" solicited
                self.status = SCStatus.DCHG # change status to discharging
        if self.actual_U < self.min_U:
            self.actual_U = self.min_U
        self.voltageseries = self.voltageseries.append({'Voltage' : self.actual_U},ignore_index = True)          
        return true_dch_power
        
    def next_is_discharge_limit(self,power):
        if self.actual_U **2 - (2*power*self.timedelta.total_seconds() / self.capacitance)  < 0: #only true when the power demanded for 1 second cannot be provided
            return True
        else:
            return False
        
    def discharge_limit_met(self):
        self.actual_U = self.min_U
        self.status = SCStatus.FDCHGD
        
    def selfdischarge(self):
        self.status = SCStatus.SFDCHG
        self.actual_U = self.actual_U - self.leak_I * self.timedelta.total_seconds() / self.capacitance
        if (self.actual_U <= self.min_U):
            self.status = SCStatus.FDCHGD
            self.actual_U =  self.min_U
        self.voltageseries = self.voltageseries.append({'Voltage' : self.actual_U},ignore_index = True)
    
    def set_min_U(self,min_U):
        self.min_U = min_U
        
class SCStatus:
    CHG = 0x01 #charging
    DCHG = 0x02 #discharging
    SFDCHG = 0x04 #self-discharging
    FCHGD = 0x08 # fully charged
    FDCHGD = 0x10 # fully discharged
    IDLE = 0x00
    