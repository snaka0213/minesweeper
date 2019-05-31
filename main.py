#!/usr/bin/env python3

import copy, tkinter, tkinter.simpledialog
from myClass import Object, Status, BoardData, count_around, check_win, remain_mine

# objects
WALL, NONE = Object.wall, Object.none
MINE, PANEL, CHECK, OPENED = Object.mine, Object.panel, Object.check, Object.opened
obj_list = [' ', '1', '2', '3',
'4', '5', '6', '7', '8', '＊', ' ', '＃']
color_list = ['LightGray', 'Blue', 'Green', 'Red',
'Purple', 'Maroon', 'Turquoise', 'Black', 'Gray', 'Silver']

# init_showing_board
def init_showing_board(status):
    height = status.height
    width = status.width

    return [[None for j in range(width+2)]for i in range(height+2)]

# set_status
def set_status(status, level):
    if level == 1:
        return Status(10, 9, 9, 0, False)
    elif level == 2:
        return Status(40, 16, 16, 0, False)
    elif level == 3:
        return Status(99, 16, 30, 0, False)
    else:
        status.time = 0
        status.state = False
        return status

# restart_window
def restart_window():
    text = "Choose Levels (1/2/3) / Enter to Retry"
    level = tkinter.simpledialog.askstring("MineSweeper", text)
    if level == None: # is pushed "Cancel"
        end_game()
    else:
        if level == '': # is pushed "OK" without any string
            level = 0
        restart_game(int(level))

# end_game
def end_game():
    status.state = False
    check_answer(False)
    message.set("Game Over / Click to Restart")
    showing_message.unbind("<Button-1>")
    showing_message.unbind("<Button-2>")
    showing_message.bind("<Button-1>", lambda ev: restart_window())

# restart_game
def restart_game(level):
    global status, board_data, game_frame, showing_board
    status = set_status(status, level)
    board_data = BoardData(status)
    board_data.initialize()
    showing_board = init_showing_board(status)


    game_frame.destroy()
    game_frame = tkinter.Frame(root_frame, relief = 'sunken', borderwidth = 3, bg = 'LightGray')
    game_frame.pack(pady = 5, padx = 5)

    message.set("Solve / Right Click to Restart")
    showing_message.bind("<Button-1>", lambda ev: auto_solver())
    showing_message.bind("<Button-2>", lambda ev: end_game())
    timer.set(str(status.time))
    remain.set(str(status.mine))

    initialize_board()
    fitting_window(root, False)

# check_answer
def check_answer(result):
    open_board = board_data.open_board
    closed_board = board_data.closed_board
    height = status.height
    width = status.width

    for i in range(height):
        for j in range(width):
            if result == False and closed_board[i+1][j+1] == MINE:
                open_board[i+1][j+1] = MINE
                showing_board[i+1][j+1].config(
                    relief = 'ridge',
                    text = obj_list[MINE],
                    bg = 'red',
                )
            elif result == True and open_board[i+1][j+1] == PANEL and closed_board[i+1][j+1] == MINE:
                check_panel(i+1, j+1)

# open_panel
def open_panel(i, j):
    open_board = board_data.open_board
    closed_board = board_data.closed_board

    if open_board[i][j] != PANEL:
        pass
    else:
        if closed_board[i][j] == MINE:
            status.state = False
            end_game()
        else:
            if status.state == False:
                status.state = True
                start_timer()
            open_board[i][j] = count_around(closed_board, MINE, i, j)
            if open_board[i][j] == 0:
                for dx in (-1, 0, 1):
                    for dy in (-1, 0, 1):
                        if dx == 0 and dy == 0:
                            continue
                        open_panel(i+dx, j+dy)

            object = obj_list[open_board[i][j]]
            color = color_list[open_board[i][j]]
            showing_board[i][j].config(relief = 'ridge', text = object, fg = color)

        if check_win(board_data):
            status.state = False
            check_answer(True)
            message.set("Game Clear! / Click to Restart")
            remain.set(str(remain_mine(status, open_board)))
            showing_message.unbind("<Button-1>")
            showing_message.unbind("<Button-2>")
            showing_message.bind("<Button-1>", lambda ev: restart_window())

# check_panel
def check_panel(i, j):
    open_board = board_data.open_board

    board_data.check_panel(i, j)
    object = obj_list[open_board[i][j]]
    showing_board[i][j].config(text = object)
    remain.set(str(remain_mine(status, open_board)))

# open_around
def open_around(i, j):
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            if dx == 0 and dy == 0:
                continue
            else:
                open_panel(i+dx, j+dy)

# check_around
# reflect == True -> also checks on showing_board
def check_around(board, i, j, reflect):
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            if dx == 0 and dy == 0:
                continue
            else:
                if board[i+dx][j+dy] != PANEL:
                    pass
                else:
                    board[i+dx][j+dy] = CHECK
                    if reflect == True:
                        object = obj_list[CHECK]
                        showing_board[i+dx][j+dy].config(text = object)
                        remain.set(str(remain_mine(status, board)))


# open_all (for copy_board)
def open_all(board):
    height = status.height
    width = status.width

    for i in range(height):
        for j in range(width):
            if board[i+1][j+1] == PANEL:
                board[i+1][j+1] = OPENED


# check contradiction (contradict -> False)
def check_contra(board):
    height = status.height
    width = status.width

    answer = True
    for i in range(height):
        for j in range(width):
            if board[i+1][j+1] not in range(1, 9):
                continue
            elif board[i+1][j+1] < count_around(board, CHECK, i+1, j+1):
                answer = False
                break
        else:
            continue
        break

    return answer

# computer (straightforward)
def cpu_simple():
    open_board = board_data.open_board
    height = status.height
    width = status.width

    counter = 0
    while counter != height*width:
        counter = 0
        for i in range(height):
            for j in range(width):
                if open_board[i+1][j+1] in range(1, 9) and count_around(open_board, PANEL, i+1, j+1) != 0:
                    if open_board[i+1][j+1] == count_around(open_board, PANEL, i+1, j+1) + count_around(open_board, CHECK, i+1, j+1):
                        check_around(open_board, i+1, j+1, True)
                    elif open_board[i+1][j+1] == count_around(open_board, CHECK, i+1, j+1):
                        open_around(i+1, j+1)
                    else:
                        counter += 1
                else:
                    counter += 1


# computer (for copy_board)
def cpu_virtual(board):
    height = status.height
    width = status.width

    counter = 0
    while counter != height*width:
        counter = 0
        for i in range(height):
            for j in range(width):
                if board[i+1][j+1] in range(1, 9) and count_around(board, PANEL, i+1, j+1) != 0:
                    if board[i+1][j+1] == count_around(board, PANEL, i+1, j+1) + count_around(board, CHECK, i+1, j+1):
                        check_around(board, i+1, j+1, False)
                    elif board[i+1][j+1] == count_around(board, CHECK, i+1, j+1):
                        for dx in (-1, 0, 1):
                            for dy in (-1, 0, 1):
                                if dx == 0 and dy == 0:
                                    continue
                                else:
                                    if board[i+1+dx][j+1+dy] != PANEL:
                                        pass
                                    else:
                                        board[i+1+dx][j+1+dy] = OPENED
                    else:
                        counter += 1
                else:
                    counter += 1

        if remain_mine(status, board) == 0:
            open_all(board)
            break


# computer (use contradiction)
def cpu_contra():
    open_board = board_data.open_board
    height = status.height
    width = status.width

    counter = 0
    while counter!= height*width:
        counter = 0
        for i in range(height):
            for j in range(width):
                if open_board[i+1][j+1] == PANEL:
                    copy_board = copy.deepcopy(open_board)
                    copy_board[i+1][j+1] = CHECK
                    cpu_virtual(copy_board)
                    if check_contra(copy_board) == False:
                        open_panel(i+1, j+1)
                        cpu_simple()
                    else:
                        counter += 1
                else:
                    counter += 1


# auto_solver
def auto_solver():
    cpu_simple()
    cpu_contra()

# timer
def start_timer():
    if status.state == False:
        pass
    else:
        status.time += 1
        root.after(1000, start_timer)
        timer.set(str(status.time))

# initialize_board
def initialize_board():
    height = status.height
    width = status.width

    for i in range(height):
        for j in range(width):
            label = tkinter.Label(game_frame)
            label.coordinate = (i+1, j+1)
            label.config(
                height = 1, width = 2, bd = 2,
                bg = 'LightGray', relief = 'raised',
            )
            label.bind("<Button-1>", lambda ev: open_panel(ev.widget.coordinate[0], ev.widget.coordinate[1]))
            label.bind("<Button-2>", lambda ev: check_panel(ev.widget.coordinate[0], ev.widget.coordinate[1]))
            label.grid(row = i, column = j)
            showing_board[i+1][j+1] = label


# fitting_window
# centering == True -> also centering_window
def fitting_window(window, centering):
    window.update_idletasks()
    window_width = window.winfo_reqwidth()
    window_height = window.winfo_reqheight()
    window.geometry('{}x{}'.format(window_width, window_height))

    if centering == True:
        x = window.winfo_screenwidth() // 2 - window_width // 2
        y = window.winfo_screenheight() // 2 - window_height // 2
        window.geometry('+{}+{}'.format(x, y))

    window.deiconify()

# global parameters
status = Status(mine = 10, width = 9, height = 9, time = 0, state = False)
board_data = BoardData(status)
board_data.initialize()

# frame
root = tkinter.Tk()
root.title("MineSweeper")

root_frame = tkinter.Frame(root, relief = 'ridge', bg = 'LightGray')
status_frame = tkinter.Frame(root_frame, relief = 'sunken', borderwidth = 3, bg = 'LightGray')
game_frame = tkinter.Frame(root_frame, relief = 'sunken', borderwidth = 3, bg = 'LightGray')
root_frame.pack()
status_frame.pack(pady = 5, padx = 5, fill = 'x')
game_frame.pack(pady = 5, padx = 5)

# message
message = tkinter.StringVar()
message.set("Solve / Right Click to Restart")
showing_message = tkinter.Label(
    status_frame,
    textvariable = message,
    bg = 'LightGray', bd = 2,
    relief = 'raised',
)
showing_message.pack(fill = 'x')

# remain_mine
remain = tkinter.StringVar()
remain.set(str(status.mine))
showing_remain = tkinter.Label(
    status_frame,
    textvariable = remain, width = 5,
    bg = 'LightGray',
)
showing_remain.pack(side = 'left')

# time
timer = tkinter.StringVar()
timer.set(str(status.time))
showing_time = tkinter.Label(
    status_frame,
    textvariable = timer, width = 5,
    bg = 'LightGray',
)
showing_time.pack(side = 'right')

# restart_button
showing_message.bind("<Button-1>", lambda ev: auto_solver())
showing_message.bind("<Button-2>", lambda ev: end_game())

# showing_board
showing_board = init_showing_board(status)

# main
if __name__ == '__main__':
    initialize_board()
    fitting_window(root, True)
    root.mainloop()
