
import pandas as pd

# 1. Configurações e Carga
pd.options.display.max_columns = None
dados = pd.read_csv('/content/ANIMBR20.csv', encoding='latin1')

# Usamos o rename para tornar os nomes legíveis.
# Caso alguma chave não exista no CSV, o Pandas simplesmente ignora (resiliência).
dicionario_renomear = {
'NU_IDADE_N': 'idade_original',
'ID_MUNICIP': 'id_municipio_notif',
'ID_MN_RESI': 'id_municipio_resid',
'ID_OCUPA_N': 'id_ocupacao',
'SG_UF_NOT': 'uf_notificacao',
'CS_SEXO': 'sexo',
'CS_RACA': 'raca',
'ID_ZONA_RE': 'zona_residencia'
}
dados = dados.rename(columns=dicionario_renomear)


# 2. Seleção de Colunas e Limpeza
colunas_para_remover = ['TP_NOT', 'ID_AGRAVO']
dados_limpos = dados.drop(columns=colunas_para_remover).reset_index(drop=True)



# 3. Tratamento da Idade (Vetorizado)
# Agora usando o nome renomeado 'idade_original'
dados_limpos['IDADE_REAL'] = (dados_limpos['idade_original'] - 4000).clip(lower=0)


# 4. Tratamento de Municípios, Ocupação e UF
municipios_df = pd.read_csv('/content/populacao ibge 6 municipio br.csv')
dic_municipios = municipios_df.set_index('IBGE6')['Municipio'].to_dict()
dados_limpos['MUNICIPIO_NOTIF_NOME'] = dados_limpos['id_municipio_notif'].map(dic_municipios)
dados_limpos['MUNICIPIO_RESID_NOME'] = dados_limpos['id_municipio_resid'].map(dic_municipios)

ocupacao_df = pd.read_csv('/content/CBO2002 - Ocupacao.csv')
dic_ocupacao = ocupacao_df.set_index('CODIGO')['TITULO'].to_dict()
dados_limpos['OCUPACAO_NOME'] = dados_limpos['id_ocupacao'].map(dic_ocupacao)

uf_df = pd.read_csv('/content/cod_uf.csv')
dic_uf = uf_df.set_index('Código UF')['UF'].to_dict()
dados_limpos['UF_NOT_NOME'] = dados_limpos['uf_notificacao'].map(dic_uf)

# 5. Dicionários de Tradução
dic_raca = {1: 'Branca', 2: 'Preta', 3: 'Amarela', 4: 'Parda', 5: 'Indígena', 9: 'Ignorado'}
dic_zona = {1: 'Urbana', 2: 'Rural', 3: 'Periurbana', 9: 'Ignorado'}
dic_sexo = {'M': 'Masculino', 'F': 'Feminino', 'I': 'Ignorado'}

# 6. Mapeamento
traducoes = {
'sexo': dic_sexo,
'raca': dic_raca,
'zona_residencia': dic_zona
}

for coluna, dicionario in traducoes.items():
    if coluna in dados_limpos.columns:
        if coluna == 'sexo':
           dados_limpos[coluna] = dados_limpos[coluna].astype(str).replace(dicionario)
        else:
           dados_limpos[coluna] = pd.to_numeric(dados_limpos[coluna], errors='coerce').replace(dicionario)

# Preencher valores NaN
colunas_preencher = ['MUNICIPIO_NOTIF_NOME', 'MUNICIPIO_RESID_NOME', 'sexo', 'raca', 'zona_residencia']
for col in colunas_preencher:
    if col in dados_limpos.columns:
        dados_limpos[col] = dados_limpos[col].fillna('Não Informado')

# 7. Cálculo de Métrica
media_idade = dados_limpos['IDADE_REAL'].mean()

# 8. Exibição
print(f"Média de Idade Processada: {media_idade:.2f} anos")
print(dados_limpos[['MUNICIPIO_NOTIF_NOME', 'sexo', 'raca', 'IDADE_REAL']].head(10))

# 9. Exportação otimizada
dados_limpos.to_csv('dados_processados_final.csv', index=False, sep=';', encoding='utf-8-sig')
