from utility.data_frames import get_df_weather, get_d_cidades
import pandas as pd

d_cidades = get_d_cidades()
df_weather = get_df_weather()

#d_cidades.groupby(by='regiao')['codigo_ibge'].apply(list).reset_index()

start_date = '2023-02-01 '
end_date = '2023-03-31 '


df_weather_filtered = (df_weather[df_weather['days_datetime'].isin(pd.date_range(start_date, end_date))]
                                [['days_datetime','days_temp','codigo_ibge']])

df_teste = df_weather.groupby(by=['regiao', df_weather_filtered['days_datetime'].dt.strftime('%Y-%m')])['days_temp'].mean()

print(pd.date_range(start_date, end_date))


print(df_weather_filtered)
