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
    plt.title(f'Best Overall {num_beers} Beers')
    plt.show()

except pg8000.Error as e:
    messagebox.showerror('Database error', e.args[0]["M"])

# Top 5 beers with more than 50 reviewers
num_beers = 10
query = """SELECT beer.name, COUNT(*) FROM beer, review WHERE beer.id = review.beer_id GROUP BY beer.name ORDER BY COUNT(*) DESC LIMIT %s;"""

try:
    cursor.execute(query, (num_beers,))
    results = cursor.fetchall()
    names = [str(i[0]) for i in reversed(results)]
    y_pos = np.arange(len(names))
    rating = [float(i[1]) for i in reversed(results)]
    # Display graph
    plt.barh(names, rating, align='center', alpha=0.9)
    plt.yticks(y_pos, names)
    plt.xlabel('Number of Reviews')
    plt.title(f'Most Reviewed {num_beers} Beers')
    plt.show()

except pg8000.Error as e:
    messagebox.showerror('Database error', e.args[0]["M"])

# Top 5 beers by taste with more than 50 reviewers
num_beers = 10
query = """SELECT beer.name, AVG(review.taste) FROM beer, review WHERE beer.id = review.beer_id GROUP BY beer.name HAVING COUNT(*) > 50 ORDER BY AVG(taste) DESC LIMIT %s;"""

try:
    cursor.execute(query, (num_beers,))
    results = cursor.fetchall()
    names = [str(i[0]) for i in reversed(results)]
    y_pos = np.arange(len(names))
    rating = [float(i[1]) for i in reversed(results)]
    # Display graph
    plt.barh(names, rating, align='center', alpha=0.9)
    plt.yticks(y_pos, names)
    plt.xlabel('Average Tasting Rating')
    plt.title(f'Best Tasting Beers')
    plt.show()

except pg8000.Error as e:
    messagebox.showerror('Database error', e.args[0]["M"])

# Top 5 beers by aroma with more than 50 reviewers
num_beers = 10
query = """SELECT beer.name, AVG(review.aroma) FROM beer, review WHERE beer.id = review.beer_id GROUP BY beer.name HAVING COUNT(*) > 50 ORDER BY AVG(aroma) DESC LIMIT %s;"""

try:
    cursor.execute(query, (num_beers,))
    results = cursor.fetchall()
    names = [str(i[0]) for i in reversed(results)]
    y_pos = np.arange(len(names))
    rating = [float(i[1]) for i in reversed(results)]
    # Display graph
    plt.barh(names, rating, align='center', alpha=0.9)
    plt.yticks(y_pos, names)
    plt.xlabel('Average Aroma Rating')
    plt.title(f'Best Smelling Beers')
    plt.show()

except pg8000.Error as e:
    messagebox.showerror('Database error', e.args[0]["M"])

# Top 5 beers by palate with more than 50 reviewers
num_beers = 10
query = """SELECT beer.name, AVG(review.palate) FROM beer, review WHERE beer.id = review.beer_id GROUP BY beer.name HAVING COUNT(*) > 50 ORDER BY AVG(palate) DESC LIMIT %s;"""
try:
    cursor.execute(query, (num_beers,))
    results = cursor.fetchall()
    names = [str(i[0]) for i in reversed(results)]
    y_pos = np.arange(len(names))
    rating = [float(i[1]) for i in reversed(results)]
    # Display graph
    plt.barh(names, rating, align='center', alpha=0.9)
    plt.yticks(y_pos, names)
    plt.xlabel('Average Palate Rating')
    plt.title(f'Best Beers by Tongue Feel')
    plt.show()

except pg8000.Error as e:
    messagebox.showerror('Database error', e.args[0]["M"])

# Top 5 beers by appearance with more than 50 reviewers
num_beers = 10
query = """SELECT beer.name, AVG(review.appearance) FROM beer, review WHERE beer.id = review.beer_id GROUP BY beer.name HAVING COUNT(*) > 50 ORDER BY AVG(appearance) DESC LIMIT %s;"""

try:
    cursor.execute(query, (num_beers,))
    results = cursor.fetchall()
    names = [str(i[0]) for i in reversed(results)]
    y_pos = np.arange(len(names))
    rating = [float(i[1]) for i in reversed(results)]
    # Display graph
    plt.barh(names, rating, align='center', alpha=0.9)
    plt.yticks(y_pos, names)
    plt.xlabel('Average Appearance Rating')
    plt.title(f'Best Looking Beers')
    plt.show()

except pg8000.Error as e:
    messagebox.showerror('Database error', e.args[0]["M"])

# Top beer styles
num_styles = 10
query = """SELECT beer.style, AVG(review.overall) FROM beer, review WHERE beer.id = review.beer_id GROUP BY beer.style HAVING COUNT(*) > 50 ORDER BY AVG(overall) DESC LIMIT %s;"""
top_beer_styles = set()

try:
    cursor.execute(query, (num_styles,))
    results = cursor.fetchall()
    names = [str(i[0]) for i in reversed(results)]
    top_beer_styles.update(names)
    y_pos = np.arange(len(names))
    rating = [float(i[1]) for i in reversed(results)]
    # Display graph
    plt.barh(names, rating, align='center', alpha=0.9)
    plt.yticks(y_pos, names)
    plt.xlabel('Average Overall Rating')
    plt.title(f'Top {num_beers} Styles')
    plt.show()

except pg8000.Error as e:
    messagebox.showerror('Database error', e.args[0]["M"])


# Most consumed beer styles
num_styles = 10
query = """SELECT beer.style, COUNT(*) FROM beer, review WHERE beer.id = review.beer_id GROUP BY beer.style ORDER BY COUNT(*) DESC LIMIT %s;"""
top_beer_styles = set()

try:
    cursor.execute(query, (num_styles,))
    results = cursor.fetchall()
    names = [str(i[0]) for i in reversed(results)]
    top_beer_styles.update(names)
    y_pos = np.arange(len(names))
    rating = [float(i[1]) for i in reversed(results)]
    # Display graph
    plt.barh(names, rating, align='center', alpha=0.9)
    plt.yticks(y_pos, names)
    plt.xlabel('Number of Reviews')
    plt.title(f'Most Reviewed Styles')
    plt.show()

except pg8000.Error as e:
    messagebox.showerror('Database error', e.args[0]["M"])


# Top beer manufactures
num_breweries = 10
query = """SELECT brewery.name, AVG(review.overall) FROM beer, review, brewery WHERE beer.id = review.beer_id AND beer.brewery_id = brewery.id AND brewery.id IN (SELECT brewery_id FROM beer GROUP BY brewery_id HAVING COUNT(*) > 10) AND beer.id IN (SELECT beer_id FROM review GROUP BY beer_id HAVING COUNT(*) > 20) GROUP BY brewery.name ORDER BY AVG(overall) DESC LIMIT %s;"""
try:
    cursor.execute(query, (num_breweries,))
    results = cursor.fetchall()
    names = [str(i[0]) for i in reversed(results)]
    y_pos = np.arange(len(names))
    rating = [float(i[1]) for i in reversed(results)]
    # Display graph
    plt.barh(names, rating, align='center', alpha=0.9)
    plt.yticks(y_pos, names)
    plt.xlabel('Average Overall Rating')
    plt.title(f'Top {num_breweries} Breweries')
    plt.show()

except pg8000.Error as e:
    messagebox.showerror('Database error', e.args[0]["M"])


# Most rated beer manufactures
num_breweries = 10
query = """SELECT brewery.name, COUNT(*) FROM review JOIN beer ON review.beer_id = beer.id JOIN brewery ON beer.brewery_id = brewery.id GROUP BY brewery.id ORDER BY COUNT(*) DESC LIMIT %s;"""
try:
    cursor.execute(query, (num_breweries,))
    results = cursor.fetchall()
    names = [str(i[0]) for i in reversed(results)]
    y_pos = np.arange(len(names))
    rating = [float(i[1]) for i in reversed(results)]
    # Display graph
    plt.barh(names, rating, align='center', alpha=0.9)
    plt.yticks(y_pos, names)
    plt.xlabel('Number of Reviews')
    plt.title(f'Most Reviewed Breweries')
    plt.show()

except pg8000.Error as e:
    messagebox.showerror('Database error', e.args[0]["M"])


# Top contributors
num_reviewers = 10
query = """SELECT review.reviewer_name, COUNT(*) FROM review GROUP BY review.reviewer_name ORDER BY COUNT(*) DESC LIMIT %s;"""
try:
    cursor.execute(query, (num_reviewers,))
    results = cursor.fetchall()
    names = [str(i[0]) for i in reversed(results)]
    y_pos = np.arange(len(names))
    rating = [float(i[1]) for i in reversed(results)]
    # Display graph
    plt.barh(names, rating, align='center', alpha=0.9)
    plt.yticks(y_pos, names)
    plt.xlabel('Number of Reviews')
    plt.title(f'The Drunks of the Drunks')
    plt.show()

except pg8000.Error as e:
    messagebox.showerror('Database error', e.args[0]["M"])

# ABV to rating
query = """SELECT beer.abv, AVG(review.overall) FROM beer, review WHERE beer.id = review.beer_id GROUP BY beer.abv HAVING AVG(review.overall) IS NOT NULL AND beer.abv IS NOT NULL;"""

try:
    cursor.execute(query)
    results = cursor.fetchall()
    abv = [float(i[0]) for i in results]
    rating = [float(i[1]) for i in results]
    # Display graph
    plt.plot(abv, rating, "b+")
    plt.ylabel('Average Overall Rating')
    plt.xlabel('Alcohol by Volume')
    plt.title(f"ABV versus Rating")
    plt.show()

except pg8000.Error as e:
    messagebox.showerror('Database error', e.args[0]["M"])

# ABV to rating with style transposed

# ABV to rating
query = """SELECT beer.abv, beer.style, AVG(review.overall) FROM beer, review WHERE beer.id = review.beer_id GROUP BY beer.abv, beer.style HAVING AVG(review.overall) IS NOT NULL AND beer.abv IS NOT NULL;"""

try:
    cursor.execute(query)
    results = cursor.fetchall()
    abv = [float(i[0]) for i in results]
    style = [str(i[1]) for i in results]
    for i, name in enumerate(style):
        if name not in top_beer_styles:
            style[i] = "Other"

    rating = [float(i[2]) for i in results]
    df = pd.DataFrame(dict(x=abv, y=rating, Style=style))

    sns.pairplot(x_vars=["x"], y_vars=["y"], data=df, hue="Style", height=5, markers='+', palette="husl")
    plt.ylabel('Average Overall Rating')
    plt.xlabel('Alcohol by Volume')
    plt.title(f"ABV versus Rating (With Top {num_styles} Styles Annotated)")
    plt.show()

except pg8000.Error as e:
    messagebox.showerror('Database error', e.args[0]["M"])

# number of reviews versus overall rating
query = """SELECT COUNT(*), AVG(review.overall) FROM review GROUP BY review.beer_id HAVING AVG(review.overall) IS NOT NULL;"""

try:
    cursor.execute(query)
    results = cursor.fetchall()
    num_reviews = [float(i[0]) for i in results]
    rating = [float(i[1]) for i in results]
    # Display graph
    plt.plot(rating, num_reviews, "b+")
    plt.xlabel('Average Overall Rating')
    plt.ylabel('Number of Reviews')
    plt.title(f"Number of Reviews versus Overall Rating")
    plt.show()

except pg8000.Error as e:
    messagebox.showerror('Database error', e.args[0]["M"])

# Plot average rating in each review category versus number of reviews
query = """SELECT AVG(review.aroma), AVG(review.palate), AVG(review.taste), AVG(review.appearance), COUNT(*) FROM review GROUP BY review.beer_id HAVING AVG(review.overall) IS NOT NULL;"""

try:
    cursor.execute(query)
    results = cursor.fetchall()
    aroma = [float(i[0]) for i in results]
    palate = [float(i[1]) for i in results]
    taste = [float(i[2]) for i in results]
    appearance = [float(i[3]) for i in results]
    count = [float(i[4]) for i in results]

    df = pd.DataFrame(dict(Aroma=aroma, Palate=palate, Taste=taste, Appearance=appearance, y=count))

    sns.pairplot(x_vars=["Aroma", "Palate", "Taste", "Appearance"], y_vars=["y"], data=df, height=5, markers='+')
    plt.ylabel('Number of Reviews')
    plt.title(f"Number of Reviews Versus Rating in Each Category")
    plt.show()

except pg8000.Error as e:
    messagebox.showerror('Database error', e.args[0]["M"])


# Average Brand Rating versus number of its beers being rated
query = """SELECT AVG(review.overall), COUNT(*) FROM review JOIN beer ON review.beer_id = beer.id GROUP BY beer.brewery_id;"""

try:
    cursor.execute(query)
    results = cursor.fetchall()
    rating = [float(i[0]) for i in results]
    num_reviews = [float(i[1]) for i in results]
    # Display graph
    plt.plot(rating, num_reviews, "b+")
    plt.ylabel('Average Overall Rating For Brewery')
    plt.xlabel("Number of Reviews of Brewery's Beer")
    plt.title(f"Brewery's Quality versus Number of Reviews")
    plt.show()

except pg8000.Error as e:
    messagebox.showerror('Database error', e.args[0]["M"])


##############
# Statistics #
##############

#################
# Whatever else #
#################
