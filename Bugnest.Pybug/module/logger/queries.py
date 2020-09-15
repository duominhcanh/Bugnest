# <<< create table

# tạo bảng notes
CREATE_TABLE_NOTES = '''
CREATE TABLE notes
(
    note_1000 int,
    note_2000 int,
    note_5000 int,
    note_10000 int,
    note_20000 int,
    note_50000 int,
    note_100000 int,
    note_200000 int,
    note_500000 int
);
'''

# tạo bảng cash in log
CREATE_TABLE_CASH_IN_LOG = '''
CREATE TABLE cash_in_log
(
  created TEXT NOT NULL,
  emp_id TEXT,
  debt REAL,
  note_1000 int,
  note_2000 int,
  note_5000 int,
  note_10000 int,
  note_20000 int,
  note_50000 int,
  note_100000 int,
  note_200000 int,
  note_500000 int,
  step int,
  CONSTRAINT PK_cash_in_log PRIMARY KEY (created)
);
'''

# tạo bảng cash out log
CREATE_TABLE_CASH_OUT_LOG = '''
CREATE TABLE cash_out_log
(
  created TEXT NOT NULL,
  emp_id TEXT,
  debt REAL,
  status TEXT,
  step int,
  CONSTRAINT PK_cash_out_log PRIMARY KEY (created)
);
'''

# tạo bảng event log
CREATE_TABLE_CASH_EVENT_LOG = '''
CREATE TABLE event_log
(
  created TEXT NOT NULL,
  name TEXT,
  loc TEXT,
  description TEXT,
  level int,
  CONSTRAINT PK_event_log PRIMARY KEY (created)
);
'''

CREATE_TABLE_INFO = '''
CREATE TABLE info
(
  last_login TEXT
);
'''

# >>> create table
GET_LAST_LOGIN = '''
select last_login from info
'''

SET_LAST_LOGIN = lambda urs: '''
update info set last_login= '{0}';
'''.format(urs)

# <<< init

# khởi tạo bảng notes
INIT_NOTES = '''
insert into notes(
    note_1000, note_2000, note_5000, 
    note_10000, note_20000, note_50000, 
    note_100000, note_200000, note_500000)
values( 0, 0, 0, 0, 0, 0, 0, 0, 0);
'''

INIT_INFO = '''
insert into info(last_login) values('');
'''
# >>> init

# <<< cash in log

# thêm cash in log mới
INSERT_CASH_IN_LOG = lambda created, emp_id, debt: '''
insert into cash_in_log(
    created, emp_id, debt, 
    note_1000, note_2000, note_5000,
    note_10000, note_20000, note_50000,
    note_100000, note_200000, note_500000, step)
values('{0}', '{1}', {2}, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);
'''.format(created, emp_id, debt)

# lấy toàn bộ cash in log trong db
GET_ALL_CASH_IN_LOG = '''
select * from cash_in_log
'''

# cập nhật bước thực hiện cho cash in log
SET_STEP_CASH_IN_LOG = lambda step, created: '''
update cash_in_log set step= {0} where created = '{1}'
'''.format(step, created)

# lấy cash in log theo ngày tạo
GET_CASH_IN_LOG_BY_CREATED = lambda created: '''
select * from cash_in_log where created = '{0}';
'''.format(created)

# cập nhật tiền cho cash in log
UPDATE_CASH_IN_LOG = lambda note ,note_count, created: '''
update cash_in_log set {0}= {1} where created= '{2}';
'''.format(note, note_count, created)

# xóa cash in log
DELETE_CASH_IN_LOG = lambda created: '''
delete from cash_in_log where created = '{0}'
'''.format(created)
# >>> cash in log

# <<< cash out log

# thêm cash in log mới
INSERT_CASH_OUT_LOG = lambda created, emp_id, debt, status: '''
insert into cash_out_log(created, emp_id, debt, status, step)
values('{0}', '{1}', {2}, {3}, 0);
'''.format(created, emp_id, debt, status)

# lấy tất cả cash out log trong db
GET_ALL_CASH_OUT_LOG = '''
select * from cash_out_log
'''

# cập nhật bước thực hiện cho cash out log
SET_STEP_CASH_OUT_LOG = lambda step, created: '''
update cash_out_log set step= {0} where created = '{1}';
'''.format(step, created)

# xóa cash out log
DELETE_CASH_OUT_LOG = lambda created: '''
delete from cash_out_log where created = '{0}'
'''.format(created)
# >>> cash out log

# <<< event log

# thêm event log mới
INSERT_EVENT_LOG = lambda created, name, loc, desc, level: '''
insert into event_log(
    created, name, loc, 
    description, level)
values('{0}', '{1}', '{2}', '{3}', {4})
'''.format(created, name, loc, desc, level)

# xóa event log
DELETE_EVENT_LOG = lambda created: '''
delete from event_log where created = '{0}'
'''.format(created)

# lấy tất cả event log
GET_ALL_EVENT_LOG = '''
select * from event_log
'''

# <<< note log

# lấy tât cả note log trong db
GET_ALL_NOTES = '''
select * from notes
'''

# cập nhật số lượng note trong db
UPDATE_NOTE_COUNT = lambda col_name, value: '''
update notes set {0}= {1}
'''.format(col_name, value)

# reset số lượng note về 0
RESET_NOTE_COUNT = lambda col_name: '''
update notes set {0}= 0
'''.format(col_name)
# >>> note log