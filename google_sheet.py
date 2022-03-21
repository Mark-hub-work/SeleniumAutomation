import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint


class GoogleSheet:
    def __init__(self, sheetname):
        self.sheetname = sheetname
        self.scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
        self.creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", self.scope)
        self.client = gspread.authorize(self.creds)

    def find_empty_cell(self, row):
        # note the numbering of the columns in google sheets starts with A = 1
        col = 2
        sheet = self.client.open(self.sheetname).sheet1
        cell = sheet.cell(row, col)
        while(cell.value != None):
            pprint(cell)
            col += 1
            cell = sheet.cell(row, col)
        pprint(cell)

        return col

    def getCell(self, row, column):
        sheet = self.client.open(self.sheetname).sheet1
        cell = sheet.cell(row, column).value
        pprint(cell)

    def update_cell(self, row, col, value):
        sheet = self.client.open(self.sheetname).sheet1
        sheet.update_cell(row, col, value)
        cell = sheet.cell(row, col)
        pprint(cell)

