#!/usr/bin/python

import serial
import argparse
from time import sleep
from sys import exit

DIR_RX = 0
DIR_TX = 1

parser = argparse.ArgumentParser()
parser.add_argument('port', nargs=1)
args = parser.parse_args()

def csv_text_to_struct(csv):
    ret = [(float(x[0]), int(x[1],0)) for x in [x.split(',') for x in csv.strip().split('\n')][1:]]
    return ret

def validate_esc_settings(txfile, rxfile):
    with open(txfile, 'r') as f:
        tx_data = csv_text_to_struct(f.read())

    with open(rxfile, 'r') as f:
        rx_data = csv_text_to_struct(f.read())

    tx_idx = 0

    sequence = []

    for rx_tuple in rx_data:
        if rx_tuple in tx_data:
            direction = DIR_TX
        else:
            direction = DIR_RX

        sequence.append((rx_tuple[1], direction))

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
        return False

    return True

sleep(1)
print "Checking valid config 1"
res_1 = validate_esc_settings("golden_tx.csv","golden_rx.csv")
print "Config 1 PASS" if res_1 else "Config 1 FAIL"
sleep(1)
print "Checking valid config 2"
res_2 = validate_esc_settings("golden_tx_rev.csv","golden_rx_rev.csv")
print "Config 2 PASS" if res_2 else "Config 2 FAIL"

print "##### PASS #####" if res_1 or res_2 else "##### FAIL #####"
exit(0 if res_1 or res_2 else 1)
