#-------------該当ユーザーをチャンネル退出させる機能--------------
import json
from slack_class import SlackAPI

# 定義したクラスをインポート
slack_api = SlackAPI()

# メールアドレスのリスト
email_address_list = [
    'example@info.com',
]

# ユーザーIDのリスト
user_id_list = [] 

# メールアドレスからユーザーIDをリスト形式で取得
for email_address in email_address_list:
    user_id = slack_api.get_user_id_by_email(
        email_address=email_address,
    )
    user_id_list.append(user_id)

# ワークスペースの全てのチャンネルのチャンネルIDを取得
channel_id_list = slack_api.get_conversations()

# 全てのプライベートチャンネルにおいて、該当ユーザーが参加していれば退出させる処理を実行
for user_id in user_id_list:
    for channel_id in channel_id_list:
        slack_api.kick_conversation(
            user_id_list=user_id_list, 
            channel_id_list=channel_id_list
        )
