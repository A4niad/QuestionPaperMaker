import json

import mysql.connector as sqlcon

from data import SUBJECT_DATA


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
        return self.db.is_connected()

    def get_questions(self, subject, qtype=None):
        result = []
        if subject not in self.tables:
            return result

        self.cursor.execute(f"""
            select * from {subject} where type = '{qtype}'
        """)

        data = self.cursor.fetchall()
        for i in data:
            i = list(i)
            if i[3] != 0:
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


if __name__ == "__main__":
    with open("config.json", "r") as f:
        config = json.load(f)

    db = Database("localhost", config["user"], config["password"])

    if not db.is_connected():
        raise Exception("Database connection error")

    db.cursor.execute("create database if not exists cbse_questions")
    db.load_tables("cbse_questions")

    # create subject data tables if it doesn't exist
    if len(db.tables) == 0:
        for subject in SUBJECT_DATA:
            db.cursor.execute(f"""
                create table if not exists {subject}(
                    question text not null,
                    type varchar(3) not null,
                    mcq_options text,
                    cb_question_id integer
                )
            """)
            db.cursor.execute(f"""
                create table if not exists {subject}_case_based(
                    id integer not null,
                    question text not null,
                    type varchar(3) not null,
                    mcq_options text
                )
            """)

            for qtype in SUBJECT_DATA[subject]:
                qid = 1 if qtype == "cb" else 0
                for question in SUBJECT_DATA[subject][qtype]:
                    db.cursor.execute(f"""
                            insert into {subject} (question, type, mcq_options, cb_question_id)
                            values ('{question[0]}', '{qtype}',
                                    '{question[1]}', {qid})
                        """)

                    if qtype == "cb":
                        for i in question[2]:
                            db.cursor.execute(f"""
                                insert into {subject}_case_based (id, question, type, mcq_options)
                                values ({qid}, '{i[0]}', '{i[1]}', '{i[2]}')
                            """)
                        qid += 1

        db.db.commit()

    db.close()
