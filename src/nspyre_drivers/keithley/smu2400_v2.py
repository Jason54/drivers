

import logging
import time

import numpy as np

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())
import pyvisa


class Keithley2400():


    def __init__(self, resource, label = None):
        self.connect(resource, label)

    def connect(self, resource, label = None):
        '''
        Connect to the instrument.

        Parameters:
        -----------
        resource : str
            A string containing the VISA address of the device.
        label : str
            The name of the device that will be used to label data uniquely.
        Returns:
        ----------
        N/A
        '''
        rm = pyvisa.ResourceManager()
        self.label = label

        # VisaIOError VI_ERROR_RSRC_NFOUND
        try:
          self.visaobj = rm.open_resource(resource)
        except pyvisa.VisaIOError as e:
          print(e.args)
          raise SystemExit(1)

    def get_idn(self):
        return self.visaobj.query('*IDN?')

    def set_voltage(self,voltage):
        self.visaobj.write('SOUR:VOLT {}'.format(voltage))

    def get_voltage_setpoint(self):
        return float(self.visaobj.query('SOUR:VOLT?'))

    def get_voltage(self):
        r = self.visaobj.query('MEAS:VOLT?')
        r2= r.split(",")
        r3 = [float(x) for x in r2]

        return r3[0]

    def get_output(self):
        statestring = self.visaobj.query(':OUTP:STAT?')
        if statestring == "0\n":
            return False
        if statestring == "1\n":
            return True
        #return self.visaobj.query(':OUTP:STAT?')

    def set_output(self,state):
        if state:
            self.visaobj.write(':OUTP:STAT {}'.format(1))
        else:
            self.visaobj.write(':OUTP:STAT {}'.format(0))

    def set_voltage_limit(self,voltage):
        ###self.visaobj.write(':VOLT:PROT {}'.format(voltage))
        self.visaobj.write(':SOUR:CURR:VLIM {}'.format(voltage))

    def set_voltage_range(self,voltage):
        self.visaobj.write(':SOUR:VOLT:RANG {}'.format(voltage))

    def set_current_compliance(self,curr):
        ###self.visaobj.write(':CURR:PROT {}'.format(curr))
        self.visaobj.write(':SOUR:VOLT:ILIM {}'.format(curr))
    
    def get_current(self):
        self.visaobj.write(':SENS:FUNC "CURR"')
        r= self.visaobj.query('READ?')
        ###return float(r)
        r2= r.split(",") 
        r3 = [float(x) for x in r2]
        return r3[0]
    
    ###def get_current(self):
        ###self.visaobj.write(':SENS:FUNC "CURR"')
        ###r= self.visaobj.query('READ?')
        ###r2= r.split(",")
        ###r3 = [float(x) for x in r2]
        ###return r3[1]






    """ Represents the Keithely 2400 SourceMeter and provides a
    high-level interface for interacting with the instrument.
    .. code-block:: python
        keithley = Keithley2400("GPIB::1")
        keithley.apply_current()                # Sets up to source current
        keithley.source_current_range = 10e-3   # Sets the source current range to 10 mA
        keithley.compliance_voltage = 10        # Sets the compliance voltage to 10 V
        keithley.source_current = 0             # Sets the source current to 0 mA
        keithley.enable_source()                # Enables the source output
        keithley.measure_voltage()              # Sets up to measure voltage
        keithley.ramp_to_current(5e-3)          # Ramps the current to 5 mA
        print(keithley.voltage)                 # Prints the voltage in Volts
        keithley.shutdown()                     # Ramps the current to 0 mA and disables output
    """
