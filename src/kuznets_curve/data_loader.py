from dbnomics import fetch_series
import pandas as pd 
import numpy as np

#download data 
#Data for inequalities
def data_download():
    inequalities = fetch_series([
        "OECD/DP_LIVE/BRA.INCOMEINEQ.PALMA.RT.A",
        "OECD/DP_LIVE/CAN.INCOMEINEQ.PALMA.RT.A",
        "OECD/DP_LIVE/CHL.INCOMEINEQ.PALMA.RT.A",
        "OECD/DP_LIVE/CZE.INCOMEINEQ.PALMA.RT.A",
        "OECD/DP_LIVE/DEU.INCOMEINEQ.PALMA.RT.A",
        "OECD/DP_LIVE/ESP.INCOMEINEQ.PALMA.RT.A",
        "OECD/DP_LIVE/GBR.INCOMEINEQ.PALMA.RT.A",
        "OECD/DP_LIVE/ITA.INCOMEINEQ.PALMA.RT.A",
        "OECD/DP_LIVE/KOR.INCOMEINEQ.PALMA.RT.A",
        "OECD/DP_LIVE/PRT.INCOMEINEQ.PALMA.RT.A",
        "OECD/DP_LIVE/TUR.INCOMEINEQ.PALMA.RT.A",
        "OECD/DP_LIVE/USA.INCOMEINEQ.PALMA.RT.A"
    ])

    print(inequalities.columns)

    #Data for GDP per capita 
    GDP_pct = fetch_series([
        "WB/WDI/A-NY.GDP.PCAP.KD-BRA",
        "WB/WDI/A-NY.GDP.PCAP.KD-CAN",
        "WB/WDI/A-NY.GDP.PCAP.KD-CHL",
        "WB/WDI/A-NY.GDP.PCAP.KD-CZE",
        "WB/WDI/A-NY.GDP.PCAP.KD-DEU",
        "WB/WDI/A-NY.GDP.PCAP.KD-ESP",
        "WB/WDI/A-NY.GDP.PCAP.KD-GBR",
        "WB/WDI/A-NY.GDP.PCAP.KD-ITA",
        "WB/WDI/A-NY.GDP.PCAP.KD-KOR",
        "WB/WDI/A-NY.GDP.PCAP.KD-PRT",
        "WB/WDI/A-NY.GDP.PCAP.KD-TUR",
        "WB/WDI/A-NY.GDP.PCAP.KD-USA"
    ])
    print(GDP_pct.columns)


    #columns we want to keep
    col_ine = ["original_period","value", "Country"]
    col_gdp = ["original_period","value", "country (label)"]

    #dataset with data of interest 
    df_ine = inequalities[col_ine].rename(columns={"value" :"Palma ratio"})
    df_gdp = GDP_pct[col_gdp].rename(columns={"value":"GDP per capita", "country (label)":"Country"})

    return df_ine, df_gdp

def merge_data(dfs):
    df_ine, df_gdp = dfs
    countries = df_gdp["Country"].unique()
    
    merged_dfs = {}
    for country in countries:
        country_dfs = [df[df['Country'] == country] for df in dfs]
        merged_df = country_dfs[0]
        for df in country_dfs[1:]:
            merged_df = pd.merge(merged_df, df, on="original_period", how="left")
        merged_dfs[country] = merged_df
    
    return merged_dfs

