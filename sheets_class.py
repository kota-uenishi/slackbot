#-------------Sheets API の機能をまとめたクラス--------------
import json
import requests

class SheetsAPI():

    # Sheets API に必要な引数
    SHEET_ID = ''
    SHEETS_API_TOKEN = ''

    # Sheets API を使ってスプレッドシートの内容を取得する関数
    def get_contents_from_sheet(self, sheet_name, major_dimension='ROWS'):
        # Sheets API の URL を作成
        SHEETS_API_URL = 'https://sheets.googleapis.com/v4/spreadsheets/' + self.SHEET_ID + '/values/' + sheet_name
        # majorDimension には ROWS または COLUMNSを指定 リストの基準となる軸方向の指定が可能
        payload = {
            'key': self.SHEETS_API_TOKEN,
            'majorDimension': major_dimension,
        }
        # try-except文
        try:
            req = requests.get(
                SHEETS_API_URL,
                params=payload,
            ).json()
            return req['values']
        except requests.exceptions.RequestException as e:
            print('Error: ', e)
