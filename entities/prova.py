import pandas as pd

# Obtener el tiempo actual como pandas.Timestamp
now = pd.Timestamp.now()
print("Fecha y hora actuales:", now)

# Convertir pandas.Timestamp a timestamp (en nanosegundos)
timestamp = now.value
print("Timestamp (nanosegundos):", timestamp)

# Convertir timestamp a pandas.Timestamp
timestamp_in_seconds = timestamp // 10**9  # Convertir a segundos
ts_from_timestamp = pd.Timestamp(timestamp_in_seconds, unit='s')
print("pandas.Timestamp desde timestamp:", ts_from_timestamp)