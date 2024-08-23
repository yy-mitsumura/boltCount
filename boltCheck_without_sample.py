import os
import math
import tkinter as tk
from tkinter import ttk
douitsu_angle=0.05
douitsu_length=1
ci_abs=1e-2
jogai_diff=1

def segments_are_close(seg1, seg2, tol):
    return (
        math.isclose(seg1[0], seg2[0], rel_tol=0, abs_tol=tol) and
        math.isclose(seg1[1], seg2[1], rel_tol=0, abs_tol=tol) and
        math.isclose(seg1[2], seg2[2], rel_tol=0, abs_tol=tol) and
        math.isclose(seg1[3], seg2[3], rel_tol=0, abs_tol=tol)
    )
def chushutu(file):

    found_hashtag = False
    lines_after_hashtag = []  # 結果を格納するリスト
    for line in file:
        stripped_line = line.strip()
        if stripped_line == '#': # '#'行を見つける
            found_hashtag = True
        elif found_hashtag and line.startswith(' '):  # 先頭が半角スペースの行を処理する条件に変更
            lines_after_hashtag.append(stripped_line)
    
    #近似していたら除外する
    new_list = []
    idx_num_list = []
    new_list4=[]
    for var in lines_after_hashtag:
        new_list.append(var.split())
    new_list = [[float(x) for x in sublist] for sublist in new_list]
    for i in range(len(new_list)):
        x1, y1, x2, y2 = new_list[i]
        if (x1>x2) or (x1 == x2 and y1 > y2):
            new_list4.append([x2, y2, x1, y1])
        else:
            new_list4.append(new_list[i])

    for i in range(len(new_list4)):
        for j in range(i+1, len(new_list4)):
                if segments_are_close(new_list4[i], new_list4[j], jogai_diff):
                    idx_num_list.append(i)    

    for i,var in enumerate(new_list4):
        
        print(var, math.atan2(new_list4[i][3] - new_list4[i][1], new_list4[i][2] - new_list4[i][0]), math.sqrt((new_list4[i][2] - new_list4[i][0])**2 + (new_list4[i][3] - new_list4[i][1])**2))            
    indices_to_remove = set(tuple(idx_num_list))
    new_list2 = [x for i, x in enumerate(new_list) if i not in indices_to_remove]
    lines_after_hashtag2 = [" ".join(str(x) for x in sublist) for sublist in new_list2]
    #ciの処理
    ci_list=[]
    file.seek(0)
    found_hashtag2 = False
    for line2 in file:

        stripped_line2 = line2.strip()
      
        if stripped_line2 == '#': # '#'行を見つける
            found_hashtag2 = True
        elif found_hashtag2 and line2.startswith('ci'):  # 先頭が半角スペースの行を処理する条件に変更
            ci_list.append(stripped_line2)    


    ci_new_list=[]
    ci_idx_num_list=[]
    for var in ci_list:
        ci_new_list.append(var.split())
    for i in range(len(ci_new_list)):
        for j in range(i+1, len(ci_new_list)):
            if math.isclose(float(ci_new_list[i][1]), float(ci_new_list[j][1]), rel_tol=0, abs_tol=ci_abs) and math.isclose(float(ci_new_list[i][2]), float(ci_new_list[j][2]), rel_tol=0, abs_tol=ci_abs): #同じような座標の時に　#この行を省くと座標問わず同じ半径の処理になってしまう
                if math.isclose(float(ci_new_list[i][3]), float(ci_new_list[j][3]), rel_tol=0, abs_tol=ci_abs)==True: #同じような半径の時に
                    ci_idx_num_list.append(i)
    indices_to_remove2 = set(tuple(ci_idx_num_list))
    ci_new_list2 = [x for i, x in enumerate(ci_new_list) if i not in indices_to_remove2]
    ci_lines_after_hashtag = [" ".join(str(x) for x in sublist) for sublist in ci_new_list2]
    lines_after_hashtag2.extend(ci_lines_after_hashtag)    
    return lines_after_hashtag2

def are_lines_equal(line1, line2):
    if line1.split()[0]=="ci" or line2.split()[0]=="ci":
        if line1.split()[3] == line2.split()[3]:

            return True
        else:
            return False
    x1, y1, x2, y2 = map(float, line1.split())
    x3, y3, x4, y4 = map(float, line2.split())

    angle1 = math.atan2(y2 - y1, x2 - x1)
    if angle1 < 0:
        angle1 = angle1 + math.pi
    angle2 = math.atan2(y4 - y3, x4 - x3)
    if angle2 < 0:
        angle2 = angle2 + math.pi


    if math.isclose(angle1, angle2, rel_tol=0, abs_tol=douitsu_angle): 
        length1 = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        length2 = math.sqrt((x4 - x3)**2 + (y4 - y3)**2)
        if math.isclose(length1, length2, rel_tol=0, abs_tol=douitsu_length):

            return True
    elif math.isclose(angle1+math.pi, angle2, rel_tol=0, abs_tol=douitsu_angle):

        length1 = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        length2 = math.sqrt((x4 - x3)**2 + (y4 - y3)**2)
        if math.isclose(length1, length2, rel_tol=0, abs_tol=douitsu_length):

            return True
    elif math.isclose(angle1-math.pi, angle2, rel_tol=0, abs_tol=douitsu_angle):

        length1 = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        length2 = math.sqrt((x4 - x3)**2 + (y4 - y3)**2)
        if math.isclose(length1, length2, rel_tol=0, abs_tol=douitsu_length):

            return True

    return False



def count_equal_lines(check_list, target_list):
    result_dict = {}

    for check_line in check_list:
        count = 0
        for target_line in target_list:
            if are_lines_equal(check_line, target_line):
                count += 1
        result_dict[check_line] = count

    root = tk.Tk()
    root.geometry("400x300+0+0")
    root.attributes("-topmost",True)
    root.bind("<Enter>", lambda event: root.destroy())
    root.bind("<Return>", lambda event: root.destroy())
    root.bind("<Escape>", lambda event: root.destroy())
    lb = tk.Label(root, font=("", 30))
    tb=ttk.Treeview(root)
    tb["columns"] = ("本数", "x1", "y1", "x2", "y2")
    tb.column("#0", width=0)
    tb.column("本数", width=25)
    tb.column("x1", width=50)
    tb.column("y1", width=50)
    tb.column("x2", width=50)
    tb.column("y2", width=50)    
    tb.heading("本数", text="本数")
    tb.heading("x1", text="x1")
    tb.heading("y1", text="y1")
    tb.heading("x2", text="x2")
    tb.heading("y2", text="y2")
    scllbr = tk.Scrollbar(root)
    lb.pack()
    scllbr.pack(side=tk.RIGHT, fill=tk.Y)
    scllbr.config(command=tb.yview)
    tb.pack(expand=True, fill="both")
    def sort_treeview(tree, col, reverse):
        data = [(int(tree.set(child, col)), child) for child in tree.get_children("")]
        data.sort(reverse=reverse)

        for index, (val, child) in enumerate(data):
            tree.move(child, "", index)

        tree.heading(col, command=lambda: sort_treeview(tree, col, not reverse))

    if len(set(result_dict.values()))==1:
        lb.config(text=list(result_dict.values())[0])
        tb.pack_forget()
        scllbr.pack_forget()
    else:
        lb.config(text="線分の組み合わせが\n一致しません")
        inserted_values=set()
        for line, count in result_dict.items():
            if count not in inserted_values:
                lines = line.split()
                tb.insert("","end",text="",values=(int(count), lines[0], lines[1], lines[2], lines[3]))
                inserted_values.add(count)
    sort_treeview(tb, "本数", True)
    for var in result_dict:
        print(var)
    root.mainloop()
def func():
    with open("JWC_TEMP.TXT") as file:
        check_list = list(set(chushutu(file)))
    with open("JWC_TEMP.TXT") as file:
        target_list = list(set(chushutu(file)))

    count_equal_lines(check_list, target_list)


func()