#-------------チャンネル新規参加者に対して案内メッセージ送信とプライベートチャンネルの招待をする機能--------------
import json
from slack_class import SlackAPI
from sheets_class import SheetsAPI

# 定義したクラスをインポート
slack_api = SlackAPI()
sheets_api = SheetsAPI()

# メンバー対象とする強制参加チャンネルID
CHANNEL_ID = 'C00000000'
# 追加するチャンネルIDをまとめたスプレッドシート名
CHANNEL_ID_SHEET_NAME = 'channel_id'
# 送信する案内文をまとめたスプレッドシート名
TEXT_SHEET_NAME = 'text'

# 前回取得した結果の userlist がある json ファイルをインポート
old_user_list = open('user_list.json', 'r')

# 現在のチャンネルのメンバーを取得
new_user_list = slack_api.get_conversation_members(
    channel_id=CHANNEL_ID,
)

# 新規参加者いればメッセージを送信
# set関数で集合に変換し,その差分で新規メンバーを抽出し、その集合の長さで判定する
if len(set(new_user_list) - set(old_user_list)) != 0:

    # set関数で集合に変換し、その差分で新規メンバーを抽出
    new_participants = list(set(new_user_list) - set(old_user_list))

    # 追加するチャンネルIDをスプレッドシートから取得
    channel_id_list = sheets_api.get_contents_from_sheet(
        sheet_name=TEXT_SHEET_NAME,
    )
    # 送信する内容をスプレッドシートから取得
    text_list = sheets_api.get_contents_from_sheet(
        sheet_name=CHANNEL_ID_SHEET_NAME,
    )
    
    # for文を使って処理を行う
    for new_user_id in new_participants:
        # チャンネルに招待
        for channel_id in channel_id_list:
            slack_api.invite_conversation(
                channel_id=channel_id[0],
                user_id=new_user_id,
            )
        # 案内文をDMで送信
        for text in text_list:
            # 空要素があればpass
            if len(text) == 0:
                continue
            slack_api.chat_message(
                id=channel_id,
                text=text,
            )

# 今回取得した userlist のファイルを上書き保存
with open('user_list.json', 'w') as f:
    json.dump(new_user_list, f, indent=4)