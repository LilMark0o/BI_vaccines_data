import pandas as pd

df = pd.read_csv('fin_dim_vacunacion_detalle.csv')

if 'total_dosis' in df.columns:
    df = df.drop(columns=['total_dosis'])

if 'pct_cobertura' in df.columns:
    df['pct_cobertura'] = df['doses_aplicadas'] / df['programatica1_ano']
    df['pct_cobertura'] = df['pct_cobertura'].round(2)

df['doses_aplicadas'] = df['doses_aplicadas'].astype(int)

to_ignore = ['neumo_1ra_dosis_1',
             'neumo_12m_2da_dosis', 'neumo_24_m_dosis_unica', 'dpt_1er_ref.1', 'dpt_5an_2do_ref.1',
             'ha_u_dosis']

for index, row in df.iterrows():
    if row['vaccine_header'] in to_ignore:
        df = df.drop(index)

df.to_csv('fin_dim_vacunacion_detalle.csv', index=False)
