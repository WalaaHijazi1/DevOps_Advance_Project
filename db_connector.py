import pyodbc



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
                                # that can be set as aan iterator.
        cursor.execute("SELECT DB_NAME()")
        db_name = cursor.fetchone()[0]
        print(f"Connected successfully! {db_name}")

        # The next command execute SQL queries using the execute() method of the cursor object.
        # it checks if a table exist in the database, if it doesn't it creates one by the name 'users'
        # INFORMATION_SCHEMA is a system databases that exists by default and contains all the information of the databases.
        #if the table doesn't exist it creates one with the name 'users', with the following details:
        # users_id INT IDENTITY(1,1) PRIMARY KEY NOT NULL: users_id is an identifier that represents the first column of the table,
        # it is the primary key, and it's not null, the (1,1) incrementing starting at 1 and increasing by 1 for each new row.
        # user_name VARCHAR(50) NOT NULL: stores user_name with a maximum variable-length string of 50 characters, NOT NULL insures that it has a value.
        # creation_date DATETIME DEFAULT GETDATE() VARCHAR(50):  stores creation_date with a maximum variable-length string of 50 characters,
        # DATETIME DEFAULT GETDATE() writes the date of the day!
        cursor.execute("""
            IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'users')
            BEGIN
            CREATE TABLE users (
                users_id INT IDENTITY(1,1) PRIMARY KEY NOT NULL,
                user_name VARCHAR(50) NOT NULL,
                creation_date DATETIME DEFAULT GETDATE()
                )
            END
        """)

        conn.commit() # The commit() method is used to make sure the changes made to the database.
        return conn, cursor
    
    # if it wasn't ablr to connect to the databse than it will returns an error:
    except Exception as e:
        print(f"Connection failed: {e}")
        return None, None
