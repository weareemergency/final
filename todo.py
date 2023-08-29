from tkinter import *
from pprint import pprint
from PIL import ImageTk, Image
from pathlib import Path
from tkinter.scrolledtext import ScrolledText
import ranking, pymysql
# import footer

class todo_list:
    def __init__(self, canvas, root):
        # DB init 
        self.host = '127.0.0.1'
        self.user = 'root'
        self.password = '1234'
        self.database = 'test'
        self.connection = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)

        # Image path & resize init 
        self.todo_image_path = "img/Rect16.png"
        self.check_image_path = "img/check.png"
        self.check_not_image_path = "img/check.png"
        self.black_img_path = "img/1B1B1B.png"
        self.resize915_538 = (915, 538)
        self.resize49_49 = (49, 49)
        self.resize1050_1200 = (1050, 1200)

        # base
        self.canvas = canvas
        self.root = root
        self.todo()

    def connect_db(self):
        data = None

        if self.connection:
            print("MySQL Connect")
            data = todo_list.select_todo(self, 1)
        
        else:
            print("fail")

        return data

    def select_todo(self, id):
        cursor = self.connection.cursor()
        query = f"SELECT * FROM todolist where id = {id}"  
        cursor.execute(query)

        result = cursor.fetchall()

        return result
        
    
    def ranking_go(self):
        black_img = Image.open(self.black_img_path)
        black_img = black_img.resize(self.resize1050_1200)
        root.black_img = ImageTk.PhotoImage(black_img)

        star_button = Label(self.root,image=root.black_img,width=1050,height=1200, bg="white",borderwidth=0, highlightthickness=0)

        canvas.create_window(540, 1000, window=star_button)
        ranking.rank_list(self.canvas, self.root)

    def image_open(path, resize):
        name = Image.open(path)
        name = name.resize(resize)
        name = ImageTk.PhotoImage(name)

        return name

    def label(self, text, name, width, height):
        if name == 'title_label':
            return Label(self.root, text="투두리스트>",font=('NaumGothic',25),bg="#1b1b1b",fg="white",borderwidth=0, highlightthickness=0, justify="left")
    
        elif name == 'nav_label':
            text = text 
            return Label(self.root, font=('Noto Sans', 16, 'bold'), text=text,fg="black", bg="white")
        
        else:
            return Listbox(self.root, font=('NaumGothic',20),width=width, height=height, borderwidth=0,bg="white",highlightthickness=0)
        
    def todo(self):
        # db checking line 
        todo_list.connect_db(self)

        self.root.todo_ract = todo_list.image_open(self.todo_image_path, self.resize915_538)
        self.root.check = todo_list.image_open(self.check_image_path, self.resize49_49)
        self.root.check_not = todo_list.image_open(self.check_not_image_path, self.resize49_49)

        title = "title_label"
        nav = "nav_label"
        detail = "detail_label"

        self.todo_name_label= todo_list.label(self, None, title, None, None)
    
        self.todo_lable = todo_list.label(self, "Todo List", nav, None, None)
        self.due_lable = todo_list.label(self, "Due Date", nav, None, None)
        self.com_lable = todo_list.label(self, "Complete", nav, None, None)

        self.todo_ract = Label(self.root, image=self.root.todo_ract, bg="#1b1b1b", borderwidth=0, highlightthickness=0)
        
        self.view_list = todo_list.label(self, None, detail, 25, 13)
        self.date_list = todo_list.label(self, None, detail, 10, 13)
        self.check_box = todo_list.label(self, None, detail, 2, 14)

        self.img_list = ScrolledText(self.root, width=10, height=26,borderwidth=0,highlightthickness=0)
        
        self.ranking_Button = Button(self.root, text="랭킹 보러가기>",font=('NaumGothic',25),bg="#1b1b1b",fg="white",borderwidth=0, highlightthickness=0, justify="left", command=self.ranking_go)
        
        # DB Code line ---- 
        data = todo_list.connect_db(self)
        # print(data) # (1, '김병찬', datetime.date(2023, 8, 30), 0) 형식으로 출력 
        # print(len(data))

        for i in range(len(data)):
            self.img_list.image_create(INSERT, image=self.root.check_not)
            self.img_list.insert(INSERT, '\n')
            self.img_list.insert(INSERT, '\n')

            # 날짜
            self.date_list.insert(0, data[i][2])
            self.date_list.insert(END, '')
        
            # Todo
            self.view_list.insert(0, data[i][1])
            self.view_list.insert(END, '')

            #listbox 클릭 활성화를 종료한다
            self.view_list.bindtags((self.view_list, self.root, "all"))
            self.date_list.bindtags((self.date_list, self.root, "all"))
        
            self.canvas.create_window(540,1140, window=self.ranking_Button)
            self.canvas.create_window(915,884, window=self.img_list)
            self.canvas.create_window(950, 875, window=self.check_box)
            self.canvas.create_window(330, 890, window=self.view_list)
            self.canvas.create_window(686, 890, window=self.date_list)
            self.canvas.create_window(540, 840, window=self.todo_ract)
            self.canvas.create_window(200, 524, window=self.todo_name_label)
            self.canvas.create_window(180, 630, window=self.todo_lable)
            self.canvas.create_window(670, 630, window=self.due_lable)
            self.canvas.create_window(890, 630, window=self.com_lable)
            
            self.todo_lable.lift()
            self.due_lable.lift()
            self.com_lable.lift()
            self.check_box.lift()

if __name__=="__main__":
    root = Tk()#Tk 생성
    # root.overrideredirect(True)
    canvas = Canvas(root, bg="#1b1b1b") 
    # gui화면 설정 배경 bg="색갈입력" 현재 #1b1b1b 설정됨
    canvas.pack(fill=BOTH, expand=TRUE)
    #header.Header_menu(canvas, root)
    #footer.footer_menu(canvas, root)
    todo_list(canvas, root)
    root.geometry("1080x1920")
    # 화면 크기를 지정한다
    root.mainloop()