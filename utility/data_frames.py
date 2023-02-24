import pandas as pd
from glob import glob
from pathlib import Path

path_home = f'{Path.cwd()}/data'

def get_df_weather():
    arquivos_weather = glob(f'{path_home}/f_weather'+'*/*/*.parquet.gzip')
    df_weather = pd.DataFrame()
    for arquivo in arquivos_weather:
        frame = pd.read_parquet(arquivo)
        df_weather = pd.concat([df_weather, frame], axis=0, ignore_index=True)

    del frame 
    df_weather = (df_weather.sort_values(by=['days_datetime','address'])
                        .reset_index(drop=True))
    return df_weather


def get_d_calendario(data_inicio, data_fim):
    d_calendario = pd.DataFrame(pd.date_range(data_inicio, data_fim, name='data'))
    d_calendario['ano'] = d_calendario['data'].dt.year
    d_calendario['mes_ano'] = d_calendario['data'].dt.strftime('%b-%y')
    d_calendario['mes'] = d_calendario['data'].dt.strftime('%B')
    return d_calendario

def get_d_cidades():
    d_capitais = pd.read_csv(f'{path_home}/d_diversos/d_municipios_e_estados.csv',
                         dtype=str,
                         usecols=['capital','nome_mun','nome_uf','uf','codigo_ibge'])
    d_capitais = d_capitais[d_capitais['capital']=='1'].sort_values(by='uf').reset_index(drop=True)
    return d_capitais

