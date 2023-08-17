import pyperclip
import re
import os
class SqlTransformer:
    select=0
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

    
    def __init__(self):
        pass


    def inputs(self):
        
        tablename=input("请输入表名：\n")
        print_strs='''选择SQL数据类型转化形式：
        0:不转换。
        1:Hive SQL to Oracle SQL
        2:Oracle SQL to Hive SQL
        3:Hive SQL to PostgreSQL
        请输入编号：
        '''
        print(print_strs)
        self.select=eval(input())
        print("选择为:",self.select)
        cin = []
        print('请输入复制的字段，输入完成后按回车再按ctrl+c结束输入：')
        while True:
            try:
                cin.append(input())
            except:
                break
        return cin,tablename
    

    #输入处理
    def process(self,cin):
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
    def get_sql(self,field,tablename):
        if(len(field)%2!=0):
            print("输入有误！请确保输入的结尾有换行！")
            return 
        SQL=f"create table {tablename}("
        strs=field
        # print(strs)
        for i in range(0,len(strs),2):
            SQL+='\n    '+strs[i]+' '+strs[i+1]
            if i !=len(strs)-2:
                SQL+=','

        SQL+='\n)'
        pyperclip.copy(SQL)
        print("语句已生成！")
        
    def work(self):
        field_list,tablename=self.inputs()
        field_list=self.process(field_list)
        select=self.select
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
        if trans_dict!=None:
            field_list=self.transform(field_list,trans_dict)
        self.get_sql(field_list,tablename)
    #替换字段
    def transform(self,field_list,trans_dict):
        keys=trans_dict.keys()
        for i in range(1,len(field_list),2):
            data_type=field_list[i]

            #正则表达式匹配特殊字段 
            for key in keys:
                if self.re_match(key,data_type):
                    field_list[i]=trans_dict[key]
                    break 
            #替换字段
            if data_type in keys:
                field_list[i]=trans_dict[data_type]
                

            
        return field_list
    
    def re_match(self,key,data_type):

        pattern=f'{key}.*'
        match=re.search(pattern,data_type)
        return match!=None

if __name__=='__main__':
    ST=SqlTransformer()
    while True:
        print("请确保结尾有换行符。\n执行完成后结果将自动拷贝到剪切板")
        ST.work()
        os.system('cls') 




