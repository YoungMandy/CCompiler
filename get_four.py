# pr_str = "zy(){;xa;xb;;a=3;w(a<b){a=3;}u{;a=2;r(a);};s0;}#"
#词法分析后的字符串
pr_str=""
flag_world_list=[chr(i) for i in range(97,99)]  #添加a-c
##语句分析步数
step = 0
##变量名,生成最终代码使用
variate_name_list =[]
##四元式dict
four_dict ={}

#语句数量
num =0
#中间变量标号
T_num=0
#四元式标号
four_num = 1   



##处理程序头
def op_head_end():
    global pr_str
    pr_str = pr_str[5:]
    pr_str = pr_str[:-2]


##处理变量声明
def op_var():
    global pr_str
    var_num =1;
    for single in pr_str:
        if single ==";":  #通过" ; " 判断声明的范围
            var_num +=1
        else:
            break
    temp_step =var_num
    tmp_num=var_num
    while tmp_num!=0:   #存储出现的变量
        variate_name_list.append(pr_str[temp_step])
        tmp_num-=1
        temp_step+=3
    var_len =var_num*3+var_num-1
    pr_str = pr_str[var_len:]

##获取语句数量,去除语句数量标号:" ; "
def  op_stance():
    global pr_str
    stance_num =1
    global step
    for single in pr_str:
        if single ==";":  #通过" ; " 判断的范围
            stance_num +=1
        else:
            break
    ter_len =stance_num-1
    pr_str = pr_str[ter_len:]  #去掉语句数量声明:   ; 
    return stance_num
    # if pr_str[step] in  flag_world_list:   #赋值语句入口
    #     four_dict[four_num]=["=",pr_str[step+2],"/",single]
    #     step+=4     #指向下一条语句

#中间变量生成
def op_temp():   #调用一次，标号+1
    global T_num
    T_num+=1
    T="T"+str(T_num)
    variate_name_list.append(T)
    return T


#处理赋值语句
def op_value():
    global step
    global pr_str
    global four_num
    four_dict[four_num]=["=",pr_str[step+2],"/",pr_str[step]]
    four_num+=1
    step+=4       #指向下一语句
#处理输出语句
def op_print():
    global step
    global pr_str
    global four_num
    four_dict[four_num]=["r",pr_str[step+2],"/","/"]
    four_num+=1
    step+=5        #指向下一语句
#处理输入语句
def op_scanf():
    global step
    global pr_str
    global four_num
    four_dict[four_num]=["c",pr_str[step+2],"/","/"]
    four_num+=1
    step+=5        #指向下一语句

##处理while语句
def op_while():
    global step   #字符索引位置
    global pr_str #待分析的字符串
    global four_num  #四元式标号
    stance_num =1  #while里，语句数量
    T=op_temp()  #获取中间变量T标号
    four_dict[four_num] = [pr_str[step+3],pr_str[step+2],pr_str[step+4],T]
    temp_pr_str = pr_str[step+7:]
    four_dict[four_num+1] = ["FJ","wait",T,"/"]
    wait_four_num=four_num+1   #记住待回填四元式号数
    for single in temp_pr_str:
        if single ==";":  #通过" ; " 判断的范围
            stance_num +=1
        else:
            break
    ter_len =stance_num-1
    tmp_pr_str = temp_pr_str[ter_len:]  #去掉语句数量声明:   ;
    four_num+=2
    step =step+7+stance_num-1  #指向whlie语句里的语句,pr_str
    while stance_num!=0 :
        if pr_str[step] in flag_world_list:   #赋值语句入口
            # print(12558)
            op_value()
        elif pr_str[step] =="r":      #输出语句入口
            op_print()
        elif pr_str[step] =="f":      #输入语句入口
            op_scanf()
        stance_num -=1
    four_dict[four_num] = ["RJ",wait_four_num-1,"/","/"]  #无条件跳转至条件判断
    four_num+=1
    four_dict[wait_four_num][1]=four_num   #回填 
    step+=1
    # print("duan"+pr_str[step])    

##处理if语句
def op_if():
    global step
    global pr_str
    global four_num
    stance_num =1
    T=op_temp() #中间变量
    four_dict[four_num] = [pr_str[step+3],pr_str[step+2],pr_str[step+4],T]
    temp_pr_str = pr_str[step+7:]
    four_dict[four_num+1] = ["FJ","wait",T,"/"]
    wait_four_num1=four_num+1   #记住待回填四元式号数1
    for single in temp_pr_str:
        if single ==";":  #通过" ; " 判断的范围
            stance_num +=1
        else:
            break
    ter_len =stance_num-1
    tmp_pr_str = temp_pr_str[ter_len:]  #去掉语句数量声明:   ;
    four_num+=2
    step =step+7+stance_num-1  #指向if语句里的语句,pr_str
    temp_step = 0
    while stance_num!=0 :
        if pr_str[step] in flag_world_list:   #赋值语句入口
           op_value()
        elif pr_str[step] =="r":      #输出语句入口
            op_print()
        elif pr_str[step] =="f":      #输入语句入口
            op_scanf()
        stance_num -=1
    four_dict[four_num] = ["RJ","wait","/","/"]  #假设有else,无条件跳转至下一语句
    wait_four_num2 =four_num  #记住待回填四元式号数2
    four_num+=1
    four_dict[wait_four_num1][1]=four_num  #回填
    step+=1
    if pr_str[step] =="u":  #存在else
        temp_pr_str =pr_str[step+2:] #去掉else语句前的语句
        stance_num=1
        for single in temp_pr_str:
            if single ==";":  #通过" ; " 判断的范围
                stance_num +=1
            else:
                break
        ter_len =stance_num-1
        tmp_pr_str = temp_pr_str[ter_len:]  #去掉语句数量声明:   ;
        step =step+2+stance_num-1  #指向else语句里的语句,pr_str
        while stance_num!=0 :
            if pr_str[step] in flag_world_list:   #赋值语句入口
               op_value()
            elif pr_str[step] =="r":      #输出语句入口
                op_print()
            elif pr_str[step] =="f":      #输入语句入口
                op_scanf()
            stance_num -=1   
        four_dict[wait_four_num2][1]=four_num   #回填
        step+=1
        print("else出现"+pr_str[step])
    else:
        four_num-=1
        four_dict.pop(four_num) #无else,去除else预设句
        four_dict[wait_four_num1][1]=four_num
        

          
def make_four(test_str):
    global pr_str
    global step
    pr_str=test_str
    op_head_end()  #去掉主函数框架
    print(pr_str)
    op_var()  #去掉声明列表
    print(pr_str)
    stance_num=op_stance()  #获取语句数量
    while stance_num!=0 :
        if pr_str[step] in flag_world_list:   #赋值语句入口
           op_value()
        elif pr_str[step] =="t":  #while
            op_while()            
        elif pr_str[step] =="w":   #if
            op_if()
        elif pr_str[step] =="r":    #printf
            op_print()
        elif pr_str[step] =="f":      #输入语句入口
            op_scanf()
        stance_num -=1
    four_dict[four_num]=["re","/","/","/"] #结束语句
    four_list=[]
    ##输出四元式
    print("#"*100+"\n"+"四元式：")
    for si in four_dict:
        tmp=str(si)+"  ("
        print(str(si).center(10)+"(",end="")
        step=0
        for val in four_dict[si]:
            if step<3:
                print(val,end="")
                print(",",end="")
                if isinstance(val,int):
                    val =str(val)
                tmp+=val+","
            else:
                print(val,end="")
                print(")")
                if isinstance(val,int):
                    val =str(val)
                tmp+=val+")\n"
            step+=1
        four_list.append(tmp)
    print("#"*100)
    ##存储四元式
    four_file =open("four.txt","w+")
    four_file.writelines(four_list)
    four_file.close()
    return four_dict,variate_name_list







        

    