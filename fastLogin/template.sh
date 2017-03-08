#!/usr/bin/expect

spawn ssh mqq@ip_placeholder
expect {
        "password:" { send "XXXXXXX\r" }
        "(yes/no)?" { send "yes\r"
        expect "password:" { send "XXXXXXX\r" }
        }
    }
#change_to_server_path
   interact

