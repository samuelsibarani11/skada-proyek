import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html
import dash_bootstrap_components as dbc

# Membaca dataset
df = pd.read_csv("Ecommerce_Sales_Prediction_Dataset.csv")

# Preprocessing (sesuaikan dengan nama kolom di dataset)
df["Date"] = pd.to_datetime(df["Date"], format="mixed", errors="coerce")
df["Month"] = df["Date"].dt.to_period("M").astype(str)
df["Sales"] = df["Price"] * df["Units_Sold"]
df["Profit"] = df["Sales"] - (
    df["Marketing_Spend"] + (df["Price"] * (df["Discount"] / 100) * df["Units_Sold"])
)

# Inisialisasi aplikasi Dash
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Dashboard Penjualan Produk"

# Layout Dashboard
app.layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                html.H1(
                    "Dashboard Analisis Penjualan Produk",
                    className="text-center my-4",
                    style={"color": "#2c3e50"},
                )
            )
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H4("Tren Penjualan Bulanan", className="text-center"),
                        dcc.Graph(
                            figure=px.line(
                                df.groupby("Month")["Sales"].sum().reset_index(),
                                x="Month",
                                y="Sales",
                                title="Total Penjualan Bulanan",
                                labels={"Sales": "Penjualan", "Month": "Bulan"},
                            ).update_layout(title_font_size=20)
                        ),
                    ],
                    width=12,
                )
            ],
            className="mb-4",
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H4(
                            "Segmentasi Produk Berdasarkan Keuntungan",
                            className="text-center",
                        ),
                        dcc.Graph(
                            figure=px.pie(
                                df.groupby("Product_Category")["Profit"]
                                .sum()
                                .reset_index(),
                                names="Product_Category",
                                values="Profit",
                                title="Keuntungan per Kategori Produk",
                            ).update_layout(title_font_size=20)
                        ),
                    ],
                    md=6,
                ),
                dbc.Col(
                    [
                        html.H4(
                            "Penjualan Berdasarkan Segmen Pelanggan",
                            className="text-center",
                        ),
                        dcc.Graph(
                            figure=px.bar(
                                df.groupby("Customer_Segment")["Sales"]
                                .sum()
                                .reset_index(),
                                x="Customer_Segment",
                                y="Sales",
                                title="Total Penjualan per Segmen Pelanggan",
                                color="Customer_Segment",
                                labels={
                                    "Customer_Segment": "Segmen Pelanggan",
                                    "Sales": "Penjualan",
                                },
                            ).update_layout(title_font_size=20)
                        ),
                    ],
                    md=6,
                ),
            ],
            className="mb-4",
        ),
    ],
    fluid=True,
)

# Menjalankan server
if __name__ == "__main__":
    app.run_server(debug=True)
