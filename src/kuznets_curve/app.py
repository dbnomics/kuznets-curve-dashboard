import importlib

import streamlit as st
from charts import plot_kuznets_curve
from data_loader import data_download, merge_data
from PIL import Image
from streamlit_option_menu import option_menu


def main() -> None:
    package_dir = importlib.resources.files("kuznets_curve")
    st.set_page_config(
        page_title="DBnomics Kuznets Curve",
        page_icon=str(package_dir / "images/favicon.png"),
    )

    def local_css(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    local_css(str(package_dir / "styles.css"))

    st.image(str(package_dir / "images/dbnomics.svg"), width=300)

    st.title(":blue[Kuznets Curve]")
    st.markdown(
        """
        <style>
        hr {
            height: 1px;
            border: none;
            color: #333;
            background-color: #333;
            margin-top: 3px;
            margin-bottom: 3px;
        }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    with st.sidebar:
        selected = option_menu(
            menu_title="Menu",
            options=["Explanations", "Kuznets Curve", "Sources"],
            icons=["book", "bar-chart", "search"],
            menu_icon=":",
            default_index=0,
        )

    if selected == "Explanations":
        st.subheader(":blue[**Explanations**]")
        st.write(
            "\n"
            "**Simon Kuznets** (1901-1985) was an American economist who received the Nobel Prize in Economics in 1971 for his work on economic growth and development.\n"
            "\n"
            "Kuznets' main work focuses on the cycles of growth. He conducted empirical research on long-term series.\n"
            "\n"
            "The Kuznet's curve (1955) depicts an inverse U-shaped relationship between economic development and inequalities.\n"
            "The U shape means that at its inception economic growth creates more inequalities.\n"
        )

        kuznets_example = Image.open(package_dir / "images/kuznets_example.png")
        st.image(
            kuznets_example,
            caption="Kuznets Curve in theory",
            use_column_width=True,
            output_format="PNG",
            width=100,
        )

        st.write(
            "After a certain threshold inequalities are supposed to decrease.\n"
            "\n"
            "**How to explain the different stages of economic growth?**\n"
            "\n"
            "At the first stage, inequalities are what create economic growth. The investements are focused on infrastructure capital and natural capital.\n"
            "The investors capture all the richess created : it increases inequalities.\n"
            "At the second stage, inequalities reduce : a shift occurs from secondary sector to tertiary sector.\n"
            "There are more potentialities of added value.\n"
            "At the same time, countries implement a social system that leads to more redistribution.\n"
            "So, according to Kuznets, the reduction of inequalities is a normal step of economoic growth.\n"
            "\n"
            "The Kuznets Curve was consistent before the 1970s. Since, inequalities have increased in developed countries challenging Kuznets' theory.\n"
            "\n"
            "Many criticisms, have been made by economists such as Thomas Piketty.\n"
            "According to Piketty, reduction of inequalities is not automatically linked to economic development.\n"
            "Economic History shows that the reduction of inequalities is often linked to external events like the implementation of income-taxes."
        )

    if selected == "Kuznets Curve":
        # Plot for Kuznets Curve
        st.subheader(":blue[**Charts**]")
        df_gdp, df_ine = data_download()
        merged_dfs = merge_data((df_gdp, df_ine))

        country = st.selectbox("Select a country", list(merged_dfs.keys()))

        if country:
            fig = plot_kuznets_curve(merged_dfs[country], country)
            st.plotly_chart(fig)

        st.write(
            "**What is the Palma ratio ?**\n"
            "The Palma ratio measures inequalities by dividing the share received by the 10% richest by the share of the 40% poorest.\n"
            "A higher Palma ratio indicates greater inequalities"
        )

    if selected == "Sources":
        st.subheader("**Data**")
        st.write(
            "\n"
            "- [GDP per Capita](https://db.nomics.world/WB/WDI?dimensions=%7B\"indicator\"%3A%5B\"NY.GDP.PCAP.KD\"%5D%7D&tab=list).\n"
            "\n"
            "- [Palma Ratio](https://db.nomics.world/OECD/DP_LIVE?q=palma+ratio&tab=list)"
        )
        st.markdown("---")
        st.write("[Source Code](https://github.com/dbnomics/kuznets-curve-dashboard)")
        st.write("[DBnomics](https://db.nomics.world)")


if __name__ == "__main__":
    main()
