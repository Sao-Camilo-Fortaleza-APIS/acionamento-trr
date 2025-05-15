import os
from dash import Dash, html, dcc, Output, Input, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import database
from dash_iconify import DashIconify
from sql_p import sql, sql_r

app = Dash(__name__,  suppress_callback_exceptions=True, external_stylesheets=[dbc.icons.FONT_AWESOME,dbc.themes.BOOTSTRAP, 'assets/styles.css'], assets_folder='assets')
server = app.server

app.layout = html.Div(children=[
#---------------------------------CABEÇALHO-----------------------------------#
    html.Div([
        html.Img(src='/assets/logo_branca.png', className='logo'),
        html.H1('ACIONAMENTOS E REAVALIAÇÕES PENDENTES', className='titulo'),
        html.H2('TRR',id='nome-setor', className='subtitulo')
    ],className='cabecalho'),

#----------------------------------CONTAINER PARA AS DUAS TABELAS---------------------------#
    html.Div([
        #----------------------------------TABELA ACIONAMENTO---------------------------#
        html.Div([
            html.H3('ACIONAMENTO',style={'textAlign': 'center', 'marginBottom': '10px'} ,className='subtitulo-tabela'),
            dash_table.DataTable(
                id = 'table-data-p',
                page_size=7,
                fill_width=True,
                style_as_list_view=True,
                columns = [
                    {'name':'CÓDIGO','id':'IE_STATUS', 'presentation': 'markdown'},
                    {'name':'TEMPO DE ESPERA','id':'TEMPO_RESTANTE_FORMATADO'},
                    {'name':'NR. ACIONAMENTO','id':'NR_ACIONAMENTO'},
                    {'name':'DATA ACIONAMENTO','id':'DT_ACIONAMENTO'},
                    {'name':'QTD. PENDENTES','id':'QT_CHAMADOS_PENDENTES'},
                    {'name':'SETOR','id':'DS_SETOR'},
                    {'name':'ATENDIMENTO','id':'NR_ATENDIMENTO'},
                    {'name':'PACIENTE','id':'NM_PACIENTE'},
                    
                ],
                cell_selectable = False,
                style_table={
                'borderRadius': '10px',
                'overflowY': 'auto',
                'height': 'calc(50vh - 100px)',  # Altura dinâmica de metade da viewport menos espaço para título
                'border': '1px solid #ccc',
            },
            style_cell={
                'font-family': 'Trebuchet MS',
                'fontWeight': 'bold',
                'font_size': '18px',
                'text_align': 'center',
            },
            style_header={ #estilo do cabeçalho
                'font_family': 'Trebuchet MS',
                'font_size': '13px',
                'text_align': 'center',
                'fontWeight': 'bold',
                'backgroundColor': '#950707',
                'color': 'white'
                
            },
                            
                markdown_options={"html": True},
                css=[{'selector':'.show-hide', 'rule': 'display : none'}]
            )
        ],className='table-container',style={'width': '100%', 'height': '45vh', 'padding':'15px'}),

        #----------------------------------TABELA REAVALIAÇÃO---------------------------#
        html.Div([
            html.H3('REAVALIAÇÃO',style={'textAlign': 'center', 'marginBottom': '10px'} ,className='subtitulo-tabela'),
            dash_table.DataTable(
                id = 'table-data-r',
                page_size=7,
                fill_width=True,
                style_as_list_view=True,
                columns = [
                    {'name':'CÓDIGO','id':'IE_STATUS', 'presentation': 'markdown'},
                    {'name':'TEMPO DE ESPERA','id':'TEMPO_RESTANTE_FORMATADO'},
                    {'name':'NR. SOLICITAÇÃO','id':'NR_ACIONAMENTO'},
                    {'name':'DATA SOLICITAÇÃO','id':'DT_ACIONAMENTO'},
                    {'name':'QTD. PENDENTES','id':'QT_CHAMADOS_PENDENTES'},
                    {'name':'SETOR','id':'DS_SETOR'},
                    {'name':'ATENDIMENTO','id':'NR_ATENDIMENTO'},
                    {'name':'PACIENTE','id':'NM_PACIENTE'},
                    
                ],
                cell_selectable = False,
                style_table={
                'borderRadius': '10px',
                'overflowY': 'auto',
                'height': 'calc(50vh - 100px)',  # Altura dinâmica de metade da viewport menos espaço para título
                'border': '1px solid #ccc',
            },
            style_cell={
                'font-family': 'Trebuchet MS',
                'fontWeight': 'bold',
                'font_size': '18px',
                'text_align': 'center',
            },
            style_header={ #estilo do cabeçalho
                'font_family': 'Trebuchet MS',
                'font_size': '13px',
                'text_align': 'center',
                'fontWeight': 'bold',
                'backgroundColor': '#950707',
                'color': 'white'
                
            },
                            
                markdown_options={"html": True},
                css=[{'selector':'.show-hide', 'rule': 'display : none'}]
            )
        ],className='table-container',style={'width': '100%', 'height': '45vh', 'padding':'15px'}),
    ], style={'display': 'flex', 'flexDirection': 'column'}),

#-------------------------------------INTERVALO DE ATUALIZACAO----------------#
    dcc.Interval(
        id='interval-component',
        interval=5*1000,
        n_intervals=0
    )

])

# Callback para atualizar a tabela de dados planejados
@app.callback(
    Output('table-data-p','data'),
    Input('interval-component','n_intervals')
)
def update_table_p(n):
    df = database.execute_query(sql)
    df = pd.DataFrame(df)
    
    def condition(x):
        if x == 'Vermelho (Alto Risco)':
            src_icon = '<svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" viewBox="0 0 72 72"><circle cx="36" cy="36" r="28" fill="#d22f27"/><circle cx="36" cy="36" r="28" fill="none" stroke="#000" stroke-linejoin="round" stroke-width="2"/></svg>'
        elif x == 'Amarelo (Médio Risco)':
            src_icon = '<svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" viewBox="0 0 72 72"><circle cx="36" cy="36" r="28" fill="#f3e22b"/><circle cx="36" cy="36" r="28" fill="none" stroke="#000" stroke-linejoin="round" stroke-width="2"/></svg>'
        elif x == 'Verde (Baixo Risco)':
            src_icon = '<svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" viewBox="0 0 72 72"><circle cx="36" cy="36" r="28" fill="#2bf342"/><circle cx="36" cy="36" r="28" fill="none" stroke="#000" stroke-linejoin="round" stroke-width="2"/></svg>'
        elif x == 'Azul (Baixo Risco)':
            src_icon = '<svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" viewBox="0 0 72 72"><circle cx="36" cy="36" r="28" fill="#3227d3"/><circle cx="36" cy="36" r="28" fill="none" stroke="#000" stroke-linejoin="round" stroke-width="2"/></svg>'
        elif x == 'Branco (Sem risco)':
            src_icon = '<svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" viewBox="0 0 72 72"><circle cx="36" cy="36" r="28" fill="#FFFFFF"/><circle cx="36" cy="36" r="28" fill="none" stroke="#000" stroke-linejoin="round" stroke-width="2"/></svg>'
        elif x == 'Laranja (Admissão)':
            src_icon = '<svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" viewBox="0 0 72 72"><circle cx="36" cy="36" r="28" fill="#ffa200"/><circle cx="36" cy="36" r="28" fill="none" stroke="#000" stroke-linejoin="round" stroke-width="2"/></svg>'
        return src_icon

    df['IE_STATUS'] = df['IE_STATUS'].apply(condition)
    return df.to_dict('records')

# Callback para atualizar a tabela de dados realizados
@app.callback(
    Output('table-data-r','data'),
    Input('interval-component','n_intervals')
)
def update_table_r(n):
    df = database.execute_query(sql_r)
    df = pd.DataFrame(df)
    
    def condition(x):
        if x == 'Vermelho (Alto Risco)':
            src_icon = '<svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" viewBox="0 0 72 72"><circle cx="36" cy="36" r="28" fill="#d22f27"/><circle cx="36" cy="36" r="28" fill="none" stroke="#000" stroke-linejoin="round" stroke-width="2"/></svg>'
        elif x == 'Amarelo (Médio Risco)':
            src_icon = '<svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" viewBox="0 0 72 72"><circle cx="36" cy="36" r="28" fill="#f3e22b"/><circle cx="36" cy="36" r="28" fill="none" stroke="#000" stroke-linejoin="round" stroke-width="2"/></svg>'
        elif x == 'Verde (Baixo Risco)':
            src_icon = '<svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" viewBox="0 0 72 72"><circle cx="36" cy="36" r="28" fill="#2bf342"/><circle cx="36" cy="36" r="28" fill="none" stroke="#000" stroke-linejoin="round" stroke-width="2"/></svg>'
        elif x == 'Azul (Baixo Risco)':
            src_icon = '<svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" viewBox="0 0 72 72"><circle cx="36" cy="36" r="28" fill="#3227d3"/><circle cx="36" cy="36" r="28" fill="none" stroke="#000" stroke-linejoin="round" stroke-width="2"/></svg>'
        elif x == 'Branco (Sem risco)':
            src_icon = '<svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" viewBox="0 0 72 72"><circle cx="36" cy="36" r="28" fill="#FFFFFF"/><circle cx="36" cy="36" r="28" fill="none" stroke="#000" stroke-linejoin="round" stroke-width="2"/></svg>'
        elif x == 'Laranja (Admissão)':
            src_icon = '<svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" viewBox="0 0 72 72"><circle cx="36" cy="36" r="28" fill="#ffa200"/><circle cx="36" cy="36" r="28" fill="none" stroke="#000" stroke-linejoin="round" stroke-width="2"/></svg>'
        return src_icon

    df['IE_STATUS'] = df['IE_STATUS'].apply(condition)
    return df.to_dict('records')

##FLASK_SERVER_PORT= os.environ.get('FLASK_SERVER_PORT') 
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8051,debug=True, dev_tools_ui=False)