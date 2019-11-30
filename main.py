#!/usr/bin/python3

from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from tkinter import font
import pg8000
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import math

# implements a simple login window
class LoginWindow:
    def __init__(self, window):
        self.window = window

        self.window.title('Login')
        self.window.grid()

        # styling
        self.font = font.Font(family = 'Arial', size = 12)
        Style().configure('TButton', font = self.font)
        Style().configure('TLabel', font = self.font)

	# setup widgets
        self.user_label = Label(window, text='Username: ')
        self.user_label.grid(column = 0, row = 0)
        self.user_input = Entry(window, width = 20, font = self.font)
        self.user_input.grid(column = 1, row = 0)

        self.pw_label = Label(window, text='Password: ')
        self.pw_label.grid(column = 0, row = 1)
        self.pw_input = Entry(window, width = 20, show='*', font = self.font)
        self.pw_input.grid(column = 1, row = 1)

        self.button_frame = Frame(window)
        self.button_frame.grid(column = 0, columnspan = 2, row = 2)

        self.ok_button = Button(self.button_frame, text='OK', command=self.ok_action)
        self.ok_button.grid(column = 0, row = 0)

        self.cancel_button = Button(self.button_frame, text='Cancel', command=quit)
        self.cancel_button.grid(column = 1, row=0)

        self.window.bind('<Return>', self.enter_action)
        self.user_input.focus_set()

    def enter_action(self, event):
        self.ok_action()

    def ok_action(self):
        try:        
            credentials = {'user'     : self.user_input.get(),
                           'password' : self.pw_input.get(),
                           'database' : 'csci403',
                           'host'     : 'bartik.mines.edu' }
            self.db = pg8000.connect(**credentials)
            self.window.destroy()
        except pg8000.Error as e:
            messagebox.showerror('Login Failed', e.args[0]["M"])
# end LoginWindow

##############################################
# EXAMPLES
#    def search_by_album(self, search_string):
#        query = """SELECT ar.name, al.title, al.year, al.id 
#                   FROM artist AS ar, album AS al
#                   WHERE lower(al.title) LIKE lower(%s)
#                   AND ar.id = al.artist_id
#                   ORDER BY ar.name, al.year, al.title"""
#
#        search_string = '%' + search_string + '%'
#        try:
#            self.cursor.execute(query, (search_string, ))
#
#            resultset = self.cursor.fetchall()
#            return resultset
#
#        except pg8000.Error as e:
#            messagebox.showerror('Database error', e.args[0]["M"])
#            return None
#
#    def insert_artist(self, artist_name):
#        query = """INSERT INTO artist (name) VALUES (%s)"""
#        try:
#            self.cursor.execute(query, (artist_name,))
#        except pg8000.Error as e:
#            messagebox.showerror('Database error', e.args[0]["M"])
#            return
#
#    def get_artists(self): 
#        query = """SELECT ar.name 
#                   FROM artist AS ar ORDER BY ar.name"""
#        try:
#            self.cursor.execute(query)
#
#            resultset = [str(i[0]) for i in self.cursor.fetchall()]
#            return resultset
#
#        except pg8000.Error as e:
#            messagebox.showerror('Database error', e.args[0]["M"])
#            return None
#
#    def insert_album(self, artist_name, album_name, year):
#        query = """INSERT INTO album (artist_id, title, year) 
#                   VALUES ((SELECT id FROM artist WHERE name = %s), %s, %s)"""
#        try:
#            self.cursor.execute(query, (artist_name, album_name, year))
#        except pg8000.Error as e:
#            messagebox.showerror('Database error', e.args[0]["M"])
#
#    def update_album(self, album_id, album_name, year):
#        query = """UPDATE album 
#                   SET title = %s, year = %s 
#                   WHERE id = %s"""
#        try:
#            self.cursor.execute(query, (album_name, year, album_id))
#        except pg8000.Error as e:
#            messagebox.showerror('Database error', e.args[0]["M"])
#
#    def delete_album(self, album_id):
#        query = """DELETE FROM album 
#                   WHERE id = %s"""
#        try:
#            self.cursor.execute(query, (album_id,))
#        except pg8000.Error as e:
#            messagebox.showerror('Database error', e.args[0]["M"])
# end of Application
######################################################################

############################
# application startup code #
############################

# Use CPW's login screen to login
lw = Tk()
lwapp = LoginWindow(lw)
lw.mainloop()

# Create global variables for our database and cursor
db = lwapp.db
cursor = db.cursor()

##################
# Visualizations #
##################

# Top 5 beers with more than 50 reviewers
num_beers = 10
query = """SELECT beer.name, AVG(review.overall) FROM beer, review WHERE beer.id = review.beer_id GROUP BY beer.name HAVING COUNT(*) > 50 ORDER BY AVG(overall) DESC LIMIT %s;"""

try:
    cursor.execute(query, (num_beers,))
    results = cursor.fetchall()
    names = [str(i[0]) for i in reversed(results)]
    y_pos = np.arange(len(names))
    rating = [float(i[1]) for i in reversed(results)]
    # Display graph
    plt.barh(names, rating, align='center', alpha=0.9)
    plt.yticks(y_pos, names)
    plt.xlabel('Average Overall Rating')
    plt.title(f'Top {num_beers} Beers')
    plt.show()

except pg8000.Error as e:
    messagebox.showerror('Database error', e.args[0]["M"])

# Top beer


##############
# Statistics #
##############

#################
# Whatever else #
#################
