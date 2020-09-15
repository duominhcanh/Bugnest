import socket
from random import randint
from datetime import datetime
import threading
from time import sleep

from module.io import interdisplay as view
from module.io import keyboard
from module import api
from module import logger
from module.logger.storage import VND_NOTES
from module import locker
from module.validator import Validator

class App:
    def __init__(self):
        view.init()
        locker.set_pin(17)
        self.note_reader = Validator(port_name= 'COM5')

        self.running = True
        self.login_pwd = None


    def run(self):
        if self.login() == False: return

        #Kiểm tra thông tin giao dịch cuối
        cash_in_trans = logger.get_cash_in_logs()
        cash_out_trans = logger.get_cash_out_logs()
        if len(cash_in_trans) > 0:
            if cash_in_trans[-1]['step'] in (1, 2): 
                #Nếu giao dịch chưa hoàn tất, hoàn tất nó thôi
                self.insert_cash(cash_in_trans[-1])
        elif len(cash_out_trans) > 0:
            if cash_out_trans[-1]['step'] in (3,):
                #Nếu giao dịch chưa hoàn tất, hoàn tất nó thôi
                self.get_cash(cash_out_trans[-1])

        while self.running:
            action = self.show_main_menu()
            if action == 1: self.insert_cash()
            if action == 2: self.get_cash()
            elif action == 3: self.show_config()

    def insert_cash(self, last_trans=None):

        # nếu bắt đầu từ đầu, thực hiện từ bước 1 đến bước 3
        # nếu không nhảy đến bước 3

        # bước 1:
        # nhập thông tin nhân viên, lấy thông tin nợ, xác nhận có nhận tiền hay
        # không

        # bước 2:
        # nhận tiền

        # bước 3: kiểm tra xác thực, cập nhật tiền

        view_title = 'nap tien'
        # ------ Khởi tạo ------
        def do_countdown(time, stop_counting=[False]):
            start_waiting_time = datetime.now()
            while True:
                if stop_counting[0]: 
                    return
                    #endif
                collapsed_seconds = (datetime.now() - start_waiting_time).total_seconds()
                if collapsed_seconds >= time:
                    keyboard.cancel()
                    break
                    #endif
                sleep(1)
                #endwhile
            #endef

        step = 1
        emp_id= ''
        inserted_cash = [0 for i in range(0, 9)] #danh sách các tờ tiền đã đưa vào
        total_payment = 0 # tổng số tiền phải nạp
        trans_created = None #thời gian tao trans
        total_inserted = 0 # tổng số tiền đã đưa vào máy
        stop_counting = [False] # có nên dừng đếm ngược không ta?

        if last_trans != None: 
            step = 3
            emp_id = last_trans['emp_id']
            total_payment = last_trans['debt']
            trans_created = last_trans['created']
            total_inserted = sum([x * y for (x, y) in zip([last_trans['note_1000'],
                last_trans['note_2000'],
                last_trans['note_5000'],
                last_trans['note_10000'],
                last_trans['note_20000'],
                last_trans['note_50000'],
                last_trans['note_100000'],
                last_trans['note_200000'],
                last_trans['note_500000'],], VND_NOTES)])       

        # ------ bước 1 ------
        if step == 1:
            # nhập mã nhân viên
            emp_id = view.show_input(view_title, 'nhap ma nhan vien')
            view.show_msg(view_title, 'dang xu ly...')
            # lấy thông tin nợ
            get_debt_response = api.get_debt(emp_id, logger.get_balance())

            # check nếu không được nạp tiền thì thoát
            task_canceled = False
            if get_debt_response.is_error:
                task_canceled = True
            else:
                total_payment = get_debt_response.data.total_payment# sale da shit
                if total_payment <= 0:
                    task_canceled = True
                    #endif
                #endif

            if task_canceled:
                view.show_msg(view_title, get_debt_response.message, hint= 'nhan enter de tiep tuc', wait= True)
                return
                #endif
                
            th_countdown = threading.Thread(target=do_countdown, args=(90, stop_counting))
            menu_title = view_title
            menu_items = (('NO {0}'.format(total_payment), '0'),
                         ('1.TIEP TUC', '1'),
                         ('0.QUAY LAI', '0'))
            th_countdown.start()
            result = view.show_menu(menu_title, menu_items)
            stop_counting[0] = True
            if result in ('0', None): 
                return
                #endif
            step+=1
            #endif - (bước 1)

        # ------ bước 2 ------
        if step == 2:
            def cash_in(icash):
                keyboard.reset()
                now[0] = datetime.now()
                inserted_ammount = sum([x * y for (x, y) in zip(inserted_cash, VND_NOTES)])
                readed_ammount = VND_NOTES[icash]
                if (inserted_ammount + readed_ammount) >= total_payment:
                    self.note_reader.cancel()
                    #endifqpo
                #enddef

            def stop_handler(e): 
                self.note_reader.cancel()
                keyboard.reset()
                #enddef

            def on_reader_error(e):
                logger.error(e, 'validator')
                keyboard.reset()

            def cash_stacked(icash):
                #update things
                inserted_cash[icash]+=1
                logger.set_step_cash_in_log(trans_created,1)
                logger.set_note_count(icash, logger.get_note_count(icash) + 1)
                logger.update_cash_in_log(trans_created, icash)

                #views shits
                view.show_msg(view_title, 'NHAN {0}'.format(VND_NOTES[icash]), 'TONG {0}'.format(sum([x * y for (x, y) in zip(inserted_cash, VND_NOTES)])))
                keyboard.bind('enter', stop_handler) 
                #enddef

            def do_cashin_countdown(start_waiting_time, time, stop_counting):
                while True:
                    if stop_counting[0]: return
                    collapsed_seconds = (datetime.now() - start_waiting_time[0]).total_seconds()
                    if collapsed_seconds >= time:
                        self.note_reader.cancel()
                        keyboard.reset()
                        break
                        #endif
                    sleep(1)
                    #endwhile
                #endef

            trans_created = datetime.now()
            view.show_msg(view_title,'DUA TIEN VAO MAY',hint= 'enter de hoan tat')
            
            logger.add_cash_in_log(trans_created, emp_id, total_payment)
            
            keyboard.bind('enter', stop_handler)       
            now = [datetime.now()]
            th_countdown = threading.Thread(target=do_cashin_countdown, args=(now, 60, stop_counting))
            th_countdown.start()
            self.note_reader.sale(cash_in, cash_stacked, on_reader_error)
            total_inserted = sum([x * y for (x, y) in zip(inserted_cash, VND_NOTES)])

            view.show_msg(view_title, 'dang xu ly...')
            logger.set_step_cash_in_log(trans_created,2)
            step+=1
            #endif (bước 2)

        # ------ bước 3 ------
        if step == 3:
            update_debt_response = api.update_debt(emp_id, total_inserted, logger.get_balance())
            logger.set_step_cash_in_log(trans_created,3)
            logger.event('sale trans', 'app')
            stop_counting[0] = False
            th_countdown = threading.Thread(target=do_countdown, args=(20, stop_counting))
            th_countdown.start()
            view.show_msg(view_title, 'TONG {0} >> '.format(total_inserted)+ update_debt_response.message, hint= 'nhan enter de tiep tuc', wait= True)
            stop_counting[0] = True
            #endif (bước 3)
        #enddef (nạp tiền)

    def get_cash(self, last_trans=None):

        # bước 1
        # nhập mã quản lý
        # xác nhận quyền nhập otp

        # bước 2
        # nhập otp

        # bước 3
        # mở khóa

        # bước 4
        # trừ tiền

        # ------ khởi tạo ------
        def __do_countdown(time, stop_counting=[False]):
            start_waiting_time = datetime.now()
            while True:
                if stop_counting[0]: 
                    return
                    #endif
                collapsed_seconds = (datetime.now() - start_waiting_time).total_seconds()
                if collapsed_seconds >= time:
                    keyboard.cancel()
                    break
                    #endif
                sleep(1)
                #endwhile
            #endef

        view_title = 'rut tien'
        step = 1
        managerid = ''
        chk_permission_resp = None
        trans_created = None
        total_payment = None
        payment_status = None
        stop_counting = [False] # có nên dừng đếm ngược không ta?

        if last_trans != None:
            step = 4
            managerid = last_trans['emp_id']
            trans_created = last_trans['created']
            total_payment = last_trans['debt']
            payment_status = last_trans['status']

        # ------ bước 1 ------
        if step == 1:
            managerid = view.show_input(view_title, 'nhap ma thu ngan')
            view.show_msg(view_title, 'dang xu ly...', wait= False)
            self.otp = str(randint(100000, 999999)) #tạo otp ngẫu nhiên
            print(self.otp) # testing, bỏ trong môi trường thật

            chk_permission_resp = api.check_permission(managerid, self.otp, logger.get_balance())

            # check nếu có lỗi, dừng cuộc chơi
            if chk_permission_resp.is_error:
                view.show_msg(view_title, chk_permission_resp.message, hint= 'nhan enter de tiep tuc', wait= True)
                return
                #endif
            trans_created = datetime.now()
            payment_status = chk_permission_resp.data.payment_status
            logger.add_cash_out_log(trans_created, managerid, logger.get_balance(), payment_status)
            step+=1
            #endif (bước 1)

        # ------ bước 2 ------
        if step == 2:
            begin_time = datetime.now()
            attempts = 0
            while True:
                if attempts > 2:                    
                    view.show_msg(view_title, 'het luot gui otp', hint= 'nhan enter de tiep tuc', wait= True)
                    self.otp = None
                    return
                    #endif
                menu_title = 'RUT TIEN'
                nenu_items = (('1 NHAP OTP', '1'),
                              ('2 GUI LAI OTP', '2'),
                              ('0 quay lai', '0'),)

                user_choice = int(view.show_menu(menu_title, nenu_items))
                if user_choice == 0: return
                elif (user_choice == 2) or chk_permission_resp.data.otp_expire_date < datetime.now():
                    if attempts < 2:
                        view.show_msg(view_title, 'dang xu ly ...')
                        self.otp = str(randint(100000, 999999)) #tạo otp ngẫu nhiên
                        print(self.otp) # testing, bỏ trong môi trường thật
                        chk_permission_resp = api.check_permission(managerid, self.otp, logger.get_balance())

                    attempts+=1
                    continue
                    #endif

                user_otp = view.show_input(view_title, 'nhap otp')
                if user_otp == chk_permission_resp.data.otp: 
                    if chk_permission_resp.data.otp_expire_date < datetime.now():
                        view.show_msg(view_title, 'otp da het han', hint= 'enter de thu lai', wait= True)
                    else:
                        break
                else:
                    view.show_msg(view_title, 'sai otp', hint= 'enter de thu lai', wait= True)
                    #endif
                #endwhile
            total_payment = chk_permission_resp.data.total_payment
            logger.set_step_cash_out_log(trans_created, 2)
            step+=1
            #endif (bước 2)

        # ------ bước 3 ------
        if step == 3:            
            if payment_status in ('0', '1'):
                # mở máy
                view.show_msg(view_title, 'TONG: {0}'.format(int(total_payment)), 
                              hint= 'nhan enter de mo may', wait= True)

                locker.unlock()      
                #endif
            #endif
            logger.set_step_cash_out_log(trans_created, 3)
            step+=1
            #endif

        # ------ bước 4 ------
        if step == 4:
            change_resp = None
            view_msg = ''
            if payment_status in ('0', '1'):
                if payment_status == '0':
                    # nếu số tiền trong máy > 0, cập nhật lên api thôi
                    view.show_msg(view_title, 'dang xu ly ...')
                    change_resp = api.change(managerid, total_payment, logger.get_balance())
                    logger.reset_notes_count()      
                    view_msg = change_resp.message

                if payment_status == '0':
                    # nếu số tiền trong máy > 0, cập nhật ở trên rồi, coi thử
                    # được không
                    if change_resp.is_error: logger.error('change failed', 'app')
                else:
                    # nếu số tiền trong máy = 0
                    # không update số tiền lên server, lỗi đấy
                    view_msg = 'da mo may'
                    #endif
            logger.set_step_cash_out_log(trans_created, 4)
            th_countdown = threading.Thread(target=__do_countdown, args=(20, stop_counting))
            th_countdown.start()
            view.show_msg(view_title, view_msg, hint= 'nhan enter de tiep tuc', wait= True)
            stop_counting[0] = True
        #enddef

    def login(self):
        view_title = 'dang nhap'

        urs = view.show_input(view_title, 'nhap tai khoan may thu ngan')

        last_login = logger.get_last_login()
        if last_login != urs:
            if logger.get_balance() > 0:
                view.show_msg(view_title, 'may dang giu so tien lon hon 0, vui long dang nhap bang nhan vien khac',
                              hint= 'nhan enter de tiep tuc', wait= True)
                return False

        pwd = view.show_input(view_title, 'nhap mat khau may thu ngan', display_char= '*')
        view.show_msg(view_title, 'dang xu ly...')
        login_resp = api.login(urs, pwd)
        if login_resp.is_error:
            view.show_msg(view_title, login_resp.message, hint= 'nhan enter de tiep tuc', wait= True)
            return False
        else:
            logger.set_last_login(urs)
            logger.event('login success, username: {}'.format(urs), 'app')
            view.show_msg(view_title, 'nguoi dung {0} dang nhap thanh cong'.format(login_resp.status), 
                          hint= 'nhan enter de tiep tuc', wait= True)
            self.login_pwd = pwd
            return True

    def show_main_menu(self):
        menu_title = 'chon chuc nang'
        nenu_items = (('1 nap tien', '1'),
            ('2 rut tien', '2'),
            ('3 cai dat', '3'),)
        urs_choice = view.show_menu(menu_title, nenu_items)
        return int(urs_choice)

    def show_config(self):
        view_title = 'cai dat'
        pwd = view.show_input(view_title, 'nhap mat khau dang nhap may thu ngan', display_char= '*')
        if pwd != self.login_pwd:
            view.show_msg(view_title, 'mat khau khong dung, vui long thu lai sau', hint= 'nhan enter de tiep tuc', wait= True)
            return

        menu_title = 'cai dat'
        nenu_items = (('1 thong tin may', '1'),
            ('2 dang xuat', '2'),
            ('0 quay lai', '0'),)
        urs_choice = int(view.show_menu(menu_title, nenu_items))

        if urs_choice == 0: return
        if urs_choice == 1: self.show_info()
        elif urs_choice == 2: self.logout()

    def show_info(self):
        menu_title = 'thong tin may'
        nenu_items = (('1 thong tin ket noi', '1'),
            ('2 thong tin tien mat', '2'),
            ('0 quay lai', '0'),)
        urs_choice = int(view.show_menu(menu_title, nenu_items))

        if urs_choice == 0: return
        if urs_choice == 1: self.show_network_info()
        elif urs_choice == 2: self.show_cash_info()

    def show_cash_info(self):
        menu_title = 'thong tin tien'
        nenu_items = (('tong {0}'.format(logger.get_balance()), '0'),
            ('1 chi tiet', '1'),
            ('0 quay lai', '0'),)

        urs_choice = int(view.show_menu(menu_title, nenu_items))

        if urs_choice == 1:
            cashs_count = logger.get_notes()
            
            menu_title = 'chi tiet thong tin tien'
            nenu_items = [['{0}:{1} to'.format(VND_NOTES[i], cashs_count[i]), 'enter'] for i in range(0, len(cashs_count))]
            nenu_items.append(['nhan enter de quay lai', 'enter'])
            view.show_menu(menu_title, nenu_items)

    def show_network_info(self):
        menu_title = 'thong tin ket noi'
        nenu_items = (('', '0'),
            ('IP {0}'.format([(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]), '0'),
            ('0 quay lai', '0'),)

        view.show_menu(menu_title, nenu_items)

    def logout(self):
        menu_title = 'dang xuat'
        nenu_items = (('', '1'),
            ('1 tiep tuc xang xuat', '1'),
            ('2 huy thao tac', '2'),)
        urs_choice = int(view.show_menu(menu_title, nenu_items))

        if urs_choice == 1: self.running = False
