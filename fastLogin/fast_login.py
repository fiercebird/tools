#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import datetime
import time
import copy
#coding:utf-8

"""
to fast login to proxy server version 2.0

format  :python fast_login server_key_word type num set
example :python fast_login.py spdy test [1/2/3...] [sz1/sz2/...]
meaning :
    server_key_word:like spdy adblock subres
    type           :test or real
    num            :which machine wanted,when its a set

[1]  extend by randyma 2015-8-4
format  :python fast_login 10.196.22.172:/data/home/logSearch/result/1438650072627_4619
meaning :when you use the log platform you will know
"""

def usage():
    print "-------------------------------info of python-------------------------------"
    print "python：", sys.argv[0]
    for i in range(1, len(sys.argv)):
        print "param",i,":",sys.argv[i]
    if(len(sys.argv)<3) :
        print "arguments miss..."
        print """
        to fast login to proxy server

        format  :python fast_login server_key_word type num set
        example :python fast_login.py spdy test [1/2/3...] [sz1/sz2/...]
        meaning :
            server_key_word:like spdy adblock subres
            type           :test or real
            num            :which machine wanted,when its a set
        """
        os._exit(0)
def myend():
    print "****   customer  terminal ******"
    os._exit(0)
def println(arr):
    for line in arr:
        print line




def init_proxy_data(arr):
    file_object = open("proxy.data")
    for line in file_object:
        line = line.strip()
        if(line.find("#") == 0) :
	    #print "find # line:",line
            continue
        arr.append(line.split("|"))
    file_object.close()

def get_proxy_data_result(arr,key,env):
    result = []
    for line in arr:
        if (line[0].lower().find(key) != -1 and  line[1].lower().find(env) != -1):
            result.append(line)
    return result

def write_to_file(str_content,filename):
    file_object = open(filename,'w')
    file_object.write(str_content)
    file_object.close()
def read_from_file(str_content,filename):
    file_object = open(filename)
    str_content = file_object.read()
    file_object.close()

def create_ssh_login_file(arr):
    count = 0
    os.system("rm tmp*.sh")
    template_file_object = open("template.sh")
    template_str = template_file_object.read()
    #print "  ....   %s  \n " ,template_str
    for line in arr:
        count += 1
        ip = line[2]
        ssh_file = "tmp" + str(count) + ".sh"
        server_path = "/usr/local/app/taf/app_log/MTT/" + line[0]
        to_server_path = "send \"cd " + server_path + "> /dev/null 2>&1\\r\""
	line.append(ssh_file)
        new_ssh_file_str = template_str
        new_ssh_file_str = new_ssh_file_str.replace("ip_placeholder",ip)
        new_ssh_file_str = new_ssh_file_str.replace("#change_to_server_path",to_server_path)        
        write_to_file(new_ssh_file_str,ssh_file)
        #print "new ssh file \n ",new_ssh_file_str
        ssh_command = "chmod 777 " + ssh_file
        print "ssh command:" , ssh_command
        os.system(ssh_command)
    template_file_object.close()

def login_mmt(ssh_file_name):
    #return 
    print "\n\n+++++++++++++++++    run ssh login  +++++++++++++++++++++++\n\n"
    login_command = "./" + ssh_file_name
    os.system(login_command)

#something like 10.196.22.172:/data/home/logSearch/result/1438650072627_4619
def check_if_is_log_login():
    if(len(sys.argv) < 2):
	pass
    ip_path = sys.argv[1]
    arrs = ip_path.split(':')
    ip = arrs[0]
    if(len(ip.split('.')) != 4):
        return 
    path = arrs[1]
    ssh_file = "tmp.sh"
    to_log_path = "send \"cd " + path + "> /dev/null 2>&1 \\r\""
    template_file_object = open("template.sh")
    template_str = template_file_object.read()
    template_file_object.close()
    new_ssh_file_str = template_str
    new_ssh_file_str = new_ssh_file_str.replace("ip_placeholder",ip)
    new_ssh_file_str = new_ssh_file_str.replace("#change_to_server_path",to_log_path)
    write_to_file(new_ssh_file_str,ssh_file)
    ssh_command = "chmod 777 " + ssh_file
    print "ssh command:" , ssh_command
    os.system(ssh_command)
    login_mmt(ssh_file)
    myend()
    

if __name__=="__main__":
    check_if_is_log_login()
    usage()
    proxy_data = []
    init_proxy_data(proxy_data)
    #print "len of proxy_data ",len(proxy_data)
    #print "data[1]:",proxy_data[0]
    server_key_word=(sys.argv[1]).lower()
    environment=(sys.argv[2]).lower()
    result = get_proxy_data_result(proxy_data,server_key_word,environment)
    create_ssh_login_file(result)
    print "-------------------------------------result:--------------------------------------"
    print "%s server at %s environment  find %d ip as" % (server_key_word,environment,len(result))
    iCount = 0
    for line in result:
        iCount += 1
        print "<%d> %s" %(iCount,line)
    print " \n "
    if(len(result) == 0) :
        print ">>>>>>>>>        nothing fount, exit"
    elif(len(result) == 1):
        print ">>>>>>>>>        use <%d> %s " % (1,result[0][2])
        login_mmt(result[0][3])
    else:
        choice = raw_input("input the num :")
        if(choice.find("go") != -1):
            print ">>>>>>>>>        use <%d> %s " % (1,result[0][2])
            login_mmt(result[0][3])
        elif(choice.find("exit") != -1):
            print ">>>>>>>>>        nothing choice, exit"
        elif(choice.isdigit()):
            line_number = int(choice)
            print ">>>>>>>>>        use <%d> %s " % (line_number,result[line_number-1][2])
            login_mmt(result[line_number-1][3])
        else:
            print ">>>>>>>>>        input error (%s) exit" % choice
    pass


            

    

