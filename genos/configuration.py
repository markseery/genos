########################################################################################
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
########################################################################################
#
#   Details
#   -------------
#
#       Name: configuration.py
#       Author: Mark Seery
#
#   Notes
#   -----
#
#       Retrieve configuration data from the config.yaml file
#       Currently used as class, may later be converted to a server/process
#       May go back and add namespace and make it a general key/value store
#
########################################################################################
import yaml
import os

class Configuration():
    def getConfig(self):
        with open('./config.yaml', 'r') as file:
            configuration = yaml.safe_load(file)
        return configuration
    
    # Decided to leave it as each method grabbing a new copy of
    # the config file, if there is ever a need to change while
    # running, it will be easier to pick up changes
    # seems redundant, I know. Will revisit later
    
    def getHost(self,name): return self.getConfig()['host'][name]
    def getPort(self,name): return self.getConfig()['port'][name]
    def getAppName(self): return self.getConfig()['application']['name']
    def getGpt4Default(self): return self.getConfig()['llm']['gpt4default']
    def getGpt3Default(self): return self.getConfig()['llm']['gpt3default']
    def getMaxLLMSize(self): return self.getConfig()['llm']['maxLLMSize']
    
    def getOpenAIKey(self):
    ########################################################################################
    #   First check if the openai key is in the config file
    #   Then check if it is in the environment variables
    #   If not found, return False
    ########################################################################################
        key = False
        configuration = self.getConfig()
        
        try: key = configuration['application']['openAIKey']
        except: key = False

        try: key = os.environ["OPENAI_API_KEY"]    
        except: key = False

        return key