import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ==========================================
# 1. CARGA DE DATOS Y PREPARACIÓN
# ==========================================
print("Cargando bases de datos... (esto puede tardar unos segundos)")

# Nombres exactos de los archivos
df_mortalidad = pd.read_excel('Anexo1.NoFetal2019_CE_15-03-23.xlsx')
df_divipola = pd.read_excel('Divipola_CE_.xlsx')
# Saltamos las primeras 8 filas donde están los logos y metadata del ministerio
df_causas = pd.read_excel('Anexo2.CodigosDeMuerte_CE_15-03-23.xlsx', skiprows=8)

# Convertimos los códigos a texto (string) para que el cruce no falle por formatos numéricos
df_mortalidad['COD_DEPARTAMENTO'] = df_mortalidad['COD_DEPARTAMENTO'].astype(str)
df_mortalidad['COD_MUNICIPIO'] = df_mortalidad['COD_MUNICIPIO'].astype(str)
df_mortalidad['COD_MUERTE'] = df_mortalidad['COD_MUERTE'].astype(str).str.strip()

df_divipola['COD_DEPARTAMENTO'] = df_divipola['COD_DEPARTAMENTO'].astype(str)
df_divipola['COD_MUNICIPIO'] = df_divipola['COD_MUNICIPIO'].astype(str)

df_causas['Código de la CIE-10 cuatro caracteres'] = df_causas['Código de la CIE-10 cuatro caracteres'].astype(str).str.strip()

# 1.1 Cruce con Divipola (Nombres de departamento y municipio)
df_completo = pd.merge(
    df_mortalidad, 
    df_divipola, 
    on=['COD_DEPARTAMENTO', 'COD_MUNICIPIO'], # Cruzamos por las dos columnas coincidentes
    how='left'
)

# 1.2 Cruce con Causas de Muerte
df_completo = pd.merge(
    df_completo, 
    df_causas, 
    left_on='COD_MUERTE', 
    right_on='Código de la CIE-10 cuatro caracteres', 
    how='left'
)

# 1.3 Función para la variable del Ciclo de Vida
def categorizar_edad(codigo):
    if pd.isna(codigo): return 'Sin información'
    try:
        codigo = int(codigo)
    except:
        return 'Sin clasificar'
    
    if codigo in [0, 1, 2, 3, 4]: return 'Mortalidad neonatal'
    elif codigo in [5, 6]: return 'Mortalidad infantil'
    elif codigo in [7, 8]: return 'Primera infancia'
    elif codigo in [9, 10]: return 'Niñez'
    elif codigo == 11: return 'Adolescencia'
    elif codigo in [12, 13]: return 'Juventud'
    elif codigo in [14, 15, 16]: return 'Adultez temprana'
    elif codigo in [17, 18, 19]: return 'Adultez intermedia'
    elif codigo in [20, 21, 22, 23, 24]: return 'Vejez'
    elif codigo in [25, 26, 27, 28]: return 'Longevidad / Centenarios'
    elif codigo == 29: return 'Edad desconocida'
    else: return 'Sin clasificar'

df_completo['CICLO_DE_VIDA'] = df_completo['GRUPO_EDAD1'].apply(categorizar_edad)

# 1.4 Convertir Sexo de DANE (1, 2, 3) a texto legible
df_completo['SEXO_NOMBRE'] = df_completo['SEXO'].replace({1: 'Hombre', 2: 'Mujer', 3: 'Indeterminado'})

# Rellenar valores nulos de las descripciones para no romper los gráficos
col_causa_nombre = 'Descripcion  de códigos mortalidad a cuatro caracteres'
df_completo[col_causa_nombre] = df_completo[col_causa_nombre].fillna('No especificada')
df_completo['MUNICIPIO'] = df_completo['MUNICIPIO'].fillna('Desconocido')
df_completo['DEPARTAMENTO'] = df_completo['DEPARTAMENTO'].fillna('Desconocido')

print("Datos procesados con éxito. Generando gráficas...")

# ==========================================
# 2. PROCESAMIENTO DE DATAFRAMES Y GRÁFICAS (PLOTLY)
# ==========================================

# G1. Treemap (Alternativa de Mapa por Departamento)
df_mapa = df_completo.groupby('DEPARTAMENTO').size().reset_index(name='Total_Muertes')
fig_mapa = px.treemap(df_mapa, path=['DEPARTAMENTO'], values='Total_Muertes', 
                      title='Proporción de Muertes por Departamento (Alternativa a Mapa Geoespacial)',
                      color='Total_Muertes', color_continuous_scale='Reds')

# G2. Líneas: Variación por mes
df_mes = df_completo.groupby('MES').size().reset_index(name='Total')
fig_lineas = px.line(df_mes, x='MES', y='Total', markers=True, title='Variación de Muertes Totales por Mes')
fig_lineas.update_xaxes(tickmode='linear', tick0=1, dtick=1) # Fuerza a mostrar los 12 meses

# G3. Barras: Top 5 ciudades más violentas (Homicidios por arma de fuego - X95)
df_homicidios = df_completo[df_completo['COD_MUERTE'].str.contains('X95', na=False)]
top_5_violentas = df_homicidios.groupby('MUNICIPIO').size().reset_index(name='Homicidios').nlargest(5, 'Homicidios')
fig_barras = px.bar(top_5_violentas, x='MUNICIPIO', y='Homicidios', 
                    title='Top 5 Ciudades Más Violentas (Homicidios por Arma de Fuego X95)', 
                    color='Homicidios', color_continuous_scale='Reds', text_auto=True)

# G4. Circular: Top 10 ciudades con menor índice de mortalidad
top_10_menor = df_completo.groupby('MUNICIPIO').size().reset_index(name='Total').nsmallest(10, 'Total')
fig_pie = px.pie(top_10_menor, names='MUNICIPIO', values='Total', 
                 title='Top 10 Ciudades con Menor Índice de Mortalidad')

# G5. Tabla: Top 10 causas de muerte
top_10_causas = df_completo.groupby(['COD_MUERTE', col_causa_nombre]).size().reset_index(name='Total').nlargest(10, 'Total')
fig_tabla = go.Figure(data=[go.Table(
    header=dict(values=['Código CIE-10', 'Causa de Muerte', 'Total Casos'], fill_color='paleturquoise', align='left'),
    cells=dict(values=[top_10_causas['COD_MUERTE'], top_10_causas[col_causa_nombre], top_10_causas['Total']], align='left'))
])
fig_tabla.update_layout(title='Top 10 Causas de Muerte Principales en Colombia')

# G6. Barras apiladas: Muertes por sexo en cada departamento
df_sexo_depto = df_completo.groupby(['DEPARTAMENTO', 'SEXO_NOMBRE']).size().reset_index(name='Total')
fig_apiladas = px.bar(df_sexo_depto, x='DEPARTAMENTO', y='Total', color='SEXO_NOMBRE', 
                      title='Comparativa de Muertes por Sexo en Cada Departamento', barmode='stack')
fig_apiladas.update_layout(xaxis_tickangle=-45)

# G7. Histograma: Distribución de muertes por rangos del ciclo de vida
fig_hist = px.histogram(df_completo, x='CICLO_DE_VIDA', title='Distribución de Muertes por Ciclo de Vida',
                        color='CICLO_DE_VIDA',
                        category_orders={"CICLO_DE_VIDA": ["Mortalidad neonatal", "Mortalidad infantil", 
                                                           "Primera infancia", "Niñez", "Adolescencia", 
                                                           "Juventud", "Adultez temprana", "Adultez intermedia", 
                                                           "Vejez", "Longevidad / Centenarios", "Edad desconocida"]})
fig_hist.update_layout(xaxis_tickangle=-45)


# ==========================================
# 3. CONSTRUCCIÓN DE LA APLICACIÓN DASH
# ==========================================
app = dash.Dash(__name__)
server = app.server # Necesario para publicar en la nube

app.layout = html.Div(style={'font-family': 'Arial, sans-serif', 'padding': '20px', 'backgroundColor': '#f9f9f9'}, children=[
    html.H1("Dashboard de Análisis de Mortalidad en Colombia (2019)", style={'textAlign': 'center', 'color': '#2c3e50'}),
    html.P("Actividad 4 - Aplicación Web Interactiva", style={'textAlign': 'center', 'fontSize': '18px', 'marginBottom': '30px'}),
    
    html.Hr(),

    html.Div([dcc.Graph(figure=fig_mapa)], style={'marginBottom': '30px', 'boxShadow': '0 4px 8px 0 rgba(0,0,0,0.1)'}),
    
    html.Div(style={'display': 'flex', 'flexWrap': 'wrap', 'gap': '2%'}, children=[
        html.Div([dcc.Graph(figure=fig_lineas)], style={'width': '49%', 'boxShadow': '0 4px 8px 0 rgba(0,0,0,0.1)'}),
        html.Div([dcc.Graph(figure=fig_barras)], style={'width': '49%', 'boxShadow': '0 4px 8px 0 rgba(0,0,0,0.1)'}),
    ]),

    html.Div(style={'display': 'flex', 'flexWrap': 'wrap', 'gap': '2%', 'marginTop': '30px'}, children=[
        html.Div([dcc.Graph(figure=fig_pie)], style={'width': '49%', 'boxShadow': '0 4px 8px 0 rgba(0,0,0,0.1)'}),
        html.Div([dcc.Graph(figure=fig_tabla)], style={'width': '49%', 'boxShadow': '0 4px 8px 0 rgba(0,0,0,0.1)'}),
    ]),

    html.Div([dcc.Graph(figure=fig_apiladas)], style={'marginTop': '30px', 'boxShadow': '0 4px 8px 0 rgba(0,0,0,0.1)'}),
    html.Div([dcc.Graph(figure=fig_hist)], style={'marginTop': '30px', 'boxShadow': '0 4px 8px 0 rgba(0,0,0,0.1)'})
])

# ==========================================
# 4. EJECUCIÓN DEL SERVIDOR
# ==========================================
if __name__ == '__main__':
    print("Iniciando servidor Dash... Visita http://127.0.0.1:8050/ en tu navegador")
    app.run(debug=True)
