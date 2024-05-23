

import logging
import time

import numpy as np

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())
import pyvisa


class BK891C():
   

    def __init__(self, resource, label = None):
        self.connect(resource, label)

    def connect(self, resource, label = None):
       
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

    def get_signal_frequency(self):
        return float(self.visaobj.query(':FREQ?'))
    def set_signal_frequency(self, freq):
        self.visaobj.write(':FREQ {}'.format(freq))

    def get_signal_rms_voltage(self):
        return float(self.visaobj.query(':LEV:AC?'))
    def set_signal_rms_voltage(self, volt):
        self.visaobj.write(':LEV:AC {}'.format(volt))

    def get_measurement_function(self):
        return self.visaobj.query(':MEAS:FUNC?')
    def set_measurement_function(self, num):
        self.visaobj.write(':MEAS:FUNC {}'.format(num))

    def get_measurement_CSQ(self):
        self.set_measurement_function(0)
        result = self.visaobj.query(':MEAS:RESU?').split(',')
        return np.array([float(result[0].strip().strip('F')), float(result[1].strip())])
    
    def get_measurement(self, num):
        self.set_measurement_function(num)
        result = self.visaobj.query(':MEAS:RESU?').split(',')
        if num == 0:
            return np.array([float(result[0].strip().strip('F')), float(result[1].strip())])
        elif num == 1:
            return np.array([float(result[0].strip().strip('F')), float(result[1].strip())])
        elif num == 2:
            return np.array([float(result[0].strip().strip('F')), float(result[1].strip().strip('ohm'))])
        elif num == 3:
            return np.array([float(result[0].strip().strip('F')), float(result[1].strip())])
        elif num == 4:
            return np.array([float(result[0].strip().strip('F')), float(result[1].strip())])
        elif num == 5:
            return np.array([float(result[0].strip().strip('F')), float(result[1].strip().strip('ohm'))])
        elif num == 6:
            return np.array([float(result[0].strip().strip('F')), float(result[1].strip().strip('S'))])
        elif num == 7:
            return np.array([float(result[0].strip().strip('H')), float(result[1].strip())])
        elif num == 8:
            return np.array([float(result[0].strip().strip('H')), float(result[1].strip())])
        elif num == 9:
            return np.array([float(result[0].strip().strip('H')), float(result[1].strip().strip('ohm'))])
        elif num == 10:
            return np.array([float(result[0].strip().strip('H')), float(result[1].strip())])
        elif num == 11:
            return np.array([float(result[0].strip().strip('H')), float(result[1].strip())])
        elif num == 12:
            return np.array([float(result[0].strip().strip('H')), float(result[1].strip().strip('ohm'))])
        elif num == 13:
            return np.array([float(result[0].strip().strip('H')), float(result[1].strip().strip('S'))])
        elif num == 14:
            return np.array([float(result[0].strip().strip('ohm')), float(result[1].strip().strip('deg'))])
        elif num == 15:
            return np.array([float(result[0].strip().strip('S')), float(result[1].strip().strip('deg'))])
        elif num == 16:
            return np.array([float(result[0].strip().strip('ohm')), float(result[1].strip().strip('ohm'))])
        elif num == 17:
            return np.array([float(result[0].strip().strip('S')), float(result[1].strip().strip('S'))])
        elif num == 18:
            return np.array(float(result[0].strip().strip('ohm')))


