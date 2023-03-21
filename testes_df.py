from utility.data_frames import get_df_weather, get_d_cidades
from dash import dcc ,html, Input, Output, callback, State
import pandas as pd
import json

d_cidades = get_d_cidades()
df_weather = get_df_weather()

filtro_regiao = d_cidades['codigo_ibge'].unique()
start_date = '2022-01-01'
end_date = '2023-03-30'

df_weather_filtered = (df_weather[(df_weather['days_datetime'].isin(pd.date_range(start_date, end_date))) &
                                    (df_weather['codigo_ibge'].isin(filtro_regiao))]
                                [['days_datetime','days_temp','codigo_ibge', 'days_precip']])
df_weather_filtered = df_weather_filtered.merge(d_cidades[['codigo_ibge', 'uf','regiao']], how='left')


df_weather_filtered.sort_values(by=['regiao', 'uf', 'days_datetime'], 
                                    ignore_index=True, inplace=True)
df_weather_filtered['days_precip_acum'] = df_weather_filtered.groupby(by=['codigo_ibge'])['days_precip'].cumsum()

print(df_weather_filtered.loc[df_weather_filtered['codigo_ibge'] == '5002704'])
