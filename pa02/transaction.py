'''
transaction.py is a Object Relational Mapping to the transactions table

The ORM will work map SQL rows with the schema
    (rowid, item_num, amount, category, date, description)
to Python Dictionaries.

This app will store the data in a SQLite database ~/tracker.db

'''
import sqlite3

def to_trans_dict(trans_tuple):
    '''to_trans_dict is a transaction tuple
    (rowid, item_num, amount, category, date, description)'''
    transaction = {
        'rowid': trans_tuple[0],
        'item_num': trans_tuple[1],
        'amount': trans_tuple[2],
        'category': trans_tuple[3],
        'date': trans_tuple[4],
        'description': trans_tuple[5]
    }
    return transaction

def to_trans_dict_list(trans_tuples):
    ''' convert a list of transaction tuples into a list of dictionaries'''
    return [to_trans_dict(trans) for trans in trans_tuples]

class Transaction():
    ''' Transaction represents a table of transaction'''
    def __init__(self, dbfile):
        con = sqlite3.connect(dbfile)
        cur = con.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS transactions
                    (item_num real, amount real, category text, date text, description text)''')
        con.commit()
        con.close()
        self.dbfile = dbfile

    def select_all(self):
        ''' return all of the transactions as a list of dicts.'''
        con = sqlite3.connect(self.dbfile)
        cur = con.cursor()
        cur.execute("SELECT rowid,* from transactions")
        tuples = cur.fetchall()
        con.commit()
        con.close()
        return to_trans_dict_list(tuples)

    def add(self, transaction):
        ''' add a transaction to the transactions table.'''
        con = sqlite3.connect(self.dbfile)
        cur = con.cursor()
        cur.execute("INSERT INTO transactions VALUES(?,?,?,?,?)",
                    (transaction['item_num'], transaction['amount'], transaction['category'],
                        transaction['date'], transaction['description']))
        con.commit()
        cur.execute('SELECT last_insert_rowid()')
        last_rowid = cur.fetchone()
        con.commit()
        con.close()
        return last_rowid[0]

    def delete(self, rowid):
        ''' delete a transaction with a specified rowid '''
        con = sqlite3.connect(self.dbfile)
        cur = con.cursor()
        cur.execute("DELETE FROM transactions WHERE rowid=(?)", (rowid,))
        con.commit()
        con.close()

    def summarize_by_date(self, date):
        ''' return a list of transactions grouped by date '''
        con = sqlite3.connect(self.dbfile)
        cur = con.cursor()
        #date format is MM-DD-YYYY
        cur.execute("SELECT date FROM transactions WHERE date LIKE ?", ('%'+date+'%',))
        tuples = cur.fetchall()
        con.commit()
        con.close()
        return to_trans_dict_list(tuples)

    def summarize_by_month(self, month):
        '''return a list of transactions grouped by month from date'''
        con = sqlite3.connect(self.dbfile)
        cur = con.cursor()
        cur.execute("SELECT date FROM transactions WHERE date LIKE ?", (month+'-%',))
        tuples = cur.fetchall()
        con.commit()
        con.close()
        return to_trans_dict_list(tuples)

    def summarize_by_year(self, year):
        '''return a list of transactions grouped by year from date'''
        con = sqlite3.connect(self.dbfile)
        cur = con.cursor()
        cur.execute("SELECT date FROM transactions WHERE date LIKE ?", ('%-'+year,))
        tuples = cur.fetchall()
        con.commit()
        con.close()
        return to_trans_dict_list(tuples)

    def summarize_by_category(self):
        '''return a list of transactions grouped by category'''
        con = sqlite3.connect(self.dbfile)
        cur = con.cursor()
        cur.execute("SELECT category, sum(amount) FROM transactions GROUP BY category")
        tuples = cur.fetchall()
        con.commit()
        con.close()
        return to_trans_dict(tuples)
