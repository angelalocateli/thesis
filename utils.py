from IPython.display import display, clear_output
import numpy as np
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import ipywidgets as widgets
import io


def joinDate(df):    
    # DETECÇÃO DE PADRÕES
    db = {}  # irá armazenar os padrões em dias consecutivos
    code = 0 # chave de acesso ao db

    for index, row_i in df.iterrows():
        if index == 0: row_0 = row_i

        # salve os tempos iniciais e finais (b e f) do padrão
        b = datetime.datetime.strptime(row_0['Data'], '%d/%m/%Y')    
        f = datetime.datetime.strptime(row_i['Data'], '%d/%m/%Y')
        diff = (f - b).days

        # padrão que não se repete em dias consecutivos
        pattern = [
            datetime.datetime.strftime(f, '%d/%m/%y'),
            datetime.datetime.strftime(f, '%d/%m/%y'),
            *row_i[1:]
        ]    

        # padrão que se repete em dias consecutivos
        if (row_i[1:].equals(row_0[1:])) and diff <= 1:                    
            pattern = [
                datetime.datetime.strftime(b, '%d/%m/%y'),
                datetime.datetime.strftime(f, '%d/%m/%y'),
                *row_i[1:]
            ]
        else:
            code += 1

        # guarde o padrão no novo db
        if db.get(code, 0):
            db[code][1] = pattern[1] # apenas altera a data f caso já exista
        else:
            db[code] = pattern

        # passo
        row_0 = row_i


    # transpor db para voltar ao formato convencional    
    db = pd.DataFrame(db).transpose()    

    new_col = list((df.columns).insert(1, 'f'))
    new_col[0] = 'b'

    # montar um DataFrame com os suportes de cada padrão encontrado em db
    db = db.rename(columns={old:new for old, new in zip(db.columns, new_col)})
    
    return db


def get_supports(df):
    df_uniques = df.drop(columns=['b', 'f'])
    supports = df.groupby(df_uniques.columns.tolist(), as_index=False).size()
    supports['frequencia'] = (supports['size'] / df.shape[0]).round(3)
    
    return supports


def match(df, row):
    """
    Busca uma linha em um df e retorna um novo df com os índices encontrados.
    """
    for col in df:
        df = df.loc[(df[col] == row[col])]
    return df


def timeRelation(df_analysis, df_reference): 
    gaps = range(-7, 8)
    tx_tables = {}
    try:
        for row in df_reference.iloc[:, :-2].iterrows():
            i, ref_pattern = row
            # tx_tables[str(df_reference.iloc[i, :-2])] = {}
            tx_tables[str(ref_pattern)] = {}
            for gap in gaps:
                # busca o padrão de referência no df_analysis        
                matches = match(df_analysis.iloc[:, 2:], ref_pattern)

                # quantidade de vezes que o padrão de ref foi encontrado em df_analysis
                matches_size = matches.shape[0]

                # guarda apenas os índices encontrados
                matches_indices = matches.index

                # padrões encontrados em tx
                tx_indices = matches_indices + gap
                tx_indices = tx_indices[(tx_indices >= 0) & (tx_indices < df_analysis.shape[0])]
                tx_data = df_analysis.iloc[tx_indices]

                # filtra os padrões apenas onde há ao menos um atributo == sup
                tx_data = tx_data[(tx_data.MP25 =='sup_media') |
                                  (tx_data.MP10 =='sup_media') |
                                  (tx_data.CO   =='sup_media') |
                                  (tx_data.SO2  =='sup_media') |
                                  (tx_data.NO2  =='sup_media') |
                                  (tx_data.O3   =='sup_media')]

                # descarta a data 
                tx_patterns = tx_data.iloc[:, 2:]

                # tabela tx
                tx_table = tx_patterns.groupby(tx_patterns.columns.tolist(), as_index=False).size()
                tx_table['suporte'] = (tx_table['size'] / matches_size).round(4)
                sup_count = tx_table[tx_table.internacao == 'sup_media']['size'].sum()
                inf_count = tx_table[tx_table.internacao == 'inf_media']['size'].sum()
                tx_table['confianca'] = None
                tx_table.loc[tx_table.internacao == 'sup_media', 'confianca'] = \
                tx_table['size'] / sup_count
                tx_table.loc[tx_table.internacao == 'inf_media', 'confianca'] = \
                tx_table['size'] / inf_count
                

                # grava a tabela tx no dicionário final
                tx_tables[str(ref_pattern)][gap] = tx_table   
    
    # debugg indices
    except:
        return tx_indices, df_analysis
    
    return tx_tables