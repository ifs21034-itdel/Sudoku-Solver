import tkinter as tr
import re


def ceksudoku(board):
    for y in range(9):
        for x in range(9):
            if board[y][x] > 9:
                return False

            if board[y][x] != 0 and board[y].count(board[y][x]) > 1:
                return False

            for col in range(9):
                if board[y][x] != 0 and col != y:
                    if board[col][x] == board[y][x]:
                        return False

            for i in range(3):
                for j in range(3):
                    if board[y][x] != 0 and (i + 3 * (y // 3), j + 3 * (x // 3)) != (y, x):
                        if board[i + 3 * (y // 3)][j + 3 * (x // 3)] == board[y][x]:
                            return False
    return True


def get_sudoku():
    window = tr.Tk() # Membuat jendela utama dengan tkinter
    window.title('Solve a Sudoku')
    window.geometry('600x450')

    width = 3
    labels = []
    entrys = []
    sudoku = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0]]

    for i in range(81):
        entrys.append(tr.Entry(window, width=width)) # Membuat kotak input dengan tkinter
        labels.append(tr.Label(window, width=3, height=1, bg='white')) # Membuat label dengan tkinter

    l1 = tr.Label(window, text='SUDOKU SOLVER MENGGUNAKAN HEURISTIK', bg='white', font=('Arial', 9)) # Membuat label dengan tkinter
    l1.place(x='10', y='15')

    l2 = tr.Label(window, text='inputkan angka-angka pada sudoku di bawah!', bg='yellow', font=('Arial', 11))
    l2.place(x='10', y='43')

    b1 = tr.Button(window, text='Cari Solusi', bg='white', activebackground='orange', font=(
        'Arial', 12), command=lambda: get_data())  # Membuat tombol dengan tkinter
    b1.place(x='230', y='320')

    b2 = tr.Button(window, text='Reset', bg='white', activebackground='orange', font=(
        'Arial', 12), command=lambda: bersihkan_data())
    b2.place(x='20', y='320')

    l0 = tr.Label(window, text='Data entry tidak valid!', font=('Arial', 20))

    for e in entrys:
        e.place(x=str(entrys.index(e) % 9 * 28 + entrys.index(e) // 3 % 3 * 6 + 20),
                y=str(entrys.index(e) // 9 * 24 + entrys.index(e) // 27 * 6 + 70))

    def get_data():
        for e in entrys:
            sudoku[entrys.index(e) // 9][entrys.index(e) % 9] = int(e.get()) if re.match('\d+', e.get()) else 0

        apply_singleton_heuristic(sudoku)  # Terapkan heuristic Singleton sebelum mencari solusi

        if ceksudoku(sudoku):
            data = sudoku
            data_list = data_list_filter(data, buat_data_list(data), 0)
            newdata = fill_num(data, data_list, 0)

            cetaksudoku(newdata)
            l0.place(x='-350', y='-150')
            for l in labels:
                labels[labels.index(l)]['text'] = newdata[labels.index(
                    l) // 9][labels.index(l) % 9]
                l.place(x=str(labels.index(l) % 9 * 28 + labels.index(l) // 3 % 3 * 6 + 300),
                        y=str(labels.index(l) // 9 * 24 + labels.index(l) // 27 * 6 + 70))
        else:
            print('Error!, Periksa data tidak valid.')
            for l in labels:
                l.place(x='-100', y='-100')
            l0.place(x='310', y='160')

    def bersihkan_data():
        for e in entrys:
            e.delete(0, 10)

    window.mainloop()


def cetaksudoku(data):
    for i in range(9):
        for j in range(9):
            print('{:^3}'.format(data[i][j]), end='')
        print('')
    print('')


def buat_data_list(data):
    data_list = []
    for y in range(9):
        for x in range(9):
            if data[y][x] == 0:
                data_list.append([(x, y), [1, 2, 3, 4, 5, 6, 7, 8, 9]])
    return data_list


def judge(data, x, y, num):
    if data[y].count(num) > 0:  # Line
        return False

    for col in range(9):  # Kolom
        if data[col][x] == num:
            return False

    for a in range(3):  # Kotak 3x3
        for b in range(3):
            if data[a + 3 * (y // 3)][b + 3 * (x // 3)] == num:
                return False
    return True


def data_list_filter(data, data_list, start):
    for blank_index in range(start, len(data_list)):
        data_list[blank_index][1] = []
        for num in range(1, 10):
            if judge(data, data_list[blank_index][0][0], data_list[blank_index][0][1], num):
                data_list[blank_index][1].append(num)
    return data_list


def fill_num(data, data_list, start):
    if start < len(data_list):
        one = data_list[start]
        for num in one[1]:
            if judge(data, one[0][0], one[0][1], num):
                data[one[0][1]][one[0][0]] = num
                tem_data = fill_num(data, data_list, start + 1)
                if tem_data != None:
                    return tem_data
        data[one[0][1]][one[0][0]] = 0
    else:
        return data

def apply_singleton_heuristic(data):
    # Fungsi untuk menerapkan heuristic "Singleton"
    for y in range(9):
        for x in range(9):
            if data[y][x] == 0:
                possibilities = list(range(1, 10))
                for num in range(1, 10):
                    if not judge(data, x, y, num):
                        possibilities.remove(num)
                if len(possibilities) == 1:
                    data[y][x] = possibilities[0]

if __name__ == '__main__':
    try:
        get_sudoku()
    except:
        print('Error! Cek kembali data anda~')
