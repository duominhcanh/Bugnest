import keyboard
from time import sleep

STOP_PENDING = False

def wait(break_keys= ('enter')):
    global STOP_PENDING

    STOP_PENDING= False
    recorded = []

    def __on_key(key):
        if key.event_type == keyboard.KEY_UP:
            if key.name in break_keys:
                recorded.append(key.name)
                cancel()

    keyboard.hook(__on_key)
    while not STOP_PENDING: sleep(0.25)
    keyboard.unhook(__on_key)
    reset()
    if len(recorded) == 0: return None
    return recorded[0]

def bind(key, action) -> None: keyboard.on_release_key(key, action)

def read(on_content= None, accepted_keys:tuple=('0', '1','2','3','4','5','6','7','8','9'), break_keys=('enter')) -> str:
    global STOP_PENDING

    STOP_PENDING= False
    recorded = []

    def __on_key(key):
        if key.event_type == keyboard.KEY_UP:
            if key.name in accepted_keys: 
                recorded.append(key.name)
            elif key.name == 'backspace':
                if len(recorded) > 0: 
                    recorded.remove(recorded[-1])
            elif key.name in break_keys: 
                cancel()

            content= ''.join(recorded)
            if on_content != None: on_content(content)

    keyboard.hook(__on_key)
    while not STOP_PENDING: sleep(0.25)
    keyboard.unhook(__on_key)
    reset()
    if len(recorded) == 0: return None
    return ''.join(recorded)

def cancel(): 
    global STOP_PENDING

    STOP_PENDING= True

def reset(): 
    global STOP_PENDING

    STOP_PENDING= False
    keyboard.unhook_all()
    
