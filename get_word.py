##关键字
key_world_list =["while","if","else","return","void","main","printf","int","scanf"]
key_translate_list =["t","w","u","s","z","y","r","x","f"]
##标识符
flag_world_list=[chr(i) for i in range(97,99)]  #添加a-c
##常数
constant_world_list = [chr(i) for i in range(48,57)]  #添加0-9
##运算符
operator_world_list = ["+","-","*","/","=",">","<","==","!="]
##界符
delimiter_world_list = [";","{","}","(",")"]
##词法分析后的语句字符list
procedure_str_list =[]
##语法分析需要的字符串样式
procedure_str =""

##检测：空格、制表符
def is_difference(world):
    if (world ==" ") or (world=="\t"):
        return True
    return False
##检测字母a-z
def is_letter(letter):
    if (ord(letter)>96) and (ord(letter)<123):
        return True
    return False
def analy_word():
    for line in open("procedure.c"):
        #line = line.rstrip('\n')    #去除回车符
        step=0     #对语义line当前索引的位置
        flag=0   #特殊处理标识，
        p_flag=0 #printf,scanf
        tr_flag=0
        # line_len =len(line.rstrip('\n'))
        tmp=""    #单词的中间变量，
        if line.find("printf")!=-1:
            n=line.find("printf")
            tmp1=line[n:n+7]
            tmp2=line[n+12:]
            line =tmp1+tmp2
        elif line.find("scanf")!=-1:
            n=line.find("scanf")
            tmp1=line[n:n+6]
            tmp2=line[n+12:]
            line =tmp1+tmp2
            # print(line)
        for single in line:
            if flag ==1:   #字符串标志
                tmp +=single
                flag =0
                step +=1
                continue
            elif flag ==2:
                tmp +=single
                procedure_str_list.append(tmp)
                flag=0
                tmp =""
                step +=1
                continue
            if single =="\n":        #遇到回车，分析下一句
                break
            elif is_difference(single)==False: #过滤：空格、制表符
                ##对字母的处理
                if is_letter(single):    
                    tmp += single
                    if is_letter(line[step+1]):  #向前一个是字母，继续探索
                        flag =1
                        step +=1
                        continue
                    else:
                        procedure_str_list.append(tmp) #向前一个不是字母，停止探索，添加tmp,制空tmp
                        tmp=""
                        step +=1
                ##非字母处理
                else:
                    ##刚完成tmp的叠加，遇到非字母，存储tmp,制空tmp 。如：if(a>b)       
                    if tmp!="":
                        procedure_str_list.append(tmp)
                        tmp =""
                    if single in delimiter_world_list:  #处理界符
                        procedure_str_list.append(single)
                        step +=1
                    elif single in constant_world_list:   #处理数字
                        step +=1
                        procedure_str_list.append(single)
                    elif single in operator_world_list:  #处理运算符
                        if line[step+1] == "=":    #处理  ==
                            flag =2  #==,标志符
                            tmp +=single
                            step +=1
                        else:
                             procedure_str_list.append(single)
                             step +=1
            else: #非限定字符 
                if tmp !="": #tmp非空，则存储tmp。如：void  main()
                    procedure_str_list.append(tmp)
                    tmp =""
                step +=1
    ##词法分析结果可视化
    print(procedure_str_list)
    print("*"*50+"\n"+"词法分析结果："+"\n")
    print("字符".center(10)+"属性".center(10))
    for single in procedure_str_list:
        if single in key_world_list:
            print(single.center(10)+"关键字".center(10))
        elif single in flag_world_list:
            print(single.center(10)+"标识符".center(10))
        elif single in constant_world_list:
            print(single.center(10)+"常数  ".center(10))
        elif single in operator_world_list:
            print(single.center(10)+"运算符".center(10))
        elif single in delimiter_world_list:
            print(single.center(10)+"界符  ".center(10))
    print("*"*50)

    ##字符转为为语法分析所需样式
    procedure_str =""
    for single in procedure_str_list:
        if single in key_world_list:
            procedure_str += key_translate_list[key_world_list.index(single)]
        else:
            procedure_str +=single
    procedure_str +="#"
    print("*"*50+"\n"+"程序转译后的字符串："+"\n"+procedure_str+"\n"+"*"*50)
    return procedure_str


