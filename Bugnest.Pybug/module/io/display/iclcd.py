#buld-in modules
from threading import Thread
from time import sleep
import os

if os.name != 'nt': import module.io.display.i2clib as i2clib

class LCDRow:
    def __init__(self, content=''):
        self.content = content
        self.offset = 0
        self.first_show = True

LCD_ROWS = 0
LCD_COLS = 0
LCD_CONTENT = None
CONSOLE_CONTENT= None
STOP_TH_SHOW = False
TH_SHOW = Thread()
LCD= None
if os.name != 'nt':LCD = i2clib.lcd()

def __DO_LCD_SHOW():
    while not STOP_TH_SHOW:
        for row in range(0, len(LCD_CONTENT)):
            lcd_row = LCD_CONTENT[row]
            #loop mỗi dòng của lcd
            if len(lcd_row.content) > LCD_COLS:
                #nếu len > LCD_COLS
                if lcd_row.offset > len(lcd_row.content):
                    lcd_row.offset = 0
                    if lcd_row.first_show: 
                        lcd_row.content = (' ' * LCD_COLS) + lcd_row.content
                        lcd_row.first_time = False

                content = lcd_row.content[lcd_row.offset:(lcd_row.offset + LCD_COLS)].ljust(LCD_COLS)

                if os.name != 'nt': LCD.lcd_display_string(content, row + 1)

                lcd_row.offset+=1
            else:
                #Không thì
                if os.name != 'nt': LCD.lcd_display_string(lcd_row.content.ljust(LCD_COLS), row + 1)

        sleep(0.25)

def set_content(content, row):
    LCD_CONTENT[row].content = content
    LCD_CONTENT[row].offset = 0
    LCD_CONTENT[row].first_show = True

    CONSOLE_CONTENT[row] = content

def init(rows=0, cols=0):
    global LCD_ROWS, LCD_COLS, LCD_CONTENT, CONSOLE_CONTENT

    LCD_ROWS = rows
    LCD_COLS = cols
    LCD_CONTENT = [LCDRow() for row in range(0, LCD_ROWS)]
    LCD_CONTENT = ['' for row in range(0, LCD_ROWS)]


def wipe():
    global LCD_CONTENT, CONSOLE_CONTENT

    LCD_CONTENT = [LCDRow() for row in range(0, LCD_ROWS)]
    CONSOLE_CONTENT = ['' for row in range(0, LCD_ROWS)]

def stop():
    global STOP_TH_SHOW

    if TH_SHOW.is_alive():
        STOP_TH_SHOW = True
        TH_SHOW.join()


def show():
    global TH_SHOW
    global STOP_TH_SHOW

    stop()

    for row in CONSOLE_CONTENT: print(row.ljust(LCD_COLS))
    for col in range(0, LCD_COLS): print('-', end= '')
    print()


    STOP_TH_SHOW = False
    if os.name != 'nt':LCD = i2clib.lcd()
    TH_SHOW = Thread(target= __DO_LCD_SHOW)
    TH_SHOW.start()


