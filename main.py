from get_production import get_base_data 
from get_word import analy_word
from get_four import make_four
from get_assembly import make_assembly
#产生式#
analy={} 
analy["right"] = [] #产生式右部
analy["left"] = [] #产生式左部
##终结符
ter_colt_list = [] #含$
su_ter_colt_list = [] #不含$
##非终结符
non_colt_list = []
first_dict = {}       #FIRST集
follow_dict = {}      #FOLLOW集
analy_left_list = []  #产生式左部list
analy_right_list = [] #产生式右部list
#LL1分析表,二维数组。列：终结符;行：非终结符;value:产生式右部
analy_table_list = []
#剩余字符串-逆序-语法分析
left_any=""
#分析栈
analy_stack = []
#四元式
four_dict ={}
#语法分析错误
analy_flag=0

## 求FIRST集
def get_first(non_colt):
    tag = 0;  #记录右部出现空的次数，flag=1,则tag+1
    flag = 0;  #记录右部出现空的标志，出现为1
    step = 0;
    
    for (analy_left, analy_right) in zip(analy_left_list, analy_right_list):
        if analy_left == non_colt:     #终结符匹配产生式
            if analy_left not in first_dict:
                first_dict[non_colt]=[]       #FIRST以非终结符建立关键字
            if analy_right[0] in ter_colt_list:   #产生式右部首字符为非终结符，则字符属于FIRST集
                first_dict[non_colt].append(analy_right[0])
                # print(analy_right[0])
            else:
                for single_right in analy_right:
                    if single_right in ter_colt_list :   #终结符结束
                        first_dict[non_colt].append(single_right)
                        break
                    get_first(single_right)  #递归，求右部非终结符的FIRST
                    # print(first_dict)
                    for  ter in first_dict[single_right]:
                        if ter == "$":              
                            flag =1
                        else:
                            first_dict[non_colt].append(ter)  #$不属于FIRST(single_right)，FIRST(single_right)属于FIRST(non_colt)
                    if flag == 0:  #当前判断元素存在$的情况，不需要找下一个元素的first
                        break
                    else:
                        tag +=flag
                        flag = 0
                    break
                if tag == len(analy_right):  #所有右部first(Y)都有$(空),将$加入FIRST(X)中  
                    first_dict[non_colt].append("$")


#求FOLLOW集
def get_follow(non_colt):
    for (analy_left, analy_right) in zip(analy_left_list, analy_right_list):
        index = -1  #记录FOLLOW(B),B在产生式右部的索引
        step = 0
        right_len = len(analy_right)
        for single_right in analy_right:   #非终结符匹配产生式右部
            if single_right == non_colt:
                index = step               #将当前索引位置赋予index,记录FOLLOW(B),B在产生式右部的索引
                if non_colt not in follow_dict:
                    follow_dict[non_colt]=[]       #FOLLOW以非终结符建立关键字
                break  
            step +=1    #记录遍历过程中，当前遍历字符的索引
        if (index != -1) and (index < right_len-1 ):  #找到匹配non_colt的产生式，且在non_colt后存在字符
            nxt = analy_right[index+1]   #非终结符non_colt在右部的的下一字符X
            if nxt in ter_colt_list:     #X是终结符,则找到FOLLOW
                follow_dict[non_colt].append(nxt)
            else:
                isExt = 0
                for single_first in first_dict[nxt]: # non_coltB, 找first(B)
                    if single_first == "$":    #first(B)为空，做标记,isExt=1
                        isExt = 1              
                    else:
                        follow_dict[non_colt].append(single_first) #存储FOLLOW
                if(isExt == 1) and (analy_left != non_colt ):  #first(B)为空，找non_colt所在产生式的左部S的follow(S)
                    get_follow(analy_left)
                    for single in  follow_dict[analy_left]:  #将follow(S)，赋予follow(non_colt)
                        follow_dict[non_colt].append(single)
        elif (index !=-1) and (index == right_len -1 ) and (non_colt != analy_left):  ##找到匹配non_colt的产生式，且在non_colt后不存在字符
            get_follow(analy_left) #找non_colt所在产生式的左部S的follow(S)
            tmp = analy_left
            for single in follow_dict[tmp]:   #将follow(S)，赋予follow(non_colt)
                follow_dict[non_colt].append(single)


##分析表格式化输出
def print_table():
    print("*"*100+"\n"+"LL(1)分析表:")
    for  ter in su_ter_colt_list:
        print(ter.center(8),end="")
    print("")
    for non, row in  zip(non_colt_list,analy_table_list):
        print( non+":",end="")
        for right in row:
            print(right.center(8),end="")
        print("")
##求LL(1)分析表
def get_table():
    analy_table_list = [['empty' for col in range(len(su_ter_colt_list))] for row in range(len(non_colt_list))]
    for (analy_left, analy_right) in zip(analy_left_list, analy_right_list):  #终结符，处理
        if analy_right[0]  in ter_colt_list:
            if analy_right[0] !='$':
                analy_table_list[non_colt_list.index(analy_left)][su_ter_colt_list.index(analy_right[0])] = analy_right 
            if analy_right[0] == '$':
                for follow in follow_dict[analy_left]:
                    analy_table_list[non_colt_list.index(analy_left)][su_ter_colt_list.index(follow)] = analy_right
        else:   #非终结符
            for first in first_dict[analy_right[0]]:
                analy_table_list[non_colt_list.index(analy_left)][su_ter_colt_list.index(first)] = analy_right
            if '$' in first_dict[analy_right[0]]:
                for follow in follow_dict[analy_left]:
                    analy_table_list[non_colt_list.index(analy_left)][su_ter_colt_list.index(follow)] = analy_right
    return analy_table_list

##LL1语法分析
def analysis(test_str):
    global analy_flag
    four_num=0
    four_tmp_var =0
    first_sentence_flag =0
    while_flag=0
    left_any = test_str[::-1]   #剩余未分析字符串，字符逆序
    analy_stack.append('#')     #分析栈，将#入栈，初始
    analy_stack.append(non_colt_list[0])  #开始符入栈
    print("LL(1)文法分析过程：\n"+"分析栈".center(30)+"剩余输入串".center(70)+"推导式".center(20))
    while len(left_any) > 0:
        ##分析栈
        out = ""
        for single in analy_stack:
            out += single
        print(out.center(30),end="")

        ##剩余输入串
        out =""
        out = left_any[::-1]
        print(out.center(70),end="")
        char1 = analy_stack[len(analy_stack)-1]
        char2 = left_any[len(left_any) -1]
        if (char1 == char2) and (char1 == '#'):   #结束分析，接受字符串
            print("接受语法".center(40))
            return
        if char1 == char2:
            analy_stack.pop()       #匹配，分析栈出栈操作
            left_any=left_any[:-1]  #匹配,字符串，去除末尾字符
            print("匹配".center(40))
        elif analy_table_list[non_colt_list.index(char1)][su_ter_colt_list.index(char2)]!="empty":
            right_str = analy_table_list[non_colt_list.index(char1)][su_ter_colt_list.index(char2)]
            analy_stack.pop()
            if right_str !="$":   #产生式不是$，则逆序入栈。是$则不入栈
                copy=right_str[::-1]  
                for single in copy:
                    analy_stack.append(single)
            #推导式
            print(right_str.center(40))
        else:
            print("出错！".center(40))
            analy_flag =1
            return

if __name__ == "__main__":
    analy, non_colt_list, ter_colt_list, su_ter_colt_list = get_base_data(analy,non_colt_list,ter_colt_list,su_ter_colt_list)
    follow_step = 0
    print(analy)
    print(non_colt_list)
    print(ter_colt_list)
    print(su_ter_colt_list)
    analy_left_list = analy["left"]  #产生式左部list
    analy_right_list = analy["right"] #产生式右部list
    ##求FIRST集
    for non_colt in non_colt_list:   
        get_first(non_colt)
    for key in first_dict:   #FIRST集，终结符去重
       temp_list = list(set(first_dict[key]))  
       temp_list.sort(key=first_dict[key].index)
       first_dict[key] = temp_list
    
    ##求FOLLOW集
    for non_colt in non_colt_list:   
        if follow_step == 0 :       #开始符的follow集，#
            follow_dict[non_colt]=["#"]
            follow_step +=1
        get_follow(non_colt)
    for key in follow_dict:   #FOLLOW集，终结符去重
       temp_list = list(set(follow_dict[key]))  
       temp_list.sort(key=follow_dict[key].index)
       follow_dict[key] = temp_list
    line_sign ="#"
    print("FIRST集")
    print(line_sign*100)
    for key in first_dict:
        print(key,first_dict[key])
    print(line_sign*100)

    print("FOLLOW集")
    for key in follow_dict:
        print(key,follow_dict[key])
    print(line_sign*100)

    ##求LL(1)分析表
    analy_table_list=get_table()
    print_table()
    #词法分析
    #test_str = "zy(){;xa;xb;;;a=2;b=3;w(a<b){;t(a<b){a=0;}w(a<b){a=3;}}u{r(a);}s0;}#"
    try:
        test_str =analy_word()
    except:
        print("词法分析出错！！")
    else:
    #语法分析，支持if,while的多重嵌套
        analysis(test_str)
        if analy_flag!=1:
    ##四元式与汇编代码的生成，暂不支持if,while的多重嵌套
    #生成四元式
            four_dict,variate_name_list = make_four(test_str)
    #生成汇编
            make_assembly(four_dict,variate_name_list)





