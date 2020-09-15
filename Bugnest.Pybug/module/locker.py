#build-in modules
from time import sleep
from threading import Thread
import os
if os.name != 'nt': import RPi.GPIO as GPIO

class LockerError(Exception): 
    '''
    Lỗi phát sinh trong quá trình dử dụng khóa điện
    '''

    def __init__(self, msg): 
        super().__init__('Locker Error >> '+ msg)

GPIO_PIN= None

def set_pin(pin:int):
    '''
    Cài đặt chân <pin> GPIO cho khóa
    '''

    global GPIO_PIN

    GPIO_PIN= pin

def unlock(hold:int= 5):
    '''
    Mở hóa trong vòng <hold> giây
    '''

    if GPIO_PIN == None: raise LockerError('Không mở được khóa')

    def do_unlock():
        if os.name == 'nt': 
            print('unlocked')
            return

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(GPIO_PIN, GPIO.OUT)
        GPIO.output(GPIO_PIN, GPIO.LOW)
        sleep(hold)
        GPIO.output(GPIO_PIN, GPIO.HIGH)

    Thread(target= do_unlock, daemon= True).start()
