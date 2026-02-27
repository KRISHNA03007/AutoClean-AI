import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import skew
from sklearn.preprocessing import PowerTransformer
from io import BytesIO

st.set_page_config(page_title="Clean Data", layout="wide")

# ============================================================
# HOME BUTTON (TOP RIGHT) - CHANGED TO RIGHT SIDE
# ============================================================
col1, col2, col_home = st.columns([8, 1, 1])  # Changed column ratios to push button to right

with col_home:
    if st.button("HOME", use_container_width=True, key="home_btn"):
        st.switch_page("app.py")

# Button Styling
st.markdown("""
<style>
div.stButton > button {
    background-color: #ff6b6b !important;
    color: white !important;
    font-weight: 700 !important;
}

.custom-table {
    width: 80%;
    margin-left: auto;
    margin-right: auto;
    border-collapse: collapse;
    font-size: 14px;
}
.custom-table th, .custom-table td {
    border: 2px solid black !important;
    text-align: center !important;
    padding: 6px;
}
.custom-table th {
    font-weight: 800;
    background-color: #f2f2f2;
    color: black;
}
</style>
""", unsafe_allow_html=True)

st.title("Clean Data")

# ============================================================
# SESSION STATE
# ============================================================
if "original_df" not in st.session_state:
    st.session_state.original_df = None

if "cleaned_df" not in st.session_state:
    st.session_state.cleaned_df = None

# Add a version counter to force UI updates
if "update_counter" not in st.session_state:
    st.session_state.update_counter = 0

# ============================================================
# FILE UPLOAD (FIXED — LOADS ONLY ONCE)
# ============================================================
uploaded_file = st.file_uploader(
    "Upload Dataset (CSV, Excel, Parquet)",
    type=["csv", "xlsx", "xls", "parquet"]
)

# VERY IMPORTANT FIX: Load only once
if uploaded_file is not None and st.session_state.original_df is None:
    file_type = uploaded_file.name.split(".")[-1]

    if file_type == "csv":
        df = pd.read_csv(uploaded_file)
    elif file_type in ["xlsx", "xls"]:
        df = pd.read_excel(uploaded_file)
    elif file_type == "parquet":
        df = pd.read_parquet(uploaded_file)
    else:
        st.error("Unsupported file type")
        st.stop()

    st.session_state.original_df = df.copy()
    st.session_state.cleaned_df = df.copy()
    st.session_state.update_counter += 1

# ============================================================
# MAIN WORKFLOW
# ============================================================
if st.session_state.cleaned_df is not None:

    df = st.session_state.cleaned_df

    # ---------------- Columns & Dtypes ----------------
    st.subheader("Columns and Data Types")

    col_info = pd.DataFrame({
        "Column Name": df.columns,
        "Data Type": df.dtypes.astype(str)
    })

    st.markdown(col_info.to_html(index=False, classes="custom-table"),
                unsafe_allow_html=True)

    # ---------------- Missing & Skewness ----------------
    st.subheader("Missing Values and Skewness")

    missing = df.isnull().sum()
    numeric_cols = df.select_dtypes(include=np.number).columns

    skewness = []
    for col in df.columns:
        if col in numeric_cols:
            skewness.append(round(skew(df[col].dropna()), 3))
        else:
            skewness.append("N/A")

    summary_df = pd.DataFrame({
        "Column": df.columns,
        "Missing Values": missing.values,
        "Skewness": skewness
    })

    st.markdown(summary_df.to_html(index=False, classes="custom-table"),
                unsafe_allow_html=True)

    # ---------------- Duplicates ----------------
    st.subheader("Duplicate Records")
    duplicate_count = df.duplicated().sum()
    st.write(f"Total Duplicate Rows: {duplicate_count}")

    # ============================================================
    # COLUMN OPERATIONS
    # ============================================================
    st.subheader("Column Operations")

    # Use a unique key that depends on update_counter to force refresh
    col_to_drop = st.selectbox("Select Column to Drop", df.columns, 
                               key=f"drop_col_{st.session_state.update_counter}")

    c1, c2, _ = st.columns([1,1,6])
    with c1:
        if st.button("Drop", key=f"drop_column_btn_{st.session_state.update_counter}"):
            df = df.drop(columns=[col_to_drop])
            st.session_state.cleaned_df = df
            st.session_state.update_counter += 1
            st.rerun()
    with c2:
        if st.button("Reset", key=f"reset_drop_column_btn_{st.session_state.update_counter}"):
            st.session_state.cleaned_df = st.session_state.original_df.copy()
            st.session_state.update_counter += 1
            st.rerun()

    # ---------------- Rename Column ----------------
    st.subheader("Rename Column")

    col_to_rename = st.selectbox("Select Column", df.columns, 
                                 key=f"rename_col_{st.session_state.update_counter}")
    new_name = st.text_input("New Column Name", key=f"new_name_{st.session_state.update_counter}")

    c3, c4, _ = st.columns([1,1,6])
    with c3:
        if st.button("Apply", key=f"rename_apply_btn_{st.session_state.update_counter}"):
            if new_name.strip():
                df = df.rename(columns={col_to_rename: new_name})
                st.session_state.cleaned_df = df
                st.session_state.update_counter += 1
                st.rerun()
    with c4:
        if st.button("Reset", key=f"rename_reset_btn_{st.session_state.update_counter}"):
            st.session_state.cleaned_df = st.session_state.original_df.copy()
            st.session_state.update_counter += 1
            st.rerun()

    # ---------------- Change Data Type ----------------
    st.subheader("Change Data Type")

    col_dtype = st.selectbox("Select Column", df.columns, 
                             key=f"dtype_col_{st.session_state.update_counter}")
    dtype_option = st.selectbox("New Data Type", ["int", "float", "str"],
                               key=f"dtype_option_{st.session_state.update_counter}")

    c5, c6, _ = st.columns([1,1,6])
    with c5:
        if st.button("Apply", key=f"dtype_apply_btn_{st.session_state.update_counter}"):
            try:
                df[col_dtype] = df[col_dtype].astype(dtype_option)
                st.session_state.cleaned_df = df
                st.session_state.update_counter += 1
                st.rerun()
            except Exception as e:
                st.error(f"Type conversion failed: {str(e)}")
    with c6:
        if st.button("Reset", key=f"dtype_reset_btn_{st.session_state.update_counter}"):
            st.session_state.cleaned_df = st.session_state.original_df.copy()
            st.session_state.update_counter += 1
            st.rerun()

    # ============================================================
    # HANDLE MISSING VALUES
    # ============================================================
    st.subheader("Handle Missing Values")

    selected_col = st.selectbox("Select Column", df.columns, 
                                key=f"missing_col_{st.session_state.update_counter}")

    if df[selected_col].dtype in ["int64", "float64"]:
        method = st.selectbox("Method",
                              ["Drop", "0", "Mean", "Median", "Custom Value"],
                              key=f"method_num_{st.session_state.update_counter}")
        custom_val = None
        if method == "Custom Value":
            custom_val = st.number_input("Enter Custom Value", 
                                        key=f"custom_num_{st.session_state.update_counter}")
    else:
        method = st.selectbox("Method",
                              ["Drop", "Mode", "Custom Value"],
                              key=f"method_cat_{st.session_state.update_counter}")
        custom_val = None
        if method == "Custom Value":
            custom_val = st.text_input("Enter Custom Value", 
                                      key=f"custom_cat_{st.session_state.update_counter}")

    c7, c8, _ = st.columns([1,1,6])
    with c7:
        if st.button("Apply", key=f"missing_apply_btn_{st.session_state.update_counter}"):
            try:
                if method == "Drop":
                    df = df.dropna(subset=[selected_col])
                elif method == "Mean":
                    df[selected_col] = df[selected_col].fillna(df[selected_col].mean())
                elif method == "Median":
                    df[selected_col] = df[selected_col].fillna(df[selected_col].median())
                elif method == "Mode":
                    df[selected_col] = df[selected_col].fillna(df[selected_col].mode()[0])
                elif method == "0":
                    df[selected_col] = df[selected_col].fillna(0)
                elif method == "Custom Value":
                    df[selected_col] = df[selected_col].fillna(custom_val)

                st.session_state.cleaned_df = df
                st.session_state.update_counter += 1
                st.rerun()
            except Exception as e:
                st.error(f"Error handling missing values: {str(e)}")
    with c8:
        if st.button("Reset", key=f"missing_reset_btn_{st.session_state.update_counter}"):
            st.session_state.cleaned_df = st.session_state.original_df.copy()
            st.session_state.update_counter += 1
            st.rerun()

    # ============================================================
    # HANDLE DUPLICATES
    # ============================================================
    st.subheader("Handle Duplicates")

    c9, c10, _ = st.columns([1,1,6])
    with c9:
        if st.button("Drop", key=f"duplicate_drop_btn_{st.session_state.update_counter}"):
            df = df.drop_duplicates()
            st.session_state.cleaned_df = df
            st.session_state.update_counter += 1
            st.rerun()
    with c10:
        if st.button("Reset", key=f"duplicate_reset_btn_{st.session_state.update_counter}"):
            st.session_state.cleaned_df = st.session_state.original_df.copy()
            st.session_state.update_counter += 1
            st.rerun()

    # ============================================================
    # SKEWNESS TRANSFORMATION
    # ============================================================
    st.subheader("Skewness Transformation")

    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()

    if len(numeric_cols) > 0:
        skew_col = st.selectbox("Select Numeric Column", numeric_cols,
                                key=f"skew_col_{st.session_state.update_counter}")
        transform_method = st.selectbox("Transformation Method",
                                        ["Box-Cox", "Yeo-Johnson"],
                                        key=f"transform_{st.session_state.update_counter}")

        c11, c12, _ = st.columns([1,1,6])
        with c11:
            if st.button("Apply", key=f"skew_apply_btn_{st.session_state.update_counter}"):
                try:
                    method = "box-cox" if transform_method == "Box-Cox" else "yeo-johnson"
                    pt = PowerTransformer(method=method)
                    reshaped = df[[skew_col]].dropna()
                    transformed = pt.fit_transform(reshaped)
                    df.loc[reshaped.index, skew_col] = transformed
                    st.session_state.cleaned_df = df
                    st.session_state.update_counter += 1
                    st.rerun()
                except Exception as e:
                    if transform_method == "Box-Cox":
                        st.error("Box-Cox requires positive values.")
                    else:
                        st.error(f"Transformation failed: {str(e)}")
        with c12:
            if st.button("Reset", key=f"skew_reset_btn_{st.session_state.update_counter}"):
                st.session_state.cleaned_df = st.session_state.original_df.copy()
                st.session_state.update_counter += 1
                st.rerun()
    else:
        st.info("No numeric columns available for skewness transformation.")

    # ============================================================
    # PREVIEW
    # ============================================================
    st.subheader("Cleaned Dataset Preview")

    preview_df = st.session_state.cleaned_df.head()
    st.markdown(preview_df.to_html(index=False, classes="custom-table"),
                unsafe_allow_html=True)

    # ============================================================
    # DOWNLOAD
    # ============================================================
    st.subheader("Download Cleaned Dataset")

    download_format = st.selectbox("Select Format",
                                   ["CSV", "Excel", "Parquet"],
                                   key=f"download_{st.session_state.update_counter}")

    df_download = st.session_state.cleaned_df

    def convert_csv(df):
        return df.to_csv(index=False).encode("utf-8")

    def convert_excel(df):
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
            df.to_excel(writer, index=False, sheet_name="Cleaned_Data")
        return buffer.getvalue()

    def convert_parquet(df):
        buffer = BytesIO()
        df.to_parquet(buffer, index=False)
        return buffer.getvalue()

    if download_format == "CSV":
        data = convert_csv(df_download)
        file_name = "cleaned_data.csv"
        mime = "text/csv"
    elif download_format == "Excel":
        data = convert_excel(df_download)
        file_name = "cleaned_data.xlsx"
        mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    else:
        data = convert_parquet(df_download)
        file_name = "cleaned_data.parquet"
        mime = "application/octet-stream"

    colA, colB, colC = st.columns([3,2,3])
    with colB:
        st.download_button("DOWNLOAD FILE",
                           data=data,
                           file_name=file_name,
                           mime=mime,
                           use_container_width=True,
                           key=f"download_btn_{st.session_state.update_counter}")