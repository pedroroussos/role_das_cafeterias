import streamlit as st
import pandas as pd
import plotly.express as px

PRIMARY = '#3B1B0D'
SECONDARY = '#DDD1C0'
TERTIARY = '#C5A481'
HIGHLIGHT = "#9E692F"

st.set_page_config(layout="wide")


@st.cache_data
def load_data():
    return pd.read_csv('caf.csv', sep=';', decimal=',')

df = load_data()

st.title("Rota das Cafeterias")

col1, col2 = st.columns([2, 1])

with col2:
    edited_df = st.data_editor(
        df[['id', 'cafe', 'visitado']],
        use_container_width=True,
        hide_index=True,
        column_config={
            "visitado": st.column_config.CheckboxColumn("visitado")
        },
        height = 700
    )

with col1:
    edited_df["lat"] = df['lat']
    edited_df["long"] = df['long']
    edited_df["size"] = 1
    edited_df["id"] = edited_df["id"].apply(str)
    edited_df["visitado"] = edited_df["visitado"].apply(lambda x: "Visitado" if x else "Não Visitado")

    fig = px.scatter_map(
        edited_df,
        lat="lat",
        lon="long",
        color="visitado",
        hover_name="cafe",
        zoom=11.5,
        size='size',
        text = 'id',
        size_max = 14,
        center={"lat": df["lat"].min()+(df["lat"].max()-df["lat"].min())/2, "lon": df["long"].min()+(df["long"].max()-df["long"].min())/2},
        height=700,
        opacity = .85,
        color_discrete_map={
        'Visitado': PRIMARY,
        'Não Visitado': TERTIARY
        },
    )

    fig.update_layout(
        map_style="carto-positron",
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        dragmode="zoom",
        showlegend=True,
        font=dict(
            size=12,
            color='white',
            family="Segoe UI"
        ),
    )

    fig.update_layout(
        map={
            "layers": [
                {
                    "sourcetype": "geojson",
                    "source": {
                        "type": "Feature",
                        "geometry": {
                            "type": "Polygon",
                            "coordinates": [[
                                [-180, -90],
                                [-180,   90],
                                [ 180,   90],
                                [ 180, -90],
                                [-180, -90]
                            ]]
                        }
                    },
                    "type": "fill",
                    "color": "rgba(221, 209, 192, 0.3)",
                }
            ]
        }
    )


    fig.update_layout(
        legend_title_text='',
        legend=dict(
            x=0.98,
            y=0.97,
            xanchor='right',
            yanchor='top',
            bgcolor='rgba(255,255,255,0.7)',  # optional background box
            borderwidth=1,
            font=dict(
                size=12,
                color=PRIMARY
            )
        )
    )


    st.plotly_chart(fig, use_container_width=True)