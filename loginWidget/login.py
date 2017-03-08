#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import re



"""
@copyright: Copyright (C) 1998-2012 TENCENT Inc.All Rights Reserved.
@author: allsochen@tencent.com
@date 2013-04-19 下午04:19:25
@edit 2014-12-01  monkeyhe 增加自定义配置
@edit 2017-03-07  monkeyhe 格式调整
@version: 1.0
@
"""

class Node(object):

    def __init__(self, ip, name, desc):
        self.ip = ip
        self.name = name
        self.desc = desc

class NodeTable(object):
    def __init__(self, nodes):
        self.nodes = nodes

    def __str__(self):
        table = []
        table.append("+%-5s+%-15s+%-25s+%-20s+\n" % ("-" * 5, "-" * 15, "-" * 25, "-" * 20))
        table.append("|%-5s|%-15s|%-25s|%-20s|\n" % ("index", "ip", "name", "description"))
        table.append("+%-5s+%-15s+%-25s+%-20s+\n" % ("-" * 5, "-" * 15, "-" * 25, "-" * 20))
        for index in range(len(self.nodes)):
            node = self.nodes[index]
            table.append("|%-5s|%-15s|%-25s|%-20s|\n" % (str(index), node.ip, node.name, node.desc))
        table.append("+%-5s+%-15s+%-25s+%-20s+\n" % ("-" * 5, "-" * 15, "-" * 25, "-" * 20))
        return "".join(table)

class MysqlConfig(object):
    def __init__(self, env, ip, port, database, user, password, charset = 'gbk'):
        self.env = env
        self.ip = ip
        self.port = str(port)
        self.database = database
        self.user = user
        self.password = password
        self.charset = charset

    def build(self):
        return ("mysql -h{ip} -P{port} -u{user} -p{password} -D{database} " + 
                "--default-character-set={charset}").format(ip = self.ip,
                                                            port = self.port,
                                                            user = self.user,
                                                            password = self.password,
                                                            database = self.database,
                                                            charset = self.charset);

class MysqlTable(object):
    def __init__(self, nodes):
        self.nodes = nodes

    def __str__(self):
        table = []
        column = ["", "%-5s", "%-5s", "%-30s", "%-15s", "%-5s", "%-10s", "%-10s", "%-10s", ""];
        head = "+".join(column) + "\n";
        line = "|".join(column) + "\n";
        header = head % ("-" * 5, "-" * 5, "-" * 30, "-" * 15, "-" * 5, "-" * 10, "-" * 10, "-" * 10);
        
        table.append(header);
        table.append(line % ("index", "env", "database", "ip", "port", "user", "password", "charset"))
        table.append(header);
        for index in range(len(self.nodes)):
            node = self.nodes[index]
            table.append(line % (str(index), node.env, node.database, node.ip, node.port, 
                                 node.user, node.password, node.charset))
        table.append(header);
        return "".join(table)



####################### CONFIG BEGIN ######################    
hosts = {}
# Add your short IP here.
hosts["111"] = "172.17.150.111"
hosts["222"] = "10.123.128.222"
hosts["123"] = "10.12.197.123"

mysqls = {
        "video": [
            MysqlConfig("test", "10.123.123.123", 1234, "db_name", "XXXX", "", "utf8"),
            MysqlConfig("REAL", "10.123.123.123", 1234, "db_name", "XXXX", "XXXXX", "utf8")
            ],
        "old": [
            MysqlConfig("test", "10.123.123.123", 1234, "db_name", "XXXX", "", "utf8"),
            MysqlConfig("REAL", "10.123.123.123", 1234, "db_name", "XXXX", "XXXX@XXXX", "utf8")
            ],
}

# Add your set IP here, 
# Notice: can't name you node by 'mysql'.
nodes = {
#    "login": [
#        Node("172.17.150.109", "LoginServer", "wupsz1")
#    ],
#    "hadoop": [
#        Node("10.196.23.143", "hadoop", "hadoop")
#    ],
#    "logtool": [
#        Node("10.147.22.228", "logtool", "logtool")
#    ],
#    "remote": [
#        Node("10.196.23.142", "LoginServer", "login"),
#    ],
    "cron": [
        Node("10.196.23.97",    "VideoCronServer", "Cron"),
        Node("10.147.18.163",   "VideoCronServer", "Cron")
    ],
    "center": [
            Node("12.231.129.103", "VideoCenterServer", "SZ"), 
            Node("10.231.129.104", "VideoCenterServer", "SZ"), 
            Node("10.169.24.16  ", "VideoCenterServer", "TJ"), 
            Node("10.168.16.205 ", "VideoCenterServer", "TJ"), 
            Node("10.147.18.100 ", "VideoCenterServer", "SH"), 
            Node("10.147.23.98  ", "VideoCenterServer", "SH"), 
    ],
    "html": [
            Node("10.209.7.83",     "VideoHtmlServer", "SZ"),
            Node("10.233.136.75",   "VideoHtmlServer", "TJ"),
            Node("10.150.170.93",   "VideoHtmlServer", "SH"),
    ],
}


######################CONFIG END ##########################    


class Utilities(object):
    @staticmethod
    def ssh(ip):
        cmd = "x %s" % ip
        os.system(cmd)

    @staticmethod
    def isIP(ip):
        ip = re.findall(r'\d+.\d+.\d+.\d+', ip)
        return len(ip) == 1

    @staticmethod
    def mysql(config):
        cmd = config.build();
        print("execute `%s`" % cmd)
        os.system(cmd)

class Login(object):
    def __init__(self, option, desc):
        self.option = option
        self.desc = desc

    def start(self):
        if Utilities.isIP(self.option):
            Utilities.ssh(self.option)
        elif self.option.isdigit():
            ip = hosts.get(self.option)
            if ip == None:
                print ("Can't find IP by specified number.")
                sys.exit()
            else:
                Utilities.ssh(ip)
        else:
            values = []
            if nodes.has_key(self.option):
                values = nodes.get(self.option)
            else:
                for key in nodes.keys():
                    if key.find(self.option) != -1:
                        values.extend(nodes.get(key))
            if self.desc != "":
                filters = []
                for i in range(len(values)):
                    if values[i].name.find(self.desc) != -1 or values[i].desc.find(self.desc) != -1:
                        filters.append(values[i])
                values = filters
            if len(values) == 0:
                print ("Can't find IP by specified option.")
                sys.exit()
            elif len(values) == 1:
                print(NodeTable(values))
                print("as")
                Utilities.ssh(values[0].ip)
                sys.exit()
            else:
                print(NodeTable(values))
            while True:
                try:
                    index = input("Please input your index to login: \n")
                    if int(index) < len(values):
                        Utilities.ssh(values[index].ip)
                        break
                except:
                    print ("Please entry number in below index!\n")
                    sys.exit()

class Mysql(object):
    def __init__(self, database, env = ""):
        self.database = database
        self.env = env
    
    def start(self):
        if not mysqls.has_key(self.database):
            print ("Can't find database `%s`." % self.database)
            sys.exit()
        values = mysqls.get(self.database)
        if self.env != "":
            filters = []
            for value in values:
                if value.env.find(self.env) != -1:
                    filters.append(value)
            values = filters
        if len(values) == 0:
            print ("Can't find database `%s` by env `%s`." % (self.database, self.env))
            sys.exit()
        if len(values) == 1:
            # Execute mysql directly.
            print(MysqlTable(values))
            Utilities.mysql(values[0])
            sys.exit()
        else:
            # Waiting for user input.
            print(MysqlTable(values))
            index = 0;
            while True:
                try:
                    index = input("Please input your index to login mysql:\n")
                    if int(index) < len(values):
                        break
                except:
                    print ("Please entry index number in below table!\n")
                    sys.exit()
            Utilities.mysql(values[index])
            sys.exit()


if __name__ == '__main__':
#     try:
    if len(sys.argv) < 2:
        print ("Usage: god [number, option, servername] | god mysql [database] [env]")
        print ("     : god help | god all | god mysql | god option desc")
        sys.exit()
    else:
        option = sys.argv[1]
        if option == "help" or option == "man":
            print ("NAME\r\n\tgod - convenient command for ssh/mysql.\r\n")
            print ("SYNOPSIS\r\n\tgod [OPTION]...| god mysql [OPTION]")
            print ("EXAMPLE\r\n\tgod 109")
            print ("\r\n\tgod login")
            print ("\r\n\tgod hadoop")
            print ("AUTHOR\r\n\tWritten by allsochen")
            print ("DESCRIPTION\r\n")
            for key in nodes.keys():
                nodeT = nodes.get(key)[0]
                print ("\tgod %s\t ----Name: %s -Desc: %s" % (key, nodeT.name, nodeT.desc))
            sys.exit()
        elif option == "all":
            print ("--------host info----------")
            for key in hosts.keys():
                print ("god %s\t\t\t-- %s" % (key, hosts.get(key)))
            print ("--------node info----------")
            for key in nodes.keys():
                nodeList = nodes.get(key)
                for i in range(len(nodeList)):
                    nodeT = nodeList[i]
                    print ("god %s\t%i\t----Name: %s -Desc: %s" % (key, i, nodeT.name, nodeT.desc))
        elif option == "mysql":
            # Handle mysql login.
            if len(sys.argv) >= 3:
                database = ""
                env = ""
                database = sys.argv[2]
                if (len(sys.argv) >= 4):
                    env = sys.argv[3]
                mysql = Mysql(database, env)
                mysql.start()
            else:
                print ("Usage: god mysql [database] [env]")
                sys.exit()
        else:
            desc = ""
            if len(sys.argv) == 3:
                desc = sys.argv[2]
            login = Login(option, desc)
            login.start()
#     except Exception as e:
#         print ("Good luck to you... (*^__^*)")
