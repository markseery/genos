# genos
A system for doing various datascience and gen AI things

Exploring the use of LLMs.
Capable of collecting, storing, and visualizing data
Separation of concerns into different servers/processes for distribution, flexibility, scale, etc.

Pre-req
-------

To use ChatGPT/OpenAI put API key in enviroment variable OPENAI_API_KEY
Requirements doc coming, but some of the dependencies are:

ollama
openai
taipy
flask
yaml

future requirements will likely include:

langchain
clickhouse database
neo4j network graph database
brew install ffmpeg (optional)
pip3 install elevenlabs (optional)

Note this was developed on a M2 Apple Laptop, so some of the install assumptions may be related to that.


Start
-----

python3 ./llmserver.py
python3 ./appgui.py

Use
---

![image](https://github.com/markseery/genos/assets/76133757/34c07120-888c-4b9b-9b9c-cf350d9b13fa)


Select the LLM you want to use from the dropdown widget.
Ask a question


