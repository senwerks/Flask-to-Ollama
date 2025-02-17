# SageBridge, a basic Flask-to-Ollama interface

A flask-based web-app for running locally and talking to local LLMs you have instsalled in Ollama. A more basic version of other web-interfaces designed for non-technical users (originally created for my kids).

Automatically gets the list of models installed in Ollama and lets you send prompts to them.

Project dependencies setup for `uv`, so run with `uv run app.py`, or if you prefer `pip` then do `pip install flask requests` then `flask run`

![Screenshot of Flask-to-Ollama](https://raw.githubusercontent.com/senwerks/Flask-to-Ollama/refs/heads/main/flask-to-ollama.png)

## TODO

- Fix the formatting of the responses, eg math responses are still broken due to markdown formatting clashing with mathjax formatting.
- Add a better "waiting for response" message, maybe with a timer/animation to show it's still waiting.