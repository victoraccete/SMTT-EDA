import pandas as pd
pd.options.mode.chained_assignment = None

def load_data(url: str, dt_cols: list) -> pd.DataFrame:
    '''Importa o dataset do endereço especificado e converte as colunas para o tipo datetime.
       Args: 
            url: endereço (str) do .csv
            dt_cols: lista de colunas para serem convertidas para datetime
        Return:
            pandas DataFrame 
    '''
    df = pd.read_csv(url, index_col=0) # index_col=0 to ignore unnamed column
    for col in dt_cols:
        df[col] = pd.to_datetime(df[col])
    
    return df

def get_unperformed_frequency(df: pd.DataFrame, by="hour") -> pd.DataFrame:
    ''' Gera um DataFrame do Pandas contendo a frequência de viagens não realizadas
        por hora do dia ou por dia da semana. 
        Args:
            df: DataFrame do pandas que vai ser usado como base.
            by: Pode ser "hour" (hora do dia) ou "weekday" (dia da semana). 
        Return:
            Pandas DataFrame com informação de frequência de acordo com a separação indicada. 
    '''
    if by == "hour":
        frequency_df = df.groupby(df['hora_prevista'].dt.hour).count()
        frequency_df = frequency_df.iloc[:, :1].reset_index()
        frequency_df.columns = ['Hora prevista', 'Viagens não realizadas']
    elif by == "weekday":
        df['dia_da_semana'] = df['hora_prevista'].dt.weekday
        frequency_df = df.groupby(df['dia_da_semana']).count()
        frequency_df = frequency_df.iloc[:, :1].reset_index().replace(weekday_map)
        frequency_df.columns = ['Dia da semana', 'Viagens não realizadas']
    else:
        raise AssertionError("Modo do parâmetro 'by' admite apenas 'hour' ou 'weekday'")

    return frequency_df

def get_top_n_unperformed(df: pd.DataFrame, n: int) -> pd.DataFrame:
    ''' Gera um pandas DataFrame com as 'n' linhas que mais frequentemente não cumpriram suas viagens.
        Args: 
            df: DataFrame do pandas para ser usado como base. 
            n: Inteiro. Número de itens para serem mostrados. Ex: n=10 mostra apenas
            as 10 linhas que mais não cumpriram suas viagens.
        Return:
            DataFrame do pandas com: nome da linha, empresa e quantidade de viagens não realizadas. 
    '''
    top_unperformed = df.groupby(['nome_linha', 'apelido_empresa'], as_index=False)
    top_unperformed = top_unperformed.size().rename(columns={'size': 'viagens não realizadas'})
    top_unperformed = top_unperformed.sort_values(by=['viagens não realizadas']).iloc[-n:, :]
    return top_unperformed


def generate_delay_status_column(df: pd.DataFrame) -> pd.DataFrame:
    ''' Cria uma coluna no DataFrame para indicar com mais rapidez se a viagem foi 
        atrasada, adiantada ou pontual. 
        Args:
            df: DataFrame do pandas a ser usada como base.
        Return:
            O mesmo dataframe da entrada, mas com uma coluna extra de status de atraso. 
    '''
    df.loc[(df['hora_prevista'] < df['hora_realizada']), 'status_de_atraso'] = 'Atrasado'
    df.loc[(df['hora_prevista'] > df['hora_realizada']), 'status_de_atraso'] = 'Adiantado'
    df.loc[(df['hora_prevista'] == df['hora_realizada']), 'status_de_atraso'] = 'Pontual'

    return df

def calculate_delay(df: pd.DataFrame) -> pd.DataFrame:
    ''' Calcula o tempo de atraso de cada linha do DataFrame com uma coluna extra 
        contendo o valor em minutos desse atraso. Adiantamentos foram considerados como
        atrasos negativos. 
        Args:
            df: DataFrame do Pandas usado como base.
        Return:
            O mesmo DataFrame da entrada, mas com a coluna extra do tempo de atraso. 
    '''
    # *-1 since it's a negative delay (an advancement)
    df.loc[(df['status_de_atraso'] == 'Adiantado'), 'tempo_de_atraso'] = (df['hora_prevista'] - df['hora_realizada']).dt.seconds / 60 * -1
    df.loc[(df['status_de_atraso'] == 'Atrasado'), 'tempo_de_atraso'] = (df['hora_realizada'] - df['hora_prevista']).dt.seconds / 60
    df.loc[(df['status_de_atraso'] == 'Pontual'), 'tempo_de_atraso'] = 0

    return df

def fix_outliers_delays(df: pd.DataFrame):
    ''' Corrige os atrasos e adiantamentos extremamente discrepantes causados por horários
        próximos da meia noite. 
        Args: 
            df: DataFrame do pandas com coluna 'tempo_de_atraso' a ser corrigida. 
        Return:
            DataFrame do Pandas corrigida.
    '''
    df.loc[(df['tempo_de_atraso'] > 1000), 'status_de_atraso'] = 'Adiantado'
    df.loc[(df['tempo_de_atraso'] > 1000), 'tempo_de_atraso'] = df['tempo_de_atraso'] - 1400
    df.loc[(df['tempo_de_atraso'] < -1000), 'status_de_atraso'] = 'Adiantado'
    df.loc[(df['tempo_de_atraso'] < -1000), 'tempo_de_atraso'] = df['tempo_de_atraso'] + 1400
    return df

def get_delay_info(df: pd.DataFrame):
    ''' Gera um DataFrame do Pandas com informações sobre atraso. 
        Status do atraso: 'adiantado', 'atrasado', ou 'pontual'
        Frequência: frequência de ocorrência de cada status.
        Total: total de viagens
        Percentual: percentual de cada um dos status

        Args:
            df: DataFrame a ser usado como base.
        Return:
            DataFrame com informações de atraso por empresa e por situação de atraso.
    '''
    df = performed_travels.groupby(['apelido_empresa', 'status_de_atraso']).count().reset_index()
    df = df.iloc[:, :3]
    df.columns = ['Empresa', 'Status', 'Frequência']
    for index, company in enumerate(['Cidade de Maceió', 'Real Alagoas', 'São Francisco', 'Veleiro']):
        df.loc[(df['Empresa'] == company), 'Total'] = df.groupby(['Empresa']).sum().iloc[index, 0]
    df['Percentual'] = (100*df['Frequência']/df['Total']).round(2)
    return df


def get_delay_avg_info(df: pd.DataFrame, by="hour") -> pd.DataFrame:
    ''' Gera um dataframe com informações de atraso por hora do dia ou por dia da semana.
        Args:
            df: DataFrame com informações a serem visualizadas.
            by: pode ser "hour" (por hora do dia) ou "weekday" (por dia da semana)
    '''
    if by == "hour":
        delay_info = df.groupby(df['hora_realizada'].dt.hour).mean().reset_index()
        delay_info = delay_info.loc[:, ['hora_realizada', 'tempo_de_atraso']]
        delay_info.columns = ['Hora da viagem', 'Atraso médio']
        delay_info['Atraso médio'] = delay_info['Atraso médio'].round(2) 
    elif by == "weekday":
        df['dia_da_semana'] = df['hora_prevista'].dt.weekday
        delay_info = df.groupby(df['dia_da_semana']).mean()
        delay_info = delay_info.iloc[:, -1:].reset_index().replace(weekday_map)
        delay_info.columns = ['Dia da semana', 'Atraso médio']
        delay_info['Atraso médio'] = delay_info['Atraso médio'].round(2) 
    else:
        raise AssertionError("Modo do parâmetro 'by' admite apenas 'hour' ou 'weekday'")
    
    return delay_info


def get_top_n_delayed(df: pd.DataFrame, n:int) -> pd.DataFrame:
    ''' Gera um pandas DataFrame com as 'n' linhas que mais atrasaram.
        Args: 
            df: DataFrame do pandas para ser usado como base. 
            n: Inteiro. Número de itens para serem mostrados. Ex: n=10 mostra apenas
            as 10 linhas que mais atrasaram.
        Return:
            DataFrame do pandas com: nome da linha, empresa, frequência de atrasos,
            percentual de viagens com atraso da linha
    '''
    number_of_travels = df.groupby(['nome_linha', 'apelido_empresa'], as_index=False).size().sort_values(by=['size'])
    delayed_only = df[df['status_de_atraso'] == 'Atrasado']
    top_delayed = delayed_only.groupby(['nome_linha', 'apelido_empresa'], as_index=False).size()
    top_delayed = top_delayed.rename(columns={'size': 'Frequência de atrasos'})
    top_delayed['Percentual de viagens com atraso'] = (100*top_delayed['Frequência de atrasos']/number_of_travels['size']).round(1)
    top_delayed = top_delayed.sort_values(by=['Percentual de viagens com atraso']).iloc[-n:, :]
    
    return top_delayed