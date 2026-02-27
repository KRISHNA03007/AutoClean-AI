# pages/Quick_Insights.py
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
import tempfile
import matplotlib
matplotlib.use('Agg')

# -------------------- PAGE CONFIG --------------------
st.set_page_config(page_title="Quick Insights - AutoClean AI", layout="wide")

# -------------------- SESSION STATE --------------------
if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None
if "df" not in st.session_state:
    st.session_state.df = None

# -------------------- CUSTOM CSS --------------------
st.markdown("""
<style>
.section-title { font-size:2rem; text-align:center; color:#ff6b6b; font-weight:700; margin:20px 0 10px 0; }
.dataframe { width:100%; border:2px solid #000; border-collapse:collapse; margin:10px 0; font-size:1.1rem; }
.dataframe th, .dataframe td { border:2px solid #000 !important; text-align:center; padding:8px; font-size:1.1rem; }
.dataframe th { font-weight:700; background:#f0f0f0; }
.stApp { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); }
</style>
""", unsafe_allow_html=True)

# -------------------- BUTTONS LAYOUT --------------------
col1, col2, col3 = st.columns([8,1,1])

with col3:  # Move to extreme right
    if st.button("HOME", use_container_width=True):
        st.session_state.uploaded_file = None
        st.session_state.df = None
        st.switch_page("app.py")

# Red background with white text for HOME button
st.markdown("""
<style>
div.stButton > button {
    background-color: #ff6b6b !important;
    color: white !important;
    font-weight: 700 !important;
}
</style>
""", unsafe_allow_html=True)

# Dark + Bold Styling for HOME button
st.markdown("""
<style>
div.stButton > button {
    font-weight: 800 !important;
    color: #000000 !important;
}
</style>
""", unsafe_allow_html=True)

# -------------------- HEADER --------------------
st.markdown('<h1 class="section-title">Quick Insights</h1>', unsafe_allow_html=True)

# -------------------- FILE UPLOAD --------------------
uploaded_file = st.file_uploader("Upload your dataset (CSV, Excel, Parquet)", 
                                 type=["csv","xlsx","xls","parquet"])

if uploaded_file:
    st.session_state.uploaded_file = uploaded_file

if st.session_state.uploaded_file:
    uploaded_file = st.session_state.uploaded_file
    file_type = uploaded_file.name.split('.')[-1]
    try:
        if file_type in ["xlsx","xls"]:
            df = pd.read_excel(uploaded_file)
        elif file_type=="csv":
            df = pd.read_csv(uploaded_file)
        elif file_type=="parquet":
            df = pd.read_parquet(uploaded_file)
        else:
            st.error("Unsupported file type")
            st.stop()
        st.session_state.df = df
    except Exception as e:
        st.error(f"Error reading file: {str(e)}")
        st.stop()

# -------------------- DISPLAY DATA & ANALYSIS --------------------
if st.session_state.df is not None:
    df = st.session_state.df

    # --- File Overview ---
    st.markdown('<h2 class="section-title">File Overview</h2>', unsafe_allow_html=True)
    file_size_bytes = uploaded_file.size

    if file_size_bytes < 1024:
        file_size_display = f"{file_size_bytes} Bytes"
    elif file_size_bytes < 1024 * 1024:
        file_size_display = f"{round(file_size_bytes / 1024, 2)} KB"
    else:
        file_size_display = f"{round(file_size_bytes / (1024 * 1024), 2)} MB"

    file_info = pd.DataFrame({
        "Attribute": ["File Name", "File Type", "File Size", "Rows", "Columns"],
        "Value": [
            uploaded_file.name,
            file_type.upper(),
            file_size_display,
            df.shape[0],
            df.shape[1]
        ]
    })
    st.markdown(file_info.to_html(index=False, classes="dataframe"), unsafe_allow_html=True)

    # --- Column Overview ---
    st.markdown('<h2 class="section-title">Columns Overview</h2>', unsafe_allow_html=True)
    col_info = pd.DataFrame({"Column Name":df.columns,"Data Type":df.dtypes.astype(str)})
    st.markdown(col_info.to_html(index=False, classes="dataframe"), unsafe_allow_html=True)

    # --- Dataset Sample ---
    st.markdown('<h2 class="section-title">Dataset Sample</h2>', unsafe_allow_html=True)
    st.markdown("**First 3 Rows:**")
    st.markdown(df.head(3).to_html(index=False, classes="dataframe"), unsafe_allow_html=True)
    st.markdown("**Last 3 Rows:**")
    st.markdown(df.tail(3).to_html(index=False, classes="dataframe"), unsafe_allow_html=True)

    # --- Summary Statistics ---
    st.markdown('<h2 class="section-title">Summary Statistics</h2>', unsafe_allow_html=True)
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object','category']).columns.tolist()

    if numeric_cols:
        st.markdown("**Numeric Columns:**")
        num_summary = df[numeric_cols].describe().T
        num_summary['median'] = df[numeric_cols].median()
        num_summary['skew'] = df[numeric_cols].skew().round(3)
        st.markdown(num_summary.to_html(classes="dataframe"), unsafe_allow_html=True)

    if categorical_cols:
        st.markdown("**Categorical Columns:**")
        cat_summary = pd.DataFrame({
            "Column": categorical_cols,
            "Unique Values":[df[c].nunique() for c in categorical_cols],
            "Most Frequent":[df[c].mode()[0] if not df[c].mode().empty else None for c in categorical_cols],
            "Frequency":[df[c].value_counts().iloc[0] if not df[c].value_counts().empty else None for c in categorical_cols]
        })
        st.markdown(cat_summary.to_html(index=False, classes="dataframe"), unsafe_allow_html=True)

    # --- Data Issues Overview ---
    st.markdown('<h2 class="section-title">Data Issues Overview</h2>', unsafe_allow_html=True)
    data_issues = pd.DataFrame({
        "Column":df.columns,
        "Missing Values":df.isnull().sum(),
        "Missing %":(df.isnull().sum()/len(df)*100).round(2),
        "Skewness":[df[c].skew() if np.issubdtype(df[c].dtype,np.number) else "N/A" for c in df.columns]
    })
    st.markdown(data_issues.to_html(index=False, classes="dataframe"), unsafe_allow_html=True)

    # --- Duplicates ---
    total_duplicates = df.duplicated().sum()
    st.markdown(f"<h3 style='font-size: 24px; margin: 10px 0; font-weight: 600;'>Total Duplicate Rows: {total_duplicates}</h3>", unsafe_allow_html=True)

    # --- Numeric Column Distributions (SMALLER SIZE) ---
    st.markdown('<h2 class="section-title">Numeric Column Distributions</h2>', unsafe_allow_html=True)
    if numeric_cols:
        cols_per_row = 3
        for i in range(0, min(len(numeric_cols), 6), cols_per_row):
            row_cols = st.columns(cols_per_row)
            for j, col in enumerate(numeric_cols[i:i+cols_per_row]):
                with row_cols[j]:
                    fig, ax = plt.subplots(figsize=(2.5, 2.5))
                    sns.histplot(df[col].dropna(), kde=True, color='#ff6b6b', ax=ax)
                    ax.set_xlabel(col, fontsize=8)
                    ax.set_ylabel('')
                    ax.tick_params(labelsize=6)
                    st.pyplot(fig)
                    plt.close(fig)

    # --- Correlation Analysis (SMALLER SIZE IN STREAMLIT) ---
    if len(numeric_cols) > 1:
        st.markdown('<h2 class="section-title">Correlation Analysis</h2>', unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(4, 3))
        sns.heatmap(df[numeric_cols].corr(), annot=True, cmap='coolwarm', center=0, 
                    linewidths=1, ax=ax, annot_kws={'size':8}, fmt='.2f')
        ax.tick_params(labelsize=8)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    # -------------------- PDF REPORT FUNCTION --------------------
    def generate_pdf():
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []

        # Title
        title_style = ParagraphStyle('title', parent=styles['Heading1'], alignment=TA_CENTER, fontSize=22, textColor=colors.HexColor('#ff6b6b'))
        story.append(Paragraph("Quick Insights Report", title_style))
        story.append(Spacer(1,20))

        # Helper function to convert DataFrame to ReportLab Table
        def df_to_table(df):
            # Convert DataFrame to list of lists
            data = [df.columns.tolist()] + df.values.tolist()
            table = Table(data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            return table

        # 1. File Overview
        story.append(Paragraph("1. File Overview", styles['Heading2']))
        story.append(Spacer(1,8))
        file_info_table = df_to_table(file_info)
        story.append(file_info_table)
        story.append(Spacer(1,15))

        # 2. Columns Overview
        story.append(Paragraph("2. Columns Overview", styles['Heading2']))
        story.append(Spacer(1,8))
        col_info_table = df_to_table(col_info)
        story.append(col_info_table)
        story.append(Spacer(1,15))

        # 3. Dataset Sample
        story.append(Paragraph("3. Dataset Sample", styles['Heading2']))
        story.append(Spacer(1,8))
        story.append(Paragraph("First 3 Rows:", styles['Heading4']))
        first_rows = df.head(3)
        first_rows_table = df_to_table(first_rows.reset_index(drop=True))
        story.append(first_rows_table)
        story.append(Spacer(1,8))
        story.append(Paragraph("Last 3 Rows:", styles['Heading4']))
        last_rows = df.tail(3)
        last_rows_table = df_to_table(last_rows.reset_index(drop=True))
        story.append(last_rows_table)
        story.append(Spacer(1,15))

        # 4. Summary Statistics
        story.append(Paragraph("4. Summary Statistics", styles['Heading2']))
        story.append(Spacer(1,8))
        
        if numeric_cols:
            story.append(Paragraph("Numeric Columns:", styles['Heading4']))
            num_summary_reset = num_summary.reset_index()
            num_summary_reset.columns = ['Statistic'] + list(num_summary_reset.columns[1:])
            num_summary_table = df_to_table(num_summary_reset)
            story.append(num_summary_table)
            story.append(Spacer(1,8))

        if categorical_cols:
            story.append(Paragraph("Categorical Columns:", styles['Heading4']))
            cat_summary_table = df_to_table(cat_summary)
            story.append(cat_summary_table)
            story.append(Spacer(1,15))

        # 5. Data Issues Overview
        story.append(Paragraph("5. Data Issues Overview", styles['Heading2']))
        story.append(Spacer(1,8))
        data_issues_table = df_to_table(data_issues)
        story.append(data_issues_table)
        story.append(Spacer(1,8))

        # 6. Duplicates
        story.append(Paragraph(f"6. Total Duplicate Rows: {total_duplicates}", styles['Heading2']))
        story.append(Spacer(1,15))

        # 7. Numeric Column Distributions - LARGER IMAGES IN PDF
        if numeric_cols:
            story.append(Paragraph("7. Numeric Column Distributions", styles['Heading2']))
            story.append(Spacer(1,8))
            for col in numeric_cols[:6]:
                # Create larger figure for PDF with higher DPI
                fig, ax = plt.subplots(figsize=(6, 4))  # Larger figure size
                sns.histplot(df[col].dropna(), kde=True, ax=ax, color="#ff6b6b")
                ax.set_xlabel(col, fontsize=12)
                ax.set_ylabel('Frequency', fontsize=12)
                ax.tick_params(labelsize=10)
                img_path = tempfile.NamedTemporaryFile(delete=False, suffix=".png").name
                fig.savefig(img_path, bbox_inches="tight", dpi=150)  # Higher DPI for quality
                plt.close(fig)
                story.append(Paragraph(f"{col} Distribution", styles['Heading4']))
                story.append(Image(img_path, width=400, height=300))  # Much larger image in PDF
                story.append(Spacer(1,15))
            story.append(Spacer(1,8))

        # 8. Correlation Analysis - LARGER IMAGE IN PDF
        if len(numeric_cols) > 1:
            story.append(Paragraph("8. Correlation Analysis", styles['Heading2']))
            story.append(Spacer(1,8))
            # Create larger figure for PDF with higher DPI
            fig, ax = plt.subplots(figsize=(7, 6))  # Larger figure size
            sns.heatmap(df[numeric_cols].corr(), annot=True, cmap="coolwarm", center=0,
                        linewidths=1, ax=ax, annot_kws={'size':10}, fmt='.2f')
            ax.tick_params(labelsize=10)
            plt.tight_layout()
            img_path = tempfile.NamedTemporaryFile(delete=False, suffix=".png").name
            fig.savefig(img_path, bbox_inches="tight", dpi=150)  # Higher DPI for quality
            plt.close(fig)
            story.append(Image(img_path, width=450, height=400))  # Much larger image in PDF

        # Build PDF
        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()

    # -------------------- PDF DOWNLOAD BUTTON --------------------
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.download_button(
        label="DOWNLOAD PDF REPORT",
        data=generate_pdf(),
        file_name="Report.pdf",
        mime="application/pdf"
    )