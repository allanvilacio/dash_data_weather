from utility.data_frames import get_df_weather, get_d_cidades
import pandas as pd

d_cidades = get_d_cidades()
df_weather = get_df_weather()

#d_cidades.groupby(by='regiao')['codigo_ibge'].apply(list).reset_index()

start_date = '2023-01-01 '
end_date = '2023-12-31 '



df_weather_filtered = (df_weather[(df_weather['days_datetime'].isin(pd.date_range(start_date, end_date))) &
                                  (df_weather['codigo_ibge'].isin(['5300108', '5208707', '5002704', '5103403']))
                                  ]
                                [['days_datetime','days_temp','codigo_ibge']])

df_weather_filtered = df_weather_filtered.merge(d_cidades[['codigo_ibge', 'uf','regiao']], how='left')


filtro_regiao = []
for label, value in (d_cidades.groupby(by='regiao')['codigo_ibge']
                     .apply(list)
                     .reset_index()
                     .values):
    filtro_regiao.append([label, value])

print(filtro_regiao)