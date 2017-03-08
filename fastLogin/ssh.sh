#!/usr/bin/expect

spawn ssh mqq@[lindex $argv 0]
expect {
        "password:" { send "XXXXXXX\r" }
        "(yes/no)?" { send "yes\r"
        expect "password:" { send "XXXXXX\r" }
        }
    }
   interact

