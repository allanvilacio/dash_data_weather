import pandas as pd
from glob import glob
from pathlib import Path

PATH_HOME = f'{Path.cwd()}/database'

def get_df_weather(start_date, end_date, filtro_codigo_ibge):

    arquivos_weather = glob(f'{PATH_HOME}/f_weather'+'*/*/*.parquet.gzip')
    df_weather = pd.DataFrame()
    range_date = pd.date_range(start_date, end_date)
    filtro_arquivos = range_date.strftime('%Y_%m').drop_duplicates()

    for arquivo in arquivos_weather:
        for filtro in filtro_arquivos:
            if filtro in arquivo:
                frame = pd.read_parquet(arquivo)
                frame = (frame[(frame['days_datetime'].isin(range_date)) &
                                        (frame['codigo_ibge'].isin(filtro_codigo_ibge))])
            
                df_weather = pd.concat([df_weather, frame], axis=0, ignore_index=True)

    del frame

    df_weather = (df_weather.sort_values(by=['days_datetime','address']).reset_index(drop=True))

    return df_weather


def get_d_calendario(data_inicio, data_fim):
    d_calendario = pd.DataFrame(pd.date_range(data_inicio, data_fim, name='data'))
    d_calendario['ano'] = d_calendario['data'].dt.year
    d_calendario['mes_ano'] = d_calendario['data'].dt.strftime('%b-%y')
    d_calendario['mes'] = d_calendario['data'].dt.strftime('%B')
    return d_calendario

def get_d_cidades():
    d_capitais = pd.read_csv(f'{PATH_HOME}/d_diversos/d_municipios_e_estados.csv',
                         dtype=str,
                         usecols=['capital','nome_mun','nome_uf','uf','codigo_ibge','regiao'])
    d_capitais = d_capitais[d_capitais['capital']=='1'].sort_values(by='uf').reset_index(drop=True)
    return d_capitais

