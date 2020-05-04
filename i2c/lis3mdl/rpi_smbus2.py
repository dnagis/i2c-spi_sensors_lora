#!/bin/python3
# -*-coding:Latin-1 -*

#lis3mdl (magnetometer)

from smbus2 import SMBus
import time
from math import atan2, degrees
import sys

SLAVE_ADDR		=  0x1E

WHO_AM_I_ADDR 	 = 0x0F #Dummy: pratique pour tester un controle positif

CTRL_REG1_ADDR   = 0x20 #les controles: reglages
CTRL_REG2_ADDR   = 0x21
CTRL_REG3_ADDR   = 0x22
CTRL_REG4_ADDR   = 0x23
CTRL_REG5_ADDR   = 0x24

STATUS_REG_ADDR  = 0x27
OUT_X_L_ADDR     = 0x28 #Les 6 mag(netometer) values a chaque fois: "H"igh and "L"ow Bytes, the value is expressed as two's complement (cf ci dessous)
OUT_X_H_ADDR     = 0x29
OUT_Y_L_ADDR     = 0x2A
OUT_Y_H_ADDR     = 0x2B
OUT_Z_L_ADDR     = 0x2C
OUT_Z_H_ADDR     = 0x2D
TEMP_OUT_L_ADDR  = 0x2E 
TEMP_OUT_H_ADDR  = 0x2F
INT_CFG_ADDR     = 0x30
INT_SRC_ADDR     = 0x31
INT_THS_L_ADDR   = 0x32
INT_THS_H_ADDR   = 0x33


bus = SMBus(1)


print("{:#010b}".format(bus.read_byte_data(SLAVE_ADDR, WHO_AM_I_ADDR)))

bus.write_byte_data(SLAVE_ADDR, CTRL_REG1_ADDR, 0x70)
print("{:#010b}".format(bus.read_byte_data(SLAVE_ADDR, CTRL_REG1_ADDR)))



