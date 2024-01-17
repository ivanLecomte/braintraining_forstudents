""" 
Ivan Lecomte
Projet DBPY
16.01.2024
"""

import database
from mysql.connector import Error
import hashlib



#Function that insert the input of the new user data in the database
def insert_new_acc_data(username, password):
    try:
        connection = database.connect_to_database()#Firstly, tries to connect with database
        if connection:
            cursor = connection.cursor()

            #Check if the user given is already in the database or not by counting the number of result ( 0 = no user with this username, 1 = already an user with the username, 2 = impossible because the case is set as unique)
            cursor.execute(f"SELECT COUNT(*) FROM players WHERE pseudo = '{username}'")
            user_count = cursor.fetchone()[0]
            #if 1 it means the user is already existing so -> error
            if user_count > 0:
                print(f"L'utilisateur avec le nom d'utilisateur '{username}' existe déjà.")
                return
            
            #If the code arrives here it means user count was 0, so no user in the database with the username given, then we can insert the data into the table, but first we hash the password because we do not wante raw password in database
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            query = f"INSERT INTO players (pseudo, password) VALUES ('{username}','{hashed_password}')"
            cursor.execute(query)
            connection.commit()

            print(f"Données du nouveau compte insérées avec succès pour l'utilisateur: '{username}'")

    except Error as e:
        print(f"Erreur lors de l'insertion des données du nouveau compte : {e}")
    #Whatever happended the connections will be closed
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Connexion à la base de données fermée")

#This function compare user infos with the ones arleady in the database
def log_user(username, password):
        try:
            connection = database.connect_to_database()
            if connection:
                cursor = connection.cursor(dictionary=True)

                #Select in the database the username that has been asked
                cursor.execute(f"SELECT id, pseudo, password FROM players WHERE pseudo = '{username}'")
                user_data = cursor.fetchone()
                #Here to know if user_data is True, then it means that the user has been found
                if user_data:
                    user_id = user_data['id']
                    stored_password = user_data['password']

                    #Transform the raw password in the crypted one
                    hashed_password = hashlib.sha256(password.encode()).hexdigest()
                    #Here is the security, it checks if the password given is the same as the one in the database, to identify the user
                    if hashed_password == stored_password:
                        print(f"Utilisateur '{username}' connecté avec succès. ID: {user_id}")#if it was the same the user can be logged
                        return True, user_id
                    else:
                        print(f"Mot de passe incorrect pour l'utilisateur '{username}'")#if it was wrong, access denied  
                        return False

                else: #Here in the case if the previous if got False, it means the user hasn't been found in the database
                    print(f"L'utilisateur '{username}' n'existe pas dans la base de données.")
                    return False
        #Here in the case if the connection with the database is not established
        except Error as e:
            print(f"Erreur lors de la connexion de l'utilisateur : {e}")
        #Whatever happended the connections will be closed
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("Connexion à la base de données fermée")