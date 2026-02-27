# pages/Visual_Explorer.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from io import BytesIO
import plotly.graph_objects as go
from matplotlib.patches import Circle
import squarify

st.set_page_config(page_title="Visual Explorer", layout="wide")

# =========================
# CUSTOM CSS (Same as Clean Data)
# =========================
st.markdown("""
<style>
.section-title { font-size:2rem; text-align:center; color:#ff6b6b; font-weight:700; margin:20px 0 10px 0; }
.dataframe { width:100%; border:2px solid #000; border-collapse:collapse; margin:10px 0; font-size:1.1rem; }
.dataframe th, .dataframe td { border:2px solid #000 !important; text-align:center; padding:8px; font-size:1.1rem; }
.dataframe th { font-weight:700; background:#f0f0f0; }
.stApp { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); }

/* Custom table styling */
.custom-table {
    width: 100%;
    border: 2px solid #000 !important;
    border-collapse: collapse;
    margin: 10px 0;
    font-size: 1.1rem;
}
.custom-table th, .custom-table td {
    border: 2px solid #000 !important;
    text-align: center !important;
    padding: 8px;
    font-size: 1.1rem;
}
.custom-table th {
    font-weight: 700;
    background-color: #f0f0f0;
}

div.stButton > button {
    background-color: #ff6b6b !important;
    color: white !important;
    font-weight: 700 !important;
}
</style>
""", unsafe_allow_html=True)

# =========================
# HOME BUTTON (Same style as Clean Data)
# =========================
col1, col2, col3 = st.columns([8,1,1])

with col3:  # Move to extreme right
    if st.button("HOME", use_container_width=True, key="home_btn"):
        st.switch_page("app.py")

# Dark + Bold Styling for HOME button
st.markdown("""
<style>
div.stButton > button {
    font-weight: 800 !important;
    color: #000000 !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center;'>Visual Explorer</h1>", unsafe_allow_html=True)
st.markdown("---")


# --------------------------
# Helper Functions
# --------------------------

def donut_chart(data, ax):
    wedges, texts, autotexts = ax.pie(
        data.values,
        labels=data.index,
        autopct='%1.1f%%',
        startangle=90
    )
    centre_circle = Circle((0, 0), 0.70, fc='white')
    ax.add_artist(centre_circle)
    ax.set_aspect('equal')


def pareto_chart(data, ax):
    data_sorted = data.sort_values(ascending=False)
    cumulative = data_sorted.cumsum() / data_sorted.sum() * 100

    ax.bar(data_sorted.index, data_sorted.values)
    ax.set_xticklabels(data_sorted.index, rotation=45, ha='right')

    ax2 = ax.twinx()
    ax2.plot(data_sorted.index, cumulative.values, color='red', marker='o')
    ax2.axhline(80, linestyle='--')


def treemap(data, ax):
    squarify.plot(sizes=data.values, label=data.index, ax=ax)
    ax.axis('off')


def density_2d(x, y, ax):
    h = ax.hist2d(x, y, bins=40)
    plt.colorbar(h[3], ax=ax)


def bubble_plot(x, y, df, ax):
    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    size_col = None
    for col in numeric_cols:
        if col not in [x, y]:
            size_col = col
            break

    if size_col:
        sizes = (df[size_col] - df[size_col].min())
        sizes = sizes / (sizes.max() + 1e-9) * 300 + 30
    else:
        sizes = 80

    ax.scatter(df[x], df[y], s=sizes, alpha=0.6)
    ax.set_xlabel(x)
    ax.set_ylabel(y)


def sankey_diagram(df, col1, col2):
    ct = pd.crosstab(df[col1], df[col2])

    labels = list(ct.index) + list(ct.columns)
    source = []
    target = []
    value = []

    for i, idx in enumerate(ct.index):
        for j, col in enumerate(ct.columns):
            if ct.loc[idx, col] > 0:
                source.append(i)
                target.append(len(ct.index) + j)
                value.append(ct.loc[idx, col])

    fig = go.Figure(data=[go.Sankey(
        node=dict(label=labels),
        link=dict(source=source, target=target, value=value)
    )])

    return fig


# --------------------------
# File Upload
# --------------------------

uploaded_file = st.file_uploader(
    "Upload Dataset",
    type=["csv", "xlsx", "xls", "parquet"]
)

if uploaded_file is not None:

    file_type = uploaded_file.name.split(".")[-1].lower()

    if file_type == "csv":
        df = pd.read_csv(uploaded_file)
    elif file_type in ["xlsx", "xls"]:
        df = pd.read_excel(uploaded_file)
    elif file_type == "parquet":
        df = pd.read_parquet(uploaded_file)
    else:
        st.error("Unsupported file format")
        st.stop()

    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    categorical_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
    datetime_cols = df.select_dtypes(include=["datetime64"]).columns.tolist()

    all_cols = df.columns.tolist()

    st.success("Dataset Uploaded Successfully ✅")

    viz_type = st.radio(
        "Select Visualization Type",
        ["Univariate", "Bivariate", "Multivariate"],
        horizontal=True
    )

    # =====================================================
    # UNIVARIATE
    # =====================================================

    if viz_type == "Univariate":

        column = st.selectbox("Select Column", all_cols)
        
        # Smaller figure size
        fig, ax = plt.subplots(figsize=(8, 4))

        if column in numeric_cols:

            plot_type = st.selectbox(
                "Select Plot Type",
                ["Histogram", "Box Plot", "KDE Plot", "Violin Plot", "Scatter Plot"]
            )

            if plot_type == "Histogram":
                sns.histplot(df[column], kde=True, ax=ax)
            elif plot_type == "Box Plot":
                sns.boxplot(y=df[column], ax=ax)
            elif plot_type == "KDE Plot":
                sns.kdeplot(df[column], fill=True, ax=ax)
            elif plot_type == "Violin Plot":
                sns.violinplot(y=df[column], ax=ax)
            elif plot_type == "Scatter Plot":
                ax.scatter(df.index, df[column])

        elif column in categorical_cols:

            plot_type = st.selectbox(
                "Select Plot Type",
                ["Bar Plot (Count)", "Count Plot", "Pie Chart",
                 "Donut Chart", "Pareto Chart", "Treemap"]
            )

            counts = df[column].value_counts()

            if plot_type in ["Bar Plot (Count)", "Count Plot"]:
                sns.countplot(x=df[column], ax=ax)
                ax.tick_params(axis='x', rotation=45)
            elif plot_type == "Pie Chart":
                counts.plot.pie(autopct='%1.1f%%', ax=ax)
                ax.set_ylabel("")
            elif plot_type == "Donut Chart":
                donut_chart(counts, ax)
            elif plot_type == "Pareto Chart":
                pareto_chart(counts, ax)
            elif plot_type == "Treemap":
                treemap(counts, ax)

        plt.tight_layout()
        st.pyplot(fig)
        
        # ================= DOWNLOAD BUTTON (Bottom Left) =================
        col_left, col_right = st.columns([1, 3])
        with col_left:
            # Save plot to buffer
            buf = BytesIO()
            fig.savefig(buf, format="png", dpi=300, bbox_inches="tight")
            buf.seek(0)
            
            st.download_button(
                label="DOWNLOAD",
                data=buf,
                file_name=f"{plot_type.replace(' ', '_')}.png",
                mime="image/png",
                use_container_width=True
            )

    # =====================================================
    # BIVARIATE
    # =====================================================

    elif viz_type == "Bivariate":

        col1 = st.selectbox("Select First Column", all_cols)
        col2 = st.selectbox("Select Second Column", all_cols)

        # Smaller figure size
        fig, ax = plt.subplots(figsize=(8, 4))

        if col1 in numeric_cols and col2 in numeric_cols:

            plot_type = st.selectbox(
                "Select Plot Type",
                ["Scatter Plot", "Line Plot",
                 "2D Density Plot", "Bubble Plot", "Area Plot"]
            )

            if plot_type == "Scatter Plot":
                sns.scatterplot(x=df[col1], y=df[col2], ax=ax)
            elif plot_type == "Line Plot":
                sns.lineplot(x=df[col1], y=df[col2], ax=ax)
            elif plot_type == "2D Density Plot":
                density_2d(df[col1], df[col2], ax)
            elif plot_type == "Bubble Plot":
                bubble_plot(col1, col2, df, ax)
            elif plot_type == "Area Plot":
                df.sort_values(col1).plot.area(
                    x=col1, y=col2, ax=ax
                )

        elif col1 in categorical_cols and col2 in categorical_cols:

            plot_type = st.selectbox(
                "Select Plot Type",
                ["Bar Plot (Grouped)", "Stacked Bar Chart",
                 "100% Stacked Bar Chart", "Heatmap", "Sankey Diagram"]
            )

            if plot_type == "Sankey Diagram":
                fig_plotly = sankey_diagram(df, col1, col2)
                st.plotly_chart(fig_plotly, use_container_width=True)
                st.stop()

            ct = pd.crosstab(df[col1], df[col2])

            if plot_type == "Bar Plot (Grouped)":
                ct.plot(kind='bar', ax=ax)
            elif plot_type == "Stacked Bar Chart":
                ct.plot(kind='bar', stacked=True, ax=ax)
            elif plot_type == "100% Stacked Bar Chart":
                ct.div(ct.sum(axis=1), axis=0).plot(
                    kind='bar', stacked=True, ax=ax
                )
            elif plot_type == "Heatmap":
                sns.heatmap(ct, annot=True, fmt='d', ax=ax)

        else:

            if col1 in numeric_cols:
                num_col, cat_col = col1, col2
            else:
                num_col, cat_col = col2, col1

            plot_type = st.selectbox(
                "Select Plot Type",
                ["Box Plot", "Violin Plot",
                 "Bar Plot (Mean)", "Strip Plot",
                 "Swarm Plot", "Point Plot",
                 "Histogram with Hue",
                 "KDE Plot with Hue", "Boxen Plot"]
            )

            if plot_type == "Box Plot":
                sns.boxplot(x=df[cat_col], y=df[num_col], ax=ax)
            elif plot_type == "Violin Plot":
                sns.violinplot(x=df[cat_col], y=df[num_col], ax=ax)
            elif plot_type == "Bar Plot (Mean)":
                df.groupby(cat_col)[num_col].mean().plot(kind='bar', ax=ax)
            elif plot_type == "Strip Plot":
                sns.stripplot(x=df[cat_col], y=df[num_col], ax=ax)
            elif plot_type == "Swarm Plot":
                sns.swarmplot(x=df[cat_col], y=df[num_col], ax=ax)
            elif plot_type == "Point Plot":
                sns.pointplot(x=df[cat_col], y=df[num_col], ax=ax)
            elif plot_type == "Histogram with Hue":
                sns.histplot(data=df, x=num_col, hue=cat_col, ax=ax)
            elif plot_type == "KDE Plot with Hue":
                sns.kdeplot(data=df, x=num_col, hue=cat_col, ax=ax)
            elif plot_type == "Boxen Plot":
                sns.boxenplot(x=df[cat_col], y=df[num_col], ax=ax)

        plt.tight_layout()
        st.pyplot(fig)
        
        # ================= DOWNLOAD BUTTON (Bottom Left) =================
        col_left, col_right = st.columns([1, 3])
        with col_left:
            # Save plot to buffer
            buf = BytesIO()
            fig.savefig(buf, format="png", dpi=300, bbox_inches="tight")
            buf.seek(0)
            
            st.download_button(
                label="DOWNLOAD",
                data=buf,
                file_name=f"{plot_type.replace(' ', '_')}.png",
                mime="image/png",
                use_container_width=True
            )

    # =====================================================
    # MULTIVARIATE
    # =====================================================

    elif viz_type == "Multivariate":

        selected_cols = st.multiselect(
            "Select Columns (Min 3)", all_cols
        )

        if len(selected_cols) >= 3:

            numeric_selected = [
                col for col in selected_cols
                if col in numeric_cols
            ]

            plot_type = st.selectbox(
                "Select Plot Type",
                ["Pairplot", "Correlation Heatmap"]
            )

            if plot_type == "Pairplot":

                if len(numeric_selected) >= 2:
                    pairplot_fig = sns.pairplot(df[numeric_selected], height=2.5)
                    st.pyplot(pairplot_fig)
                    
                    # ================= DOWNLOAD BUTTON (Bottom Left) =================
                    col_left, col_right = st.columns([1, 3])
                    with col_left:
                        # Save plot to buffer
                        buf = BytesIO()
                        pairplot_fig.savefig(buf, format="png", dpi=300, bbox_inches="tight")
                        buf.seek(0)
                        
                        st.download_button(
                            label="DOWNLOAD",
                            data=buf,
                            file_name="Pairplot.png",
                            mime="image/png",
                            use_container_width=True
                        )
                else:
                    st.warning("Select at least 2 numeric columns")

            elif plot_type == "Correlation Heatmap":

                if len(numeric_selected) >= 2:
                    # Smaller figure size for heatmap
                    fig, ax = plt.subplots(figsize=(8, 6))
                    sns.heatmap(
                        df[numeric_selected].corr(),
                        annot=True,
                        fmt=".2f",
                        ax=ax
                    )
                    plt.tight_layout()
                    st.pyplot(fig)
                    
                    # ================= DOWNLOAD BUTTON (Bottom Left) =================
                    col_left, col_right = st.columns([1, 3])
                    with col_left:
                        # Save plot to buffer
                        buf = BytesIO()
                        fig.savefig(buf, format="png", dpi=300, bbox_inches="tight")
                        buf.seek(0)
                        
                        st.download_button(
                            label="DOWNLOAD",
                            data=buf,
                            file_name="Correlation_Heatmap.png",
                            mime="image/png",
                            use_container_width=True
                        )
                else:
                    st.warning("Select at least 2 numeric columns")

        else:
            st.warning("Select at least 3 columns")