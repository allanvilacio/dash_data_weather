from utility.data_frames import get_df_weather, get_d_cidades

# Data frames
df_weather = get_df_weather()
d_cidades = get_d_cidades()



print(df_weather[df_weather.index == df_weather.index.max()][['days_datetime', 'days_tempmax']])