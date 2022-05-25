#-------------Slack API の機能をまとめたクラス--------------

import json
import requests

class SlackAPI():

    # OAuth Tokens
    SLACK_OAUTH_TOKEN = 'xoxb-00000-00000-00000-0000000'
    # Team ID
    TEAM_ID = 'T000000000'

    # Slack API URL
    USERS_LOOKUPBYEMAIL   = 'https://slack.com/api/users.lookupByEmail'  # https://api.slack.com/methods/users.lookupByEmail
    CONVERSATIONS_LIST    = 'https://slack.com/api/conversations.list'   # https://api.slack.com/methods/conversations.list
    CONVERSATIONS_INVITE  = 'https://slack.com/api/conversations.invite' # https://api.slack.com/methods/conversations.invite
    CONVERSATIONS_KICK    = 'https://slack.com/api/conversations.kick'   # https://api.slack.com/methods/conversations.kick
    CONVERSATIONS_MEMBERS = 'https://slack.com/api/conversations.members'# https://api.slack.com/methods/conversations.members
    CHAT_POSTMESSAGE      = 'https://slack.com/api/chat.postMessage'     # https://api.slack.com/methods/chat.postMessage
    CHAT_SCHEDULEDMESSAGE = 'https://slack.com/api/chat.scheduleMessage' # https://api.slack.com/methods/chat.scheduleMessage

    # 共通のヘッダーを構成
    headers = {
        'Authorization': 'Bearer ' + SLACK_OAUTH_TOKEN,
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    # メールアドレスからユーザーIDを取得する関数
    def get_user_id_by_email(self, email_address):
        payload = {
            # 引数にメールアドレスを指定
            'email': email_address,
        }
        # try-except文
        try:
            # リクエスト処理
            req = requests.post(
                self.LOOKUP_BY_EMAIL,
                payload,
                headers=self.headers,
            ).json()
            # リスポンスがTrueであれば、ユーザーIDをリストに代入
            if req['ok']:
                return req['user']['id']
        except requests.exceptions.RequestException as e:
            print('Error: ', e)

    # チャンネルに参加しているメンバーを取得する関数
    def get_conversation_members(self, channel_id):
        user_id_list, cursor = [], ''
        payload = {
            'channel': channel_id,
            'limit': 200,
            'cursor': cursor,
        }
        # try-except文
        try:
            # do-while文
            while True:
                # 上限200人までしか取得できないため、複数回に分けて取得
                req = requests.post(
                    self.CONVERSATIONS_MEMBERS,
                    data=payload,
                    headers=self.headers,
                ).json()
                user_id_list+= req['members']
                cursor = req['response_metadata']['next_cursor']
                # 全員のデータが集まれば break
                if not cursor:
                    break
            return user_id_list
        except requests.exceptions.RequestException as e:
            print('Error: ', e)
    
    # ワークスペースの全てのチャンネルを取得する関数
    def get_conversations(self, types='public_channel,private_channel'):
        channel_id_list = []
        payload = {
            # リストとして取得するチャンネルのタイプを指定
            'types': types,
        }
        try:
            # リクエスト処理
            req = requests.post(
                self.CONVERSATIONS_LIST,
                data=payload,
                headers=self.headers,
            ).json()
            # 得られた json データから channel ID のみを抽出してリストに代入
            for i in range(len(req['channels'])):
                channel_id_list.append(req['channels'][i]['id'])
        except requests.exceptions.RequestException as e:
            print('Error: ', e)
        return channel_id_list
    
    # チャンネルへの招待をする関数
    def invite_conversation(self, channel_id, user_id):
        payload = {
            'channel': channel_id,
            'users': user_id,
        }
        try:
            req = requests.post(
                self.CONVERSATIONS_INVITE,
                data=payload,
                headers=self.headers,
            ).json()
        except requests.exceptions.RequestException as e:
            print('Error: ', e)
    
    # 指定されたユーザーが該当するチャンネルに居れば退出させる関数
    def kick_conversation(self, user_id, channel_id):
        headers = self.headers
        payload = {
            # チャンネルIDを指定
            'channel': channel_id,
            # ユーザーIDを指定
            'user': user_id,
        }
        # try-except文
        try:
            # リクエスト処理
            req = requests.post(
                self.CONVERSATIONS_KICK,
                data=payload,
                headers=headers,
            ).json()
        except requests.exceptions.RequestException as e:
            print('Error: ', e)
    
    # メッセージを送信する関数
    def chat_message(self, id, text, time=None):
        payload = {
            # 送信するチャンネルIDまたはユーザーIDを指定
            # ユーザーIDを指定した場合はDMを送信する
            'channel': id,
            'text': text,
        }
        # try-excecpt文
        try:
            # timeがなければ、直後に送信
            if not time:
                req = requests.post(
                    self.CHAT_POSTMESSAGE,
                    data=payload,
                    headers=self.headers,
                ).json()
            # timeが指定されていれば、メッセージをスケジューリング
            else:
                # postリクエストの引数を追加
                payload['post_at'] = time
                req = requests.post(
                    self.CHAT_SCHEDULEDMESSAGE,
                    data=payload,
                    headers=self.headers,
                ).json()
        except requests.exceptions.RequestException as e:
            print('Error: ', e)