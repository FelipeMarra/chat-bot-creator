import os.path
import sqlite3
import numpy as np
import sys
#TODO solve path problems
sys.path.append('../what-sentiment-bot/')
from preprocess import preprocess_tweet


class FreqsTable():
    ######################### CONSTRUCTORS ################################

    #table = FreqsTable(tweets,ys)
    @classmethod
    def build_from(cls, tweets, ys):
        # create class
        table = cls.__new__(cls)  # Does not call __init__
        # Don't forget to call any polymorphic base class initializers
        super(FreqsTable, table).__init__()

        # create db
        table.__create_words_freqs()
        conn, cur = table.__connect_bd()

        # np array to list
        yslist = np.squeeze(ys).tolist()

        # builds frequences dict by looping all tweets words
        for y, tweet in zip(yslist, tweets):
            for word in preprocess_tweet(tweet):
                # update freqs count
                freq_type = "pos_freq" if y == 1 else "neg_freq"
                cur.execute("UPDATE words SET " + freq_type + " = " +
                            freq_type + " + 1 WHERE word LIKE ?", (word,))

                # if the word is not into the table yet...
                if(cur.rowcount == 0):
                    pos = 1 if y == 1 else 0
                    neg = 1 if y == 0 else 0
                    cur.execute("""
                        INSERT INTO words VALUES (?, ?, ?, ?)
                    """, (word, pos, neg, 0.0))

        # close db
        table.__disconnect(conn)

        # return class
        return table

    ########################### CONNECTION ##################################
    def __connect_bd(self):
        # create words table
        freqs_path = os.path.abspath("db/freqs_table/db.db")
        # connect to db
        conn = sqlite3.connect(freqs_path)
        # create  cursor
        cur = conn.cursor()
        return conn, cur
    

    def __disconnect(self, conn):
        conn.commit()
        conn.close()

    def connect(self):
        freqs_path = os.path.abspath("what-sentiment-bot/ml/naive_bayes/db/freqs_table/db.db")
        db = sqlite3.connect(freqs_path)
        return db
    
    def close(self, db):
        db.close()
    ####################### Query & Fetch #################################
    def fetch_all_words(self):
        conn, cur = self.__connect_bd()

        cur.execute("SELECT * FROM words")

        row = cur.fetchall()

        self.__disconnect(conn)

        return row

    ########################### UTILS ##################################

    def count_words(self):
        conn, cur = self.__connect_bd()

        cur.execute('SELECT COUNT(*) FROM words')

        n_rows = cur.fetchone()[0]

        self.__disconnect(conn)

        return n_rows

    def sum_column(self, c):
        conn, cur = self.__connect_bd()

        cur.execute('SELECT SUM(' + c + ') FROM words')

        sum_c = cur.fetchone()[0]

        self.__disconnect(conn)

        return sum_c

    def get_column(self, c):
        conn, cur = self.__connect_bd()
        
        column = [column[0] for column in cur.execute('SELECT ' + c + ' FROM words')]

        self.__disconnect(conn)

        return column

    def get_utils(self):
        conn, cur = self.__connect_bd()
        
        logprior = [logprior[0] for logprior in cur.execute('SELECT logprior from utils')]

        self.__disconnect(conn)

        return logprior

    def get_loglikelihood(self, word:str):
        conn, cur = self.__connect_bd()

        cur.execute('SELECT loglikelihood FROM words WHERE word LIKE ?',(word,))

        result = cur.fetchone()
        if result is not None:
            loglikelihood = result[0]
        else:
            loglikelihood = 0

        self.__disconnect(conn)

        return loglikelihood

    ########################### CRUD ##################################

    def __create_words_freqs(self):
        conn, cur = self.__connect_bd()

        # create word freqs table
        cur.execute("""
            CREATE TABLE words (
                word text,
                pos_freq integer,
                neg_freq integer,
                loglikelihood real
            )
        """)

        self.__disconnect(conn)

    def create_utils(self):
        conn, cur = self.__connect_bd()
        
        cur.execute("""
            CREATE TABLE utils (
                
                logprior real
            )
        """)
        
        self.__disconnect(conn)

    def add_word(self, word: str, pos_freq: int, neg_freq: int, loglikelihood: float):
        conn, cur = self.__connect_bd()

        cur.execute("""
            INSERT INTO words VALUES (?, ?, ?)
        """, (word, pos_freq, neg_freq, loglikelihood))

        self.__disconnect(conn)

    def update_loglikelihood(self, loglikelihood: float, word):
        conn, cur  = self.__connect_bd()

        cur.execute("UPDATE words SET loglikelihood = ? WHERE word LIKE ?", (loglikelihood, word,))

        self.__disconnect(conn)
    
    def add_logprior(self, logprior: float):
        conn, cur = self.__connect_bd()
        
        cur.execute("INSERT INTO utils (logprior) values(?)",(logprior,))
        
        self.__disconnect(conn)