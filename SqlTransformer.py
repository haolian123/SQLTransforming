import pyperclip
import re
import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
class SqlTransformer:
    __select=0
    # Hive SQL to Oracle SQL
    h2o = {
        'string': 'varchar2(500)',
        'decimal': 'number',
        'timestamp': 'date',
        'float': 'float',
        'int': 'int',
        'double': 'double',
        'bigint': 'bigint',
        'boolean': 'boolean'
    }


    # Oracle SQL to Hive SQL
    o2h = {
        'varchar': 'string',
        'varchar2': 'string',
        'number': 'decimal(22,0)',
        'date': 'timestamp',
        'float': 'float',
        'int': 'int',
        'double': 'double',
        'bigint': 'bigint',
        'boolean': 'boolean'
    }

    # Hive SQL to PostgreSQL
    h2p = {
        'string': 'varchar(500)',
        'decimal': 'numeric',
        'timestamp': 'timestamp',
        'float': 'real',
        'double': 'double',
        'int': 'integer',
        'bigint': 'bigint',
        'boolean': 'boolean'
    }

    select_dict={
        "不转化":0,
        "Hive SQL to Oracle SQL":1,
        "Oracle SQL to Hive SQL":2,
        "Hive SQL to PostgreSQL":3
    }

    def __init__(self):

        # 创建一个窗口对象
        self.window = tk.Tk()

        # 设置窗口标题
        self.window.title('SQLTransformer')

        # 设置窗口大小和位置
        self.window.geometry('480x550+500+200')

        #表名
        self.tablename=tk.StringVar()
        self.tablename.set("tablename")
        #中文字体
        font_chinese="华文中宋"
        font_color='black'

        # 创建一个标签，显示"表名"
        self.tablename_label = tk.Label(self.window, text="表名：", font=(font_chinese, 13))
        self.tablename_label.configure(fg=font_color, font=(font_chinese, 15,'bold'))
        self.tablename_label.place(x=10, y=15)

        # 创建一个文本框，用于显示表名
        self.tablename_entry = tk.Entry(self.window, textvariable=self.tablename, width=30, state='normal',font=('Arial',15))
        self.tablename_entry.place(x=110, y=20)
        
        # 创建一个标签，显示"转化形式"

        self.transform_mode_label = tk.Label(self.window, text="转化方式", font=(font_chinese, 13))
        self.transform_mode_label.configure(fg=font_color, font=(font_chinese, 15,'bold'))
        self.transform_mode_label.place(x=10, y=50)

        #添加一个下拉框
        self.combobox = ttk.Combobox(self.window,width=18, state="readonly",textvariable="不转化",font=(font_chinese, 13),values=["不转化", "Hive SQL to Oracle SQL", "Oracle SQL to Hive SQL",'Hive SQL to PostgreSQL'])
        self.combobox.bind("<<ComboboxSelected>>", lambda event: self.__on_combobox_select(event, combobox=self.combobox))
        self.combobox.current(0)
        self.combobox.place(x=110, y=60)

        # 创建一个按钮，点击后调用thread_run函数，用于运行程序
        self.exec_button = tk.Button(self.window, text='生成', width=5, height=2, command=self.__run)
        self.exec_button.place(x=350, y=18)
        self.exec_button.configure(fg=font_color, font=(font_chinese, 17,'bold'))

        # 创建一个文本框

        self.text = tk.Text(self.window, height=30, width=50, font=('Arial', 12))
        self.text.place(x=4, y=100)
        self.text.insert("end",'将SQL的字段名和数据类型粘贴(ctrl+v)到此处')
      
        # 创建一个滚动条
        self.scrollbar = tk.Scrollbar(self.window)

        # 设置滚动条与文本框的关联
        self.scrollbar.config(command=self.text.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text.config(yscrollcommand=self.scrollbar.set)

        # 滚动到文本框末尾
        self.text.see('end')


    def __on_combobox_select(self,even,combobox):
        selected_item = combobox.get()
        #返回选择的选项号
        self.__select= self.select_dict[selected_item]


    #输入处理
    def __process(self,cin):
        res=[]
        flag=False
        for line in cin:
            if len(line.strip())<1:
                continue
            line=line.strip()
            line=line.strip(',')
            tmp_arr=line.split()
            if tmp_arr[0].lower()=='create':
                flag=True#去除末尾的括号
                continue
            tmp_arr=[s.lower() for s in tmp_arr]
            res.extend(tmp_arr)
        if flag:
            res.pop()
        return res
    

    #得到sql语句
    def __get_sql(self,field,tablename):
        if(len(field)%2!=0):
            raise Exception("请检查每个字段是否有唯一的数据类型与之对应！")
        SQL=f"create table {tablename}("
        strs=field

        for i in range(0,len(strs),2):
            SQL+='\n    '+strs[i]+' '+strs[i+1]
            if i !=len(strs)-2:
                SQL+=','

        SQL+='\n)'
        pyperclip.copy(SQL)
        
        messagebox.showinfo('生成成功！',"语句已复制到剪切板！")

    #将输入的文本转化为列表
    def __get_filed_list(self,text):
        filed_list=text.split('\n')
        return filed_list
    
    def __run(self):
        try:
            #得到表名和字段+数据类型
            tablename=self.tablename.get()
            SQL_text = self.text.get("1.0", "end-1c")
            
            #将输入文本转化为列表
            field_list=self.__get_filed_list(SQL_text)
            #将列表拆分为字段名+数据类型的形式
            field_list=self.__process(field_list)
            #得到转化形式
            select=self.__select
            #转化字典
            trans_dict=None

            if select == 1:
                #Hive SQL to Oracle SQL
                trans_dict=self.h2o
            elif select ==2:
                #Oracle SQL to Hive SQL
                trans_dict=self.o2h
            elif select ==3:
                # Hive SQL to PostgreSQL
                trans_dict=self.h2p
            #需要转化
            if trans_dict!=None:
                field_list=self.__transform(field_list,trans_dict)
            #得到sql语句
            try:
                self.__get_sql(field_list,tablename)
            except Exception as e:
                messagebox.showerror('生成失败！',e)
        except:
            messagebox.showerror('生成失败！',"请检查粘贴的内容是否符合格式要求！")
        

    #替换字段
    def __transform(self,field_list,trans_dict):
        #获得字典的键
        keys=trans_dict.keys()
        for i in range(1,len(field_list),2):
            data_type=field_list[i]

            #正则表达式匹配特殊字段 
            for key in keys:
                if self.__re_match(key,data_type):
                    field_list[i]=trans_dict[key]
                    break 
            #替换字段
            if data_type in keys:
                field_list[i]=trans_dict[data_type]
        return field_list
    
    def __re_match(self,key,data_type):
        # 正则匹配
        pattern=f'^{key}.*'
        match=re.search(pattern,data_type)
        return match!=None
    
if __name__=='__main__':
    M=SqlTransformer()
    M.window.mainloop()


