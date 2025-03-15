import pyodbc
import datetime


def connect_data_table():
    # Connection details
    server = "tcp:usersdbserver.database.windows.net,1433"
    database = "users_data"
    username = "adminwalaa"  # Your Azure AD login
    password = "Walaa2511"  # Your Azure AD password

    # Create connection string
    conn_str = f"""
        DRIVER={{ODBC Driver 18 for SQL Server}};
        SERVER={server};
        DATABASE={database};
        UID={username};
        PWD={password};
        Encrypt=yes;
        TrustServerCertificate=no;
        Connection Timeout=30;
        """

    # Connect to Azure SQL Database
    try:
        conn = pyodbc.connect(conn_str) # Create a connection that contains the necessary information to connect to your database: conn_str.
        cursor = conn.cursor() # Create a cursor object to interact with the database using the cursor() method, a cursor is a conceptual object
                                # that can be set as an iterator.
        cursor.execute("SELECT DB_NAME()")
        db_name = cursor.fetchone()[0]
        print(f"Connected successfully! {db_name}")

        for _ in range(10):
            username = input("Enter user name to the data base: ")

            creation_date = datetime.datetime.now()

            cursor.execute("INSERT INTO dbo.users (user_name,creation_date) VALUES (?,?)", (username,creation_date))
        conn.commit()  # Save all inserts
        print("All users inserted successfully!")

        conn.close()

    
    except Exception as e:
        print(f"Connection failed: {e}")


connect_data_table()
