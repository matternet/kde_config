#!/usr/bin/python

import serial
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('tx_csv', nargs=1)
parser.add_argument('rx_csv', nargs=1)
parser.add_argument('port', nargs=1)
args = parser.parse_args()

def csv_text_to_struct(csv):
    ret = [(float(x[0]), int(x[1],0)) for x in [x.split(',') for x in csv.strip().split('\n')][1:]]
    return ret

with open(args.tx_csv[0], 'r') as f:
    tx_data = csv_text_to_struct(f.read())

with open(args.rx_csv[0], 'r') as f:
    rx_data = csv_text_to_struct(f.read())

DIR_RX = 0
DIR_TX = 1

tx_idx = 0

sequence = []

for rx_tuple in rx_data:
    if rx_tuple in tx_data:
        direction = DIR_TX
    else:
        direction = DIR_RX

    sequence.append((rx_tuple[1], direction))

def validate_esc_settings():
    try:
        ser = serial.Serial(args.port[0], 9600, timeout=1)
        for byte, direction in sequence:
            if direction == DIR_TX:
                print 'tx 0x%02X' % (byte,)
                ser.write(chr(byte))
                rx_byte = ser.read()
                print 'rx 0x%02X, expect 0x%02X' % (ord(rx_byte), byte)
                if rx_byte != chr(byte):
                    return False
            else:
                rx_byte = ser.read()
                print 'rx 0x%02X, expect 0x%02X' % (ord(rx_byte), byte)
                if rx_byte != chr(byte):
                    return False
    except:
        print 'Exception'
        return False

    return True

print "##### PASS! #####" if validate_esc_settings() else "##### FAIL! #####"
