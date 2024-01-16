""" 
Ivan Lecomte
Projet DBPY
16.01.2024
"""


import mysql.connector
from mysql.connector import Error
import tkinter as tk
import tkinter.messagebox as messagebox

def connect_to_database():
    connection = None
    try:
        connection = mysql.connector.connect(
            host='127.0.0.1',
            port='3306',
            database='projpy',
            user='ProjPy',
            password='Pa$$w0rd',
            buffered=True,
            autocommit=True
        )
        if connection.is_connected():
            print(f"Connecté à la BD MySQL (version {connection.get_server_info()})")
            return connection
    except Error as e:
        print(f"Problème de connexion avec la base de données: {e}")
        return None
    return connection


def get_all_results_with_exercise():
    try:
        connection = connect_to_database()
        if connection:
            cursor = connection.cursor(dictionary=True)

            #Récupérer toutes les stats dans la table gameplay avec leur code d'exercice
            cursor.execute("""
                SELECT players.pseudo, gameplay.timeplayed, gameplay.date, gameplay.totalNumber, gameplay.hitNumber,
                       game.gameCode AS gameCode
                FROM gameplay 
                INNER JOIN players ON gameplay.players_id = players.id
                INNER JOIN game ON gameplay.game_id = game.id
                ORDER BY gameplay.date DESC
            """)
            all_results = cursor.fetchall()

            if all_results:
                return all_results
            else:
                print("Pas de résultat trouvé dans la base de données.")
                return None

    except Error as e:
        print(f"Erreur lors de la récupération des résultats : {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Connexion à la base de données fermée")


def get_user_id(user_pseudo):
    try:
        connection = connect_to_database()
        if connection:
            cursor = connection.cursor()

             #Récupérer l'ID de l'utilisateur
            cursor.execute(f"SELECT id FROM players WHERE pseudo = '{user_pseudo}'")
            user_row = cursor.fetchone()

            print(f"Résultat de la requête pour l'utilisateur '{user_pseudo}': {user_row}")

            if user_row:
                user_id = user_row[0]
                return user_id
            else:
                print(f"L'utilisateur avec le pseudo '{user_pseudo}' n'a pas été trouvé dans la base de données.")
                return None

    except Error as e:
        print(f"Erreur lors de la récupération de l'ID de l'utilisateur : {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Connexion à la base de données fermée")


def get_exercise_id(exercise_code):
    try:
        connection = connect_to_database()
        if connection:
            cursor = connection.cursor()

            # Récupérer l'ID de l'exercice
            cursor.execute(f"SELECT id FROM game WHERE gameCode = '{exercise_code}'")
            exercise_row = cursor.fetchone()

            if exercise_row:
                exercise_id = exercise_row[0]
                return exercise_id
            else:
                print(f"L'exercice avec le code '{exercise_code}' n'a pas été trouvé dans la base de données.")
                return None

    except Error as e:
        print(f"Erreur lors de la récupération de l'ID de l'exercice : {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Connexion à la base de données fermée")


def save_result(exercise_code, user_pseudo, start_date, duration, nb_trials, nb_ok):
    try:
        connection = connect_to_database()
        if connection:
            cursor = connection.cursor()

            # Récupérer l'ID de l'utilisateur ou l'ajouter s'il n'existe pas
            user_id = get_user_id(user_pseudo)

            if user_id is not None:
                print(f"Utilisateur '{user_pseudo}' existe déjà. ID: {user_id}")
            else:
                # Ajouter l'utilisateur et récupérer l'ID
                cursor.execute(f"INSERT INTO players (pseudo) VALUES ('{user_pseudo}')")
                connection.commit()
                user_id = cursor.lastrowid  # Récupérer l'id de l'user après l'ajout
                print(f"Utilisateur '{user_pseudo}' ajouté avec succès. ID: {user_id}")

            #Afficher un message qui confirme l'enregistrement pour tel pseudo
            print("Résultat enregistré avec succès pour l'utilisateur:", user_pseudo)

            # Ajouter l'exercice s'il n'existe pas
            exercise_id = get_exercise_id(exercise_code)
            if exercise_id is None:
                cursor.execute(f"INSERT INTO game (gameCode) VALUES ('{exercise_code}')")
                connection.commit()
                exercise_id = cursor.lastrowid  # Récupérer l'ID après l'ajout
                print(f"Exercice '{exercise_code}' ajouté avec succès. ID: {exercise_id}")

            
            # Insérer le résultat dans la table results (en excluant la colonne 'id')
            cursor.execute(
                "INSERT INTO gameplay (game_id, players_id, timePlayed, hitNumber, totalNumber, date) "
                "VALUES (%s, %s, %s, %s, %s, %s)",
                (exercise_id, user_id, duration, nb_ok, nb_trials, start_date)
            )



            connection.commit()
            print("Résultat enregistré avec succès")

    except Error as e:
        print(f"Erreur lors de l'enregistrement du résultat dans la base de données: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Connexion à la base de données fermée")


def get_filtered_results(exercise_filter, nickname_filter, start_date_filter):
    try:
        connection = connect_to_database()
        if connection:
            cursor = connection.cursor(dictionary=True)

             # Construire la requête SQL en fonction des filtres fournis
            query = """
                SELECT gameplay.id, players.pseudo, gameplay.timePlayed, gameplay.date, gameplay.totalNumber, gameplay.hitNumber,
                       game.gameCode AS gameCode
                FROM gameplay
                INNER JOIN players ON gameplay.players_id = players.id
                INNER JOIN game ON gameplay.game_id = game.id
                WHERE 1
            """

            if exercise_filter:
                query += f" AND game.gameCode = '{exercise_filter}'"

            if nickname_filter:
                query += f" AND players.pseudo = '{nickname_filter}'"

            if start_date_filter:
                query += f" AND gameplay.date >= '{start_date_filter}'"

            query += " ORDER BY gameplay.date DESC" 

            # Exécuter la requête
            cursor.execute(query)
            filtered_results = cursor.fetchall()

            if filtered_results:
                return filtered_results
            else:
                print("Aucun résultat trouvé avec les filtres spécifiés.")
                return None

    except Error as e:
        print(f"Erreur lors de la récupération des résultats filtrés : {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Connexion à la base de données fermée")


def save_info05_results(user_pseudo, start_date, duration, nb_trials, nb_ok):
    try:
        connection = connect_to_database()
        if connection:
            cursor = connection.cursor()

            # Récupérer l'ID de l'utilisateur ou l'ajouter s'il n'existe pas
            user_pseudo = entry_pseudo.get()
            user_id = get_user_id(user_pseudo)

            if user_id is not None:
                print(f"Utilisateur '{user_pseudo}' existe déjà. ID: {user_id}")
            else:
                # Ajouter l'utilisateur et récupérer l'ID
                cursor.execute(f"INSERT INTO players (pseudo) VALUES ('{user_pseudo}')")
                connection.commit()
                user_id = cursor.lastrowid  # Récupérer l'ID après l'ajout
                print(f"Utilisateur '{user_pseudo}' ajouté avec succès. ID: {user_id}")

            # Affichez le pseudo correctement ici
            print("Résultat enregistré avec succès pour l'utilisateur:", user_pseudo)

            # Ajouter l'exercice INFO05 s'il n'existe pas
            exercise_code = "INFO05"
            exercise_id = get_exercise_id(exercise_code)
            if exercise_id is None:
                cursor.execute(f"INSERT INTO game (gameCode) VALUES ('{exercise_code}')")
                connection.commit()
                exercise_id = cursor.lastrowid  # Récupérer l'ID après l'ajout
                print(f"Exercice '{exercise_code}' ajouté avec succès. ID: {exercise_id}")

            # Insérer le résultat dans la table results (en excluant la colonne 'id')
            cursor.execute(
                f"INSERT INTO gameplay (game_id, players_id, timePlayed, hitNumber, totalNumber, date)"
                f"VALUES ({exercise_id}, {user_id}, '{duration}',{nb_ok}, {nb_trials}, '{start_date}')"
            )

            connection.commit()
            print("Résultat enregistré avec succès pour l'exercice INFO05")

    except Error as e:
        print(f"Erreur lors de l'enregistrement du résultat dans la base de données: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Connexion à la base de données fermée")


def delete_result(result_id):
    try:
        connection = connect_to_database()
        if connection:
            cursor = connection.cursor()

            # Récupérer l'ID de l'utilisateur associé au résultat
            cursor.execute(f"SELECT players_id FROM gameplay WHERE id = {result_id}")
            user_id = cursor.fetchone()

            # Supprimer le résultat avec l'ID spécifié
            cursor.execute(f"DELETE FROM gameplay WHERE id = {result_id}")

            # Vérifier si la suppression a eu lieu avec succès
            if cursor.rowcount > 0:
                print(f"Résultat avec l'ID {result_id} supprimé avec succès")

                    # Vérifier si l'utilisateur associé n'a plus aucun résultat
                cursor.execute(f"SELECT id FROM gameplay WHERE players_id = {user_id[0]}")
                remaining_results = cursor.fetchall()

                if not remaining_results:
                    # Aucun autre résultat trouvé pour cet utilisateur, supprimer l'utilisateur
                    cursor.execute(f"DELETE FROM gameplay WHERE id = {user_id[0]}")
                    connection.commit()
                    print(f"Utilisateur avec l'ID {user_id[0]} supprimé car il n'a plus de résultats.")

            else:
                print(f"Aucun résultat trouvé avec l'ID {result_id}. La suppression a peut-être échoué.")

    except Error as e:
        print(f"Erreur lors de la suppression du résultat : {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Connexion à la base de données fermée")



def update_result(result_id, new_hours, new_number_try, new_number_ok, new_pseudo=None, new_game=None):
    try:
        connection = connect_to_database()
        if connection:
            cursor = connection.cursor()

            # Récupérer les informations actuelles du résultat
            result_info = get_result_info(result_id)
            if not result_info:
                print(f"Aucune information trouvée pour le résultat avec l'ID {result_id}")
                return

            # Utiliser les valeurs actuelles ou les nouvelles si elles sont fournies
            current_pseudo = result_info['current_pseudo'] if new_pseudo is None else new_pseudo
            current_game = result_info['current_game'] if new_game is None else new_game

            # Récupérer l'ID du nouvel utilisateur ou l'ajouter s'il n'existe pas
            user_id = get_user_id(current_pseudo)

            if user_id is None:
                print(f"L'utilisateur '{current_pseudo}' n'existe pas.")
                return

            # Récupérer l'ID du nouvel exercice ou l'ajouter s'il n'existe pas
            exercise_id = get_exercise_id(current_game)

            if exercise_id is None:
                print(f"L'exercice '{current_game}' n'existe pas.")
                return

            # Construire la requête SQL pour la mise à jour
            query = """
                UPDATE gameplay
                SET timeplayed = %s, totalNumber = %s, hitNumber = %s, players_id = %s, game_id = %s
                WHERE id = %s
            """

            # Exécuter la requête avec les nouveaux paramètres
            cursor.execute(query, (new_hours, new_number_try, new_number_ok, user_id, exercise_id, result_id))
            connection.commit()

            print("Résultat mis à jour avec succès.")

    except Error as e:
        print(f"Erreur lors de la mise à jour du résultat : {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Connexion à la base de données fermée")



def get_result_info(result_id):
    try:
        connection = connect_to_database()
        if connection:
            cursor = connection.cursor(dictionary=True)

            # Récupérer les informations du résultat avec l'ID spécifié
            cursor.execute(f"""
                SELECT gameplay.id, gameplay.timePlayed, gameplay.totalNumber, gameplay.hitNumber, players.pseudo AS current_pseudo, game.gameCode AS current_game
                FROM gameplay
                INNER JOIN players ON gameplay.players_id = players.id
                INNER JOIN game ON gameplay.game_id = game.id
                WHERE gameplay.id = {result_id}
            """)
            result_info = cursor.fetchone()

            if result_info:
                return result_info
            else:
                print(f"Aucune information trouvée pour le résultat avec l'ID {result_id}")
                return None

    except Error as e:
        print(f"Erreur lors de la récupération des informations du résultat : {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Connexion à la base de données fermée")



def get_all_games():
    try:
        connection = connect_to_database()
        if connection:
            cursor = connection.cursor()

            # Récupérer tous les jeux
            cursor.execute("SELECT DISTINCT gameCode FROM game")
            games = cursor.fetchall()

            if games:
                return [game[0] for game in games]
            else:
                print("Aucun jeu trouvé dans la base de données.")
                return []

    except Error as e:
        print(f"Erreur lors de la récupération des jeux : {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Connexion à la base de données fermée")


