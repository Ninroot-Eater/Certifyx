from PIL import Image, ImageDraw, ImageFont
import random
from math import ceil
import csv

class Table:
    fontsx = {"band": ImageFont.truetype("LibreBaskerville-Regular.ttf", size=45),
              "title": ImageFont.truetype("LibreBaskerville-Bold.ttf", size=55),
              "cred": ImageFont.truetype("LibreBaskerville-Regular.ttf", size=35),
              "comment": ImageFont.truetype("LibreBaskerville-Regular.ttf", size=25),
              "hori":ImageFont.truetype("LibreBaskerville-Regular.ttf", size=35)

              }

    colors = {"black": "rgb(0, 0, 0)", "name_blue": "rgb(25, 27, 109)", "red": "rgb(210,19,26)"}

    mapperv = {(0, 3): ["You need some major improvements.",
                        "You should try harder."],
               (3, 5.5): ["More improvements needed.",
                          "You need more practice."],
               (5.5, 7): ["Good job. Can get higher bands if you keep trying.",
                          "Satisfactory. More practice would help you get higher bands."],
               (7, 9): ["Very good! Keep up the good work.",
                        "Keep it up! Excellent."]}

    mappert = {0: ["Your progress has neither increased nor decreased.",
                   "No trend in the progress can be seen."],
               0.5: ["A sign of slight increase in the progress can be seen.",
                     "You have improved slightly."],
               1.0: ["You have improved steadily.",
                     "Your steady improvement can be seen."],
               1.5: ["You have progressed in this skill.",
                     "Your positive progress can be seen."],
               2.0: ["Your progress in this skill has improved a lot"],
               "over": ["Your skill has improved drastically.",
                        "A dramatic increase in scores can be seen."
                        ],
               -0.5: ["Your progress has decreased slightly.",
                      "A slight decrease in progress."],
               -1.0: ["Your progress has decreased. Try harder!",
                      "You need to try harder."],
               -1.5: ["Your skill has declined. Need to try harder."],
               -2.0: ["Your skill has declined greatly. Need to study more.",
                      "A major decline. Study more!"],
               "below": ["A dramatic decline. You should continue studying.",
                         "Huge decline in your progress. Study more!"]}
    overall_mapper = {
        0: "Not enough data to give a remark.",
        1: "No ability to use the language except a few isolated words.",
        2: "Have great difficulty understanding spoken and written English.",
        3: "Convey and understand only general meaning in very familiar situations.Frequent breakdowns in communication.",
        4: "Basic competence is limited to familiar situations. Frequently show problems in understanding and expression. Not able to use complex language.",
        5: "Have a partial command of the language, and cope with overall meaning in most situations. Able to handle basic communication in your own field.",
        6: "Have an effective command of the language despite some inaccuracies. Can use and understand fairly complex language in familiar situations.",
        7: "Have an operational command of the language, though with occasional inaccuracies, inappropriate usage and misunderstandings in some situations.",
        8: "Have a fully operational command of the language. Occasional unsystematic inaccuracies and inappropriate usage. Handles complex detailed argumentation well.",
        9: "You have a full operational command of the language. Your use of English is appropriate, accurate and fluent, and you show complete understanding."

    }

    def __init__(self,row:int,col:int,name:str,email:str,cls_name:str,width=5,border_color="#000000"):

        self.row = row + 1
        self.col = col + 1
        self.name = name
        if self.email in [None,'']:
            self.email = " "
        else:
            self.email = email
        self.cls_name = cls_name
        self.output = "ok"

        self.width = width
        self.border_color = border_color

        self.img_name = "test.png"
        self.img = Image.open(self.img_name)

        self.pairsx = []
        self.pairsy = []

        self.row_start_pos = 250
        self.col_start_pos = 400

        self.row_sz = (self.img.size[1] - self.row_start_pos - (40*self.row)) / self.row
        self.col_sz = (self.img.size[0] - (self.col*100)) / self.col

        self.array = []


        self.draw = ImageDraw.Draw(self.img)

    def create_table(self,cls_name):

        draw = self.draw



        row_start_pos = self.row_start_pos
        col_start_pos = self.col_start_pos

        draw.line((col_start_pos, row_start_pos, col_start_pos, self.img.size[1]),
                  fill=self.border_color, width=self.width)
        col_sz = self.col_sz
        for i in range(self.col):
            self.pairsy.append((col_start_pos + (col_sz/2)))

            draw.line((col_start_pos, row_start_pos, col_start_pos, self.img.size[1]), fill=self.border_color, width=self.width)
            col_start_pos += col_sz

        draw.line((0, row_start_pos, self.img.size[0], row_start_pos),
                  fill=self.border_color, width=self.width)
        row_start_pos += 150
        draw.line((0, row_start_pos, self.img.size[0], row_start_pos), fill=self.border_color, width=self.width)
        row_sz = self.row_sz
        for i in range(self.row):
            self.pairsx.append(row_start_pos + (row_sz/2))

            draw.line((0, row_start_pos, self.img.size[0], row_start_pos), fill=self.border_color, width=self.width)
            row_start_pos += row_sz

        del self.pairsx[-1]
        del self.pairsy[-1]

        self.img.save(f"{self.output}.png", "PNG")



    def place_txt(self,txt:str,font:str,y_pos:int,color:str,x_pos=None,anchor="mm"):
        if txt is None:
            txt = "Missing"
        txt_size = self.fontsx[font].getsize(txt)
        if x_pos is None:
            x_pos = ((self.img.size[0] - txt_size[0]) / 2)+ (txt_size[0]/2)

        draw = self.draw
        draw.text((x_pos,y_pos),txt,fill=self.colors[color],font=self.fontsx[font],anchor=anchor)

    def place_peri(self,peri:list,axis):
        self.place_txt(self.name,"title",150,"name_blue")
        self.place_txt(self.email, "comment", 200, "name_blue")
        self.place_txt(self.cls_name, "title", 70, "black")


        if axis == "verti":
            for i in range(len(peri)):
                self.place_txt(peri[i], "band", (self.pairsx[i]), "black", self.col_start_pos / 2)
            self.place_txt("Comment", "band", self.pairsx[-1] + (self.row_sz / 2)+ (self.row_sz*0.2), "black", self.col_start_pos / 2)

        elif axis == "hori":
            for i in range(len(peri)):
                self.place_cmt(peri[i],"hori",self.pairsy[i]-(self.col_sz/2)+10,int((self.row_start_pos+350)/2))
            self.place_cmt("Comment", "hori", self.pairsy[-1] - (self.col_sz / 2) + self.col_sz +10,
                           int((self.row_start_pos + 350) / 2))

    def place_cmt(self,txt:str,font:str,x:int,y:int,color="black",anchor="lm"):

        text_lst = txt.split()

        rt_lst = [i for i in text_lst]

        for i in rt_lst:
            self.place_txt(i,font,y,color,x,anchor)
            y+=5+self.fontsx[font].getsize("x")[1]

    def place_wrap(self,txt:str,font:str,width:int,x:int,y:int,color="black",anchor="lm"):

        if txt is None:
            txt = ""
        text_lst = txt.split()
        lst = ['']
        c=0
        for i in text_lst:
            if self.fontsx["comment"].getsize(lst[c]+i)[0] < width:
                lst[c]=lst[c]+" "+i
            else:
                c+=1
                lst.append(i+" ")

        for i in lst:
            self.place_txt(i,"comment",y,color,x,anchor)
            y+=5+self.fontsx[font].getsize("x")[1]

    def place_band(self,bands:list,axisno:int):
        self.array.append(bands)
        key = bands[-1]
        bands = [str(i) for i in bands]

        for i in range(len(bands)):
            self.place_txt(bands[i], "band", self.pairsx[axisno], "black", self.pairsy[i])
        self.place_wrap(self.mapper(key),"comment",self.col_start_pos,
                        self.pairsy[-1]+(self.col_sz/2),(self.pairsx[axisno])-(self.row_sz/2)+self.row_sz*0.2)

    def trend_n_overall(self):
        for j in range(len(self.array[0])):


            lst = []
            for i in self.array:
                lst.append(i[j])
            lst1 = []
            ll = []
            for i in lst:
                try:
                    ll.append(float(i))
                except ValueError:
                    pass
            for i in range(len(ll)-1):

                lst1.append((int(ll[i+1])-int(ll[i])))

            self.place_wrap(self.mapper(sum(lst1), trend=True), "comment", self.col_sz - (self.col_sz*0.15),
                            self.pairsy[j] - (self.col_sz / 2) +(self.col_sz*0.1), self.pairsx[-1] + (self.row_sz / 2)+ (self.row_sz*0.2))

        lst = []
        for i in self.array:
            try:
                lst.append(float(i[-1]))
            except ValueError:
                pass


        if len(lst) != 0:
            va = (sum(lst) / len(lst))
        else:
            va = "M"

        self.place_wrap(self.mapper(va, overall=True), "comment",
                        self.col_start_pos,
                        self.pairsy[-1]+(self.col_sz/2)+self.col_sz*0.1, self.pairsx[-1]+(self.row_sz/2)+self.row_sz*0.1)

    def mapper(self,value,trend=False,overall=False):
        try:
            value = float(value)

        except ValueError:
            value = "M"

        if value == "M":
            return "Please do assignments."
        if trend:
            if value in self.mappert:
                return random.choice(self.mappert[value])
            elif value < 0:
                return random.choice(self.mappert['below'])
            elif value > 0:
                return random.choice(self.mappert['over'])

        if overall:
            try:
                return self.overall_mapper[int(ceil(value))]
            except KeyError:
                print("Error in "+self.name + str(value))

        for i in self.mapperv:
            if i[0] <= value <= i[1]:
                return random.choice(self.mapperv[i])


    def save(self):
        print(f"{self.name} created.")
        self.img.save(f"certificates\\CERT{self.name}.png")


usin = {"row":4, "row_names":["Pre Test","Test 1", "Test 2", "Test 3"],
        "row_no":[[2,3,4,6],[8,9,10,12],[14,15,16,18],
                  [20,21,22,24]],
        "column":4, "column_names":["Passage 1","Passage 2", "Passage 3", "Band"],
        "class":"IETLS Reading","name":0,"email":1
        }
