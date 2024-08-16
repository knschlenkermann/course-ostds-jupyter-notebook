# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(spacex_df, values='class',
        names='Launch Site',
        title='title')
        return fig
    else:
        fig = px.pie(
            spacex_df.loc[spacex_df["Launch Site"] == entered_site].groupby(
                "class", as_index=False).count(),
            values='Launch Site',
            names='class',
            title='title'
        )
        return fig

@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'), Input(component_id="payload-slider", component_property="value")])
def get_payload_scatter(entered_site, entered_range):
    data = spacex_df.loc[(spacex_df["Payload Mass (kg)"] > min(entered_range))
                         & (spacex_df["Payload Mass (kg)"] < max(entered_range))]
    if entered_site == "ALL":
        return px.scatter(data, x="Payload Mass (kg)", y="class", color="Booster Version Category")
    else:
        return px.scatter(data.loc[data["Launch Site"] == entered_site], x="Payload Mass (kg)", y="class", color="Booster Version Category")

# Create an app layout
app.layout = html.Div(
    children=[
        html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36',
                'font-size': 40}
        ),
        # TASK 1: Add a dropdown list to enable Launch Site selection
        # The default select value is for ALL sites
        dcc.Dropdown(
                    id='site-dropdown',
                    options=[{"label": "All Sites", "value": "ALL"},
                              {"label": "CCAFS LC-40", "value": "CCAFS LC-40"},
                              {"label": "KSC LC-39A", "value": "KSC LC-39A"},
                              {"label": "VAFB SLC-4E", "value": "VAFB SLC-4E"},
                              {"label": "CCAFS SLC-40", "value": "CCAFS SLC-40"}],
                    value="ALL",
                    placeholder="Select a Launch Site here",
                    searchable=True
                    ),
        html.Br(),

        # TASK 2: Add a pie chart to show the total successful launches count for all sites
        # If a specific launch site was selected, show the Success vs. Failed counts for the site
        html.Div(dcc.Graph(id='success-pie-chart')),
        html.Br(),

        html.P("Payload range (Kg):"),
        # TASK 3: Add a slider to select payload range
        dcc.RangeSlider(id='payload-slider', min=0, max=10_000, step=1000,
                        value=[min_payload, max_payload]),

        # TASK 4: Add a scatter chart to show the correlation between payload and launch success
        html.Div(dcc.Graph(id='success-payload-scatter-chart')),
    ]
)

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output


# Run the app
if __name__ == '__main__':
    app.run_server()
