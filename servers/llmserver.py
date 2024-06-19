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
#       Name: llmserver.py
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
from flask import Flask , request
import genos.configuration as configuration
import ollama
app = Flask(__name__)

def llmInvoke(model='llama3', content='Hello!'):
    print("llmInvoke: ", model, content)
    message = {'role': 'user','content': content,}
    response = ollama.chat(model=model, messages=[message])
    print("/llmInvoke response: ", response['message']['content'])
    return (response['message']['content'])

@app.route("/hello" , methods=['GET'])
def hello():
    return llmInvoke("Hello!")

def invokeOpenAI(model='GPT3', question='Hello!'):
    print("invokeOpenAI     : ", model, question)
    from openai import OpenAI
    response = "Error in fetching response"
    if model == "GPT4": model = "gpt-4o"
    elif model == "GPT3": model = "gpt-3.5 Turbo"
    else: model = "gpt-3.5 Turbo"
    print("invokeOpenAI     : ", model, question)
    
    try:  
        client = OpenAI(api_key=OpenAIKey)

        completion = client.chat.completions.create(
            model=model,
            messages=[
                    {"role": "user", "content": question}
                ]
        )
        response = completion.choices[0].message.content

    except Exception as e:
        print("Error in invokeOpenAI: ", e)
        return("Error in llmserver invokeOpenAI: ", e)

    print("invokeOpenAI returning response 1 : ", response)

    return response

@app.route("/genoschat" , methods=['GET','POST'])
def question():
    response = ""
    
    try:
        model = request.args.get('model', default = 'llama3', type = str)
        question = request.args.get('question', default = 'Hello1', type = str)
        print("llmserver - Model in /genoschat: ", model)
        print("llmserver - Question in /genoschat: ", question)
        if model == "GPT4": response = invokeOpenAI(model,question)
        elif model == "GPT3": response = invokeOpenAI(model,question)
        else: response = llmInvoke(model,question)
    except Exception as e:
        print("llmserver - Error in /genoschat: ", e)

    if response == "": response = "Error in fetching LLM response"
    return response

@app.route("/genoschatjson" , methods=['GET'])
def jsondata():
    json = request.args.get('json')
    return json

@app.route("/genoschat/list" , methods=['GET'])
def llmList():
    modelString = ""
    
    try:
    #############################################################
    # Get list of supported models from ollama
    # If exception, assume that ollama server is not running /
    #       or not available
    #
    # As many local envioronments cannot support the largest
    #       models, only return models that are less than
    #       maxLLMSize
    #############################################################
        models = ollama.list()
        returnString = models['models']
        for entry in returnString:
            if entry['size'] < maxLLMSize:
                modelString += entry['name'] + ","
    except Exception as e:
        print("Error in llmList: ", e)

    #############################################################
    # If OpenAIKey was set during startup, assume that
    #       key is valid, and populate list with some default
    #       models
    #############################################################
    config = configuration.Configuration()
    if OpenAIKey != False:
            modelString += config.getGpt4Default()  + ","
            modelString += config.getGpt3Default()   + ","

    #print("/genoschat/list: " , modelString)
    return modelString

# main driver function
if __name__ == '__main__':
    # run() method of Flask class runs the application 
    # on the local development server.
    global maxLLMSize
    global OpenAIKey
    import genos.configuration as configuration
    config = configuration.Configuration()
    maxLLMSize = config.getMaxLLMSize()
    OpenAIKey = config.getOpenAIKey()
    app.run()




    