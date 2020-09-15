from .display import iclcd as display
from .input import keynput as keyboard

def init(rows= 4, cols= 20):
    display.init(rows, cols)

def show_msg(title, msg, hint= '', wait= False):
    display.wipe()
    display.set_content(title.upper(), 0)
    display.set_content(msg.upper(), 2)
    display.set_content(hint.upper(), 3)
    display.show()

    if wait: keyboard.wait()

def show_input(title, msg, display_char= None) -> str:
    display.wipe()
    def __ON_CONTENT(content):
        if display_char == None: display.set_content(content, 3)
        else: display.set_content(''.join([display_char for i in range(0, len(content))]), 3)
        display.show()

    display.set_content(title.upper(), 0)
    display.set_content(msg.upper(), 2)
    display.show()
    urs_input= keyboard.read(__ON_CONTENT)
    return urs_input


def show_menu(title:str, options: set) -> str:
    '''
    Hiển thị interacted menu

    params:
    title: 20 ký tự là tiêu đề của màn hình
    options: đại loại là ((<Chuỗi hiển thị>, <ký tự xác nhận>), ...)
    '''

    # Hiển thị menu xong lòng vòng để chọn, hiển thị lại, etc
    display.wipe()
    start_index = [0]

    def __do_show_menu():
        '''
        Hiển thị menu trên màn hình LCD
        '''

        title_spacing = ''.join([' ' for i in range(0, 18 - len(title))]) # Lấy spacing để căn màn hình
        left_symbol = ' '
        if start_index[0] > 0: left_symbol = '<' # Có thể nhấn prev không?
        right_symbol = ' '
        if start_index[0] < len(options) - 3: right_symbol = '>' # Có thể nhấn next không?
        title_content = ''.join([title, title_spacing, left_symbol, right_symbol]) # tính lại content

        display.wipe()
        display.set_content(title_content.upper(), 0)
        showing_indexes = (i for i in range(start_index[0], start_index[0] + 3)) # tính các mục cần hiển thị
        for i, row in zip(showing_indexes, (1, 2, 3)):
            # Lần lượt fill menu options
            if i == len(options): break
            display.set_content(options[i][0].upper(), row)
        display.show()

        # clean up things - dọn sạch mọi thứ
        del title_spacing
        del left_symbol
        del right_symbol
        del title_content
        del showing_indexes

    def __next(key):
        '''
        Cập nhật vị trí hiển thị +1 xong show menu
        '''

        if start_index[0] < len(options) - 3: start_index[0]+=3
        __do_show_menu()

    def __prev(key):
        '''
        Cập nhật vị trí hiển thị -1 xong show menu
        '''

        if start_index[0] > 0:start_index[0]-=3
        __do_show_menu()

    keyboard.bind('+', __next) # Nhấn phím next
    keyboard.bind('-', __prev) # Nhấn phím prev
    break_keys = set(item[1] for item in options) # Nhấn các lựa chọn

    __do_show_menu()
    result = keyboard.wait(break_keys)
    return result
