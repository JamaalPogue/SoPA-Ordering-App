import mysql.connector
from mysql.connector import Error

def connectToDatabase(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


# Read all from user table
def readAllUsers(cursor):
    sql_query = ("SELECT * FROM users")
    cursor.execute(sql_query)
    print("This is a test to pull all data from users table.")
    print(cursor.fetchall())
    print("Test successful. Congrats, this works.")


if __name__ == "__main__":

    # Replace parameters with DB information
    host_name = "localhost"
    user_name = "root"
    user_password = "SoPAStudentDB!#!"
    db_name = "aafesorder"

    # Initialize database connection
    connection = connectToDatabase(host_name, user_name, user_password, db_name)

    # Initialize database cursor
    cursor = connection.cursor()

    # Read user table
    readAllUsers(cursor)

    # Closing connection when done
    if connection:
        connection.close()
