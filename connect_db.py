import sqlite3
from pathlib import Path


class DatabaseConnect:
    def __init__(self):
        # Database setup
        self.db_folder = "./db"
        self.db_path = f"{self.db_folder}/vehicles_app_list_db.db"
        self.table_name = "vehicle_app_list"
        self.connection = None
        self.cursor = None

        # Inicializamos la base de datos
        self.init_database()

    def init_database(self):
        # Creamos la carpeta y el path de la base de datos necesarios si no existen
        folder_path = Path(self.db_folder)
        db_path = Path(self.db_path)

        if not folder_path.exists():
            folder_path.mkdir(parents=True)

        if not db_path.exists():
            with open(self.db_path, "w"):
                pass

        # Conectamos a la base de datos y se crea la tabla si no existe
        self.connector()
        try:
            # Comprobamos si la tabla existe
            query = f"SELECT name FROM sqlite_master WHERE type='table' and name='{self.table_name}'"
            self.cursor.execute(query)
            result = self.cursor.fetchone()

            if result:
                return
            else:
                # Creamos la tabla si no existe
                query = f"""
                    CREATE TABLE '{self.table_name}' (
                    "make" TEXT NOT NULL,
                    "model_name"	TEXT NOT NULL,
                    "year"	INTEGER,
                    "region"	TEXT NOT NULL,
                    "chassis"	TEXT NOT NULL,
                    "key_type"	TEXT NOT NULL,
                    "transponder_type"	TEXT NOT NULL,
                    "programming" TEXT NOT NULL,
                    "cloning" TEXT NOT NULL,
                    PRIMARY KEY("model_name")
                    );                   
                    """
                self.cursor.execute(query)
                # Confirmamos cambios en la base de datos
                self.connection.commit()

        except Exception as e:
            self.connection.rollback()
            return e

        finally:
            # Cerramos cursor y la conexion
            self.cursor.close()
            self.connection.close()

    def connector(self):
        # Establecemos una conexión con la base de datos SQLite
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()

    def common_update_execute(self, query):
        # Ejecución de sentencias SQL de actualización
        self.connector()
        try:
            self.cursor.execute(query)
            # Confirmamos cambios en la base de datos
            self.connection.commit()
        except Exception as e:
            # Revertimos cambios en caso de una excepción
            self.connection.rollback()
            return e
        finally:
            # Cerramos cursor y la conexion
            self.cursor.close()
            self.connection.close()

    def common_search_one_execute(self, query):
        # Ejecucion de sentencias SQL de busqueda para un resultado
        self.connector()
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchone()
            return result
        except Exception:
            return None
        finally:
            self.cursor.close()
            self.connection.close()

    def common_search_all_execute(self, query):
        # Ejecucion de sentencias SQL de busqueda para todos los resultados
        self.connector()
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            return result
        except Exception:
            return None
        finally:
            self.cursor.close()
            self.connection.close()

    def add_new_vehicle(self, **kwargs):
        # Inserta un nuevo vehiculo en la tabla
        column_name = tuple(kwargs.keys())
        values = tuple(kwargs.values())

        query = f"INSERT INTO {self.table_name} {column_name} VALUES {values};"
        result = self.common_update_execute(query)

        return result

    def update_vehicle(self, **kwargs):
        # Actualiza un vehiculo de la tabla
        values = tuple(kwargs.values())

        query = f""" UPDATE {self.table_name} SET 
                    make= '{values[0]}', 
                    year='{values[2]}', 
                    region='{values[3]}', 
                    chassis='{values[4]}', 
                    key_type='{values[5]}', 
                    transponder_type='{values[6]}',
                    programming='{values[7]}',
                    cloning='{values[8]}'  
                   WHERE model_name='{values[1]}';
            """

        result = self.common_update_execute(query)
        return result
    
    def get_data(self, search_flag="", model_name=""):
        #
        #    search_flag: ALL, PROGRAMMING, CLONING, NO_COVERAGE
        #
        if search_flag == "ALL":
            query = f"SELECT make, model_name, year, region, chassis, key_type, transponder_type, programming, cloning FROM {self.table_name}"
        elif search_flag == "PROGRAMMING":
            query = (f"SELECT make, model_name, year, region, chassis, key_type, transponder_type, programming, cloning FROM {self.table_name} "
                   f"WHERE programming = 'Yes'")
        elif search_flag == "NO_COVERAGE":
            query = (f"SELECT make, model_name, year, region, chassis, key_type, transponder_type, programming, cloning FROM {self.table_name} "
                   f"WHERE programming = 'No' AND cloning = 'No'")
        elif search_flag == "CLONING":
            query = (f"SELECT make, model_name, year, region, chassis, key_type, transponder_type, programming, cloning FROM {self.table_name} "
                   f"WHERE cloning = 'Yes'")
        else:
            query = (f"SELECT make, model_name, year, region, chassis, key_type, transponder_type, programming, cloning FROM {self.table_name} "
                   f"WHERE model_name='{model_name}'")

        # Ejecutamos sentencia SQL
        result = self.common_search_all_execute(query)
        return result
    
    def delete_vehicle(self, model_name):
        # Elimina un vehiculo de la tabla
        query = f"DELETE from {self.table_name} WHERE model_name='{model_name}'"
        result = self.common_update_execute(query)
        return result
    
    def get_vehicle_names(self, model_name):
        # Recuperamos modelos de vehiculos basados en un nombre parcial o completo
        query = f"SELECT model_name FROM {self.table_name} WHERE model_name LIKE '%{model_name}%'"
        search_result = self.common_search_all_execute(query)
        return search_result
       
    def get_single_vehicle_info(self, model_name):
        # Recuperamos informacion sobre un unico vehiculo
        query = f"SELECT make, year, region, chassis, key_type, transponder_type, programming, cloning FROM {self.table_name} WHERE model_name='{model_name}'"
        search_result = self.common_search_one_execute(query)
        return search_result
    
    def get_current_vehicles(self):
        # Recuperamos el numero de vehiculos que hay en la tabla
        query = f"SELECT COUNT(*) FROM {self.table_name}"
        search_result = self.common_search_one_execute(query)
        return search_result
    
    def get_coverage_programming(self):
        # Recuperamos el numero de vehiculos que se pueden programar
        query = f"SELECT COUNT(*) FROM {self.table_name} WHERE programming = 'Yes'"
        search_result = self.common_search_one_execute(query)
        return search_result

    def get_coverage_cloning(self):
        # Recuperamos el numero de vehiculos que se pueden clonar
        query = f"SELECT COUNT(*) FROM {self.table_name} WHERE cloning = 'Yes'"
        search_result = self.common_search_one_execute(query)
        return search_result
    
    def get_not_coverage(self):
        # Recuperamos el numero de vehiculos que no estan cubiertos todavia
        query = f"SELECT COUNT(*) FROM {self.table_name} WHERE programming = 'No' AND cloning = 'No'"
        search_result = self.common_search_one_execute(query)
        return search_result
