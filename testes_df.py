from utility.data_frames import get_df_weather, get_d_cidades

# Data frames
df_weather = get_df_weather()
d_cidades = get_d_cidades()



print(d_cidades.columns)

[{'label': label, 'value': value} for label, value in d_cidades[['nome_mun','codigo_ibge']].sort_values(by='nome_mun').values]
    
print(df_weather['days_datetime'].max().strftime('%d de %B de %Y'))