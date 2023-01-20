from oauth2client.service_account import ServiceAccountCredentials
import gspread
import pandas as pd


class google_sheet:
    def __init__(self) -> None:
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive",
        ]

        json_path = 'google1.json'
        credential = ServiceAccountCredentials.from_json_keyfile_name(
            json_path, scope)
        self.gc = gspread.authorize(credential)

    def worksheet_loads(self, url: str):
        file = self.gc.open_by_url(url)
        worksheets = file.worksheets()
        return worksheets

    def find_rows(self, worksheets: list, query: str):
        for worksheet in worksheets:
            cells = worksheet.findall(query)
            print(worksheet)
            for cell in cells:
                row = int(str(cell).split(' ')[1].split('R')[1].split('C')[0])
                print(row, worksheet.row_values(row))
            print('\n\n')

    def sheets_result_pandas(self, worksheets: list, input: str) -> None:
        pd.options.display.max_rows = None
        pd.options.display.max_columns = None
        for worksheet in worksheets:
            data = worksheet.get_all_values()
            df = pd.DataFrame(data)
            print('-'*30+'\n')
            print(worksheet)
            print(df[(df[1].str.contains(input)) | (
                df[2].str.contains(input)) | (df[3].str.contains(input))])
            print('\n')
