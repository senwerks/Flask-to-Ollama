# SageBridge, a minimal flask-based web interface for Ollama.

A very (very) minimal flask-based web-app for running locally and talking to LLMs you have installed in Ollama. A more basic version of other web-interfaces designed for non-technical users (originally created for my kids).

Automatically gets the list of models installed in Ollama and lets you send prompts to them.

Project dependencies setup for `uv`, so run with `uv run app.py`, or if you prefer `pip` then do `pip install flask requests` then `flask run`

![Screenshot of SageBridge](https://raw.githubusercontent.com/senwerks/Flask-to-Ollama/refs/heads/main/sagebridge-minimal-ollama-web-interface.png)

## TODO

- Fix the formatting of responses with math in them, eg math responses are still broken due to markdown formatting clashing with mathjax formatting. The issue is that the streaming-mode causes weirdness with newlines, breaking the mathjax wrappers so mathjax can't convert it into proper HTML.
- Do some better LLM-specific formatting. If the model replies with <think> tags (and there's actually content between the tags) then format the <think> part differently to the final response. Make it modular so we can add other formatting for other special parts of responses. It currently does replace <think> tags with <blockquote> but in a very basic way.