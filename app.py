# import streamlit as st
# import pandas as pd
# from datetime import datetime
# from io import BytesIO

# st.title("Excel Transformer")

# # Upload Excel file
# uploaded_file = st.file_uploader("📂 Upload your Excel file", type=["xlsx", "xls"])

# if uploaded_file:
#     try:
#         # Read the Excel file
#         df = pd.read_excel(uploaded_file)

#         # 🔥 Normalize headers (remove spaces + lowercase)
#         df.columns = df.columns.str.replace(r"\s+", "", regex=True).str.lower()

#         # Get current year
#         current_year = datetime.now().year

#         # Transform 'numero'
#         df["numero"] = df["numero"].apply(lambda x: f"CD/{current_year}/{int(x):06d}")

#         # Map columns
#         df["ligne de facture/libelé"] = df["libelle"]
#         df["ligne de facture/debit"] = df["debit"]
#         df["ligne de facture/credit"] = df["credit"]

#         # Map input 'compte' if it exists
#         df["ligne de facture/compte"] = df["compte"] if "compte" in df.columns else ""

#         # Fill 'journal' column by default
#         df["journal"] = "Caisse"

#         # Hide date, numero, ref if same as previous row
#         if "ref" not in df.columns:
#             df["ref"] = ""  # create empty ref if not exists
#         df.loc[df["date"] == df["date"].shift(1), ["date", "numero", "ref"]] = ""

#         # Reorder final columns
#         final_df = df[[
#             "date",
#             "numero",
#             "ref",
#             "journal",
#             "ligne de facture/compte",
#             "ligne de facture/libelé",
#             "ligne de facture/debit",
#             "ligne de facture/credit"
#         ]]

#         st.success("✅ Excel transformed successfully!")

#         # Convert to Excel for download
#         towrite = BytesIO()
#         final_df.to_excel(towrite, index=False, engine='xlsxwriter')
#         towrite.seek(0)

#         st.download_button(
#             label="📥 Download Processed Excel",
#             data=towrite,
#             file_name="output_transformed.xlsx",
#             mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
#         )

#     except Exception as e:
#         st.error(f"❌ An error occurred: {e}")


import streamlit as st
import pandas as pd
from datetime import datetime
from io import BytesIO

st.title("Excel Transformer")

# Upload Excel file
uploaded_file = st.file_uploader("📂 Upload your Excel file", type=["xlsx", "xls"])

if uploaded_file:
    try:
        # Read the Excel file
        df = pd.read_excel(uploaded_file)

        # 🔥 Normalize headers (remove spaces + lowercase)
        df.columns = df.columns.str.replace(r"\s+", "", regex=True).str.lower()

        # Get current year
        current_year = datetime.now().year

        # Transform 'numero' safely (handle empty or NaN)
        if "numero" in df.columns:
            df["numero"] = df["numero"].apply(
                lambda x: f"CD/{current_year}/{int(x):06d}" if pd.notna(x) and x != "" else ""
            )
        else:
            df["numero"] = ""

        # Map columns safely
        df["ligne de facture/libelé"] = df["libelle"] if "libelle" in df.columns else ""
        df["ligne de facture/debit"] = df["debit"] if "debit" in df.columns else 0
        df["ligne de facture/credit"] = df["credit"] if "credit" in df.columns else 0
        df["ligne de facture/compte"] = df["compte"] if "compte" in df.columns else ""

        # Fill 'journal' column by default
        df["journal"] = "Caisse"

        # Ensure 'date' and 'ref' columns exist
        if "date" not in df.columns:
            df["date"] = ""
        if "ref" not in df.columns:
            df["ref"] = ""

        # Hide date, numero, ref if same as previous row
        df.loc[df["date"] == df["date"].shift(1), ["date", "numero", "ref"]] = ""

        # Reorder final columns
        final_columns = [
            "date",
            "numero",
            "ref",
            "journal",
            "ligne de facture/compte",
            "ligne de facture/libelé",
            "ligne de facture/debit",
            "ligne de facture/credit"
        ]
        # Keep only existing columns to avoid errors
        final_df = df[[col for col in final_columns if col in df.columns]]

        st.success("✅ Excel transformed successfully!")

        # Convert to Excel for download
        towrite = BytesIO()
        final_df.to_excel(towrite, index=False, engine='xlsxwriter')
        towrite.seek(0)

        st.download_button(
            label="📥 Download Processed Excel",
            data=towrite,
            file_name="output_transformed.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        st.error(f"❌ An error occurred: {e}")
