import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures


def plot_kuznets_curve(df, country):
    df["original_period"] = pd.to_datetime(df["original_period"], errors="coerce")
    df = df.dropna(subset=["original_period"])
    df["date"] = df["original_period"].dt.strftime("%Y")
    df["customdata"] = df.apply(
        lambda row: [row["date"], row["Palma ratio"], row["GDP per capita"]], axis=1
    )

    fig = px.scatter(
        df,
        x="GDP per capita",
        y="Palma ratio",
        title=f"Kuznets curve for {country}: Palma Ratio",
        labels={
            "GDP per capita": "GDP per capita",
            "Palma ratio": "Measure of income inequalities: Palma Ratio",
        },
        custom_data=["date", "Palma ratio", "GDP per capita"],
    )

    fig.update_traces(
        hovertemplate="<br>".join(
            [
                "Date: %{customdata[0]}",
                "Palma Ratio: %{customdata[1]}",
                "GDP per capita: %{customdata[2]}",
            ]
        ),
        marker=dict(size=11, symbol="circle-open-dot"),
        selector=dict(mode="markers"),
    )

    # Polynomial Regression
    poly_features = PolynomialFeatures(degree=3)
    X_poly = poly_features.fit_transform(df[["GDP per capita"]])
    poly_model = LinearRegression()
    poly_model.fit(X_poly, df["Palma ratio"])

    x_line = np.linspace(df["GDP per capita"].min(), df["GDP per capita"].max(), 100)
    x_line_poly = poly_features.transform(x_line.reshape(-1, 1))
    y_line = poly_model.predict(x_line_poly)

    fig.add_trace(
        go.Scatter(
            x=x_line,
            y=y_line,
            mode="lines",
            name="Trend Line",
            line=dict(color="gold", width=3),
        )
    )

    return fig
def plot_kuznet_example():
    economic_development = np.linspace(0, 100, 100)
    #quadratic function
    inequality = -0.0005 * (economic_development - 50)**2 + 65
    fig = go.Figure()
    fig.add_trace(
        go.Line(
            x = economic_development,
            y = inequality, 
            line = dict(color = "limegreen")
        )
    )
    fig.update_layout(
    xaxis_title = "Economic Development",
    yaxis_title = "Inequalities", 
    title = "Example of Kuznets Curve", 
    )
    return fig