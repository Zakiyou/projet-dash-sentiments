import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

# Chargement des données
df = pd.read_csv('Commentsentiment.csv')

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Fonction pour calculer les statistiques
def calculate_statistics(df):
    total_comments = len(df)
    comments_by_bank = df['Name'].value_counts().to_dict()
    comments_by_year = df.groupby('Year').size().to_dict()
    
    if 'sentiment' in df.columns:
        sentiment_by_bank = df.groupby(['Name', 'sentiment']).size().unstack(fill_value=0).to_dict('index')
    else:
        sentiment_by_bank = {}
    
    return {
        'total_comments': total_comments,
        'comments_by_bank': comments_by_bank,
        'comments_by_year': comments_by_year,
        'sentiment_by_bank': sentiment_by_bank
    }

stats = calculate_statistics(df)

# Fonction pour créer les cartes
def create_card(content, color):
    return dbc.Col(
        html.Div(content, className=f"p-3 {color} text-white rounded text-center mb-2", style={"height": "100px", "width": "300px"}),
    )

def create_cards(stats):
    cards = [
        create_card(f"Total de Commentaires: {stats['total_comments']}", "bg-primary"),
    ]
    for bank, count in stats['comments_by_bank'].items():
        card = create_card(f"Total de Commentaires pour {bank}: {count}", "bg-secondary")
        cards.append(card)
    return cards

all_cards = create_cards(stats)

# Fonction pour diviser les cartes en pages
def get_cards_for_page(page_number, cards_per_page=16):
    start = page_number * cards_per_page
    end = start + cards_per_page
    return all_cards[start:end]

# Layout de l'application avec des onglets
app.layout = dbc.Container([
    dcc.Tabs([
        dcc.Tab(label='Accueil', children=[
            html.H1("", className="text-center mt-4"),
            html.Div(id='card-container'),
            dbc.Row([
                dbc.Col(html.Button('Précédent', id='prev-button', n_clicks=0), width=1),
                dbc.Col(html.Button('Suivant', id='next-button', n_clicks=0), width=1),
            ], className="mt-4 text-center"),
        ]),

        dcc.Tab(label='Commentaires', children=[
            html.H2(""),
            html.Div([
                html.Label("Choisir une Banque:"),
                dcc.Dropdown(
                    id='bank-dropdown',
                    options=[{'label': 'Tout', 'value': 'Tout'}] + [{'label': bank, 'value': bank} for bank in df['Name'].unique()],
                    value='Tout'
                )
            ], className="mt-4"),
            dcc.Graph(id='comments-by-bank-year', style={'height': '500px'}),
        ]),

        dcc.Tab(label='Sentiments', children=[
            html.H2(""),
            html.Div([
                html.Label("Choisir une Banque:"),
                dcc.Dropdown(
                    id='sentiment-bank-dropdown',
                    options=[{'label': 'Tout', 'value': 'Tout'}] + [{'label': bank, 'value': bank} for bank in df['Name'].unique()],
                    value='Tout'
                )
            ], className="mt-4"),
            dcc.Graph(id='sentiment-by-bank', style={'height': '500px'}),
        ]),
    ])
], fluid=True)

# Callback pour mettre à jour les cartes et gérer la pagination
@app.callback(
    Output('card-container', 'children'),
    [Input('prev-button', 'n_clicks'),
     Input('next-button', 'n_clicks')]
)
def update_cards(prev_clicks, next_clicks):
    ctx = dash.callback_context
    if not ctx.triggered:
        button_id = 'next-button'
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    page_number = getattr(update_cards, 'page_number', 0)

    if button_id == 'next-button':
        page_number += 1
    elif button_id == 'prev-button':
        page_number -= 1

    page_number = max(0, min(page_number, (len(all_cards) - 1) // 16))
    update_cards.page_number = page_number

    cards_for_page = get_cards_for_page(page_number)
    return dbc.Row(cards_for_page)

# Callback pour mettre à jour le graphique des commentaires par année
@app.callback(
    Output('comments-by-bank-year', 'figure'),
    [Input('bank-dropdown', 'value')]
)
def update_comments_by_bank_year(selected_bank):
    try:
        if selected_bank == 'Tout':
            comments_by_year = df.groupby('Year').size().reset_index(name='Nombre de Commentaires')
        else:
            filtered_df = df[df['Name'] == selected_bank]
            comments_by_year = filtered_df.groupby('Year').size().reset_index(name='Nombre de Commentaires')
        
        fig = px.bar(
            comments_by_year,
            x='Year',
            y='Nombre de Commentaires',
            title=f'Nombre de Commentaires par Année pour {selected_bank}',
            color='Year',
            color_discrete_sequence=px.colors.qualitative.Plotly
        )
        fig.update_layout(xaxis_title='Année', yaxis_title='Nombre de Commentaires', legend_title='Année')
        fig.update_traces(
            texttemplate='%{y}', 
            textposition='outside'
        )
        return fig
    except Exception as e:
        print(f"Error in update_comments_by_bank_year: {e}")
        return px.bar()

# Callback pour mettre à jour le graphique des sentiments par insurance
@app.callback(
    Output('sentiment-by-bank', 'figure'),
    [Input('sentiment-bank-dropdown', 'value')]
)
def update_sentiment_by_bank(selected_bank):
    try:
        if selected_bank == 'Tout':
            sentiment_counts = df['sentiment'].value_counts().reset_index()
        else:
            filtered_df = df[df['Name'] == selected_bank]
            if 'sentiment' in filtered_df.columns:
                sentiment_counts = filtered_df['sentiment'].value_counts().reset_index()
            else:
                sentiment_counts = pd.DataFrame(columns=['sentiment', 'count'])
        
        sentiment_counts.columns = ['Sentiment', 'Nombre de Commentaires']

        unique_sentiments = sentiment_counts['Sentiment'].unique()
        colors = px.colors.qualitative.Plotly[:len(unique_sentiments)]
        color_discrete_map = {sentiment: color for sentiment, color in zip(unique_sentiments, colors)}

        fig = px.bar(
            sentiment_counts,
            x='Sentiment',
            y='Nombre de Commentaires',
            title=f'Distribution des Sentiments pour {selected_bank}',
            color='Sentiment',
            color_discrete_map=color_discrete_map
        )
        fig.update_layout(xaxis_title='Sentiment', yaxis_title='Nombre de Commentaires', legend_title='Sentiment')
        fig.update_traces(
            texttemplate='%{y}', 
            textposition='outside'
        )
        return fig
    except Exception as e:
        print(f"Error in update_sentiment_by_bank: {e}")
        return px.bar()  

if __name__ == '__main__':
    app.run_server(debug=True)
