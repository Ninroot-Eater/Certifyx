import os
import pathlib

def file_explorer():
    home_path = pathlib.Path("C:/Users")
    def print_current_dir(path):
        for i in os.listdir(path):
            print(i)
        print("\nCWD:",path)

    print_current_dir(home_path)
    print("#####################")
    while True:


        current_dir_lst = ["."]
        for i in os.listdir(home_path):
            current_dir_lst.append(i)

        x = input(">>>")

        if x in current_dir_lst:
            if x != ".":
                home_path = home_path / x
                try:
                    print_current_dir(home_path)
                except NotADirectoryError:

                    return home_path



            elif x == ".":
                home_path = home_path.parent
                try:
                    print_current_dir(home_path)
                except NotADirectoryError:
                    print(home_path)
                    return home_path

        else:
            print("\nNo such file or directory named '{0}'".format(x))

def int_check(usr_in):
    try:
        int(usr_in)
        return True
    except ValueError:
        return False

def get_input(uni_lst=[]):
    if uni_lst is None:
        uni_lst = []
    while True:
        x = input(">>>")
        if int_check(x):
            if int(x) not in uni_lst:
                return int(x)
            else:
                print("The index is already used.")
        else:
            print("Please enter a number.")

def get_input_lst(count:int,uni_lst):

    lst = []
    for i in range(count):

        while True:
            print("Enter the column index from the parent file:\n")
            x = get_input()

            print("Enter the column index for the baby file:\n")
            y = get_input(uni_lst)

            if y not in uni_lst:
                lst.append((y,x))
                uni_lst.append(y)
                break
            else:
                pass
    return (lst,uni_lst)




