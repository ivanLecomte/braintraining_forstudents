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
            
            #If the code arrives here it means user count was 0, so no user, then we can insert the data into the table, but first we hash the password because we do not wanter raw password in database
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            query = f"INSERT INTO players (pseudo, password) VALUES ('{username}','{hashed_password}')"
            cursor.execute(query)
            connection.commit()

            print(f"Données du nouveau compte insérées avec succès pour l'utilisateur: '{username}'")

    except Error as e:
        print(f"Erreur lors de l'insertion des données du nouveau compte : {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Connexion à la base de données fermée")


def log_user(username, password):
        try:
            connection = database.connect_to_database()
            if connection:
                cursor = connection.cursor(dictionary=True)

                # Récupérer le mot de passe haché de l'utilisateur dans la base de données
                cursor.execute(f"SELECT id, pseudo, password FROM players WHERE pseudo = '{username}'")
                user_data = cursor.fetchone()

                if user_data:
                    user_id = user_data['id']
                    stored_password = user_data['password']

                    # Hasher le mot de passe fourni par l'utilisateur pour le comparer avec celui stocké
                    hashed_password = hashlib.sha256(password.encode()).hexdigest()

                    if hashed_password == stored_password:
                        print(f"Utilisateur '{username}' connecté avec succès. ID: {user_id}")
                        return True, user_id
                    else:
                        print(f"Mot de passe incorrect pour l'utilisateur '{username}'")
                        return False

                else:
                    print(f"L'utilisateur '{username}' n'existe pas dans la base de données.")
                    return False

        except Error as e:
            print(f"Erreur lors de la connexion de l'utilisateur : {e}")

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("Connexion à la base de données fermée")


#insert_new_acc_data("ivan", "1234")
#log_user("ivan", "1234")