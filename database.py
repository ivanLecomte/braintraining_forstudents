"""
Auteur: Ivan Lecomte
Module: ProjPy
Date: 24.11.2023
"""
import mysql.connector

def open_dbconnection():
    global db_connection
    db_connection = mysql.connector.connect(host='127.0.0.1', port='3306',
                                   user='ProjPy', password='Pa$$w0rd', database='projpy',
                                   buffered=True, autocommit=True)

def close_dbconnection():
    db_connection.close()


def add_pseudo(user):
    query = "INSERT INTO players (pseudo) values (%s)"
    cursor = db_connection.cursor()
    cursor.execute(query, (user,))
    inserted_id = cursor.lastrowid
    cursor.close()
    return inserted_id

def add_scores(date_start,number_of_successes, number_of_tries, duration, Players_id, Exercises_id):
    query = "INSERT INTO gameplay (game_id, players_id, timePlayed, hitNumber, totalNumber, date) values (%s, %s, %s, %s, %s, %s)"
    cursor = db_connection.cursor()
    cursor.execute(query, (Exercises_id, Players_id, duration, number_of_successes, number_of_tries, date_start))
    inserted_id = cursor.lastrowid
    cursor.close()
    return inserted_id

def get_exerciseid(exercise):
    query = "SELECT id FROM game WHERE gameCode = %s"
    cursor = db_connection.cursor()
    cursor.execute(query, (exercise,))
    row = cursor.fetchone()
    cursor.close()
    return row


# Function to get students ID
def get_playerid(player):
    query = "SELECT id FROM players WHERE pseudo = %s"
    cursor = db_connection.cursor()
    cursor.execute(query, (player,))
    row = cursor.fetchone()
    cursor.close()
    return row

def get_allScores():
    query = "SELECT * FROM gameplay"
    cursor = db_connection.cursor()
    cursor.execute(query, multi=True)
    rows = cursor.fetchall()
    cursor.close()
    return rows

def get_playername(player_id):
    query = "SELECT pseudo FROM players WHERE id = %s"
    cursor = db_connection.cursor()
    cursor.execute(query, (player_id,))
    row = cursor.fetchone()
    cursor.close()
    return row


# Function to get exercises name by the ID
def get_exercisename(exercises_id):
    query = "SELECT gameCode FROM game WHERE id = %s"
    cursor = db_connection.cursor()
    cursor.execute(query, (exercises_id,))
    row = cursor.fetchone()
    cursor.close()
    return row
