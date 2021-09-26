from cli import get_input, get_input_lst, file_explorer
import csv
from main import Table
import json

def ask_input(prompt,func_call):


    while True:
        print(prompt)
        rt = func_call()
        x = input("Continue? (y/n)")
        if x in ["y", "n"]:
            if x == "y":
                break
            else:
                print("ok")
        else:
            print("Enter a valid input.")
    return rt

usin = {"row":2, "row_names":["test1","test2"],"row_no":[[2,3],[4,5]],
        "column":2, "column_names":["a1","a2"],
        "class":"IETLS Reading","name":0,"email":1
        }
#r = [["Thiha Swan Htet", "misterjames.thiha@gmail.com",4,9,3,9 ]]
print("Certifyx 0.6.2")


usin["class"] = ask_input("Enter class' name:\n",input)
usin["name"] = ask_input("Enter column index of which the student name is located:\n",get_input)
usin["email"] = ask_input("Enter column index of which the email is located:\n",get_input)

usin["row"] = ask_input("How many tests?:\n",get_input)

lst = []
for i in range(usin["row"]):
    lst.append(ask_input(f"Enter row{i+1}'s name:\n",input))
usin["row_names"] = lst


usin["column"] = ask_input("How many columns for each test?:\n",get_input)

lst = []
for i in range(usin["column"]):
    lst.append(ask_input(f"Enter column{i+1}'s name:\n",input))
usin["column_names"] = lst


lst1 = []
for i in usin["row_names"]:
    lst = []
    for j in usin["column_names"]:
        x = ask_input(f"Enter column index for {j} in {i}:\n",get_input)
        lst.append(x)
    lst1.append(lst)

#open("input.json","w").write(json.dumps(lst1))
usin["row_no"] = lst1

usin["file"]  = ask_input("Choose your csv file:\n",file_explorer)

r = csv.reader(open(usin['file'],"r",encoding="utf-8"))
r = [i for i in r]

for i in r:


    x = Table(usin["row"], usin["column"], i[usin["name"]], i[usin["email"]],usin["class"])
    x.create_table(usin["class"])
    x.place_peri(usin["row_names"], "verti")
    x.place_peri(usin["column_names"], "hori")

    c = 0

    for j in usin["row_no"]:
        lst = []
        for o in j:

            lst.append((i[o]))
        x.place_band(lst,c)
        c+=1

    x.trend_n_overall()
    x.save()

print(usin)
input("Press enter to quit.")









