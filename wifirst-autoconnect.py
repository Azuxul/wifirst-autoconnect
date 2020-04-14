#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (C) 2020  Lancelot H. (Azuxul)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""



import requests
import credentials
from bs4 import BeautifulSoup

LOGIN_HOST = "https://smartcampus.wifirst.net/"
LOGIN_PAGE_URL = "https://smartcampus.wifirst.net/sessions/new"


USER = credentials.LOGIN
PASSWORD = credentials.PASSWORD

session = requests.Session()

headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
        "Content-Type" : "application/x-www-form-urlencoded",
    }


def getUserLoginInfo():
    rep = session.get(LOGIN_PAGE_URL, headers=headers)

    sigin = BeautifulSoup(rep.text, features="html.parser").find("form", {"id" : "signin-form"})

    if sigin:
        token_input = sigin.find("input", {"name" : "authenticity_token"})
        if token_input:
            return sigin["action"], token_input["value"]


def extractData(response):
    data = BeautifulSoup(response.text, features="html.parser").find("form", {"name" : "log"})

    if data:
        URL = data["action"]
        inputs = data.findAll("input")
        login_data = []

        if len(inputs) > 0:
            for field in inputs:
                name = field["name"]
                value = field["value"]

                login_data.append([name, value])

            return URL, login_data


def getInternalLogin():

    logInfo = getUserLoginInfo()

    url = LOGIN_HOST + logInfo[0] if logInfo[0].startswith("/") else logInfo[0]

    data = {
        "utf8" : "✓",
        "authenticity_token" : logInfo[1],
        "login" : USER,
        "password" : PASSWORD
        }

    rep = session.post(url, data=data, headers=headers)
    if rep.status_code == 200:
        
        new_url = BeautifulSoup(rep.text, features="html.parser").find("meta", {"http-equiv" : "refresh"})

        print(new_url)
        if new_url:
            start_index = new_url["content"].find("URL=") + 4
            new_url = new_url["content"][start_index:]
            
            rep = session.post(new_url, headers=headers)
         
            if rep.status_code == 200:
                return extractData(rep)


def login(withInternalLogin = True):

    if withInternalLogin:
        data = credentials.INTERNAL_LOGIN
    else:
        data = getInternalLogin()
        print(data)
    
    post = {}

    for elem in data[1]:
        post[elem[0]] = elem[1]

    rep = requests.post(data[0], data=post, headers=headers)
    if rep.history[-1].url == post["success_url"]:
        return True


import sys, getopt

def main(argv):
	password = None
	username = None
   
	try:
		opts, args = getopt.getopt(argv,"asu:p:")
	except getopt.GetoptError:
		print('wifirst-autoconnect.py')
		print('-u <username> -p <password>')
		print('-a Use direct connexion with saved info in credentials.py')
		print('-s Use password and username in credentials.py')
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print('wifirst-autoconnect.py')
			print('-u <username> -p <password>')
			print('-a Use direct connexion with saved info in credentials.py')
			print('-s Use password and username in credentials.py')
			sys.exit()
		elif opt == '-u':
			username = arg
		elif opt == '-p':
			password = arg
		elif opt == '-a':

			print('Start connexion with direct connexion info')
			login()
			return
		elif opt == '-s':
			print('Start connexion with saved username and password')
			login(False)
			return
			
	if password is not None and username is not None:
		PASSWORD = password
		USER = username
		
		print('Start connexion')
		login(False)
		return

if __name__ == "__main__":
   main(sys.argv[1:])
