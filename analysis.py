import dash
from dash import dcc, html
import plotly.graph_objects as go
import pandas as pd

# Sample data (replace this later with your real dataset)
df = pd.DataFrame({
    'Year': list(range(2009, 2023)),
    'Revenue': [50000, 65000, 80000, 100000, 120000, 150000, 180000, 210000, 230000, 260000, 280000, 300000, 325000, 365000],
    'Profit': [8000, 10000, 12000, 15000, 18000, 20000, 22000, 25000, 27000, 30000, 33000, 35000, 37000, 40000],
    'Employees': [34000, 36000, 40000, 43000, 47000, 49000, 53000, 58000, 62000, 66000, 71000, 75000, 80000, 85000],
    'ROE': [25, 28, 30, 33, 35, 36, 38, 39, 40, 42, 43, 45, 46, 48]
})
df['Profit_Margin'] = (df['Profit'] / df['Revenue']) * 100

# Initialize the Dash app
app = dash.Dash(__name__)
app.title = "Apple Financial Executive Dashboard"

# Apple color scheme
colors = {
    'background': '#1d1d1f',
    'card_bg': '#2d2d2f',
    'text': '#ffffff',
    'primary': '#007AFF',
    'green': '#32D74B',
    'orange': '#FF9F0A',
    'purple': '#BF5AF2',
    'gray': '#8E8E93'
}

# KPI Cards function
def kpi_card(title, value, suffix='', color='#007AFF'):
    return html.Div(
        style={
            'background': colors['card_bg'],
            'padding': '20px',
            'borderRadius': '12px',
            'margin': '8px',
            'display': 'flex',
            'flexDirection': 'column',
            'alignItems': 'center',
            'justifyContent': 'center',
            'width': '180px',
            'minWidth': '180px',
            'height': '120px',
            'border': f'1px solid {colors["gray"]}'
        },
        children=[
            html.Div(title, style={
                'color': colors['gray'], 
                'fontSize': '14px', 
                'marginBottom': '8px',
                'textAlign': 'center'
            }),
            html.Div(f"{value}{suffix}", style={
                'fontSize': '28px', 
                'color': color,
                'fontWeight': 'bold',
                'textAlign': 'center'
            })
        ]
    )

# App layout
app.layout = html.Div(
    style={
        'fontFamily': 'Arial, sans-serif', 
        'background': colors['background'], 
        'padding': '20px', 
        'minHeight': '100vh',
        'color': colors['text']
    },
    children=[
        # Header
        html.Div([
            html.Img(
                src='https://upload.wikimedia.org/wikipedia/commons/f/fa/Apple_logo_black.svg',
                style={
                    'height': '50px', 
                    'marginRight': '15px',
                    'filter': 'invert(1)'  # Makes black logo white
                }
            ),
            html.H1(
                "Apple Financial Dashboard 2009-2022",
                style={
                    'color': colors['text'], 
                    'fontWeight': 'bold',
                    'margin': '0'
                }
            )
        ], style={
            'display': 'flex', 
            'alignItems': 'center', 
            'marginBottom': '30px'
        }),

        # KPI Cards Row
        html.Div([
            kpi_card("REVENUE", f"${df['Revenue'].iloc[-1]/1000:,.1f}", 'B', colors['primary']),
            kpi_card("PROFIT", f"${df['Profit'].iloc[-1]/1000:,.1f}", 'B', colors['green']),
            kpi_card("PROFIT MARGIN", f"{df['Profit_Margin'].iloc[-1]:.1f}", '%', colors['orange']),
            kpi_card("EMPLOYEES", f"{df['Employees'].iloc[-1]/1000:,.0f}", 'K', colors['purple']),
            kpi_card("ROE", f"{df['ROE'].iloc[-1]:.1f}", '%', colors['green']),
        ], style={
            'display': 'flex', 
            'justifyContent': 'flex-start', 
            'gap': '15px', 
            'flexWrap': 'wrap',
            'marginBottom': '30px'
        }),

        # Chart Row 1
        html.Div([
            # Revenue & Profit Chart
            html.Div(
                style={
                    'flex': '2', 
                    'marginRight': '15px',
                    'backgroundColor': colors['card_bg'],
                    'borderRadius': '12px',
                    'padding': '20px',
                    'border': f'1px solid {colors["gray"]}'
                },
                children=[
                    dcc.Graph(
                        figure=go.Figure(
                            data=[
                                go.Scatter(
                                    x=df['Year'], 
                                    y=df['Revenue']/1000, 
                                    name='Revenue',
                                    line=dict(width=4, color=colors['primary']),
                                    hovertemplate='<b>%{x}</b><br>Revenue: $%{y:.1f}B<extra></extra>'
                                ),
                                go.Scatter(
                                    x=df['Year'], 
                                    y=df['Profit']/1000, 
                                    name='Profit',
                                    line=dict(width=4, color=colors['green']),
                                    hovertemplate='<b>%{x}</b><br>Profit: $%{y:.1f}B<extra></extra>'
                                )
                            ]
                        ).update_layout(
                            plot_bgcolor=colors['card_bg'],
                            paper_bgcolor=colors['card_bg'],
                            font_color=colors['text'],
                            title='Revenue & Profit Trend (Billions USD)',
                            height=400,
                            margin=dict(t=50, b=50, l=50, r=50),
                            xaxis=dict(
                                tickvals=df['Year'],
                                tickangle=45,
                                showgrid=True,
                                gridcolor=colors['gray']
                            ),
                            yaxis=dict(
                                showgrid=True,
                                gridcolor=colors['gray'],
                                title='Billions USD'
                            ),
                            legend=dict(
                                orientation="h",
                                yanchor="bottom",
                                y=1.02,
                                xanchor="center",
                                x=0.5
                            )
                        ),
                        config={'displayModeBar': False}
                    )
                ]
            ),
            
            # Profit Share Pie Chart
            html.Div(
                style={
                    'flex': '1', 
                    'marginLeft': '15px',
                    'backgroundColor': colors['card_bg'],
                    'borderRadius': '12px',
                    'padding': '20px',
                    'border': f'1px solid {colors["gray"]}'
                },
                children=[
                    dcc.Graph(
                        figure=go.Figure(
                            data=[
                                go.Pie(
                                    labels=['Net Profit', 'Expenses'],
                                    values=[df['Profit'].iloc[-1], df['Revenue'].iloc[-1] - df['Profit'].iloc[-1]],
                                    marker=dict(colors=[colors['green'], colors['gray']]),
                                    hovertemplate='<b>%{label}</b><br>%{value:,.0f}M USD<br>%{percent}<extra></extra>',
                                    textinfo='percent+label'
                                )
                            ]
                        ).update_layout(
                            plot_bgcolor=colors['card_bg'],
                            paper_bgcolor=colors['card_bg'],
                            font_color=colors['text'],
                            title='2022 Revenue Breakdown',
                            height=400,
                            margin=dict(t=50, b=50, l=50, r=50),
                            showlegend=False
                        ),
                        config={'displayModeBar': False}
                    )
                ]
            )
        ], style={
            'display': 'flex', 
            'marginTop': '20px',
            'flexWrap': 'wrap'
        }),

        # Chart Row 2 - Additional Metrics
        html.Div([
            # Profit Margin Chart
            html.Div(
                style={
                    'flex': '1',
                    'marginRight': '15px',
                    'backgroundColor': colors['card_bg'],
                    'borderRadius': '12px',
                    'padding': '20px',
                    'border': f'1px solid {colors["gray"]}',
                    'minWidth': '300px'
                },
                children=[
                    dcc.Graph(
                        figure=go.Figure(
                            data=[
                                go.Bar(
                                    x=df['Year'],
                                    y=df['Profit_Margin'],
                                    name='Profit Margin',
                                    marker_color=colors['orange'],
                                    hovertemplate='<b>%{x}</b><br>Margin: %{y:.1f}%<extra></extra>'
                                )
                            ]
                        ).update_layout(
                            plot_bgcolor=colors['card_bg'],
                            paper_bgcolor=colors['card_bg'],
                            font_color=colors['text'],
                            title='Profit Margin %',
                            height=400,
                            margin=dict(t=50, b=50, l=50, r=50),
                            xaxis=dict(
                                tickvals=df['Year'],
                                tickangle=45,
                                showgrid=True,
                                gridcolor=colors['gray']
                            ),
                            yaxis=dict(
                                showgrid=True,
                                gridcolor=colors['gray'],
                                title='Percentage %'
                            )
                        ),
                        config={'displayModeBar': False}
                    )
                ]
            ),

            # ROE Chart
            html.Div(
                style={
                    'flex': '1',
                    'marginLeft': '15px',
                    'backgroundColor': colors['card_bg'],
                    'borderRadius': '12px',
                    'padding': '20px',
                    'border': f'1px solid {colors["gray"]}',
                    'minWidth': '300px'
                },
                children=[
                    dcc.Graph(
                        figure=go.Figure(
                            data=[
                                go.Scatter(
                                    x=df['Year'],
                                    y=df['ROE'],
                                    name='ROE',
                                    line=dict(width=4, color=colors['purple']),
                                    hovertemplate='<b>%{x}</b><br>ROE: %{y:.1f}%<extra></extra>'
                                )
                            ]
                        ).update_layout(
                            plot_bgcolor=colors['card_bg'],
                            paper_bgcolor=colors['card_bg'],
                            font_color=colors['text'],
                            title='Return on Equity (ROE) %',
                            height=400,
                            margin=dict(t=50, b=50, l=50, r=50),
                            xaxis=dict(
                                tickvals=df['Year'],
                                tickangle=45,
                                showgrid=True,
                                gridcolor=colors['gray']
                            ),
                            yaxis=dict(
                                showgrid=True,
                                gridcolor=colors['gray'],
                                title='ROE %'
                            )
                        ),
                        config={'displayModeBar': False}
                    )
                ]
            )
        ], style={
            'display': 'flex',
            'marginTop': '20px',
            'flexWrap': 'wrap'
        })
    ]
)

if __name__ == '__main__':
    app.run(debug=True)