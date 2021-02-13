import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

pd.options.mode.chained_assignment = None
sns.set_style('white')


def plot_performed_vs_unperformed(performed: int, unperformed: int) -> None:
    ''' Plota dois gráficos lado a lado para comprar viagens realizadas e não realizadas.
        Um gráfico é um gráfico de barras, com os valores totais; e o outro gráfico é um 
        gráfico de anel com os percentuais. 
        
        Args:
            performed: Inteiro. Quantidade de viagens realizadas/cumpridas.
            unperformed: Inteiro. Quantidade de viagens não realizadas/não cumpridas. 
        Return:
            None. Apenas mostra o gráfico.
    '''

    plt.figure(figsize=(12,6))

    plt.subplot(1, 2, 1)
    plt.bar(x=['Viagens realizadas', 'Viagens não realizadas'], height=[performed, unperformed], color='lightseagreen')
    xlocs, _ = plt.xticks()
    for i, value in enumerate([performed, unperformed]):
        plt.text(x=xlocs[i], y=value-400, s=value, horizontalalignment='center', 
                 verticalalignment='top', fontsize=16, color='snow', fontweight='bold')
    plt.yticks([0, 10000, 20000])
    plt.xticks(fontsize=12)
    plt.box(False)
    
    plt.subplot(1, 2, 2)
    plt.pie(labels=['Viagens realizadas', 'Viagens não realizadas'], x=[performed, unperformed], 
            autopct='%1.2f%%', wedgeprops=dict(width=0.22), colors=['lightseagreen', 'lightcoral'])
    plt.box(False)

    plt.suptitle("Comparativo de viagens realizadas e não realizadas", fontsize=16)

    plt.show()
    return None


def plot_performed_vs_unperformed_by_direction(df: pd.DataFrame, barmode="group") -> None:
    '''Mostra um gráfico de barras interativo comparando as viagens realizadas e não realizadas,
    mas mostrando separado por viagens de 'Ida' e 'Volta'.
    Args:
        df: DataFrame do pandas a ser usada. 
        barmode: str. Referente ao modo como as barras serão apresentadas. Pode ser "group" (agrupado) ou "stack" (empilhado).
    Return:
        None. Apenas plota o gráfico.
    '''
    fig = px.histogram(data_frame=df, x='viagem_realizada', color='sentido_viagem', 
                       barmode=barmode,  template='plotly_white', 
                       color_discrete_sequence=['#4C78A8', '#00CC96'],
                       )
    fig.update_layout(
            legend=dict(
                title='Sentido da viagem',
            ),
            yaxis_title='Quantidade de viagens',
            yaxis_showticklabels=True,
            xaxis_title=''
        )
    
    fig.update_traces(hovertemplate='%{y} viagens')

    fig.show()
    return

def plot_performed_vs_unperformed_by_company(df: pd.DataFrame, barmode="group") -> None:
    '''Mostra um gráfico de barras interativo comparando as viagens realizadas e 
    não realizadas por empresa.
    Args:
        df: DataFrame do pandas a ser usada. 
        barmode: str. Referente ao modo como as barras serão apresentadas. Pode ser "group" (agrupado) ou "stack" (empilhado).
    Return:
        None. Apenas plota o gráfico.
    '''
    if not (barmode == "stack" or barmode == "group"):
        raise AssertionError("Modo de apresentação precisa ser 'stack' ou 'group'")
    
    fig = px.histogram(data_frame=df, 
             x='apelido_empresa', 
             color='viagem_realizada', 
             barmode=barmode,
             title='Viagens realizadas e não realizadas por empresa',
             labels={
                 'count': 'Quantidade de viagens',
                 'apelido_empresa': 'Empresa',
                 'viagem_realizada': 'Viagem'
             },
             template='plotly_white',
             )
    fig.update_layout(
        legend=dict(
            title='',
        ),
        yaxis_title='Quantidade de viagens',
        yaxis_showticklabels=True,
    )

    fig.update_traces(hovertemplate='%{x}<br>%{y} viagens')
    fig.show()

    return None


def plot_unperformed_frequency(df: pd. DataFrame, by="hour", kind="line"):
    ''' Plota um gráfico interativo para apresentar frequência de viagens não realizadas. 
        Pode ser por hora do dia ou por dia da semana e pode ser gráfico de linha ou de barra.
        Args:
            df: DataFrame do pandas usado como base.
            by: Pode ser "hour" (hora do dia) ou "weekday" (dia da semana)
            kind: Pode ser "line" (gráfico de linha) ou "bar" (gráfico de barra)
        Return:
            None. Apenas plota o gráfico.
    '''
    if by == "hour":
        x = 'Hora prevista'
        title = 'Média de viagens não realizadas por hora do dia'
    elif by == "weekday":
        x = 'Dia da semana'
        title = 'Média de viagens não realizadas por dia da semana'
    else:
        raise AssertionError("Modo do parâmetro 'by' admite apenas 'hour' ou 'weekday'")
    if kind == 'line':
        fig = px.line(data_frame=df, x=x, y='Viagens não realizadas', 
                  text='Viagens não realizadas', title=title, template='plotly_white')
        fig.update_traces(textposition='top center')
    elif kind == 'bar':
        fig = px.bar(data_frame=df, x=x, y='Viagens não realizadas', 
                  text='Viagens não realizadas', title=title, template='plotly_white')
    else:
        raise AssertionError("Modo do parâmetro 'kind' admite apenas 'line' ou 'bar'")

    fig.show()
    return None


def plot_top_unperformed(df: pd.DataFrame) -> None:
    ''' Plota um gráfico interativo com as linhas com mais viagens não realizadas,
        com indicação de empresa responsável também.
        Args:
            df: DataFrame do Pandas a ser usada. 
        Return:
            None. Apenas plota o gráfico.
    '''
    fig = px.bar(data_frame=df, y='nome_linha', x='viagens não realizadas', orientation='h', color='apelido_empresa',
                color_discrete_sequence=['#00CC96', '#636EFA', '#FECB52'], title="Linhas com mais viagens não realizadas", 
                 template='plotly_white', text='viagens não realizadas'
                )
    fig.update_layout(
                    legend=dict(
                        title='Empresa responsável'
                    ),
                    yaxis_categoryorder='total ascending',
                    yaxis_title='',
                    xaxis_title='Quantidade de viagens não realizadas',
                    )
    fig.update_traces(textposition='outside')
    fig.update_traces(hovertemplate='%{y}<br>%{x} viagens não realizadas')

    fig.show()
    return None

def plot_mean_delay(df: pd.DataFrame) -> None:
    ''' Plota um gráfico estático com o atraso médio por empresa, com uma linha mostrando
        o atraso médio geral (entre todas as empresas).
        Args:
            df: DataFrame do pandas com os dados a serem plotados. 
        Return:
            None. Apenas mostra o gráfico. 
    '''
    mean_delay = df.groupby(['apelido_empresa'])[['tempo_de_atraso', 'apelido_empresa']].mean().reset_index().sort_values(by='tempo_de_atraso')

    plt.figure(figsize=(14,8))
    ax = sns.barplot(data=mean_delay, x='apelido_empresa', y='tempo_de_atraso', ci=None, color='mediumturquoise')
    xlocs, _ = plt.xticks()
    for i, value in enumerate(mean_delay['tempo_de_atraso']):
        plt.text(x=xlocs[i], y=value-0.08, s=f'{value:.2f} min', horizontalalignment='center', 
                verticalalignment='top', fontsize=16, color='snow', fontweight='bold')
    plt.xticks(fontsize=12)
    ax.set_xlabel(''), ax.set_ylabel('')
    plt.title("Média de atraso por empresa (minutos)", fontdict={'size': 16, 'color': '#444'})
    mean = mean_delay['tempo_de_atraso'].mean()
    ax.plot([-0.55, 3.55], [mean]*2, label=f"Média geral: {mean:.2f} min", linestyle='--', color="firebrick", linewidth=2)
    legend = ax.legend(loc='upper left', fontsize=12)
    #legend.get_texts()[0].set_color("firebrick")
    sns.despine(bottom=True, left=True)

    plt.show()
    return None


def plot_mean_delay_by_direction(df: pd.DataFrame) -> None:
    ''' Plota um gráfico interativo para visualizar o atraso médio, por empresa, e
        por sentido da viagem (ida ou volta).
        Args:
            df: DataFrame do pandas com os dados a serem visualizados.
        Return:
            None. Apenas mostra o gráfico.
    '''
    mean_delay = df.groupby(['apelido_empresa', 'sentido_viagem'])[['tempo_de_atraso', 'apelido_empresa', 'sentido_viagem']].mean().reset_index().sort_values(by='tempo_de_atraso')
    mean_delay['tempo_de_atraso'] = mean_delay['tempo_de_atraso'].round(2)
    fig = px.bar(mean_delay, x='sentido_viagem', y='tempo_de_atraso', color='apelido_empresa', template='plotly_white', 
                barmode='group', text='tempo_de_atraso', color_discrete_sequence=['#FECB52', '#EF553B', '#00CC96', '#636EFA'])
    fig.update_layout(
        legend=dict(
            title='Empresa responsável'
        ),
        yaxis_title='Atraso médio (em minutos)',
        xaxis_title='Sentido da viagem',
    )
    fig.update_traces(textposition='outside')
    fig.show()
    return None

def plot_boxplot_delay(df: pd.DataFrame):
    '''Plota um boxplot interativo com informações sobre os atrasos por empresa.
        Args:
            df: DataFrame do Pandas com informações a serem visualizadas. 
        Return
            None. Apenas mostra o gráfico
    '''
    fig = px.box(data_frame=df, y='tempo_de_atraso', color='apelido_empresa', template='plotly_white',
                color_discrete_sequence=['#EF553B', '#00CC96', '#636EFA', '#FECB52'], title="Boxplot tempo de atraso por empresa")
    fig.update_layout(
                    legend=dict(
                        title='Empresa responsável'),
                    yaxis_title='Atraso (em minutos)',
                    )
    fig.show()
    return None

def plot_delay_info(df: pd.DataFrame) -> None:
    ''' Plota um gráfico interativo com percentual de viagens atrasadas, adiantadas e pontuais
    por empresa. 
        Args:
            df: DataFrame do Pandas com informações a serem visualizadas. 
        Return:
            None. Apenas plota o gráfico.
    '''   
    fig = px.bar(data_frame=df, x='Empresa', y='Percentual', color='Status', barmode='group', text='Percentual',
                color_discrete_sequence=['#636EFA', '#D62728', '#1C8356'], template='plotly_white', 
                title='Percentual de viagens atrasadas, adiantadas e pontuais')
    fig.update_layout(
                    legend=dict(
                        title=''),
                    yaxis_title='Percentual de ocorrência (em %)',
                    )
    fig.show()
    return None


def plot_top_delayed(df: pd.DataFrame) -> None:
    ''' Plota um gráfico interativo com as linhas com maior percentual de atraso,
        com indicação de empresa responsável também.
        Args:
            df: DataFrame do Pandas a ser usada. 
        Return:
            None. Apenas plota o gráfico.
    '''
    fig = px.bar(data_frame=df, y='nome_linha', x='Percentual de viagens com atraso', orientation='h', color='apelido_empresa',
                color_discrete_sequence=['#FECB52', '#636EFA', '#00CC96', '#EF553B'], 
                 title="10 linhas com maior percentual de viagens atrasadas", template='plotly_white',
                 text='Percentual de viagens com atraso'
                )
    fig.update_layout(
                    legend=dict(
                        title='Empresa responsável'
                    ),
                    yaxis_categoryorder='total ascending',
                    yaxis_title='',
                    xaxis_title='Percentual de viagens atrasadas na linha',
                    )
    fig.update_traces(textposition='outside')
    fig.update_traces(hovertemplate='%{y}<br>%{x}% de ocorrência de atraso')
    
    fig.show()
    
    return None