import streamlit as st
import speedtest
import pandas as pd
from datetime import datetime
import json

st.set_page_config(
    page_title="Internet Speed Test",
    page_icon="🌐",
    layout="centered"
)

st.title("🌐 Internet Speed Test Application")

st.write(
    "Click the button below to measure your internet speed."
)

if st.button("Start Speed Test"):

    with st.spinner("Running speed test..."):

        try:
            st_obj = speedtest.Speedtest()

            server = st_obj.get_best_server()

            download = st_obj.download() / 1_000_000
            upload = st_obj.upload() / 1_000_000
            ping = st_obj.results.ping

            current_time = datetime.now().strftime(
                "%d-%m-%Y %H:%M:%S"
            )

            result = {
                "Server Host": server["host"],
                "Location": server["name"],
                "Country": server["country"],
                "Ping (ms)": round(ping, 2),
                "Download (Mbps)": round(download, 2),
                "Upload (Mbps)": round(upload, 2),
                "Time": current_time
            }

            st.success("Speed Test Completed")

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Ping",
                f"{round(ping,2)} ms"
            )

            col2.metric(
                "Download",
                f"{round(download,2)} Mbps"
            )

            col3.metric(
                "Upload",
                f"{round(upload,2)} Mbps"
            )

            st.subheader("Test Details")

            df = pd.DataFrame(
                result.items(),
                columns=["Parameter", "Value"]
            )

            st.table(df)

            # Save JSON
            with open(
                "speed_report.json",
                "w"
            ) as f:
                json.dump(
                    result,
                    f,
                    indent=4
                )

            st.download_button(
                "Download JSON Report",
                data=json.dumps(
                    result,
                    indent=4
                ),
                file_name="speed_report.json",
                mime="application/json"
            )

        except Exception as e:
            st.error(
                f"Error: {e}"
            )