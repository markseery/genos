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
#       Name: appui.py
#       Author: Mark Seery
#
#   Notes
#   -----
#
#   Playing with the Taipy GUI
#
#   General principle will to keep the UI separate from other functions
#       and to keep the functions in other processes via network calls,
#       for separation of concerns, the ability to change the UI easily,
#       and to allow for multiple UIs to be used with the same functions,
#       and of course for distibution of capabilities, and potentially
#       load balancing.
#
#   Early days of getting comfortable with the Taipy GUI
#
##########################################################################
from taipy.gui import Gui, notify, Html, State
import genos.commchannel as commchannel

def on_input_message(state):
##########################################################################
#   At the moment, all entered input goes to a selected LLM
#   This will change dramatically as specifially functionality is added
##########################################################################
    try:
        notify(state, "info", "Sending message...")
        print(state.input_message)

        cc = commchannel.Commchannel()
        response = cc.sendDataArgs("http://127.0.0.1:5000/genoschat", ("model=" + state.selected_llm + "&question=" + state.input_message))      

        oldConversation = state.conversation['Conversation']
        newConversation = []
        for y in oldConversation:
            newConversation.append(y)
        newConversation.append(("( Your message ) : " + state.input_message))
        newConversation.append(("( " + state.selected_llm + " ) : " + response))
        
        state.conversation = {'Conversation' : newConversation}
        state.input_message = ""
        conversation = state.conversation
        notify(state, "success", "Response received!")
    except Exception as e:
        print("Error in on_input_message: ", e)

def style_conv(state: State, idx: int, row: int) -> str:
    """
    Apply a style to the conversation table depending on the message's author.

    Args:
        - state: The current state of the app.
        - idx: The index of the message in the table.
        - row: The row of the message in the table.

    Returns:
        The style to apply to the message.
    """
    if idx is None: return None
    elif idx % 2 == 0: return "user_message"
    else: return "gpt_message"

def on_llm_selected(state):
    selected_llm = state.selected_llm
    print(state.selected_llm)

def createLLMList():
    cc = commchannel.Commchannel()
    response = cc.sendDataArgs("http://127.0.0.1:5000/genoschat/list", "")
    llms = response.split(',')
    return llms

def on_init(state: State) -> None:
    """
    Initialize the app.

    Args:
        - state: The current state of the app.
    """
    
    state.input_message = ""
    state.context = "The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.\n\nHuman: Hello, who are you?\nAI: I am an AI created by OpenAI. How can I help you today? "
    state.conversation = { "Conversation": [""] }
    state.past_conversations = []
    state.selected_row = [1]
    #state.selected_conv = None
    
if __name__ == '__main__':
    global llms, text, selected_llm, input_message, conversation, past_conversations, selected_conv, selected_row
    
    text = "Original text"

    selected_llm = "llama3:latest"
    input_message = ""
    conversation = { "Conversation": [""] }
    past_conversations = []
    selected_conv = None
    selected_row = [1]

    llms = createLLMList()
    
    page2 = """
# GenOs **UI**{: .color-primary} # {: .logo-text}

<|{conversation}|table|style=style_conv|show_all|selected={selected_row}|rebuild |>

<|{input_message}|input|label=Write your message here...|on_action=on_input_message|class_name=fullwidth|change_delay=-1|>

## Default LLM model
<|{selected_llm}|selector|lov={llms}|on_change=on_llm_selected|dropdown|>
"""
    
    page = """{title}\n{conv}\n{input}\n{llmSelected}""".format(
title = "# GenOs **UI**{: .color-primary} # {: .logo-text}",
conv = "<|{conversation}|table|style=style_conv|show_all|selected={selected_row}|rebuild|>",
input = "<|{input_message}|input|label=Write your message here...|on_action=on_input_message|class_name=fullwidth|change_delay=-1||>",
llmSelected = "<|{selected_llm}|selector|lov={llms}|on_change=on_llm_selected|dropdown||>",
)

    Gui(page2).run(port=5600)

#data = {"x_col":[0,1,2], "y_col_1":[4,1,2], "y_col_2":[3,1,2]}
#Gui("<|{data}|chart|x=x_col|y[1]=y_col_1|y[2]=y_col_2|type[1]=bar|>").run(port=5600)