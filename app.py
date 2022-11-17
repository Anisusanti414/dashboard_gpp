# 1. Import Dash
import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import statistics as st
from statistics import mode
import pandas as pd
import plotly.express as px

print('BERHASIL')

# 2. Create a Dash app instance
app = dash.Dash(
    external_stylesheets=[dbc.themes.MINTY],
    name = 'Global Power Plant'
)

## --- Title
app.title = 'Power Plant Dashboard Analytics'

## --- Navbar

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="#")),
        # dbc.DropdownMenu(
        #     children=[
        #         dbc.DropdownMenuItem("More pages", header=True),
        #         dbc.DropdownMenuItem("Page 2", href="#"),
        #         dbc.DropdownMenuItem("Page 3", href="#"),
        #     ],
        #     nav=True,
        #     in_navbar=True,
        #     label="More",
        # ),
    ],
    brand="Global Power Plan",
    brand_href="#",
    color="primary",
    dark=True,
)

## Import Dataset gpp
gpp = pd.read_csv('power_plant.csv')


### CARD CONTENT
total_county = [
    dbc.CardHeader('Number of Country'),
    dbc.CardBody([
        html.H1(gpp['country_long'].nunique())
    ]),
]

total_pp =[
    dbc.CardHeader('Total Power Plant'),
    dbc.CardBody([
        html.H1(gpp['name of powerplant'].nunique())
    ]),
]

total_fuel = [
    dbc.CardHeader('Most Used Fuel', style={"color":"black"}),
    dbc.CardBody([
        html.H1(f"{mode(gpp['primary_fuel'])} = {len(gpp[gpp['primary_fuel']==(gpp.describe(include='object')).loc['top','primary_fuel']])}")
    ])
]

## -- VISUALIZATION
# Data aggregation
agg1 = pd.crosstab(
    index=[gpp['country code'], gpp['start_year']],
    columns='No of Power Plant'
).reset_index()

# Visualization
plot_map = px.choropleth(agg1.sort_values(by="start_year"),
             locations='country code',
              color_continuous_scale='tealgrn',
             color='No of Power Plant',
             animation_frame='start_year',
             template='ggplot2')

# BARPLOT RANGKING
# Data aggregation
gpp_indo = gpp[gpp['country_long'] == 'Indonesia']


# BOXPLOT DISTRIBUTION

# PIE Chart
# aggregation

# visualize

## --- LAYOUT
app.layout = html.Div(children=[
    navbar,

    html.Br(),

    ## -- Component Main Page --
    html.Div([

        ## -- ROW 1 --
        dbc.Row([
            ## -- COLUMN 1
            dbc.Col(
                ## -- Isi ada brapa banyak card
                [
                    dbc.Card(total_county, color = 'aquamarine',),
                    html.Br(),
                    dbc.Card(total_pp,color = 'plum',),
                    html.Br(),
                    dbc.Card(total_fuel, color = 'lightsalmon'),
                ],
                width = 3),
            ## -- COLUMN 2
            dbc.Col([
                dcc.Graph(figure=plot_map),
            ],width = 9),
        ]),

        html.Hr(),

        ## -- ROW 2 --
        dbc.Row([
            ## -- COLUMN 1
            dbc.Col([
                html.H1('Analysis by Country'),
                dbc.Tabs([
                    ##--- TAB 1 : RANGKING
                    dbc.Tab(
                        dcc.Graph(
                            id='plotranking',
                            #figure = plot_ranking, #diganti di bawah yang callback pendefinisiannya ada di return
                        ),
                        label = 'Rangking'),

                    ## -- TAB 2 : DISTRIBUTION
                    dbc.Tab(
                        dcc.Graph(
                            id='plotdist',
                            #figure = plot_dist, sudah di call back
                        ),
                    label = 'Distibution'),
                ]),
            ],width = 8),
            ## -- COLUMN 2
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader('Select Country'),
                    dbc.CardBody(
                        dcc.Dropdown(
                            id='choose_country',
                            options = gpp['country_long'].unique(),
                            value = 'Indonesia',
                        ),
                    ),
                ]),
                dcc.Graph(
                    id='plotpie',
                    #figure = plot_pie,
                ),

            ],
            width = 4),
        ]),


    ],style={
        'paddingLeft':'30px',
        'paddingRight':'30px'
    } 
    
    )
    #html.H1(children='Dashboard Overview'), #judul dashboard

])

### CALLBACK Plor RANKING
@app.callback(
    Output(component_id='plotranking', component_property='figure'),
    Input(component_id='choose_country',component_property='value')
)

def update_plot1(country_name):
    gpp_indo = gpp[gpp['country_long'] == country_name]

    top_indo = gpp_indo.sort_values('capacity in MW').tail(10)

    # Visualize
    plot_ranking = px.bar(
        top_indo,
        x = 'capacity in MW',
        y = 'name of powerplant',
        template = 'ggplot2',
        title = f'Rangking of Overall Power Plants in {(country_name)}'
    )

    return plot_ranking

### CALLBACK Plor DISTRIBUTION
@app.callback(
    Output(component_id='plotdist', component_property='figure'),
    Input(component_id='choose_country',component_property='value')
)

def update_plot2(country_name):
    gpp_indo = gpp[gpp['country_long'] == country_name]

    # Visualize
    plot_dist = px.box(
    gpp_indo,
    color='primary_fuel',
    y='capacity in MW',
    template='ggplot2',
    title='Distribution of capacity in MW in each fuel',
    labels={
        'primary_fuel': 'Type of Fuel'
    }
).update_xaxes(visible=False)

    return plot_dist

### CALLBACK Plot PIE
@app.callback(
    Output(component_id='plotpie', component_property='figure'),
    Input(component_id='choose_country',component_property='value')
)

def update_plot3(country_name):
    gpp_indo = gpp[gpp['country_long'] == country_name]

    # aggregation
    agg2=pd.crosstab(
        index=gpp_indo['primary_fuel'],
        columns='No of Power Plant'
    ).reset_index()


    #Visualization
    plot_pie = px.pie(
        agg2,
        values='No of Power Plant',
        names='primary_fuel',
        color_discrete_sequence=['aquamarine', 'salmon', 'plum', 'grey', 'slateblue'],
        template='ggplot2',
        hole=0.4,
        labels={
            'primary_fuel': 'Type of Fuel'
        }
    )
    return plot_pie



## 3. Start the Dash server
if __name__ == "__main__":
    app.run_server()
