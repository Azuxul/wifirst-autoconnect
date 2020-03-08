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
    
    post = {}

    for elem in data[1]:
        post[elem[0]] = elem[1]

    rep = requests.post(data[0], data=post, headers=headers)
    if rep.history[-1].url == post["success_url"]:
        return True


#print(getInternalLogin())
login()
