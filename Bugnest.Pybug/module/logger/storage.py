#build-in modules
import sqlite3
from datetime import datetime
from os import path

#urs defined modules
import module.logger.queries as queries

DBNAME = 'config.dat'

MAX_EVENTS = 100
MAX_CASH_IN_LOG = 100
MAX_CASH_OUT_LOG = 100

VND_NOTES = [1000, 2000, 5000, 10000, 20000, 50000, 100000, 200000, 500000]
NOTE_COL_NAMES = ['note_1000', 'note_2000', 'note_5000', 
    'note_10000', 'note_20000', 'note_50000',
    'note_100000', 'note_200000', 'note_500000']

def init() -> None:
    '''
    Khởi tạo file config với các giá trị mặc định
    '''

    init_needed = not path.exists(DBNAME)
    conn = sqlite3.connect(DBNAME)
    if init_needed:
        conn.execute(queries.CREATE_TABLE_NOTES)
        conn.execute(queries.CREATE_TABLE_CASH_IN_LOG)
        conn.execute(queries.CREATE_TABLE_CASH_OUT_LOG)
        conn.execute(queries.CREATE_TABLE_CASH_EVENT_LOG)
        conn.execute(queries.CREATE_TABLE_INFO)    
        conn.execute(queries.INIT_NOTES)
        conn.execute(queries.INIT_INFO)
        conn.commit()
        conn.close()

def get_last_login():
    last_login = None
    conn = sqlite3.connect(DBNAME)
    resp = conn.execute(queries.GET_LAST_LOGIN)
    for row in resp: 
        last_login = row[0]
        break

    conn.close()
    return last_login

def set_last_login(urs):
    conn = sqlite3.connect(DBNAME)
    conn.execute(queries.SET_LAST_LOGIN(urs))
    conn.commit()
    conn.close()

#cash in log
def add_cash_in_log(created: datetime, emp_id: str, debt: float) -> None:
    '''
    Thêm log cho giao dịch mới với các giá trị mặc định, 
    Khóa là ngày tạo (created)

    params:
    created: Ngày tạo
    emp_id: mã nhân viên
    debt: Số nợ hiện hành
    '''

    logs = get_cash_in_logs()
    if len(logs) >= MAX_CASH_IN_LOG: rm_cash_in_log(logs[0]['created'])

    conn = sqlite3.connect(DBNAME)
    conn.execute(queries.INSERT_CASH_IN_LOG(created, emp_id, debt))
    conn.commit()
    conn.close()

def get_cash_in_logs() -> list:
    '''
    Lấy danh sách giao dịch nạp tiền trong hệ thống
    sắp xếp tăng dần theo ngày giao dịch
    '''
    
    logs = []
    conn = sqlite3.connect(DBNAME)
    resp = conn.execute(queries.GET_ALL_CASH_IN_LOG)
    for item in resp:
        logs.append({
            'created': datetime.strptime(item[0], '%Y-%m-%d %H:%M:%S.%f'), 
            'emp_id': item[1],
            'debt': item[2],
            'note_1000': item[3],
            'note_2000': item[4],
            'note_5000': item[5],
            'note_10000': item[6],
            'note_20000': item[7],
            'note_50000': item[8],
            'note_100000': item[9],
            'note_200000': item[10],
            'note_500000': item[11],
            'step': item[12],})

    conn.close()
    return sorted(logs,key= lambda k: k['created'])

def set_step_cash_in_log(created: datetime, step: int) -> None:
    '''
    Cập nhật bước cho giao dịch

    params:
    created: Thời gian khởi tạo giao dịch
    step: Bước cần cập nhật(0: Khởi tạo, 
    1: chưa nạp tiền, 2: đã nạp tiền,
    3: chưa cập tiền)
    '''

    conn = sqlite3.connect(DBNAME)
    conn.execute(queries.SET_STEP_CASH_IN_LOG(step, created))
    conn.commit()
    conn.close()

def update_cash_in_log(created: datetime, note_index: int) -> None:
    '''
    Cập nhật số tiền đã nạp cho giao dịch, mỗi lần +1

    params:
    created: thời gian khởi tạo giao dịch
    note_index: chỉ mục tượng trưng cho mệnh giá tiền, cụ thể

    0:1000  1:2000  2:5000  3:10000  4:20000  5:50000 6:100000  7:200000  8:500000
    '''

    conn = sqlite3.connect(DBNAME)   
    col_names = ['note_1000', 
                'note_2000', 
                'note_5000', 
                'note_10000', 
                'note_20000',
                'note_50000',
                'note_100000',
                'note_200000',
                'note_500000']

    note_count_result = conn.execute(queries.GET_CASH_IN_LOG_BY_CREATED(created))
    note_count = 0
    for row in note_count_result:
        note_count = row[note_index + 3]
        break
    conn.execute(queries.UPDATE_CASH_IN_LOG(col_names[note_index], note_count + 1, created))

    conn.commit()
    conn.close()

def rm_cash_in_log(created: datetime) -> None:
    '''
    Xóa giao dịch chỉ định

    params:
    created: thời gian khởi tạo giao dịch
    '''

    conn = sqlite3.connect(DBNAME)
    conn.execute(queries.DELETE_CASH_IN_LOG)
    conn.commit()
    conn.close()
#end cash in log

#cash out log
def add_cash_out_log(created: datetime, emp_id: str, debt: float, status) -> None:
    '''
    Thêm log cho giao dịch mới với các giá trị mặc định, 
    Khóa là ngày tạo (created)

    params:
    created: Ngày tạo
    emp_id: mã nhân viên
    debt: Số nợ hiện hành
    '''

    logs = get_cash_in_logs()
    if len(logs) >= MAX_CASH_IN_LOG: 
        rm_cash_in_log(logs[0]['created'])

    conn = sqlite3.connect(DBNAME)
    conn.execute(queries.INSERT_CASH_OUT_LOG(created, emp_id, debt, status))
    conn.commit()
    conn.close()

def get_cash_out_logs() -> list:
    '''
    Lấy danh sách giao dịch nạp tiền trong hệ thống
    sắp xếp tăng dần theo ngày giao dịch
    '''
    
    logs = []
    conn = sqlite3.connect(DBNAME)
    resp = conn.execute(queries.GET_ALL_CASH_OUT_LOG)
    for item in resp:
        logs.append({
            'created': datetime.strptime(item[0], '%Y-%m-%d %H:%M:%S.%f'), 
            'emp_id': item[1],
            'debt': item[2],
            'step': item[4],
            'status': item[3]})

    conn.close()
    return sorted(logs,key= lambda k: k['created'])

def set_step_cash_out_log(created: datetime, step: int) -> None:
    '''
    Cập nhật bước cho giao dịch

    params:
    created: Thời gian khởi tạo giao dịch
    step: Bước cần cập nhật(0: Khởi tạo, 
    1: chưa nạp tiền, 2: đã nạp tiền,
    3: chưa cập tiền)
    '''

    conn = sqlite3.connect(DBNAME)
    conn.execute(queries.SET_STEP_CASH_OUT_LOG(step, created))
    conn.commit()
    conn.close()

def rm_cash_out_log(created: datetime) -> None:
    '''
    Xóa giao dịch chỉ định

    params:
    created: thời gian khởi tạo giao dịch
    '''

    conn = sqlite3.connect(DBNAME)
    conn.execute(queries.DELETE_CASH_OUT_LOG(created))
    conn.commit()
    conn.close()
#end cash out log

#event log
def add_event(created, name, loc, desc, level):
    events = get_events()
    if len(events) >= MAX_EVENTS: 
        rm_event(events[0]['created'])

    desc = desc.translate({ord(c): " " for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+\"\'"})
    conn = sqlite3.connect(DBNAME)
    conn.execute(queries.INSERT_EVENT_LOG(created, name, loc, desc, level))
    conn.commit()
    conn.close()

def rm_event(created):
    conn = sqlite3.connect(DBNAME)
    conn.execute(queries.DELETE_EVENT_LOG(created))
    conn.commit()
    conn.close()

def get_events():
    events = []
    conn = sqlite3.connect(DBNAME)
    resp = conn.execute(queries.GET_ALL_EVENT_LOG)
    for item in resp:
        events.append({'created': datetime.strptime(item[0], '%Y-%m-%d %H:%M:%S.%f'), 'name': item[1], 'loc': item[2], 'description': item[3], 'level': item[4]})

    conn.close()
    return sorted(events,key= lambda k: k['created'])
#end event log

#cash log
def get_note_count(note_index):
    conn = sqlite3.connect(DBNAME)
    resp = conn.execute(queries.GET_ALL_NOTES)
    for row in resp:
        note_count_value = row[note_index]
        conn.close()
        return note_count_value
        #endfor
    #enddef
def set_note_count(note_index, value):
    col_name = NOTE_COL_NAMES[note_index]
    conn = sqlite3.connect(DBNAME)
    resp = conn.execute(queries.UPDATE_NOTE_COUNT(col_name, value))
    conn.commit()
    conn.close()
    #enddef
def reset_notes_count():
    conn = sqlite3.connect(DBNAME)
    for col_name in NOTE_COL_NAMES:
        conn.execute(queries.RESET_NOTE_COUNT(col_name))
        #endfor
    conn.commit()
    conn.close()
    #endef
def get_notes(): 
    return [get_note_count(i) for i in range(0, 9)]
def get_balance(): return sum([x * y for (x, y) in zip(get_notes(), VND_NOTES)])
#end cash log
