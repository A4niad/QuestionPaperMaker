# CBSE Question Paper Maker

A desktop app to generate sample CBSE Question Papers. Made using Python, Tkinter, and SQL.

## Setup

Follow the given steps to setup and run the app.

#### Requirements

- Python 3.11
- Tkinter
- SQL libraries

#### Steps

1. Install Python version 3.11 from [Python website](https://python.org/downloads) if not already installed.
2. Add python.exe folder path to system PATH environment variables. (skip this step if **python** command works in command prompt)
3. Clone the repo into a folder and open command prompt in that folder.
4. Create virtual environment using command `python -m venv venv`.
5. Activate the virtual environment using command `./venv/Scripts/activate`
6. Run `pip install -r requirements.txt` to install dependencies.
7. Create an 'out' directory for output questions txt files `mkdir out`.
8. Open `config.json` and edit the user and password fields with your MySQL details
9. Run `python CBSEQuestionPaperMaker.py` in the command prompt to launch the app.

## Project File Overview

- `requirements.txt` contains the python libraries required for the project.
- `requirements_dev.txt` contains optional tool libraries such as formatter.
- `CBSEQuestionPaperMaker.py` is the main file where the program starts.
- `database.py` contains functionality to fetch questions from database.
- `data.py` contains data to store in the database.
- `config.json` contains some required project settings configurations.
