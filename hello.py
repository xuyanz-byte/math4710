import streamlit as st
import pandas as pd
import datetime
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go
import os
from dash import Dash, dcc, html, Input, Output, callback
from plotly.data import gapminder

print("Hello")

df=pd.read_excel("/Users/jiongjiong/Desktop/Adidas.xlsx")
st.set_page_config(layout="wide")
st.markdown('<style>div.block-container{padding-top;lrem;}</style>',unsafe_allow_html=True)
image = Image.open('/Users/jiongjiong/Desktop/adidas_logo.jpeg')

col1,col2 = st.columns([0.1,0.9])
with col1:
    st.image(image,width=100)
html_title = """
    <style>
    .title-test {
    font-weight:bold;
    padding:5px;
    border-radius:6px;
    }
    </style>
    <center><h1 class="title-test">Adidas Interactive Sales Dashboard</h1></center>"""
with col2:
    st.markdown(html_title, unsafe_allow_html=True)

col3, col4, col5 = st.columns([0.1,0.45,0.45])
with col3:
    box_date = str(datetime.datetime.now().strftime("%d %B %Y"))
    st.write(f"Last updated by:  \n {box_date}")

with col4:
    fig = px.bar(df, x = "Retailer", y = "TotalSales", labels={"TotalSales" : "Total Sales {$}"},
                 title = "Total Sales by Retailer", hover_data=["TotalSales"],
                 template="gridon",height=500)
    st.plotly_chart(fig,use_container_width=True)

_, view1, dwn1, view2, dwn2 = st.columns([0.15,0.20,0.20,0.20,0.20])
with view1:
    expander = st.expander("Retailer wise Sales")
    data = df[["Retailer","TotalSales"]].groupby(by="Retailer")["TotalSales"].sum()
    expander.write(data)
with dwn1:
    st.download_button("Get Data", data = data.to_csv().encode("utf-8"),
                       file_name="RetailerSales.csv", mime="text/csv")

df["Month_Year"] = df["InvoiceDate"].dt.strftime("%b'%y")
result = df.groupby(by = df["Month_Year"])["TotalSales"].sum().reset_index()

with col5:
    fig1 = px.line(result, x = "Month_Year", y = "TotalSales", title="Total Sales Over Time",
                   template="gridon")
    st.plotly_chart(fig1,use_container_width=True)

with view2:
    expander = st.expander("Monthly Sales")
    data = result
    expander.write(data)
with dwn2:
    st.download_button("Get Data", data = result.to_csv().encode("utf-8"),
                       file_name="Monthly Sales.csv", mime="text/csv")

st.divider()

result1 = df.groupby(by="State")[["TotalSales","UnitsSold"]].sum().reset_index()

# add the units sold as a line chart on a secondary y-axis
fig3 = go.Figure()
fig3.add_trace(go.Bar(x = result1["State"], y = result1["TotalSales"], name = "Total Sales"))
fig3.add_trace(go.Scatter(x=result1["State"], y = result1["UnitsSold"], mode = "lines",
                          name ="Units Sold", yaxis="y2"))
fig3.update_layout(
    title = "Total Sales and Units Sold by State",
    xaxis = dict(title="State"),
    yaxis = dict(title="Total Sales", showgrid = False),
    yaxis2 = dict(title="Units Sold", overlaying = "y", side = "right"),
    template = "gridon",
    legend = dict(x=1,y=1.1)
)
_, col6 = st.columns([0.1,1])
with col6:
    st.plotly_chart(fig3,use_container_width=True)

_, view3, dwn3 = st.columns([0.5,0.45,0.45])
with view3:
    expander = st.expander("View Data for Sales by Units Sold")
    expander.write(result1)
with dwn3:
    st.download_button("Get Data", data = result1.to_csv().encode("utf-8"),
                       file_name = "Sales_by_UnitsSold.csv", mime="text/csv")
st.divider()

_, col7 = st.columns([0.1,1])
treemap = df[["Region","City","TotalSales"]].groupby(by = ["Region","City"])["TotalSales"].sum().reset_index()

def format_sales(value):
    if value >= 0:
        return '{:.2f} Lakh'.format(value / 1_000_00)

treemap["TotalSales (Formatted)"] = treemap["TotalSales"].apply(format_sales)

fig4 = px.treemap(treemap, path = ["Region","City"], values = "TotalSales",
                  hover_name = "TotalSales (Formatted)",
                  hover_data = ["TotalSales (Formatted)"],
                  color = "City", height = 700, width = 600)
fig4.update_traces(textinfo="label+value")

with col7:
    st.subheader(":point_right: Total Sales by Region and City in Treemap")
    st.plotly_chart(fig4,use_container_width=True)

_, view4, dwn4 = st.columns([0.5,0.45,0.45])
with view4:
    result2 = df[["Region","City","TotalSales"]].groupby(by=["Region","City"])["TotalSales"].sum()
    expander = st.expander("View data for Total Sales by Region and City")
    expander.write(result2)
with dwn4:
    st.download_button("Get Data", data = result2.to_csv().encode("utf-8"),
                                        file_name="Sales_by_Region.csv", mime="text.csv")

_,view5, dwn5 = st.columns([0.5,0.45,0.45])
with view5:
    expander = st.expander("View Sales Raw Data")
    expander.write(df)
with dwn5:
    st.download_button("Get Raw Data", data = df.to_csv().encode("utf-8"),
                       file_name = "SalesRawData.csv", mime="text/csv")
st.divider()

print("✅ App file created")
import urllib
print("Password/Enpoint IP for localtunnel is:",urllib.request.urlopen('https://ipv4.icanhazip.com').read().decode('utf8').strip("\n"))

import plotly.express as px
import plotly.graph_objects as go

css = ["https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css", ]
app = Dash(name="Gapminder Dashboard", external_stylesheets=css)

################### DATASET ####################################
gapminder_df = gapminder(datetimes=True, centroids=True, pretty_names=True)
gapminder_df["Year"] = gapminder_df.Year.dt.year

#################### CHARTS #####################################
def create_table():
    fig = go.Figure(data=[go.Table(
        header=dict(values=gapminder_df.columns, align='left'),
        cells=dict(values=gapminder_df.values.T, align='left'))
    ]
    )
    fig.update_layout(paper_bgcolor="#e5ecf6", margin={"t":0, "l":0, "r":0, "b":0}, height=700)
    return fig

color_palette = px.colors.qualitative.Set3
# ✅ Population Pie Chart
def create_population_chart(continent="Asia", year=1952):
    filtered_df = gapminder_df[(gapminder_df.Continent == continent) & (gapminder_df.Year == year)]
    filtered_df = filtered_df.sort_values(by="Population", ascending=False).head(15)
    fig = px.pie(
        filtered_df,
        names="Country",
        values="Population",
        color="Country",
        color_discrete_sequence=color_palette,  # 🔸自定义色板
        title=f"Population Distribution for {continent} in {year}"
    )
    fig.update_traces(textinfo="percent+label", pull=[0.05]*len(filtered_df))  # 增加立体感
    fig.update_layout(
        paper_bgcolor="#e5ecf6",
        height=600,
        font=dict(size=14, color="#333"),
    )
    return fig


# ✅ GDP per Capita Pie Chart
def create_gdp_chart(continent="Asia", year=1952):
    filtered_df = gapminder_df[(gapminder_df.Continent == continent) & (gapminder_df.Year == year)]
    filtered_df = filtered_df.sort_values(by="GDP per Capita", ascending=False).head(15)
    fig = px.pie(
        filtered_df,
        names="Country",
        values="GDP per Capita",
        color="Country",
        color_discrete_sequence=color_palette,
        title=f"GDP per Capita Distribution for {continent} in {year}"
    )
    fig.update_traces(textinfo="percent+label", pull=[0.05]*len(filtered_df))
    fig.update_layout(
        paper_bgcolor="#e5ecf6",
        height=600,
        font=dict(size=14, color="#333"),
    )
    return fig


# ✅ Life Expectancy Pie Chart
def create_life_exp_chart(continent="Asia", year=1952):
    filtered_df = gapminder_df[(gapminder_df.Continent == continent) & (gapminder_df.Year == year)]
    filtered_df = filtered_df.sort_values(by="Life Expectancy", ascending=False).head(15)
    fig = px.pie(
        filtered_df,
        names="Country",
        values="Life Expectancy",
        color="Country",
        color_discrete_sequence=color_palette,
        title=f"Life Expectancy Distribution for {continent} in {year}"
    )
    fig.update_traces(textinfo="percent+label", pull=[0.05]*len(filtered_df))
    fig.update_layout(
        paper_bgcolor="#e5ecf6",
        height=600,
        font=dict(size=14, color="#333"),
    )
    return fig


def create_choropleth_map(variable, year):
    filtered_df = gapminder_df[gapminder_df.Year==year]

    fig = px.choropleth(filtered_df, color=variable,
                        locations="ISO Alpha Country Code", locationmode="ISO-3",
                        color_continuous_scale="RdYlBu", hover_data=["Country", variable],
                        title="{} Choropleth Map [{}]".format(variable, year)
                     )

    fig.update_layout(dragmode=False, paper_bgcolor="#e5ecf6", height=600, margin={"l":0, "r":0})
    return fig

##################### WIDGETS ####################################
continents = gapminder_df.Continent.unique()
years = gapminder_df.Year.unique()

cont_population = dcc.Dropdown(id="cont_pop", options=continents, value="Asia",clearable=False)
year_population = dcc.Dropdown(id="year_pop", options=years, value=1952,clearable=False)

cont_gdp = dcc.Dropdown(id="cont_gdp", options=continents, value="Asia",clearable=False)
year_gdp = dcc.Dropdown(id="year_gdp", options=years, value=1952,clearable=False)

cont_life_exp = dcc.Dropdown(id="cont_life_exp", options=continents, value="Asia",clearable=False)
year_life_exp = dcc.Dropdown(id="year_life_exp", options=years, value=1952,clearable=False)

year_map = dcc.Dropdown(id="year_map", options=years, value=1952,clearable=False)
var_map = dcc.Dropdown(id="var_map", options=["Population", "GDP per Capita", "Life Expectancy"],
                        value="Life Expectancy",clearable=False)

##################### APP LAYOUT ####################################
app.layout = html.Div([
    html.Div([
        html.H1("Gapminder Dataset Analysis", className="text-center fw-bold m-2"),
        html.Br(),
        dcc.Tabs([
            dcc.Tab([html.Br(),
                     dcc.Graph(id="dataset", figure=create_table())], label="Dataset"),
            dcc.Tab([html.Br(), "Continent", cont_population, "Year", year_population, html.Br(),
                     dcc.Graph(id="population")], label="Population"),
            dcc.Tab([html.Br(), "Continent", cont_gdp, "Year", year_gdp, html.Br(),
                     dcc.Graph(id="gdp")], label="GDP Per Capita"),
            dcc.Tab([html.Br(), "Continent", cont_life_exp, "Year", year_life_exp, html.Br(),
                     dcc.Graph(id="life_expectancy")], label="Life Expectancy"),
            dcc.Tab([html.Br(), "Variable", var_map, "Year", year_map, html.Br(),
                     dcc.Graph(id="choropleth_map")], label="Choropleth Map"),
        ])
    ], className="col-8 mx-auto"),
], style={"background-color": "#e5ecf6", "height": "100vh"})

##################### CALLBACKS ####################################
@callback(Output("population", "figure"), [Input("cont_pop", "value"), Input("year_pop", "value"),])
def update_population_chart(continent, year):
    return create_population_chart(continent, year)

@callback(Output("gdp", "figure"), [Input("cont_gdp", "value"), Input("year_gdp", "value"),])
def update_gdp_chart(continent, year):
    return create_gdp_chart(continent, year)

@callback(Output("life_expectancy", "figure"), [Input("cont_life_exp", "value"), Input("year_life_exp", "value"),])
def update_life_exp_chart(continent, year):
    return create_life_exp_chart(continent, year)

@callback(Output("choropleth_map", "figure"), [Input("var_map", "value"), Input("year_map", "value"),])
def update_map(var_map, year):
    return create_choropleth_map(var_map, year)

if __name__ == "__main__":
    app.run(debug=True)
