''' 
!!WARNING!! PLEASE SET PASSWORD TO YOUR SQL PASSWORD IN CONFIG.JSON !!WARNING!! 
!!WARNING!! CODE WILL NOT WORK OTHERWISE                            !!WARNING!!
'''

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ IMPORTS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

# Import required modules

from tkinter import *            # utilized for generating UI
from tkinter import ttk  
import random                    # utilized for random selection of questions
import json                      # utilized for more efficent dictionary unpacking
import mysql.connector as sqlcon # utilized for connection with a MySQL database containing questions

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ CLASSES ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

class Database:
    """
    A class to interact with the database, to fetch and store data.
    """

    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, host, user, password, database=None):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.tables = {}

        # Connect to database
        self.db = sqlcon.connect(
            host=self.host,
            user=self.user,
            passwd=self.password,
            database=self.database
        )

        # Check connection status
        if not self.db.is_connected():
            print("Error connecting to MySQL database!")
            return

        # create cursor object
        self.cursor = self.db.cursor()

        self.load_tables(self.database)

    def load_tables(self, database):
        '''
        Function that yields all headers for the required fields
        '''
        self.database = database

        if self.database is not None:
            self.cursor.execute(f"use {self.database}")

            # get tables for headers
            self.cursor.execute("show tables")
            tables = self.cursor.fetchall()
            table_names = [i[0] for i in tables]
            for i in table_names:
                self.cursor.execute(f"desc {i}")
                headers = [i[0] for i in self.cursor.fetchall()]
                self.tables[i] = {
                    "fields": headers
                }

    def is_connected(self):
        '''
        Function that returns the connectivity status with the database
        '''
        return self.db.is_connected()

    def get_questions(self, subject, qtype=None):
        '''
        Function that returns a list of questions for a given subject and a specific
        question type
        '''
        result = []
        if subject not in self.tables:
            return result

        self.cursor.execute(f"""
            select * from {subject} where type = '{qtype}'
        """)

        data = self.cursor.fetchall()
        for i in data:
            i = list(i)
            if i[3] != 0: # Handling case based questions which require extra processing
                self.cursor.execute(f"""
                    select * from {subject}_case_based where id = {i[3]}
                """)
                i.append(self.cursor.fetchall())
            result.append(i)

        return result

    def close(self):
        """
        Closes the database connection.
        """

        self.db.close()


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ FUNCTION ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

'''
These subjectSelect() functions handle the UI of selecting a subject and making
the relevant button green. It also sets the subject to the required one
'''
def physSelect():
    global subject
    math.configure(fg="red")
    chem.configure(fg="red")
    phys.configure(fg="green")
    subject = "physics"


def chemSelect():
    global subject
    math.configure(fg="red")
    chem.configure(fg="green")
    phys.configure(fg="red")
    subject = "chemistry"


def mathSelect():
    global subject
    math.configure(fg="green")
    chem.configure(fg="red")
    phys.configure(fg="red")
    subject = "maths"


def displayPaper(paper):
    '''
    Function that displays the question paper in a new window
    '''

    # Initializing paper window
    paper_window = Toplevel()
    paper_window.geometry("1000x700")
    paper_window.resizable(False, False)
    paper_window.title("Question Paper")
    container = ttk.Frame(paper_window)
    canvas = Canvas(container)
    
    # Adding a scroll bar
    scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Adding warning label on top

    warning = Label(scrollable_frame , text="Be sure to rename your question papers to prevent overwriting!\n",
                 font=font, fg="red", anchor="w", justify=LEFT, wraplength=960)
    warning.pack(side=TOP)

    separator = ttk.Separator(scrollable_frame , orient='horizontal')
    separator.pack(fill='x')

    # Adding the question paper
    paper_label = Label(scrollable_frame , text=paper, font=("Arial", 15), fg="black", anchor="w", justify=LEFT, wraplength=960)
    paper_label.pack(side= TOP, padx=10, pady=10)

    container.pack(fill="both", expand=True)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")


def generatePaper():
    '''
    Function that generates the question paper
    '''
    global subject, status

    if not subject:
        statusUpdate("Select Subject")

    elif subject not in config["available_subjects"]: # debugging check statement (delete later)
        statusUpdate("Subject Questions Currently Unavailable")

    else:
        question_paper = ""
        layout = config["paper_layouts"][subject]
        questions = {i: db.get_questions(subject, i) for i in layout}

        count = 1
        question_paper += f"QUESTION PAPER\nSUBJECT: {subject.upper()}\nMAX MARKS: 70\n\n"
        for qtype in questions:
            question_paper += config["section_headers"][qtype]

            if len(questions[qtype]) >= layout[qtype]:
                random_questions = random.sample(questions[qtype], layout[qtype])
            else:
                random_questions = questions[qtype]

            n_opt = ["a) ", "b) ", "c) ", "d) ", "e) ", "f) ", "g) ", "h) "]

            for q in random_questions:
                if qtype == "mcq":
                    # Handles (m)ultiple-(c)hoice (q)uestions
                    options = q[2].split("\n")
                    opstr = "\n".join([n_opt[i] + s for i, s in enumerate(options)])
                    question_paper += f"Q{count}) {q[0]}{opstr}\n\n"

                elif qtype in ["sa", "ma", "la"]:
                    # Handles (s)hort (a)nswers, (m)edium (a)nswers & (l)ong (a)nswers
                    question_paper += f"Q{count}) {q[0]}\n\n"

                elif qtype == "cb":
                    # Handles (c)ase-study-(b)ased questions
                    question_paper += f"Q{count}) {q[0]}\n\n"
                    for i, subq in enumerate(q[4]):
                        if subq[2] == "mcq":
                            options = subq[3].split("\n")
                            opstr = "\n".join([n_opt[i] + s for i, s in enumerate(options)])
                            question_paper += f"Q{count}.{i + 1}) {subq[1]}\n{opstr}\n\n"
                        else:
                            question_paper += f"Q{count}.{i + 1}) {subq[1]}\n\n"

                count += 1

            question_paper += "\n"

        with open(f"out/QP({subject}).txt", "w+") as out_file:
            try:
                out_file.write(question_paper)
            except Exception as e:
                print(e)
                print("Question paper file not created! Error occured while parsing question data")
                statusUpdate("Parsing Error! Try Again")

        statusUpdate("Paper Created!")

        displayPaper(question_paper)


def statusUpdate(text):
    '''
    Function that updates the status text
    '''
    statusText.configure(text=f"Status: {text}")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ PROGRAM ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

if __name__ == "__main__":
    '''
    Main Program
    '''
    with open("config.json", "r") as f:
        config = json.load(f)

    db = Database("localhost", config["user"],
                config["password"], config["database"])

    # Important Variables and Parameters
    h = 2
    w = 20
    font = ("Arial", 20)
    beige = "#d1c0a9"
    subject = ""
    status = "Awaiting Input"

    # Setting Up Main Screen
    root = Tk()

    # Main Screen Initialization
    root.title("Question Paper Generator!")
    root.geometry("800x300")
    root.resizable(False, False)
    root.rowconfigure(0, weight=1)
    root.rowconfigure(1, weight=1)
    root.rowconfigure(2, weight=1)
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=5)

    root.configure(bg=beige)

    # Buttons
    phys = Button(root, text="PHYSICS", fg="red", height=h, width=w, font=font, command=physSelect)
    chem = Button(root, text="CHEMISTRY", fg="red", height=h, width=w, font=font, command=chemSelect)
    math = Button(root, text="MATHS", fg="red", height=h, width=w, font=font, command=mathSelect)
    generate = Button(root, text="GENERATE PAPER", fg="red", height=h, width=w, font=font, command=generatePaper)

    # Text
    title = Label(text="Question Paper Generator",
                    font=("Arial", 27), fg="blue", bg=beige)
    statusText = Label(text=f"Status: {status}", font=("Arial", 27), bg=beige, wraplength=500)

    phys.grid(column=0, row=0, padx=(7, 7), pady=(7, 7))
    chem.grid(column=0, row=1, padx=(7, 7), pady=(7, 7))
    math.grid(column=0, row=2, padx=(7, 7), pady=(7, 7))

    title.grid(column=1, row=0, padx=(7, 7), pady=(7, 7))
    generate.grid(column=1, row=1, padx=(7, 7), pady=(7, 7))
    statusText.grid(column=1, row=2, padx=(7, 7), pady=(7, 7))

    root.mainloop()

    db.close()
