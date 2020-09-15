from .constants import *
from .cypher import *
from time import sleep

ssp_seq = [chr(0) for i in range(0, 255)]

def compile(cmd_data, ssp_address):
	tx_buffer_length = len(cmd_data) + 5
	tx_data = [chr(0) for i in range(0, tx_buffer_length)]

	tx_data[0] = cmd_data[0]
	if cmd_data[0] == SSP_CMD_SYNC:
		ssp_seq[ssp_address] = 0x80

	tx_data[0] = SSP_STX
	tx_data[1] = ssp_address | ssp_seq[ssp_address]
	tx_data[2] = len(cmd_data)
	for i in range(0, len(cmd_data)):
		tx_data[3 + i] = cmd_data[i]

	crc = cal_crc_loop_ccitt_a(tx_buffer_length - 3, tx_data[1:],CRC_SSP_SEED, CRC_SSP_POLY)
	tx_data[3 + len(cmd_data)] = c_ubyte(crc.value & 0xFF).value
	tx_data[4 + len(cmd_data)] = c_ubyte((crc.value >> 8) & 0xFF).value

	j = 0
	t_buffer = [chr(0) for i in range(0, 255)]
	t_buffer[j] = tx_data[0]
	j+=1
	for i in range(1, tx_buffer_length):
		t_buffer[j] = tx_data[i]
		if tx_data[i] == SSP_STX:
			t_buffer[++j] = SSP_STX
		j+=1

	for i in range(0, j):
		tx_data[i] = t_buffer[i]
		tx_buffer_length = j

	return tx_data

def send(tx_data, port, ssp_address):
	rx_data = None
	cmd_packet = bytearray(tx_data)
	try:
		port.write(cmd_packet)
		response = port.readline()
		rx_data = list(response)
	except:
		pass

	return rx_data

def decompile(rx_data, ssp_address):
	rx_data_length = rx_data[2]
	rep_data = [rx_data[i + 3] for i in range(0, rx_data_length)]

	if ssp_seq[ssp_address] == 0x80:
		ssp_seq[ssp_address] = 0
	else:
		ssp_seq[ssp_address] = 0x80

	return rep_data
