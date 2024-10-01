import json
from json.decoder import JSONDecodeError
import os
import pandas as pd


class Lector:
    def __init__(self, path: str):
        self.path = path
        
    def _comprueba_extension(self, extension: str) -> bool:        
            file_extension = os.path.splitext(self.path)[1]
            if extension != file_extension:
                raise Exception("El archivo no tiene la extension que toca")
            else:
                return True
    
    def lee_archivo(self):   # se define en el las sublclass
        pass
    
    
    @staticmethod
    def convierte_dict_a_CSV(list_dicts: list[dict]) -> pd.DataFrame:
        df = pd.DataFrame.from_dict(list_dicts)
        return df

    
class LectorCSV(Lector):
    def __init__(self, path: str):
        super().__init__(path)  # Llama al constructor de la clase base (padre)
    
    def lee_archivo(self, datetime_columns=[]):
        df = pd.DataFrame()   # inicializar como un dataframe vacío
        
        if self._comprueba_extension('.csv'):  # llamada estándar a un método
            try:
                df = pd.read_csv(self.path)
                for column in datetime_columns:
                    if column in df:
                        df[column] = pd.to_datetime(df[column])
                    else:
                        raise ValueError(f"La column '{column}' no existe en el dataframe")
            except FileNotFoundError:
                print(f"Error: No se encontró el archivo{self.path}")
            except pd.errors.EmptyDataError:  # se produce cuando el archivo CSV está vacio
                print(f"Error: El archivo {self.path} está vacio.")
        return df

    
class LectorJSON(Lector):
    def __init__(self, path: str):
        super().__init__(path)
        
    def lee_archivo(self):
        l_d = [] # inicializar lista de diccionarios para evitar referencias antes de la asignación
        try:
            if self._comprueba_extension('.json'):
                with open(self.path, 'r') as file:
                    l_d = json.load(file)
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo {self.path}")
        except JSONDecodeError:
            print(f"Error: El archivo {self.path} no contiene JSON válido.")
        except Exception as e:
            print(f"Error al cargar el archivo JSON: {e}")
        return l_d
    
class LectorTXT(Lector):
    def __init__(self, path: str):
        super().__init__(path)
        
    def lee_archivo(self):
        l_d = [] # Inicializa una lista vacía para almacenar los diccionarios
        
        # cada diccionario es un vuelo o mejor una linea de nuestro txt
        
        try:
            if self._comprueba_extension('.txt'):
                with open(self.path, 'r', encoding='utf-8') as file:
                    lines = file.readlines()
                
                # Procesa la primera línea para obtener los encabezados de las columnas
                header = lines[0].replace(' ', '').replace('\n', '').split(',')
                lines = lines[1:]
                
                for i, l in enumerate(lines):
                    v_list = l.replace(' ', '').replace('\n', '').split(',')
                    v_dict= {}
                    for i, v in enumerate(v_list):
                        v_dict[header[i]] = v   # Asocia cada valor con su correspondiente encabezado
                    l_d.append(v_dict)
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo {self.path}")
        except Exception as e:
            print(f"Error al cargar el archivo de texto: {e}")
        return l_d
    