# auto_sort_out

# 所有功能均在测试中，不保证可靠性，源代码中还有大量的奇葩注释和蹩脚翻译提醒未解决！！！

## 功能

自动整理文件目录

+ 这个模块是用来获取指定目录文件的文件信息，包括名称、大小、创建时间、最后访问时间以及最后修改时间。

+ info，是一个字典变量，里面有文件名File、大小Size、以及mtime、atime、ctime三个时间数组，对了，Size有什么作用怎么玩暂时想不到，所以获取的时候注释掉了，尽量节省空间

+ 为了方便，时间数组用的还是那些，自己用time.localtime调用获取数据组，按照表格自己做去，为什么我不做？因为我累了！

+ path是可访问变量，用来确定路径的，在定义好类之后最好要定义path

+ total是目录下所有文件的总数，我实在是觉得每一次for都要用range(leng(self.info["File"]))这样子太蠢了，虽说那么搞会不占用什么内存空间，但是老娘都用上Python了还管这些？！而且一个整型变量也不占用多少空间吧，不然代码可读性差，自己也没法修改，反正默认大家2GB内存起步……

+ 一大堆私有变量交给配置文件config.json了，需要的话自己更改

## 注意！！！

无论那种类型的分类，都是破坏原有的目录结构，请慎用。后悔药功能暂未上线哦！即便是有后悔药功能，也不见得很有用，所以还是请慎重分类。

## 所需的Python模块（Python3）

+ os

+ re

+ shutil

+ time

+ json

~~+ sort_out~~

## 使用

建立一个demo,或者一个main的py脚本，然后：


    import sort_out as SOF 
    f=SOF.Sort_Out("/home/xxx/Documents")
    #f.path=("/home/xxx/Documents")
    f.sort_out_by_mtime("normal") #将/home/xxx/Documents中的文件按照最后修改时间的年/月目录分类
    #f.sort_out_by_filetype() #根据文件类型将/home/xxx/Picturesde文件分类，暂时为分类图片类
    #PS：如果已经分类了的目录将无法再一次进行分类
    #f.recover()#后悔药功能，只要目录下的sort_out_log文件不要删除更改就可以还原
    
## 所需文件内容
程序目录下需要：

+ main.py

+ sort_out.py

+ config.json

main.py中导入sort_out.py模块，然后根据config.json的设置确定文件类型和“雷区”

## class的内容

### 变量

+ path：要处理的目录路径

+ info：字典文件，包含所有文件的名称、大小、修改时间、最后访问时间、创建时间以及。。。文件类型

+ total：文件的总数

+ __forbidden_file：如果目录下存在这些后缀名的文件将禁止分类，详细内容在config.json中，用户可以自己添加

+ __forbidden_dir：如果目录中含有其中的关键字则禁止分类,详细内容在config.json中，用户可以自己添加

+ __file_type：按照文件类型分类的时候所需的类别，详细内容在config.json中，用户可以自己添加

### 函数调用

+ __get(file_name)：获取文件的信息，存储到info文件，作为数组的一部分

+ close()：清空上述类中的变量

+ __config()：读取config.json中的文件把内容获取

+ __check()：用于检查设定分类的目录是否在"雷区"中

+ __is_log_exsit()：用于检查设定目录及其子目录下是否含有sort_log_out文件，有则为已经分类整理过的，原则上禁止再一次分类整理

+ __mk_log()：生成日志

+ __move(dir,i)：移动文件，dir是要移动的目录，i是文件编号

+ recover()：后悔药功能，前提是分类生成的sort_out_log文件不要删除和修改，而且是此路径下所有的分类都还原

+ Get_Info()：调用了__get()，把目录下所有的文件信息都拿到手，存储到info字典中，是一个超级大的数组，数组的长度就是total——文件的数量

+ sort_out_by_mtime(T_Type,Type)：根据修改时间把文件分类，选择normal则是按照年月划分文件夹，选项all是按照年月日划分，推荐每天修改的文件太多了这么干，毕竟每个文件夹里文件高达上百也是可以了，按照月的划分怕太多你看不过来

+ sort_out_by_filetype()：根据文件类型分类，分出的类别不多，更多的是玩票的性质

+ sort_out_by_key(Key)：根据关键字分类，使用了正则表达，自由度高的代价就是容易出问题，请谨慎使用

## 配置文件config.json 
大体格式如下，看懂了记住关键字你可以自己写配置，直接叫我的默认配置滚蛋：

		{
			"File_Type":{
				"图片":["jpg","png"],
				"你想要的名字":["文件类型的名字——后缀"]
				},
			"Forbidden_Files":["ini","目录下含有这个后缀的文件就禁止分类"],
			"Forbidden_Dirs":["Windows","目录路径中含有这些关键词就别想分类了"]
			}

嗯，大致就是这样，上传的confg.json默认为中文，config_en.json为英文版——防止一些不方便用中文的系统出现bug,例如……没解决好中文现实的字符界面终端……（经验之谈）

## 准备添加的功能：

+ 添加更多的filetype和各种"雷区"

+ 利用Size区别大小文件，但是感觉作用不是太大啊

+注释和提示英文化，然后增加本地化支持
