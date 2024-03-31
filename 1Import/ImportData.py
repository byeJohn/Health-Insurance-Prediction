import sqlite3
import pandas as pd

# 1. Load Data File
df = pd.read_csv('cleanedInsurance.csv')

# 2. Create/Connect to SQLite Database
connection = sqlite3.connect('Medical.db')

# 3. Load Data File to SQLite
# fail;replace;append
df.to_sql('Insurance', connection, if_exists='replace')

# 4. Close Connection
connection.close