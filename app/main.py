# Importing libraries
import math
from tkinter import *
from tkinter import filedialog, _setit
import os
import pandas as pd
from helpers.file_handler import *
from btree.bplus_tree_data_structure import BTree
from collections import deque
import time
import threading

# Global parameters and store
keys = ['-']
data = pd.DataFrame()
b_tree = BTree(t=6, field="ID")

# Functions
def select_key(value): # this is data filter value
    selectedKey.set(value)
def open_file_dialog():
    statusLabel.config(text="Đang tải file")
    global data
    global keys
    file_path = filedialog.askopenfilename(title="Chọn 1 file", filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
    if file_path:
        file_name = os.path.basename(file_path)
        data = file_to_df(file_path)
        keys = list(data.columns)
        fileNameLabel.config(text=file_name)
        print("Selected file:", file_path)
        print("Data retrieved")
        keyMenu['menu'].delete(0, 'end')
        for option in keys:
            keyMenu['menu'].add_command(label=option, command=_setit(selectedKey, option))
    statusLabel.config(text="Idle")

def build_visual_tree():
    global b_tree
    deg = int(maxDegEntry.get())
    print(deg)
    field = selectedKey.get()
    b_tree = BTree(t=deg, field=field)
    tree_keys = list(data["ID"])
    tree_names = list(data["Name"])
    tree_scores = list(data["Score"])

    for _id, data1, data2 in zip(tree_keys, tree_names, tree_scores):
        print(_id, data1, data2)
        if field == "ID":
            b_tree.insert((_id, {"ID": _id, "Name": data1, "Score": data2}))
        elif field == "Name":
            b_tree.insert((data1, {"ID": _id, "Name": data1, "Score": data2}))
        elif field == "Score":
            b_tree.insert((data2, {"ID": _id, "Name": data1, "Score": data2}))
    statusLabel.config(text="Đang tạo cây")
    display(b_tree, level=0, canv=visualizer)
    # b_tree.display()
    statusLabel.config(text="IDLE")

def display(tree=None, level=0, canv=None, highlight_node=[]):
    canv.delete("all")
    canvas_height = canv.winfo_height()
    canvas_width = canv.winfo_width()
    print("display ran")
    queue = deque()
    queue.append({"node": tree.root, "parent": None})
    # Draw nodes
    while queue:
        level_size = len(queue)
        level_nodes = []


        for i in range(level_size):
            item = queue.popleft()
            parent_coords = item["parent"]
            node = item["node"]
            # Draw node
            text_x = level * 200 + 70
            text_y = (canvas_height / 2) - level_size / 2 * 50 + i * 40
            if node in highlight_node:
                canv.create_text(text_x, text_y, text=str([item[0] for item in node.keys]), font=("Arial", 14, "bold"), fill="red")
            else:
                canv.create_text(text_x, text_y, text=str([item[0] for item in node.keys]), font=("Arial", 12), fill="black")
            if parent_coords:
                canv.create_line(parent_coords[0] + 20 * parent_coords[2], parent_coords[1], text_x - 40 * len(node.keys) / 2, text_y, width=2, fill="black")
            # print(f'Drew node: {node.keys}', level, (canvas_height / 2) - level_size / 2 * 80 + i * 70)
            level_nodes.append(node)

            if node.child:
                for child in node.child:
                    queue.append({"node": child, "parent": (text_x, text_y, len(node.keys))})
        level += 1
    # Delay
    # time.sleep(1)
    return

def search_with_highlights(tree, key, node=None, canv=None):
    # local key is search value, regarding data_col
    if node is None:
        node = tree.root
    path = []
    data_col = selectedKey.get()
    queue = deque()
    queue.append(tree.root)
    path.append(tree.root)
    while queue:
        node = queue.popleft()
        i = 0
        while i < len(node.keys) and key > node.keys[i][0]:
            i += 1
        if i < len(node.keys) and key == node.keys[i][0]:
            display(tree=tree, canv=canv, highlight_node=path)
            return node
        elif node.child:
            queue.append(node.child[i])
            path.append(node.child[i])
        else:
            display(tree=tree, canv=canv, highlight_node=path)
            return None

def _threading_display():
    display(b_tree, canv=visualizer)
def _threading_highlight_display(value):
    search_with_highlights(b_tree, key=value, canv=visualizer)

def run_search():
    statusLabel.config(text="Đang tìm khóa")
    key = selectedKey.get()
    search_value = searchValueEntry.get()
    if key != "Name":
        search_value = float(searchValueEntry.get())
    result = search_with_highlights(b_tree, search_value, canv=visualizer)
    if result is not None:
        # print(result.keys)
        item = [f"{item['ID']} {item['Name']} {item['Score']}" for key, item in result.keys]
        resultVar.set("\n".join(item))
    else:
        # print("khong tim thay")
        resultVar.set("Không có node này")
    statusLabel.config(text="IDLE")


def run_delete():
    data_col = selectedKey.get()
    delete_value = float(deleteValueEntry.get())
    result = search_with_highlights(b_tree, delete_value, canv=visualizer)
    statusLabel.config(text="Đang xóa khóa")
    timer = threading.Timer(1.0, _threading_display)
    timer.start()
    b_tree.delete(b_tree.root, delete_value)
    if result is not None:
        # print(result.keys)
        strg = "\n".join([f"{item['ID']} {item['Name']} {item['Score']}" for key, item in result.keys])
        resultVar.set(strg)
    else:
        # print("khong tim thay")
        resultVar.set("Không có node này")
    statusLabel.config(text="IDLE")

def run_insert():
    _id = float(idValueEntry.get())
    name = nameValueEntry.get()
    score = float(scoreValueEntry.get())
    # print(_id, name, score)
    field = selectedKey.get()
    statusLabel.config(text="Đang thêm")
    search_value = ""
    if field == "ID":
        search_value = _id
    elif field == "Name":
        search_value = name
    elif field == "Score":
        search_value = score
    search_with_highlights(b_tree, key=search_value, canv=visualizer)


    if field == "ID":
        b_tree.insert((_id, {"ID": _id, "Name": name, "Score": score}))
    elif field == "Name":
        b_tree.insert((name, {"ID": _id, "Name": name, "Score": score}))
    elif field == "Score":
        b_tree.insert((score, {"ID": _id, "Name": name, "Score": score}))

    timer = threading.Timer(1.0, _threading_display)
    timer.start()
    def timer_func():
        _threading_highlight_display(search_value)

    timer_2 = threading.Timer(2.0, timer_func)
    timer_2.start()

    statusLabel.config(text="IDLE")

def write_file():
    # write_to_file(data)
    result = b_tree.traverse()
    array_csv = []
    for node in result:
        for key_data in node.keys:
            array_csv.append([key_data[1]['ID'], key_data[1]['Name'], key_data[1]['Score']])
    df = pd.DataFrame(array_csv, columns=['ID', 'Name', 'Score'])
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if not file_path:
        print("Cancelled")
    else:
        df.to_csv(file_path, index=False)

# Main UI
win = Tk()
win.title("B Tree Indexing Simulator")
win.geometry("1200x800")

# --------------------- Widgets -------------------------------

titleText = "B Tree Data Indexer"
titleLabel = Label(win, text=titleText, font=('consolas', 30), bg='light gray', fg='dark green', height=2, width=20, pady=10, padx=20)
titleLabel.pack()

containerFrame = Frame(win)
containerFrame.pack()

# Side frames
leftFrame = Frame(containerFrame, borderwidth=2, relief="flat", bg="white")
leftFrame.grid(row=0,column=0)
inputFrame = Frame(leftFrame, borderwidth=2, relief="groove", bg="white")
inputFrame.grid(row=0,column=0)
visualFrame = Frame(containerFrame, borderwidth=2, relief="flat", bg="blue")
visualFrame.grid(row=0,column=1)
resultFrame = Frame(leftFrame, borderwidth=3, relief="ridge", bg="white", width=500, height=250)
resultFrame.grid(row=2, column=0)
statusLabel = Label(leftFrame, text="Idle", font=('consolas', 16), bg='white', fg='black', pady=20, padx=20)
statusLabel.configure(relief="solid", borderwidth=2, bg="light yellow")
statusLabel.grid(row=1, column=0)

# Widgets to left side
openFileButton = Button(inputFrame, text="Chọn file", command=open_file_dialog)
fileNameLabel = Label(inputFrame, text="filename.csv", font=('consolas', 16), bg='white', fg='green')

keySelectLabel = Label(inputFrame, text="Chọn key", font=('arial', 16), bg='white', fg='black')
selectedKey = StringVar()
keyMenu = OptionMenu(inputFrame, selectedKey, *keys, command=select_key)

buildTreeButton = Button(inputFrame, text="Dựng cây", command=build_visual_tree)
maxDegLabel = Label(inputFrame, text="Nhập min degree", font=('arial', 16), bg='white', fg='black')
maxDegEntry = Entry(inputFrame)


# Search area
searchAreaLabel = Label(inputFrame, text="Tìm kiếm", font=('consolas', 20), bg='white', fg='black', pady=10, padx=20)
searchValueLabel = Label(inputFrame, text="Nhập giá trị tìm kiếm", font=('arial', 16), bg='white', fg='black')
searchValueEntry = Entry(inputFrame)
runButton = Button(inputFrame, text="Tìm kiếm", command=run_search)

# Delete area
deleteAreaLabel = Label(inputFrame, text="Xóa", font=('consolas', 20), bg='white', fg='black', pady=10, padx=20)
deleteValueLabel = Label(inputFrame, text="Nhập giá trị cần xóa", font=('arial', 16), bg='white', fg='black')
deleteValueEntry = Entry(inputFrame)
runDeleteButton = Button(inputFrame, text="Xóa", command=run_delete)

# Insert area
insertAreaLabel = Label(inputFrame, text="Thêm record", font=('consolas', 20), bg='white', fg='black', pady=10, padx=20)
idValueLabel = Label(inputFrame, text="ID", font=('arial', 16), bg='white', fg='black')
idValueEntry = Entry(inputFrame)
nameValueLabel = Label(inputFrame, text="Tên", font=('arial', 16), bg='white', fg='black')
nameValueEntry = Entry(inputFrame)
scoreValueLabel = Label(inputFrame, text="Điểm", font=('arial', 16), bg='white', fg='black')
scoreValueEntry = Entry(inputFrame)
runInsertButton = Button(inputFrame, text="Thêm", command=run_insert)

# Result area
resultVar = StringVar()
resultVar.set("")
resultAreaLabel = Label(resultFrame, text="Kết quả", font=('Arial', 20), bg='white', fg='light green', pady=10, padx=20)
resultLabel = Label(resultFrame, textvariable=resultVar, font=('consolas', 14), bg='white', fg='black', pady=10, padx=20)
saveFile = Button(resultFrame, text="Lưu file", command=write_file)

# Widgets placing
openFileButton.grid(row=0,column=1)
fileNameLabel.grid(row=0, column=0)
keySelectLabel.grid(row=1, column=0)
keyMenu.grid(row=1, column=1)
buildTreeButton.grid(row=1, column=2)

maxDegLabel.grid(row=2, column=0)
maxDegEntry.grid(row=2, column=1)

searchAreaLabel.grid(row=3, column=0, columnspan=3)
searchValueLabel.grid(row=4, column=0)
searchValueEntry.grid(row=4,column=1)
runButton.grid(row=5, column=1)

deleteAreaLabel.grid(row=6,column=0, columnspan=3)
deleteValueLabel.grid(row=7,column=0)
deleteValueEntry.grid(row=7,column=1)
runDeleteButton.grid(row=8,column=1)

insertAreaLabel.grid(row=9,column=0, columnspan=3)
idValueLabel.grid(row=10,column=0)
idValueEntry.grid(row=11,column=0)
nameValueLabel.grid(row=10,column=1)
nameValueEntry.grid(row=11,column=1)
scoreValueLabel.grid(row=10,column=2)
scoreValueEntry.grid(row=11,column=2)
runInsertButton.grid(row=12,column=1)

resultAreaLabel.pack()
resultLabel.pack()
saveFile.pack()
selectedKey.set(keys[0])
# Widget to right side
visualizer = Canvas(visualFrame, height='600', width='600', bg="white")
visualizer.grid(row=0,column=0, rowspan=1, columnspan=1)




# --------------------- Widgets END -------------------------------

# App loop
win.mainloop()