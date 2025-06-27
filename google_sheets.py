# google_sheets.py
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

def connect_to_sheet(sheet_name):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
    client = gspread.authorize(creds)
    return client.open(sheet_name)

def log_to_sheet(sheet, tab_name, df):
    try:
        try:
            ws = sheet.worksheet(tab_name)
        except:
            ws = sheet.add_worksheet(title=tab_name, rows=1000, cols=20)

        ws.clear()

        # Reset index and remove unnamed columns
        df_to_upload = df.reset_index()
        df_to_upload.columns = [str(col) for col in df_to_upload.columns]  # Ensure all are strings

        # Convert all values to string (fixes serialization issue)
        values = df_to_upload.astype(str).values.tolist()
        ws.update([df_to_upload.columns.tolist()] + values)

    except Exception as e:
        print(f"Sheet update error: {e}")

