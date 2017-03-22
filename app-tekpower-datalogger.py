#!/usr/bin/python
import os
import sys
import serial
import time
import threading
import getopt

from sys import platform
from event_queue import EventQueue

if 'linux' in platform:
    ser_port = '/dev/ttyUSB0'   # Might have to change based on machine
    from plot import ScrollingPlot
elif 'cygwin' in platform:
    ser_port = '/dev/ttyS4'     # Might have to change based on machine


plotting = True
show_data = False

def get_num(data):
    precision = 4 #decimal points
    arr = data.split(' ')
    arr1 = arr[1].split('\x00')

    value = float(arr[0])
    decimal_point_loc = int(arr1[0][0:1]) - precision
    data = value * 10**decimal_point_loc

    return data

def get_data(running, queues=[]):
    first_sample = True
    ser = serial.Serial(ser_port, 2400)
    while running.is_set():
        try:
            data = ser.readline().rstrip('\n')

            if first_sample:
                first_sample = False
                continue

            data = get_num(data)

            if show_data:
                print data

            for q in queues:
                q.push(data=data)
        except ValueError:
            continue
        except KeyboardInterrupt:
            print 'Exit'
            exit(1)
            break


def options():
    """ Handles command line options"""
    global plotting
    global show_data
    try:
         options, remainder = \
            getopt.getopt(sys.argv[1:], '', ['noplot','showdata'])
         for opt, arg in options:
             if opt in ('--noplot'):
                 plotting = False
                 print 'Plotting OFF'
             elif opt in ('--showdata'):
                 show_data = True
    except Exception as e:
        plotting = True
        show_data = False
        print (e)
        exit(1)

if __name__ == '__main__':
    try:
        # Parse command line options
        options()

        # To stop threads
        run = threading.Event()
        run.set()

        # Plotting thread
        if plotting:
            qplot = EventQueue()
            splot = ScrollingPlot(qplot, 'accumulate')
            splot.set_label('y', text='Voltage', unit='v')
            splot.set_label('x', text='Time', unit='seconds')
            t_plot = threading.Thread(target=splot.run)
            t_plot.start()

        # Data producer thread
        t_producer = threading.Thread(target=get_data,
                args=(run, [qplot] if plotting else []))
        t_producer.start()

        print 'Collecting data...'
        raw_input("Type enter to end collecting.\n")
        run.clear()

        #print("Waiting for producer thread to join...")
        t_producer.join()

        if plotting:
            print("Waiting for graph window process to join...")
            t_plot.join()
        print("Exiting")

    except Exception as e:
        print(e)
        exit(1)
