#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 16:30:43 2023

@author: mhaynam
"""

import numpy as np
import pandas as pd
# import pyodbc
from sqlalchemy.engine import URL
import seaborn as sns
import matplotlib.pyplot as plt 
plt.rc("font", size=10)

conn = "Driver={ODBC Driver 18 for SQL Server};Server=localhost;Database=master;UID=SA;PWD=SQLServerpw21!;TrustServerCertificate=yes;"
conn_url = URL.create("mssql+pyodbc", query={"odbc_connect": conn})          

from sqlalchemy import create_engine
engine = create_engine(conn_url)

# sql_query = pd.read_sql_query("SELECT TOP 10 playerID, yearID, teamID, AB, R, H\
#                               FROM Batting\
#                               WHERE 1=1\
#                                  AND yearID = 2021\
#                                  AND teamID = 'CLE'\
#                                  AND AB >= 100 ", engine)
                                 
# sql_query_bat = pd.read_sql_query("\
# SELECT teamID, yearID, SUM(AB) AS AB, SUM(R) AS R, SUM(H) AS H, SUM(BB) AS BB, SUM(HBP) AS HBP, SUM(SF) AS SF \
# FROM Batting \
# WHERE 1=1 \
#     AND yearID >= 1980 \
#     AND yearID NOT IN (1994,2020) \
# GROUP BY teamID, yearID", engine)                             

# df_bat = pd.DataFrame(sql_query_bat, columns = ['yearID', 'teamID', 'AB', 'R', 'H', 'BB', 'HBP', 'SF'])
# df_bat["BA"] = (df_bat["H"]) / (df_bat["AB"])
# df_bat["OBP"] = (df_bat["H"] + df_bat["BB"] + df_bat["HBP"]) / (df_bat["AB"] + df_bat["BB"] + df_bat["HBP"] + df_bat["SF"])
# df_bat = df_bat.sort_values(by=["R"], ascending=False)

# sql_query_field = pd.read_sql_query("\
# SELECT teamID, yearID, SUM(InnOuts) AS InnOuts, SUM(PO) AS PO, SUM(A) AS A, SUM(E) AS E, SUM(DP) AS DP \
# FROM Fielding \
# WHERE 1=1 \
#     AND yearID >= 1980 \
#     AND yearID NOT IN (1994,2020) \
# GROUP BY teamID, yearID", engine)   

# df_field = pd.DataFrame(sql_query_field, columns = ['yearID', 'teamID', 'InnOuts', 'PO', 'A', 'E', 'DP'])
# df_field = df_field.sort_values(by=["DP"], ascending=False)

# print(df_bat.head(), df_field.head())

sql_query = pd.read_sql_query("\
SELECT name, yearID, W, L, DivWin, WCWin, LgWin, WSWin, R, AB, H, _2B, _3B, HR, BB, SO, SB, CS, HBP, SF, RA, ER, ERA, CG, SHO, SV, IPouts, HA, HRA, BBA, SOA, E, DP, FP, attendance \
FROM Teams \
WHERE 1=1 \
    AND yearID >= 1980", engine)  

df = pd.DataFrame(sql_query)
df["post_birth"] = np.where((df["DivWin"]=="Y") | (df["WCWin"]=="Y"), True, False)
df["win_lg"] = np.where(df["LgWin"]=="Y", True, False)
df["win_ws"] = np.where(df["WSWin"]=="Y", True, False)

df["order_W"] = df.groupby("yearID")["W"].rank(method="min", ascending=False)
df["order_R"] = df.groupby("yearID")["R"].rank(method="min", ascending=False)
df["order_AB"] = df.groupby("yearID")["AB"].rank(method="min", ascending=False)
df["order_H"] = df.groupby("yearID")["H"].rank(method="min", ascending=False)
df["order_2B"] = df.groupby("yearID")["_2B"].rank(method="min", ascending=False)
df["order_3B"] = df.groupby("yearID")["_3B"].rank(method="min", ascending=False)
df["order_HR"] = df.groupby("yearID")["HR"].rank(method="min", ascending=False)
df["order_BB"] = df.groupby("yearID")["BB"].rank(method="min", ascending=False)
df["order_SO"] = df.groupby("yearID")["SO"].rank(method="min", ascending=False)
df["order_SB"] = df.groupby("yearID")["SB"].rank(method="min", ascending=False)
df["order_CS"] = df.groupby("yearID")["CS"].rank(method="min", ascending=False)
df["order_HBP"] = df.groupby("yearID")["HBP"].rank(method="min", ascending=False)
df["order_SF"] = df.groupby("yearID")["SF"].rank(method="min", ascending=False)
df["order_RA"] = df.groupby("yearID")["RA"].rank(method="min", ascending=False)
df["order_ER"] = df.groupby("yearID")["ER"].rank(method="min", ascending=False)
df["order_ERA"] = df.groupby("yearID")["ERA"].rank(method="min", ascending=False)
df["order_CG"] = df.groupby("yearID")["CG"].rank(method="min", ascending=False)
df["order_SHO"] = df.groupby("yearID")["SHO"].rank(method="min", ascending=False)
df["order_SV"] = df.groupby("yearID")["SV"].rank(method="min", ascending=False)
df["order_IPouts"] = df.groupby("yearID")["IPouts"].rank(method="min", ascending=False)
df["order_HA"] = df.groupby("yearID")["HA"].rank(method="min", ascending=False)
df["order_HRA"] = df.groupby("yearID")["HRA"].rank(method="min", ascending=False)
df["order_BBA"] = df.groupby("yearID")["BBA"].rank(method="min", ascending=False)
df["order_SOA"] = df.groupby("yearID")["SOA"].rank(method="min", ascending=False)
df["order_E"] = df.groupby("yearID")["E"].rank(method="min", ascending=False)
df["order_DP"] = df.groupby("yearID")["DP"].rank(method="min", ascending=False)
df["order_FP"] = df.groupby("yearID")["FP"].rank(method="min", ascending=False)
df["order_attendance"] = df.groupby("yearID")["attendance"].rank(method="min", ascending=False)

df_total_post = df.groupby("name", as_index=False)[["post_birth", "win_lg", "win_ws"]].sum()
df_total_post = df_total_post.sort_values(by=["post_birth"], ascending=False)

print(df_total_post)

plt.bar(df_total_post.name, df_total_post.post_birth)
plt.title('Postseason Births Since 1980')
plt.xlabel("Team")
plt.ylabel('Postseason Births')
plt.xticks(rotation=90)
plt.show()
























