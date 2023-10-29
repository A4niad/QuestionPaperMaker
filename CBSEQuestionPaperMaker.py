# Import required modules
from tkinter import *
from tkinter import ttk
import random
import json

from database import Database


# Functions
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
    paper_window = Toplevel()
    paper_window.geometry("1000x700")
    paper_window.resizable(False, False)
    paper_window.title("Question paper")
    container = ttk.Frame(paper_window)
    canvas = Canvas(container)
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

    warning = Label(scrollable_frame , text="Be sure to rename your question papers to prevent overwriting!\n",
                 font=font, fg="red", anchor="w", justify=LEFT, wraplength=960)
    warning.pack(side=TOP)

    separator = ttk.Separator(scrollable_frame , orient='horizontal')
    separator.pack(fill='x')

    paper_label = Label(scrollable_frame , text=paper, font=("Arial", 15), fg="black", anchor="w", justify=LEFT, wraplength=960)
    paper_label.pack(side= TOP, padx=10, pady=10)

    container.pack(fill="both", expand=True)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")


def generatePaper():
    global subject, status
    if not subject:
        statusUpdate("Select Subject")
    elif subject not in config["available_subjects"]:
        statusUpdate("Subject questions currently unavailable")
    else:
        quesiton_paper = ""
        layout = config["paper_layouts"][subject]
        questions = {i: db.get_questions(subject, i) for i in layout}

        count = 1
        quesiton_paper += f"QUESTION PAPER\nSUBJECT: {subject.upper()}\nMAX MARKS: 70\n\n"
        for qtype in questions:
            quesiton_paper += config["section_headers"][qtype]

            if len(questions[qtype]) >= layout[qtype]:
                random_questions = random.sample(questions[qtype], layout[qtype])
            else:
                random_questions = questions[qtype]

            n_opt = ["a) ", "b) ", "c) ", "d) ", "e) ", "f) ", "g) ", "h) "]
            for q in random_questions:
                if qtype == "mcq":
                    options = q[2].split("\n")
                    opstr = "\n".join([n_opt[i] + s for i, s in enumerate(options)])
                    quesiton_paper += f"Q{count}) {q[0]}{opstr}\n\n"
                elif qtype == "sa":
                    quesiton_paper += f"Q{count}) {q[0]}\n\n"
                elif qtype == "ma":
                    quesiton_paper += f"Q{count}) {q[0]}\n\n"
                elif qtype == "cb":
                    quesiton_paper += f"Q{count}) {q[0]}\n\n"
                    for i, subq in enumerate(q[4]):
                        if subq[2] == "mcq":
                            options = subq[3].split("\n")
                            opstr = "\n".join([n_opt[i] + s for i, s in enumerate(options)])
                            quesiton_paper += f"Q{count}.{i + 1}) {subq[1]}\n{opstr}\n\n"
                        else:
                            quesiton_paper += f"Q{count}.{i + 1}) {subq[1]}\n\n"
                elif qtype == "la":
                    quesiton_paper += f"Q{count}) {q[0]}\n\n"

                count += 1

            quesiton_paper += "\n"

        with open(f"out/QP({subject}).txt", "w+") as out_file:
            try:
                out_file.write(quesiton_paper)
            except Exception as e:
                print(e)
                print("Question paper file not created! Error occured while parsing question data")

        statusUpdate("Paper Created!")

        displayPaper(quesiton_paper)


def statusUpdate(text):
    statusText.configure(text=f"Status: {text}")


if __name__ == "__main__":
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
    root.geometry("1000x500")
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

    # Literal Text
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
