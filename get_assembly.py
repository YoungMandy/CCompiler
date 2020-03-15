
def make_assembly(four_dict,variate_name_list):
    # print(variate_name_list)
    # print(len(four_dict))
    four_len = len(four_dict)
    part1=["assume cs:code,ds:data","data segment"]
    for si in variate_name_list:     #声明变量
        st="\t"+si+" dd 0"
        part1.append(st)
    part1.append("data ends")
    #代码块
    part2 =["code segment","start:","\tmov ax,data","\tmov ds,ax"]
    flag =0 #忽略标识
    for si in four_dict:
        if flag ==1:
            flag=0
            continue
        if four_dict[si][0]=="=":#赋值语句入口
            part2.append("L"+str(si)+":"+"\tmov ax,"+four_dict[si][1])
            part2.append("\tmov "+four_dict[si][3]+",ax")
        elif four_dict[si][0]=="c":  #输入
            part2.append("L"+str(si)+":"+"\tmov ah,01h")
            part2.append("\tint 21h")
            part2.append("\tmov "+four_dict[si][1]+",ah")
            
        elif four_dict[si][0] =="<":
            part2.append("L"+str(si)+":\tcmp "+four_dict[si][1]+","+four_dict[si][2])
            part2.append("\tjnb "+"L"+str(four_dict[si+1][1]))
            flag=1  #忽略下一句
        elif four_dict[si][0] ==">":
            part2.append("L"+str(si)+":\tcmp "+four_dict[si][1]+","+four_dict[si][2])
            part2.append("\tjna "+"L"+str(four_dict[si+1][1]))
            flag=1  #忽略下一句
        elif four_dict[si][0]=="RJ":
            part2.append("L"+str(si)+":"+"\tjmp short "+"L"+str(four_dict[si][1]))
        elif four_dict[si][0]=="r":   #输出
            part2.append("L"+str(si)+":"+"\tmov dl,"+four_dict[si][1])
            part2.append("\tmov ah,2")
            part2.append("\tint 21h")
        elif four_dict[si][0] =="re":
            part2.append("L"+str(si)+":\tmov ax,4c00h")
            part2.append("\tint 21th")
    part2.append("code ends")
    part2.append("end start")
    total = part1+part2
    print("#"*100+"\n最终代码：")
    out_assembly = []
    for si in total:
        print(si)
        out_assembly.append(si+"\n")
    print("#"*100)
    ##存储汇编
    four_file =open("assembly.txt","w+")
    four_file.writelines(out_assembly)
    four_file.close()
   




