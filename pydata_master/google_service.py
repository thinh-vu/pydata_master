# Copyright 2022 Thinh Vu @ GitHub
# See LICENSE for details.
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
import gspread
from df2gspread import df2gspread as d2g

def google_auth(json_cred_path):
    """
    Return a creds and gc to use Authenticate the Google service
    Args:
        json_cred_path (:obj:`str`, required): The path to the service account credential in json format.
    """
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(json_cred_path, scope)
    gc = gspread.authorize(creds)
    return creds, gc

def read_gsheet(sheet_id, sheet_name, gc):
    """
    Read a Google Sheets file to return a DataFrame. Given the fact that the target Google Sheets file has been shared to your Google Service Account.
    Args:
        sheet_id (:obj:`str`, required): Google Sheets ID. Ex: `YOUR_SHEET_ID` in the URI`https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit`
        sheet_name (:obj:`str`, required): Name of the worksheet
        gc (:obj, required): gc be assigned as to the result of google_auth() function.
    """
    wks = gc.open_by_key(sheet_id)
    worksheet = wks.worksheet(sheet_name)
    df = pd.DataFrame(worksheet.get_all_records())
    return df

def save_gsheet (dataframe, sheet_id, sheet_name, creds, row_names=False, clean=False, df_size=False, start_cell='A1'):
    """
    Export a DataFrame to Google Sheets file. Given the fact that the target Google Sheets file has been shared to your Google Service Account.
    Args:
        sheet_id (:obj, required): Target DataFrame to export.
        sheet_id (:obj:`str`, required): Google Sheets ID. Ex: `YOUR_SHEET_ID` in the URI`https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit`
        sheet_name (:obj:`str`, required): Name of the worksheet
        creds (:obj, required): creds be assigned as to the result of google_auth() function.
        rows_name (:obj:`boolean`, required): False as the default value.
        clean (:obj, required): False as the default value.
        df_size(:obj, required): False as the default value.
        start_cell (:obj, required): 'A1' as the default value.
    """
    wks = gc.open_by_key(sheet_id)
    d2g.upload(dataframe, sheet_id, sheet_name, credentials=creds, row_names=row_names, clean = clean, df_size = df_size, start_cell=start_cell)
    'https://docs.google.com/spreadsheets/d/' + sheet_id

def save_gspread (dataframe, sheet_id, sheet_name, gc):
    """
    Read a Google Sheets file to return a DataFrame. Given the fact that the target Google Sheets file has been shared to your Google Service Account.
    Args:
        sheet_id (:obj:`str`, required): Google Sheets ID. Ex: `YOUR_SHEET_ID` in the URI`https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit`
        sheet_name (:obj:`str`, required): Name of the worksheet
        gc (:obj, required): gc be assigned as to the result of google_auth() function.
    """
    try:
        wks = gc.open_by_key(sheet_id)
        wks.worksheet(sheet_name).update([dataframe.columns.values.tolist()] + dataframe.values.tolist())
    except:
        wks = gc.open_by_key(sheet_id)
        rows, columns = dataframe.shape
        wks.add_worksheet(title=sheet_name, rows=rows, cols=columns)
        wks.worksheet(sheet_name).update([dataframe.columns.values.tolist()] + dataframe.values.tolist())
        message = 'Data Frame has been exported to https://docs.google.com/spreadsheets/d/' + sheet_id
    return message