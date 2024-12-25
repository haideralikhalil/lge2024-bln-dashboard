import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="LGE 2024-25 Bye Elections",
                   page_icon=":bar_chart:",
                layout="wide")



df = pd.read_excel(
    io ='voter_stats.xlsx',
    engine ='openpyxl',
    sheet_name = 'Intact',
    usecols='A:M',
    nrows = 361
    
)
print(df)

#st.dataframe(df)
st.sidebar.header("Please Filter Here")

district_options= df['ENG_DISTRICT'].unique().tolist()

district = st.sidebar.selectbox (
    "Select District",
    options =district_options ,
    index=district_options.index(df['ENG_DISTRICT'].unique()[0])  # Set default to the first district
)

patwar = st.sidebar.multiselect(
    "Patwar",
    options = df['PATWAR'].unique(),
    default = df['PATWAR'].unique(),
)

cbc = st.sidebar.multiselect(
    "CBC",
    options = df['BLOCK_CODE'].unique(),
    default = df['BLOCK_CODE'].unique(),
)

df_selection = df.query(
    #"ENG_DISTRICT == @district & PATWAR == @patwar & BLOCK_CODE == @cbc"
    "ENG_DISTRICT == @district"
)

#st.dataframe(df_selection)

st.title(":bar_chart: Voters Stats")

voters = int(df_selection['TOTAL_VOTER'].sum())
cbcs = int(df_selection['BLOCK_CODE'].count())

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Registered Voters")
    st.subheader(f"Total: {voters}")
with col2:
    st.subheader("No. of CBCs")
    st.subheader(f"{cbcs}")

st.markdown("---")

# --- BAR Charts

voters_by_district = (
    df_selection.groupby(by=["ENG_DISTRICT"]).sum()[["TOTAL_VOTER"]].sort_values(by="TOTAL_VOTER")
)

fig_voters = px.bar (
    voters_by_district,
    y = "TOTAL_VOTER",
    x = voters_by_district.index,
    orientation = "v",
    title ="<b>Registered Voters</b>",
    color_discrete_sequence = ['#0083B8'] * len(voters_by_district),
    template = "plotly_white"
)
st.plotly_chart(fig_voters)