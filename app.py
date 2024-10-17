import os
from dash import Dash, html, dcc, Output, Input, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import database
from dash_iconify import DashIconify
import sql_p

app = Dash(__name__,  suppress_callback_exceptions=True, external_stylesheets=[dbc.icons.FONT_AWESOME,dbc.themes.BOOTSTRAP, 'assets/styles.css'], assets_folder='assets')
server = app.server

app.layout = html.Div(children=[
#---------------------------------CABEÇALHO-----------------------------------#
    html.Div([
        html.Img(src='/assets/logo_branca.png', className='logo'),
        html.H1('CONTROLE DE ACIONAMENTOS PENDENTES', className='titulo'),
        html.H2('TRR',id='nome-setor', className='subtitulo')
    ],className='cabecalho'),

#----------------------------------TABELA-------------------------------------#
    html.Div([
        dash_table.DataTable(
            id = 'table-data',
            page_size=14,
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
            #'border': '1px solid',
            'borderRadius': '10px',
            'overflowY': 'auto'
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
    ],className='table',style={'width': '100%','padding':'15px'}),
    #html.Audio(id='audio-element', src='/assets/t-rex-roar.mp3', controls=False, autoPlay=False),
#-------------------------------------INTERVALO DE ATUALIZACAO----------------#
    dcc.Interval(
        id='interval-component',
        interval=5*1000,
        n_intervals=0
    )

])

@app.callback(
    Output('table-data','data'),
    #dash.dependencies.Output('audio-element','src'),
    Input('interval-component','n_intervals')
)

def update_table(n):
    df = database.get_data()
    print(df)
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
    src_audio='/assets/t-rex-roar.mp3'
    #print(df)
    return df.to_dict('records')#,src_audio

FLASK_SERVER_PORT= os.environ.get('FLASK_SERVER_PORT') 
if __name__ == '__main__':
    app.run_server(host='0.0.0.0',port=FLASK_SERVER_PORT,debug=True, dev_tools_ui=False)