import pandas as pd
from pandas.errors import OutOfBoundsDatetime
from entities.slot import Slot
from datetime import timedelta

class Aeropuerto:
    def __init__(self, vuelos: pd.DataFrame, slots: int, t_embarque_nat: int, t_embarque_internat: int):
        self.df_vuelos = vuelos
        self.n_slots = slots
        self.slots = {}
        self.tiempo_embarque_nat = t_embarque_nat
        self.tiempo_embarque_internat = t_embarque_internat

        for i in range(1, self.n_slots + 1):
            self.slots[i] = Slot()

        self.df_vuelos['fecha_despegue'] = pd.NaT
        self.df_vuelos['slot'] = 0

    def calcula_fecha_despegue(self, row) -> pd.Series:
        time_offset = self.tiempo_embarque_nat
        if row['tipo_vuelo'] == 'INTERNAT':
            time_offset = self.tiempo_embarque_internat
        
        retraso = 0
        
        if row['retraso'] != '-':
            tmp = pd.to_datetime(row['retraso'])
            retraso = (tmp.second + tmp.minute * 60)
        
        row['fecha_despegue'] = row['fecha_llegada'] + timedelta(minutes=time_offset) + timedelta(seconds=retraso)
        return row

    def encuentra_slot(self, fecha_vuelo) -> int:
        slot = -1
        for id in self.slots:
            time = self.slots[id].slot_esta_libre_fecha_determinada(fecha_vuelo)
            if time == 0:
                return id
        return slot

    def asigna_slot(self, vuelo) -> pd.Series:
        slot = -1
        fecha_vuelo = vuelo['fecha_llegada']
        intentos = 0
        max_intentos = 100  # Limitar el número de intentos para evitar bucle infinito
    
        while slot == -1 and intentos < max_intentos:
            try:
                if pd.Timestamp.min <= fecha_vuelo <= pd.Timestamp.max:
                    slot = self.encuentra_slot(fecha_vuelo)
                else:
                    raise OutOfBoundsDatetime("Fecha fuera de los límites permitidos")
                
                fecha_vuelo += timedelta(minutes=10)
                intentos += 1
            
            except Exception as e:
                print(f"Error al asignar slot para el vuelo con fecha {fecha_vuelo}: {e}")
                return vuelo

        if slot == -1:
            print(f"No se encontró un slot disponible para el vuelo {vuelo['id']} después de {intentos} intentos")
            return vuelo

        vuelo = self.calcula_fecha_despegue(vuelo)
        self.slots[slot].asigna_vuelo(vuelo['id'], vuelo['fecha_llegada'], vuelo['fecha_despegue'])
        vuelo['slot'] = slot
        print(f'El Vuelo {vuelo["id"]} con fecha de llegada y de despegue {vuelo["fecha_llegada"]}, {vuelo["fecha_despegue"]} ha sido asignado al slot {slot}')
        
        return vuelo

    def asigna_slots(self):
        self.df_vuelos.sort_values(by=['fecha_llegada'], inplace=True)
        while len(self.df_vuelos) > 0:
            df_i = self.df_vuelos.iloc[0:self.n_slots, :]
            df_i = df_i.apply(lambda vuelo: self.asigna_slot(vuelo), axis=1)
            self.df_vuelos = self.df_vuelos.iloc[self.n_slots:, :]