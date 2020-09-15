#build-in modules
import datetime
import traceback

import module.logger.storage as storage

def error(e, loc):
    storage.add_event(str(datetime.datetime.now()), 'err', loc, str(e), 1)
    print('<err :',loc,':',datetime.datetime.now(),'> ', str(e))
    traceback.print_exc()

def event(e, loc):
    storage.add_event(str(datetime.datetime.now()), 'event', loc, str(e), 0)
    print('<event :',loc,':',datetime.datetime.now(),'> ', str(e))
