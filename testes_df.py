from utility.data_frames import get_df_weather, get_d_cidades
import pandas as pd

d_cidades = get_d_cidades()
df_weather = get_df_weather()

#d_cidades.groupby(by='regiao')['codigo_ibge'].apply(list).reset_index()

start_date = '2023-01-01 '
end_date = '2023-12-31 '


filtro_regioes = d_cidades['regiao'].unique().tolist()
filtro_regioes.append('Todas as regioes')
print(filtro_regioes)

filtro = 'Sul'
filtro_regioes = d_cidades['codigo_ibge'] if filtro =='Todas as regioes' else d_cidades[d_cidades['regiao']==filtro]['codigo_ibge']


print(teste_filtro)