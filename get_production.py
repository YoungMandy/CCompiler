def get_base_data(analy,non_colt_list,ter_colt_list,su_ter_colt_list):
    # analy = {};  #产生式
    # analy["right"] = [] #产生式右部
    # analy["left"] = [] #产生式左部
    # ##终结符
    # ter_colt_list = []
    # ##非终结符
    # non_colt_list = []
    for line in open("wenfa.txt"):
        line = line.rstrip('\n')    #去除回车符
        analy["left"].append(line[0])   # A->aBc ,取A
        analy["right"].append(line[3:])
        if line[0] not in non_colt_list:
            non_colt_list.append(line[0])
        for sigle in line[3:]:      #非终结符，非A-Z
            if (sigle < 'A' ) or (sigle > 'Z' ):
                if sigle not in ter_colt_list:
                    ter_colt_list.append(sigle)
                    if sigle != '$':
                        su_ter_colt_list.append(sigle)
    ter_colt_list.append('#')
    su_ter_colt_list.append('#')  
    return  analy,non_colt_list,ter_colt_list,su_ter_colt_list