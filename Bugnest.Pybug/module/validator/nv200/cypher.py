from ctypes import *

def cal_crc_loop_ccitt_a(l, p, seed, cd):
	crc = c_ushort(seed)

	for i in range(0, l):
		crc = c_ushort(crc.value ^ (p[i] << 8))
		for j in range(0, 8):
			if crc.value & 0x8000:
			    crc = c_ushort((crc.value << 1) ^ cd)
			else:
				crc = c_ushort(crc.value << 1)
	return crc
