# wildPwn
Its a simple tool for WildFly. Tool can be used to brute force or shell deploy. *wildPwn.war* contains modified Laudanum Shell. *userList.txt* contains common usernames and *passList.txt* contains common passwords.

#Usage
Bruteforce
./wildPwn.py -m brute --target <TARGET> -user <USERNAME LIST> -pass <PASSWORD LIST> 

Deploy
./wildPwn.py -m deploy --target <TARGET> --port <PORT> -u <USERNAME> -p <PASSWORD>
