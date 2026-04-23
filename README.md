O script realiza um fluxo de ETL (Extract, Transform, Load) para converter dados brutos em informações estruturadas:

* Extract (Extração): Leitura dos arquivos brutos do SINAN e tabelas de apoio (IBGE/CBO).
* Transform (Transformação):
   * Limpeza: Remoção de colunas irrelevantes e tratamento de valores ausentes.
   * Padronização: Correção da variável de idade (conforme normas do SINAN) e tradução de códigos numéricos (IBGE, CBO e UF) para descrições textuais.
   * Mapeamento: Conversão de variáveis categóricas (Raça, Sexo, Zona de Residência) para facilitar a leitura.

* Load (Carga): Exportação do arquivo dados_processados_final.csv, estruturado e pronto para análises estatísticas e visualizações.
