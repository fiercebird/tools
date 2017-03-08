#!/usr/bin/expect

spawn ssh admin@[lindex $argv 0]
set ps [lindex $argv 1]
expect {
        "password:" { send "$ps\r" }
        "(yes/no)?" { send "yes\r"
        expect "password:" { send "$ps\r" }
        }
    }
send "ldconfig -p |grep ssl\r"
send "cd /usr/lib\r"
   interact

