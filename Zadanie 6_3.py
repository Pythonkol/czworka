import pandas as pd
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.exc import SQLAlchemyError
import os

# Ścieżki do CSV
STATIONS_CSV = r"D:\KODILLLA\czworka\clean_stations.csv"
MEASURES_CSV = r"D:\KODILLLA\czworka\clean_measure.csv"

# Połączenie z SQLite
def create_db_engine(db_file='stations.db', echo=False):
    try:
        engine = create_engine(f'sqlite:///{db_file}', echo=echo)
        print(f"Połączono z bazą danych: {db_file}")
        return engine
    except SQLAlchemyError as e:
        print(f"Błąd łączenia z bazą: {e}")
        return None

# Definiuje tabele stations i measures
def define_tables(engine):
    meta = MetaData()

    stations = Table(
        'stations', meta,
        Column('station_id', Integer, primary_key=True),
        Column('name', String, nullable=False),
        Column('latitude', Float),
        Column('longitude', Float)
    )

    measures = Table(
        'measures', meta,
        Column('measure_id', Integer, primary_key=True),
        Column('station_id', Integer, ForeignKey('stations.station_id'), nullable=False),
        Column('date', DateTime, nullable=False),
        Column('value', Float)
    )

    # Tworzenie tabel w bazie danych
    try:
        meta.create_all(engine)
        print("Utworzono tabele")
    except SQLAlchemyError as e:
        print(f"Błąd podczas tworzenia tabel: {e}")
    return stations, measures

# Dane z CSV
def load_csv_to_table(engine, table, csv_file):
    if not os.path.exists(csv_file):
        print(f"Błąd: Plik {csv_file} nie istnieje!")
        return
    try:
        df = pd.read_csv(csv_file)
        print(f"Wczytano {len(df)} wierszy z pliku {csv_file}")
        with engine.raw_connection() as raw_conn:
            df.to_sql(table.name, raw_conn, if_exists='append', index=False)
            raw_conn.commit()
        print(f"Dane wstawione do tabeli {table.name}")
    except Exception as e:
        print(f"Błąd podczas wczytywania danych z {csv_file}: {e}")
# Zapytanie
def execute_query(engine, query):
    try:
        with engine.connect() as conn:
            result = conn.execute(query).fetchall()
            print("Wynik:", result)
            return result
    except SQLAlchemyError as e:
        print(f"Błąd zapytania: {e}")
        return []

# Program
if __name__ == "__main__":
    engine = create_db_engine('stations.db', echo=True)
    if engine is None:
        exit(1)
    # Zdefiniuj tabele
    stations_table, measures_table = define_tables(engine)
    # Wczytaj CSV
    load_csv_to_table(engine, stations_table, STATIONS_CSV)
    load_csv_to_table(engine, measures_table, MEASURES_CSV)
    # Wykonuje zapytanie
    query = "SELECT * FROM stations LIMIT 5"
    execute_query(engine, query)
    # Sprawdza tabele
    print("Obecne tabele:", engine.table_names())