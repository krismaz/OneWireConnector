import serial
import io
from time import sleep, time
from struct import pack
from pymsgbox import *
import json

sio = None

lasttarget = ''

with open('settings.json', 'r') as settingsfile:
    settings = json.load(settingsfile)


def getTemperatures():
    ser.write(bytes([1]))
    ser.flush()
    res = dict()
    for i in range(int(sio.readline())):
        addr = sio.readline().strip()  # Right side evaluates first
        res[addr] = float(sio.readline())
    return res


def setTemperature(temp):
    bts = pack('f', temp)
    ser.write(bytes([2]))
    ser.write(bts)
    ser.flush()
    print('Target set:', sio.readline())


def setTarget(target):
    global lasttarget
    lasttarget = target
    ser.write(bytes([3]))
    ser.write(bytes(map(lambda x: int(x, 16), target.split(" "))))
    ser.flush()
    print('Temp set:', sio.readline())


def setupSerial(port):
    return
    print('a')
    global sio, ser
    try:
        ser = serial.Serial(
            port=port,
            baudrate=9600,
            timeout=3
        )
    except serial.serialutil.SerialException:
        print('Error communicating with device "{}"! \n' +
              'Have you provided the correct COM port?'.format(port))
        exit(1)
    print('a')
    sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser, buffer_size=1),
                           encoding='ascii',
                           newline=None)
    sio._CHUNK_SIZE = 1
    print('a')
    sleep(10)
    print('a')


def evaluate(command, index):
    if not command:
        return
    print(command, '----')
    if command[0] == '#':
        return
    op, *args = command.split(' ')
    if op == 'TARGET':
        print('TARGET command deprecated, use settings file.')
    if op == 'HEAT':
        setTemperature(float(args[0]))
        while True:
            temps = getTemperatures()
            print(index, '-', temps)
            try:
                if temps[lasttarget] >= float(args[0]):
                    break
            except KeyError:
                print('Unknown target sensor {}!'.format(lasttarget))
                print('Connected sensors are:')
                print('\n'.join(*temps.keys()))
                exit(1)
            sleep(5)
    if op == 'COOK':
        start = time()
        setTemperature(float(args[0]))
        while True:
            temps = getTemperatures()
            print(index, '-', temps)
            if time() > start + float(args[1])*60.0:
                break
            sleep(5)
    if op == 'PAUSE':
        alert(text=' '.join(args), title='', button='OK')
    if op == 'DONE':
        setTemperature(-100000000.0)
        setTarget('0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0')

i = 1

if __name__ == "__main__":
    setupSerial(settings['COM'])
    setTarget(settings['sensor'])
    while(True):
        evaluate(input().strip(), i)
        i += 1
