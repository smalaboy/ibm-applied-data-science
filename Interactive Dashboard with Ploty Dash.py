# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
launch_sites = spacex_df['Launch Site'].unique()
print("launch_sites", launch_sites)
dropdown_options = [{'label': 'All Sites', 'value': 'ALL'}] + [{"label": s, "value": s} for s in launch_sites]

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown', value="ALL", searchable=True, placeholder="Select a Launch Site here", options=dropdown_options),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider', min=0, max=10000, step=1000, value=[min_payload, max_payload], marks={0: '0', 100: '100'},),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback( Output(component_id='success-pie-chart', component_property='figure'),
               Input(component_id='site-dropdown', component_property='value'))
def dropdown_callback(selected_site):
    if selected_site == 'ALL':
        fig = px.pie(spacex_df, values='class', 
        names='Launch Site', 
        title='Success launches by site')
        return fig
    else:
        data = spacex_df[spacex_df["Launch Site"] == selected_site].groupby('class', as_index=False).count()
        # print("data")
        # print(data.head())
        fig = px.pie(data, values='Unnamed: 0', 
        names='class', 
        title=f'Success launches for {selected_site} site')
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'), Input(component_id="payload-slider", component_property="value")]
)
def succes_payload_callback(selected_site, slider_values):
    min_payload, max_payload = slider_values
    payload_filter_data = spacex_df.loc[(spacex_df['Payload Mass (kg)'] >= min_payload) & (spacex_df['Payload Mass (kg)'] <= max_payload)]
    if selected_site == 'ALL':
        data = payload_filter_data
        fig = px.scatter(data, x='Payload Mass (kg)', 
        y='class', 
        color='Booster Version Category',
        title='Correlation between payload and success')
        return fig
    else:
        data = payload_filter_data[spacex_df["Launch Site"] == selected_site]
        fig = px.scatter(data, x='Payload Mass (kg)', 
        y='class', 
        color='Booster Version Category',
        title=f'Correlation between payload and success for {selected_site} site')
    
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
