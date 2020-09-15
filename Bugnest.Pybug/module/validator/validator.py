#build-in modules
import serial

from time import sleep

#usr defined modules

from .nv200.exceptions import *
from .nv200.constants import *
from .nv200 import ssp_commands as ssp

class Validator(object):
    """SSP Validator"""

    def __init__(self, port_name='/dev/ttyUSB0', ssp_address=0):
        self.port_name = port_name
        self.port = None
        self.ssp_address = ssp_address

        self.stop_pending= False
    #end def

    def cancel(self):
        self.stop_pending= True

    def sale(self, on_cash_in, on_cash_stacked, on_error):
        try:
            self.port = serial.Serial(port= self.port_name,
		        baudrate= 9600,
		        bytesize= serial.EIGHTBITS,
		        stopbits= serial.STOPBITS_TWO,
		        parity= serial.PARITY_NONE,
		        timeout = 0.2)
            self.port.flush()
            self.port.flushOutput()
            self.port.flushInput()
            if ssp.exec(lambda: ssp.sync(self.port), 5) != SSP_RESPONSE_OK: raise ValidatorError('sync failed')
            if ssp.exec(lambda: ssp.enable(self.port), 5) != SSP_RESPONSE_OK: raise ValidatorError('enable failed')        
            if ssp.exec(lambda: ssp.enable_higher_protocol_events(self.port), 5) != SSP_RESPONSE_OK: raise ValidatorError('enable higher protocol events failed')
            if ssp.exec(lambda: ssp.set_inhibits(self.port, 0xFF, 0xFF), 5) != SSP_RESPONSE_OK: raise ValidatorError('set inhibits failed')
            crr_note_stacked= True
            while not self.stop_pending:
                events = ssp.exec(lambda: ssp.poll(self.port), 5)
                pevent = self.parse_poll(events)
                if pevent[0] == 'read': 
                    on_cash_in(pevent[1])
                    crr_note_stacked= False
                if pevent[0] == 'credit': 
                    on_cash_stacked(pevent[1])
                    crr_note_stacked= True

                sleep(0.2)
            
            if not crr_note_stacked:
                if ssp.exec(lambda: ssp.reject_note(self.port), 5) != SSP_RESPONSE_OK: raise ValidatorError('reject note failed')
            if ssp.disable(self.port) != SSP_RESPONSE_OK: raise ValidatorError('disable failed')
            if not self.port.closed: self.port.close()
        except Exception as e:
            on_error(e)
            if not self.port == None:
                try: ssp.exec(lambda: ssp.reject_note(self.port), 5) 
                except: pass
                if not self.port.closed: self.port.close()

        self.stop_pending= False
            
    #end def

    def parse_poll(self, events):
        for event in events:
            if event == SSP_POLL_RESET: return ('reset', None)
            if event == SSP_POLL_READ:
                if events[event] > 0: 
                    if (events[event] - 1) in (0, 1, 2, 3, 4, 5, 6, 7, 8, 9):
                        return ('read' ,events[event] - 1)
            if event == SSP_POLL_CREDIT: 
                return ('credit', events[event] - 1)
            if event == SSP_POLL_REJECTING: return ('rejecting', None)
            if event == SSP_POLL_REJECTED: return ('rejected', None)
            if event == SSP_POLL_STACKING: return ('stacking', None)
            if event == SSP_POLL_STACKED: return ('stacked', None)
            if event == SSP_POLL_SAFE_JAM: return ('safejam', None)
            if event == SSP_POLL_UNSAFE_JAM: return ('insafejam', None)
            if event == SSP_POLL_DISABLED: return ('disabled', None)
            if event == SSP_POLL_FRAUD_ATTEMPT: return ('fraudattemp', events[event])
            if event == SSP_POLL_STACKER_FULL: return ('stackerfull', None)
            if event == SSP_POLL_CASH_BOX_REMOVED: return ('cashboxremoved', None)
            if event == SSP_POLL_CASH_BOX_REPLACED: return ('cashboxreplaced', None)
            if event == SSP_POLL_CLEARED_FROM_FRONT: return ('clearedfront', None)
            if event == SSP_POLL_CLEARED_INTO_CASHBOX: return ('cleardcashbox', None)

        return (None, None)
