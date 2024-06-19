##########################################################################
#
#   Copyright / License notice 2024
#   --------------------------------
#
#   Permission is hereby granted, free of charge,
#       to any person obtaining a copy of this software
#       and associated documentation files (the “Software”),
#       to deal in the Software without restriction, including
#       without limitation the rights to use, copy, modify, merge,
#       publish, distribute, sublicense, and/or sell copies of the Software,
#       and to permit persons to whom the Software is furnished to do so,
#       subject to the following conditions:
#
#   The above copyright notice and this permission notice shall be included
#       in all copies or substantial portions of the Software.
#
##########################################################################
#
#   Details
#   -------------
#
#       Name: commchanel.py
#       Author: Mark Seery
#
#   Notes
#   -----
#
#   The only purpose is to create a little abstraction and future
#       flexibility for different communication mechanisms such as
#       REST, Websockets, GraphQL, etc.
#
##########################################################################
import json
import requests

import genos.configuration as configuration
config = configuration.Configuration()

class Commchannel():
    def __init__(self):
        pass

    def sendDataJson(self,url,queryData):
        try:
            response = requests.get(url, json = queryData)
            print(response.json())
            return True
        except requests.exceptions.ConnectionError:
            print("commchannel connection error on sendData: ", url)
            return False
        except Exception as e:
            print("commchannel unknown exception on sendData: ", url)
            print(e)    # the exception type
            return False
        
    def sendDataArgs(self,url,args):
        fullURL = url + "?" + args
        print("sendDataArgs - fullURL: ", fullURL)
        try:
            response = requests.get(fullURL)
            print(response.text)
            return response.text
        except requests.exceptions.ConnectionError as e:
            print("commchannel connection error on sendDataArgs: ", fullURL)
            return ('Error on connection: ', fullURL, e)
        except Exception as e:
            print("commchannel unknown exception on sendDataArgs: ", fullURL)
            print(e)    # the exception type
            return ('Error on connection: ', fullURL, e)





    



    
    

