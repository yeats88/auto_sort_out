import os,shutil,time,re,json

'''
Author:Silver Sabre
git clone https://github.com/SilverSabre/auto_sort_out.git
用来分类整理文件
'''

class Sort_Out:

    path="";
    info={"File":[],"Size":[],"mtime":[],"atime":[],"ctime":[],"FileType":[]}
    total=0; #文件数量统计，默认是0
    __file_type={};
    __forbidden_file=[];#config.json中定义
    __forbidden_dir =[];#config.json中定义
    '''
    + 私有变量file_type,是包含了可以分类的文件，不需要更改，用于文件按照类型分类
    + __forbidden_file,__forbidden_dir 分别表示当目录下和绝对目录中包含敏感词则停止分类
    + 以上三类准备更改为配置文件，方便用户自己定义，在初始化时读取

    #__log=

    #'''

    def __init__(self,path): #必选，要不然怕你出错
        self.path=os.path.abspath(path) #因为Windows下读取文件的特性，这里必须使用绝对路径
        self.Get_Info()
        '''
        来来来，我先帮你们搞到信息，怎么排序就是你们的问题了
        当然，每一次调用获取函数Get_Info（）都会重置info和total里的内容，而且是调用path变量获取，后续也可以更改的，为了方便和安全最好强制您进行初始化
        '''

    def __config(self):
        if not os.path.isfile("config.json"):
            print("错误！config.json文件丢失！")
            return False
        with open("config.json","r") as f:
            con=f.read()
        con=json.loads(con)
        self.__forbidden_file=list(con["Forbidden_Files"])
        self.__forbidden_dir =list(con["Forbidden_Dirs"])
        self.__file_type=dict(con["File_Type"])
        return True

    def close(self):#清理内存
        for i in self.info.keys():
            self.info[i]=[]
        self.total=0
        self.__forbidden_dir=[]
        self.__forbidden_file=[]
        self.__file_type={}
        self.path="";
        return True

    def __get(self,file_name):
        #获取文件的信息，内置函数
        data=os.stat(file_name);
        self.info["atime"].append(data[7]);
        self.info["mtime"].append(data[8]);
        #self.info["Size"].append(data[6]); #这个暂时无用，不需要为了省空间可以注释掉
        self.info["ctime"].append(data[9]);
        self.total=len(self.info["File"]);  #目录下所有的文件数量，反正这里使用的太频繁了，我也烦了，直接给一个变量好了，如果喜欢也可以单独拿出来看看多少个文件
        for i in range(self.total):  #反正为了方便，改成total
            s=re.findall(r'\w+\.(\w+$)',self.info["File"][i])#这里因为表达是太长了 所以懒惰的我就重新赋值给变量s
            if len(s)==0: #为了数据统一,不然怕出现out of range什么的错误
                s=[None]
            self.info["FileType"].append(s)

    def Get_Info(self):
        if not self.__config():
            return False
        if self.__is_log_exsit():
            return False
        #先检查
        #获取目录下的所有文件信息赋值给字典info里，每个内容都是一个数组
        if self.total != 0:

       #如果之前对于初始化获取了内容那么info所有内容都需要清空，包括total,不过有了self.path这个做引导就没问题了——反正都离不开Get_Info获取，这里处理好就好了
            for i in self.info.keys():
                self.info[i]=[]
                self.total=0 #这里需要把总数重置成0
        #然后接下来就是获取数据
        self.path=os.path.abspath(self.path) #因为Windows下读取文件的特性，这里必须使用绝对路径
        os.chdir(self.path)
        self.info["File"]=os.listdir(self.path)
        for name in self.info["File"]:
            name=os.path.abspath(name) #还是为了windows兼容，防止之前我忘了获取绝对路径
            self.__get(name)
        if not self.__check():#进行可行性检查，不可行则弹出警告后退出
            return False;
        return True

    def sort_out_by_time(self,T_type="mtime",Type="normal"):
        '''
        T_type:是指的是创建时间还是访问时间还是修改时间，参数为mtime、ctime、atime，默认是mtime
        Type:easy、normal、all三种，分别是按照年作为目录以及年/月目录以及年/月/日目录结构，默认是normal
        '''
        '''不需要检查'''
        self.Get_Info();
        t=[];
        for i in self.info[str(T_type)]:
            t.append(time.localtime(i));
        os.chdir(self.path)
        if Type == "easy":
            for i in range(self.total):
                dirs=str(t[i][0])
                self.__move(dirs,i)
            return True

        elif Type == "normal": #这个就是按照年/月的目录分类
            for i in range(self.total):
                dirs=str(t[i][0])+"/"+str(t[i][1])
                self.__move(dirs,i)
            return True

        elif Type == "all": #这个更详细，按照年月日的目录细分
            for i in range(self.total):
                dirs=str(t[i][0])+"/"+str(t[i][1])+"/"+str(t[i][2])
                self.__move(dirs,i)
            return True;
        else:
            return False #回复False就是失败了

    def sort_out_by_filetype(self):
        #根据文件的后缀分类，如果你的文件过于复杂最好别用，其实整个项目都建议慎用
        self.Get_Info();
        os.chdir(self.path)
        for i in range(self.total):
            for j in self.__file_type.keys():
                if self.info["FileType"][i][0] in self.__file_type[j]:
                    self.__move(str(j),i)
                    #可以使用了
                    break;#找到了就不要再搞了，尽量跳出循环
        for i in range(self.total):
            if os.path.isfile(self.info["File"][i]):#剩下的文件如果还在，那就是未知的类别
                self.__move("未闻其名",i)
                print(str(self.info["File"][i])+"has been moved to 未闻其名")
        return True

    def sort_out_by_key(self,Key):
        self.Get_Info()
        os.chdir(self.path)
        for i in range(self.total):
            if re.search(r""+str(Key),self.info["File"][i]) != None:
                if not os.path.isdir(str(Key)):
                    os.mkdir(str(Key))
                    shutil.move(self.info["File"][i],str(Key))
        return True

    def __check(self):
            '''
            安全检查，只要你的目录在禁止的目录里，那就禁止分类;目录中含有特殊文件也禁止分类;self.__forbidden_dir  self.__forbidden_file 分别是禁止的目录和文件的集合，私有变量，你不许乱改
            Type默认为无，改成reset则跳过对sort_out_log的文件检查，用于文件还原时的安全性检查
            '''
            os.chdir(self.path)
            #self.Get_Info()#在Get_Info()中已经使用了，就没必要再一次引用了
            self.path=os.path.abspath(self.path)
            if self.total==0:
                print("当前目录下没有文件可供分类整理！")
                return False
            else:
                return True
            for i in self.__forbidden_dir : #__safe_guard_dir里全是敏感词，碰到了就直接不允许
                if re.search(r""+str(i),self.path) != None:
                    print("禁止在包含"+str(i)+"类型的文件的目录中进行分类整理！")
                    return False
                else:
                    return True
            for i in range(self.total):
                if str(self.info["FileType"][i][0]) in self.__forbidden_file:
                    print("禁止在包含目录["+str(i)+"]的目录中进行分类整理！")
                    return False
                else:
                    return True

    def __move(self,dirs,num):
            #受够了，直接写一个文件移动的函数，dirs就是目标目录，而num是文件编号，不是文件名
            if os.path.isdir(dirs):
                shutil.move(str(self.info["File"][num]),str(dirs))
                print(str(self.info["File"][num])+"has been moved to "+str(dirs))
            else:
                os.makedirs(str(dirs))
                shutil.move(str(self.info["File"][num]),str(dirs))
                print(str(self.info["File"][num])+"has been moved to "+str(dirs))
            dirs=os.path.abspath(dirs)
            name=os.path.abspath(self.info["File"][num])
            message=str(name)+" "+str(dirs)#记录日志
            self.__mk_log(message)
            return True

    def __mk_log(self,message):
        '''
        记录日志，名称为sort_out_log
        每条日志格式为：
            日期 时间 源文件 移动到的文件夹 ;[回车]
        '''
        os.chdir(self.path)
        t=time.localtime(time.time())
        s_t="["+str(t[0])+"-"+str(t[1])+"-"+str(t[2])+" "+str(t[3])+":"+str(t[4])+":"+str(t[5])+"] "
        message=s_t+message+" ;\n"
        with open("sort_out_log","a") as f:
            f.writelines(message)
        return True

    def __log_path(self): #返回log所在的目录地址 不是ture or false游戏
        url=[]
        for path,dirs,files in os.walk(self.path):
            if "sort_out_log" in files:
                path=os.path.abspath(path)
                url.insert(0,path)
        return url

    def __is_log_exist(self):
        for path,dirs,files in os.walk(self.path):
            if "sort_out_log" in files:
                print("--------------------\n**Warnning!**\nThis directory has been sorted out,can not sort it out agin except recover it.\n--------------------")
                return True
        return False



    def recover(self):#恢复每一个目录下包含sort_out_log的文件夹恢复
        os.chdir(self.path)
        if not self.__check():
            return False
        if self.__is_log_exist():
            path=self.__log_path(); #返回log所在的目录地址 不是ture or false游戏
        else:
            print("目录中不包含sort_out_log文件，无法/无需还原。")
            return False
        for u in path:
            os.chdir(str(u))
            with open("sort_out_log","r") as f:
                for lines in f.readlines():
                    lines=lines.split(" ")
                    name=os.path.join(str(lines[3]),str(lines[2]))
                    name=os.path.abspath(name)
                    #u=os.path.abspath(u)
                    if os.path.isfile(name):#如果这个目录下有这个文件则移动，否则就不要管它了
                        shutil.move(str(name),str(u))
                        print(str(name)+"has been moved to "+str(u))
            with open("sort_out_log","r") as f:
                for lines in f.readlines():
                    lines=lines.split(" ")
                    #name=os.path.abspath(str(lines[3]))
                    if os.path.isdir(name):#如果有这个目录就删除，没有就不要管它了
                        os.removedirs(name)
                        print("The directory "+str(name)+"has been deleted.")
            if os.path.isfile("sort_out_log"):
                os.remove("sort_out_log")
                print("The file "+str(u)+"|"+"sort_out_log has been deleted.")
        print("Complete!")
        return True

      # End of Class Sort_Out.
