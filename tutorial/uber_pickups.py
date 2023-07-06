import streamlit as st
import pandas as pd
import numpy as np

# データの取得
DATE_COLUMN = "date/time"
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
            'streamlit-demo-data/uber-raw-data-sep14.csv.gz')


@st.cache_data
def load_data(nrows):
    # pandas dataframe形式でダウンロード
    data = pd.read_csv(DATA_URL, nrows=nrows)

    # データのリネーム
    data.rename(lambda x: str(x).lower(),
                axis="columns",
                inplace=True)

    # 日付形式の変換
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])

    return data


if __name__ == "__main__":
    # タイトルを表示
    st.title("Uber pickups in NYC")

    # ローディング画面で表示するテキスト
    data_load_state = st.text("Loading data...")

    # 10000行を読み込み
    data = load_data(10000)

    # ローディングの完了を表示
    data_load_state.text("Done! (using st.cache_data)")

    # データの表示
    if st.checkbox("Show raw data"):
        st.subheader("Raw data")
        st.write(data)

    ## ヒストグラムの表示
    st.subheader("Number of pickups by hour")

    hist_values = np.histogram(
        data[DATE_COLUMN].dt.hour, bins=24, range=(0, 24))[0]
    
    # プロット
    st.bar_chart(hist_values)

    ## データをマップ上に表示
    # スライダー
    hour_to_filter = st.slider('hour', 0, 23, 17)  # min: 0h, max: 23h, default: 17h

    # プロット
    filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
    st.subheader(f"Map of all pickups at {hour_to_filter}:00")
    st.map(filtered_data)
