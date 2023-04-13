# CBSE Question Paper Maker

A web app to generate sample CBSE Question Papers. Made using Python, Flask, and SQL.

## Setup

Follow the given steps to setup and run the app.

#### Requirements

- Python 3.11.1
- Flask
- SQL libraries

#### Steps

1. Install Python version 3.11 from [Python website](https://python.org/downloads) if not already installed.
2. Add python.exe folder path to system PATH environment variables. (skip this step if **python** command works in command prompt)
3. Clone the repo into a folder and open command prompt in that folder.
4. Create virtual environment using command `python -m venv venv`.
5. Activate the virtual environment using command `./venv/Scripts/activate`
6. Run `pip install -r requirements.txt` to install dependencies.
7. Run `python CBSEQuestionPaperMaker.py` in the command prompt to launch the flask server.
8. Go to [Flask Server](http://127.0.0.1:5000) in your browser to see the web app.

> The server will stop if you close the command prompt, so dont close it.

## Project File Overview

- `requirements.txt` contains the python libraries required for the project.
- `requirements_dev.txt` contains optional tool libraries such as formatter.
- `CBSEQuestionPaperMaker.py` is the main file where the program starts.
- `config.json` contains some required project settings configurations.
- `layout.html` is the base layout of the website it should be extended by other templates.
- `index.html` is the home page of our website.
