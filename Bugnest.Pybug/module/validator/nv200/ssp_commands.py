from .ssp_packet import send, compile, decompile
from .constants import *
from ctypes import *

def exec(proc, retry):
    for i in range(0, retry):
        try:
            resp= proc()
            return resp
        except Exception as e:
            if i >= retry: pass

def sync(port, ssp_address= 0):
    cmd_data= [SSP_CMD_SYNC]
    tx_data= compile(cmd_data, ssp_address)
    rx_data= send(tx_data, port, ssp_address)
    rep_data= decompile(rx_data, ssp_address)

    return rep_data[0]

def enable(port, ssp_address=0):
    cmd_data= [SSP_CMD_ENABLE]
    tx_data= compile(cmd_data, ssp_address)
    rx_data= send(tx_data, port, ssp_address)
    rep_data= decompile(rx_data, ssp_address)

    return rep_data[0]

def disable(port, ssp_address=0):
    cmd_data= [SSP_CMD_DISABLE]
    tx_data= compile(cmd_data, ssp_address)
    rx_data= send(tx_data, port, ssp_address)
    rep_data= decompile(rx_data, ssp_address)

    return rep_data[0]

def enable_higher_protocol_events(port, ssp_address=0):
    cmd_data= [SSP_CMD_ENABLE_HIGHER_PROTOCOL]
    tx_data= compile(cmd_data, ssp_address)
    rx_data= send(tx_data, port, ssp_address)
    rep_data= decompile(rx_data, ssp_address)

    return rep_data[0]

def set_inhibits(port, lowchannels, highchannels, ssp_address=0):
    cmd_data= [SSP_CMD_SET_INHIBITS, lowchannels, highchannels]
    tx_data= compile(cmd_data, ssp_address)
    rx_data= send(tx_data, port, ssp_address)
    rep_data= decompile(rx_data, ssp_address)

    return rep_data[0]

def reject_note(port, ssp_address=0):
    cmd_data= [SSP_CMD_REJECT_NOTE]
    tx_data= compile(cmd_data, ssp_address)
    rx_data= send(tx_data, port, ssp_address)
    rep_data= decompile(rx_data, ssp_address)

    return rep_data[0]

def poll(port, ssp_address=0):
    retries= 0
    cmd_data= [SSP_CMD_POLL]
    tx_data= compile(cmd_data, ssp_address)
    rx_data= send(tx_data, port, ssp_address)
    rep_data= decompile(rx_data, ssp_address)

    events= {}
    if rep_data[0] == SSP_RESPONSE_OK:
        i=1
        while i< len(rep_data):
            if rep_data[i] in (
                SSP_POLL_CREDIT,
                SSP_POLL_FRAUD_ATTEMPT,
                SSP_POLL_READ,
                SSP_POLL_CLEARED_FROM_FRONT,
                SSP_POLL_CLEARED_INTO_CASHBOX):

                events[rep_data[i]]= rep_data[2]

            elif rep_data[i] in (
                SSP_POLL_DISPENSING,
                SSP_POLL_DISPENSED,
                SSP_POLL_JAMMED,
                SSP_POLL_HALTED,
                SSP_POLL_FLOATING,
                SSP_POLL_FLOATED,
                SSP_POLL_TIMEOUT,
                SSP_POLL_INCOMPLETE_PAYOUT,
                SSP_POLL_INCOMPLETE_FLOAT,
                SSP_POLL_CASHBOX_PAID,
                SSP_POLL_COIN_CREDIT):

                events[rep_data[i]]= 0
                for j in range(0, 4):
                    i+=1
                    events[rep_data[i]]+= c_ulong((c_ulong(rep_data[i]).value) << (8 * i)).value
            else:
                events[rep_data[i]]= 0
            i+=1
        
        return events
    return None