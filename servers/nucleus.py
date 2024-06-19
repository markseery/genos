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
#       Name: nucleus.py
#       Author: Mark Seery
#
#   Notes
#   -----
#
#   The main distributed manager of the overall system
#
#   The goal is to achieve a level of simplicity for the
#       programmer using Simplepy, by providin one class
#       to which all the calls are made, without having
#       to keep track of the classes actually doing the work
#
##########################################################################
# todo: 
#       Placeholder until I work out a better way to deal with
#       process not terminated properly
#       sudo lsof -i -P | grep LISTEN | grep 6000
##########################################################################
import genos.configuration as configuration
import genos.commserver as commserver
import genos.logger as logger
import time
import threading 

def setGlobals():
    global appName, serviceName, host, port, config, log, lmPrefix
    log = logger.Logger()
    serviceName = 'nucleus'

    try:
        config = configuration.Configuration()
        appName = config.getAppName()
        host = config.getHost(serviceName)
        port = config.getPort(serviceName)
    except Exception as e:
        print("Error in setGlobals: ", e)
        logMessage(lmPrefix + "Error in setGlobals: " + str(e))

    lmPrefix = appName + " - " + serviceName + " : " 
    
def logMessage(message):
    source =  serviceName + ': ' + host + ':' + str(port)
    logMessage = {"level": "info", "source": source, "message": message}
    log.addLog(logMessage)
    
def queryServer(param):
    print(lmPrefix + "called query server")
    cs = commserver.CommServer()
    cs.run(host=host, port=int(port))
    print(lmPrefix + "query server should be running on: ", host, port)

if __name__ == '__main__':
    setGlobals()
    print(lmPrefix + "Initializing")
    logMessage(lmPrefix +  "Initializting")
    qsRC = threading.Thread(target=queryServer, args=(1,))
    qsRC.start()

    