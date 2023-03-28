#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 16:30:43 2023

@author: mhaynam
"""

# from itertools import product 
import numpy as np
import pandas as pd
from iso3166 import countries
from sqlalchemy.engine import URL
# import seaborn as sns
import matplotlib.pyplot as plt 
import matplotlib.image as mpimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

conn = "Driver={ODBC Driver 18 for SQL Server};Server=localhost;Database=master;UID=SA;PWD=####;TrustServerCertificate=yes;"
conn_url = URL.create("mssql+pyodbc", query={"odbc_connect": conn})          

from sqlalchemy import create_engine
engine = create_engine(conn_url)

team_colors = {
    'ARI': '#A71930',
    'ATL': '#CE1141',
    'BAL': '#DF4601',
    'BOS': '#C62033',
    'CHC': '#0E3386',
    'CHW': '#231F20',
    'CIN': '#C6011F',
    'CLE': '#E31937',
    'COL': '#37246B',
    'DET': '#0C2C56',
    'HOU': '#EB6E1F',
    'KCR': '#004687',
    'ANA': '#BA2026',
    'LAD': '#005A9C',
    'FLA': '#00A3E0',
    'MIL': '#0A2351',
    'MIN': '#002B5C',
    'NYM': '#FF5910',
    'NYY': '#142448',
    'OAK': '#003831',
    'PHI': '#E81828',
    'PIT': '#FDB827',
    'SDP': '#FFC425',
    'SFG': '#F4793E',
    'SEA': '#005C5C',
    'STL': '#B72126',
    'TBD': '#092C5C',
    'TEX': '#C0111F',
    'TOR': '#134A8E',
    'WSN': '#AB0003'
}

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
SELECT franchID, yearID, W, L, DivWin, WCWin, LgWin, WSWin, R, AB, H, _2B, _3B, HR, BB, SO, SB, CS, HBP, SF, RA, ER, ERA, CG, SHO, SV, IPouts, HA, HRA, BBA, SOA, E, DP, FP, attendance \
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

df_total_post = df.groupby("franchID", as_index=False)[["post_birth", "win_lg", "win_ws"]].sum()
df_total_post = df_total_post.sort_values(by=["post_birth"], ascending=False)

# print(df_total_post)



# def pos_image(x, y, teams, haut):
#     # teams = df_total_post.franchID
#     folder = "/Users/mhaynam/ds_portfolio/baseball_stat/"
#     img = folder + teams + '.png'
#     im = mpimg.imread(img)
#     ratio = 4 / 3
#     w = ratio * haut
#     ax.imshow(im,
#               extent=(x - w, x, y, y + haut),
#               zorder=2)
    
# plt.style.use('seaborn')
# fig, ax = plt.subplots()

# X = list(df_total_post['post_birth'])
# Y = list(df_total_post['franchID'])
# list_teams = list(zip(Y, X))
# haut = 0.8
# r = ax.barh(y=Y, width=X, height=haut, zorder=1) #, color=df_total_post['franchID'].map(team_colors))

# y_bar = [rectangle.get_y() for rectangle in r]
# y_bar.reverse()
# for teams, y in zip(list_teams, y_bar):
#     pos_image(teams[1], y, teams[0], haut)

# plt.title('Postseason Births Since 1980')
# plt.ylabel("Team")
# plt.xlabel('Postseason Births')
# plt.xticks(rotation=90)
# plt.show()

# y_bar = [rectangle.get_y() for rectangle in r]
# y_bar.reverse()
# p = list(zip(list_teams, y_bar))
# print(p)

# pays = countries.get(pays).alpha2.lower()
# print(pays)

def offset_image(x, y, label, bar_is_too_short, ax):
    # response = requests.get(f'https://www.countryflags.io/{label}/flat/64.png')
    file = f"/Users/mhaynam/ds_portfolio/baseball_stat/{label}.png"
    img = plt.imread(file)
    im = OffsetImage(img, zoom=0.06)
    im.image.axes = ax
    x_offset = 0
    if bar_is_too_short:
        x = 0
    ab = AnnotationBbox(im, (x, y), xybox=(x_offset, 0), frameon=False,
                        xycoords='data', boxcoords="offset points", pad=0)
    ax.add_artist(ab)

labels = list(df_total_post['franchID'])
# colors = ['crimson', 'dodgerblue', 'teal', 'limegreen', 'gold']
values = df_total_post['post_birth']

height = 0.9
plt.barh(y=labels, width=values, height=height, color=df_total_post['franchID'].map(team_colors), align='center', alpha=0.8)

max_value = values.max()
for i, (label, value) in enumerate(zip(labels, values)):
    offset_image(value, i, label, bar_is_too_short=value < max_value / 10, ax=plt.gca())
plt.subplots_adjust(left=0.15)

plt.title('Postseason Births Since 1980')
plt.ylabel("Team")
plt.xlabel('Postseason Births')
plt.xticks(rotation=90)
plt.show()









