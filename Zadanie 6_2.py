import sqlite3

def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        print(f"Połączono z bazą {db_file}, SQLite wersja: {sqlite3.version}")
        return conn
    except sqlite3.Error as e:
        print(f"Błąd połączenia: {e}")
        return None

def execute_sql(conn, sql):
    try:
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        print("Zapytanie wykonane.")
    except sqlite3.Error as e:
        print(f"Błąd SQL: {e}")

def create_tables(conn):
    sql_projects = """
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nazwa TEXT NOT NULL,
            start_date TEXT,
            end_date TEXT
        );
    """
    sql_tasks = """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER NOT NULL,
            nazwa TEXT NOT NULL,
            opis TEXT,
            status TEXT,
            start_date TEXT,
            end_date TEXT,
            FOREIGN KEY (project_id) REFERENCES projects (id)
        );
    """
    execute_sql(conn, sql_projects)
    execute_sql(conn, sql_tasks)

def add_project(conn, project):
    sql = 'INSERT INTO projects(nazwa, start_date, end_date) VALUES (?, ?, ?)'
    try:
        cur = conn.cursor()
        cur.execute(sql, project)
        conn.commit()
        return cur.lastrowid
    except sqlite3.Error as e:
        print(f"Błąd dodawania projektu: {e}")
        return None

def add_task(conn, task):
    sql = 'INSERT INTO tasks(project_id, nazwa, opis, status, start_date, end_date) VALUES (?, ?, ?, ?, ?, ?)'
    try:
        cur = conn.cursor()
        cur.execute(sql, task)
        conn.commit()
        return cur.lastrowid
    except sqlite3.Error as e:
        print(f"Błąd dodawania zadania: {e}")
        return None

def select_all(conn, table):
    try:
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {table}")
        return cur.fetchall()
    except sqlite3.Error as e:
        print(f"Błąd pobierania danych: {e}")
        return []

def select_where(conn, table, **conditions):
    try:
        cur = conn.cursor()
        query = " AND ".join([f"{k}=?" for k in conditions])
        values = tuple(conditions.values())
        cur.execute(f"SELECT * FROM {table} WHERE {query}", values)
        return cur.fetchall()
    except sqlite3.Error as e:
        print(f"Błąd selekcji: {e}")
        return []

def update(conn, table, id, **fields):
    try:
        params = ", ".join([f"{k}=?" for k in fields])
        values = tuple(fields.values()) + (id,)
        sql = f"UPDATE {table} SET {params} WHERE id=?"
        cur = conn.cursor()
        cur.execute(sql, values)
        conn.commit()
        print("Rekord zaktualizowany.")
    except sqlite3.Error as e:
        print(f"Błąd aktualizacji: {e}")

def delete_where(conn, table, **conditions):
    try:
        query = " AND ".join([f"{k}=?" for k in conditions])
        values = tuple(conditions.values())
        sql = f"DELETE FROM {table} WHERE {query}"
        cur = conn.cursor()
        cur.execute(sql, values)
        conn.commit()
        print("Rekordy usunięte.")
    except sqlite3.Error as e:
        print(f"Błąd usuwania: {e}")

if __name__ == "__main__":
    conn = create_connection("database.db")
    if conn:
        create_tables(conn)

        # Dodajemy projekt z datami w formacie YYYY-MM-DD HH:MM:SS
        project = ("Powtórka angielskiego", "2025-05-24 00:00:00", "2025-05-30 00:00:00")
        project_id = add_project(conn, project)
        print(f"Dodano projekt o ID: {project_id}")

        # Dodajemy zadanie do projektu z pełnymi datami i godzinami
        task = (project_id, "Czasowniki nieregularne", "Nauka 8 czasowników", "rozpoczęte",
                "2025-05-24 12:00:00", "2025-05-25 15:00:00")
        task_id = add_task(conn, task)
        print(f"Dodano zadanie o ID: {task_id}")

        # Pobieramy wszystkie projekty
        print("Projekty:", select_all(conn, "projects"))

        # Pobieramy zadania pierwszego projektu
        print("Zadania projektu 1:", select_where(conn, "tasks", project_id=1))

        # Pobieramy zadania ze statusem "rozpoczęte"
        print("Zadania rozpoczęte:", select_where(conn, "tasks", status="rozpoczęte"))

        # Aktualizujemy status zadania oraz datę zakończenia
        update(conn, "tasks", task_id, status="ended", end_date="2025-05-24 16:00:00")

        # Usuwamy zadanie
        delete_where(conn, "tasks", id=task_id)

        conn.close()