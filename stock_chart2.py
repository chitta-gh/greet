import yfinance as yf
import requests
import plotly.graph_objects as go
import pandas as pd
import streamlit as st
import numpy as np

st.title("株価チャート")

# セッションを作成
session = requests.Session()

# 銘柄コード入力
ticker = st.text_input("銘柄コードを入力してください (例: 7203.T)")
period = st.selectbox("期間を選択してください", ("1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"))

def plot_stock_chart(ticker, period):
    if ticker:
        try:
            # 📌 `auto_adjust=False` を設定し、データを取得
            data = yf.download(ticker, period=period, session=session, auto_adjust=False)

            # 📌 MultiIndex の場合、列名を修正
            if isinstance(data.columns, pd.MultiIndex):
                data.columns = data.columns.droplevel(0)  # 上位インデックスを削除

            # 📌 銘柄コードを正しい列名に変換（"Open", "High", "Low", "Close", "Adj Close", "Volume"）
            correct_columns = ["Open", "High", "Low", "Close", "Adj Close", "Volume"]
            data.columns = correct_columns  # 列名を上書き

            # 📌 修正後のデータ確認
            print("修正後のデータ:\n", data.head())

            # 📌 "Open", "High", "Low", "Close" の列があるか確認
            if "Open" not in data.columns:
                print("エラー: 'Open' 列が見つかりません。データのカラム:", data.columns)

            # 株価チャートを描画
            fig = go.Figure(data=[
                go.Candlestick(
                    x=pd.to_datetime(data.index),  # 日付
                    open=data["Open"],  # 始値
                    high=data["High"],  # 高値
                    low=data["Low"],  # 安値
                    close=data["Close"],  # 終値
                    name="株価"
                ),
                go.Bar(
                    #x=pd.to_datetime(data.index),
                    #y=data['Volume'],
                    #name="出来高",
                    #yaxis="y2"
                )
            ])

            # 📌 レイアウト調整（インデント修正済み）
            fig.update_layout(
                yaxis2=dict(overlaying="y", side="right"),
                title=f"{ticker} の株価チャート",
                xaxis_title="日付",
                yaxis_title="株価",
                yaxis2_title="出来高"
            )

            # 📌 グラフを表示（余分な `])` を削除）
            st.plotly_chart(fig, use_container_width=True)
            #st.plotly_chart(fig, use_container_width=True, theme="streamlit")

        except Exception as e:
            st.error(f"エラーが発生しました: {e}")

# 📌 修正後の関数呼び出し
plot_stock_chart(ticker, period)
