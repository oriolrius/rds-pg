import marimo

__generated_with = "0.19.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    from dotenv import load_dotenv
    import os

    load_dotenv()

    config = {
        "host": os.getenv("DB_HOST"),
        "port": os.getenv("DB_PORT", "5432"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "dbname": os.getenv("DB_NAME"),
    }

    mo.md(f"""
    # PostgreSQL RDS Demo

    **Connection config loaded from `.env`:**
    - Host: `{config['host']}`
    - Port: `{config['port']}`
    - User: `{config['user']}`
    - Database: `{config['dbname']}`
    """)
    return config, mo


@app.cell
def _(config):
    import psycopg2

    conn = psycopg2.connect(**config)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute("SELECT version();")
    version = cur.fetchone()[0]
    print(f"Connected to: {version}")
    
    return conn, cur


@app.cell
def _(cur):
    # show available databases
    cur.execute("SELECT datname FROM pg_database;")
    databases = cur.fetchall()
    print("Available databases:")
    for db in databases:
        print(f"- {db[0]}")
    return


@app.cell
def _(cur, mo):
    # Create a sample table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    mo.md("**Table `users` created.**")
    return


@app.cell
def _(cur, mo):
    # Insert sample data
    cur.execute("""
        INSERT INTO users (name, email)
        VALUES ('Alice', 'alice@example.com')
        ON CONFLICT (email) DO NOTHING;
    """)
    cur.execute("""
        INSERT INTO users (name, email)
        VALUES ('Bob', 'bob@example.com')
        ON CONFLICT (email) DO NOTHING;
    """)
    mo.md("**Sample users inserted.**")
    return


@app.cell
def _(cur, mo):
    # Query data
    cur.execute("SELECT * FROM users ORDER BY id;")
    rows = cur.fetchall()

    table_data = [{"id": r[0], "name": r[1], "email": r[2], "created_at": str(r[3])} for r in rows]
    mo.md("## Users Table")
    return (table_data,)


@app.cell
def _(mo, table_data):
    mo.ui.table(table_data)
    return


@app.cell
def _(cur, mo):
    # Update example
    cur.execute("UPDATE users SET name = 'Alice Smith' WHERE email = 'alice@example.com';")
    mo.md("**Updated Alice's name.**")
    return


@app.cell
def _(cur, mo):
    # Show updated data
    cur.execute("SELECT * FROM users ORDER BY id;")
    updated_rows = cur.fetchall()
    updated_data = [{"id": r[0], "name": r[1], "email": r[2], "created_at": str(r[3])} for r in updated_rows]
    mo.ui.table(updated_data)
    return


@app.cell
def _(mo):
    mo.md("""
    ## SQL Cells with Polars

    Load PostgreSQL data into a Polars dataframe, then use SQL cells to query it via DuckDB.
    """)
    return


@app.cell
def _(conn):
    import polars as pl

    # Load PostgreSQL table into Polars dataframe
    users_df = pl.read_database(
        query="SELECT * FROM users ORDER BY id",
        connection=conn
    )
    users_df
    return pl, users_df


@app.cell
def _(mo, users_df):
    # Now you can use SQL cells on the dataframe
    result = mo.sql(
        """
        SELECT name, email
        FROM users_df
        WHERE name LIKE '%Smith%'
        """
    )
    return result,


@app.cell
def _(mo, users_df):
    # Another SQL example - aggregation
    stats = mo.sql(
        """
        SELECT
            COUNT(*) as total_users,
            MIN(created_at) as first_user,
            MAX(created_at) as last_user
        FROM users_df
        """
    )
    return stats,


@app.cell
def _(mo):
    mo.md("""
    ## Cleanup

    Run the cell below to drop the `users` table when done.
    """)
    return


@app.cell
def _(cur):
    # Cleanup users' table
    cur.execute("DROP TABLE IF EXISTS users;")
    return


if __name__ == "__main__":
    app.run()
