#产生式#
analy={
    "left":["PRO","FUN_DE","FUN_PR","FUN_NAME","COM_STA" ,
                "VAR_LI","VAR_LI_S","VAR_LI_S","VAR_DE","VAR_DE",
                "VAR_TYPE","VAR_TYPE","STA_LI","STA_LI_S","STA_LI_S","STA",
                "STA","STA","STA","STA","STA","STA","CIR_STA","CIR_STA",
                "OUT_STA","VAR_FM_LI",
                "VAR_FM_LI_S","VAR_FM_LI_S","VAR_FM","VAR_FM","VAR_FM",
                "VAR_NAME_LI_S","VAR_NAME_LI_S","ES_ STA",
                "ELSE_SET","ELSE_SET","AS_STA","CAL_EXP",
                "SELF_OPR","SELF_OPR","OPR","OPR","OPR","OPR","C_CHAR","C_CHAR",
                "C_CHAR","C_CHAR","C_CHAR","B_EXP","B_EXP",
                "B_EXP","EXP_TE","WHILE_STA",
                "FOR_STA","VAR_NAME",
                "S_CHAR","S_CHAR","LETTER","LETTER","LETTER","LETTER","CHAR_S",
                "CHAR_S","NUM","NUM","NUM","NUM","NUM","NUM","NUM","NUM","NUM","NUM"
            ],
    "right":[
                ["FUN_DE"],["FUN_PR","FUN_NAME","(",")","COM_STA"],["void"],["main"],["{", "VAR_LI","STA_LI","return","0",";","}"],
                ["VAR_DE","VAR_LI_S"],["VAR_DE","VAR_LI_S"],["$"],["VAR_TYPE","VAR_NAME",";"],["$"],
                ["int"],["float"],["STA", "STA_LI_S"],["STA", "STA_LI_S"],["$"],["CIR_STA"],
                ["OUT_STA"],["AS_STA"],["ES_STA"],["WHILE_STA"],["FOR_STA"],["$"],["break", ";"],["continue", ";"],
                ["printf", "(","\"", "VAR_FM_LI", "\"", "," ,"VAR_NAME_LI",")",";"],["VAR_FM", "VAR_FM_LI_S"],
                ["VAR_FM","VAR_FM_LI_S"],["$"],["%d",","],["%f",","],["VAR_NAME","VAR_NAME_LI_S"],
                ["VAR_NAME","VAR_NAME_LI_S"],["$"],["if","(", "EXP", ")", "{", "STA_LI", "}" ,"ELSE_SET"],
                ["else", "{", "STA_LI", "}"],["$"],["VAR_NAME", "=", "CAL_EXP", ";"],["VAR_NAME", "OPR", "VAR_NAME"],
                ["++","VAR_NAME"],["--", "VAR_NAME"],["+"],["-"],["*"],["/"],[">"],["<"],
                [">="],["<="],["=="],["EXP_TE", "&&", "EXP_TE"],["EXP_TE" ,"||", "EXP_TE"],
                ["EXP_TE"],["VAR_NAME", "C_CHAR" ,"VAR_NAME"],["while", "(", "B_EXP", ")", "{", "STA_LI", "}"],
                ["for", "(", "VAR_NAME", ";", "B_EXP", ";", "SELF_OPR" ,")", "{", "STA_LI", "}"],["S_CHAR", "CHAR_S"],
                ["LETTER"],["_"],["a"],["b"],["c"],["d"],["LETTER", "NUM"],
                ["LETTER"],["0"],["1"],["2"],["3"],["4"],["5"],["6"],["7"],["8"],["9"]
            ]
}
##终结符
ter_colt_list = [
            "a","b","c","d","1","2","3","4","5","6","7","8","9","_",
            "{","}","(",")","+","-","*","/",";",">","<","=","==",">=",
            "<=","!=","&&","||","int","float","%d","%f","void","main","break","continue",
            "\"",",","printf","++","--","for","if","else","while","$","#"
        ]
##非终结符
non_colt_list = [
            "PRO","FUN_DE","FUN_PR","FUN_NAME" ,"COM_STA" ,
            "VAR_LI" ,"VAR_LI_S" ,"VAR_DE","VAR_TYPE", "STA_LI" ,
            "STA_LI_S" ,"STA" ,"CIR_STA" ,"OUT_STA" ,"VAR_FM_LI" ,
            "VAR_FM_LI_S" ,"VAR_FM" ,"VAR_NAME_LI_S" ,"ES_STA" ,"ELSE_SET" ,
            "AS_STA" ,"CAL_EXP" ,"SELF_OPR","OPR", "C_CHAR" ,"B_EXP" ,"EXP_TE" ,
            "WHILE_STA" ,"FOR_STA" ,"VAR_NAME" ,"S_CHAR" ,"LETTER" ,"CHAR_S" ,"NUM"
        ]
first_dict = {}
analy_left_list = analy["left"]  #产生式左部list
analy_right_list = analy["right"] #产生式右部list

# 求FIRST集
def get_first(non_colt):
    tag = 0;
    flag = 0;
    step =0;
   
    for (analy_left, analy_right) in zip(analy_left_list, analy_right_list):
        if analy_left == non_colt:
            if analy_left in first_dict: 
                pass
            else:
                first_dict[non_colt]=[]       #FIRST以非终结符建立关键字
            if analy_right[0] in ter_colt_list:   #产生式右部首字符为非终结符，则字符属于FIRST集
                first_dict[non_colt].append(analy_right[0])
                # print(analy_right[0])
            else:
                for single_right in analy_right:
                    if single_right in ter_colt_list :
                        first_dict[non_colt].append(single_right)
                        break
                    print(single_right)
                    get_first(single_right)  #递归，求右部非终结符的FIRST
                    # print(first_dict)
                    for  ter in first_dict[single_right]:
                        if ter == "$":              
                            flag =1
                        else:
                            first_dict[non_colt].append(ter)  #$不属于FIRST(single_right)，FIRST(single_right)属于FIRST(non_colt)
                    if flag == 0:
                        break
                    else:
                        tag +=flag
                        flag = 0
                if tag == len(analy_right):  #所有右部first(Y)都有$,将$加入FIRST(X)中  
                    first_dict[non_colt].append("$")


#求FOLLOW集
def get_follow():
    pass
if __name__ == "__main__":
    for non_colt in non_colt_list:
        get_first(non_colt)
        print(first_dict)
    # for non_colt in non_colt_list:
    #     if 
    for a,b in first_dict:
        print(a,b)
