
from google_auth_oauthlib.flow import InstalledAppFlow
import os

print("🚀 啟動簡易 Google Calendar 授權測試...")

SCOPES = ['https://www.googleapis.com/auth/calendar']

flow = InstalledAppFlow.from_client_secrets_file(
    'client_secret_146317806858-jnj12h153gpvr19krgbvutp2t5bpafnj.apps.googleusercontent.com.json',
    SCOPES
)

creds = flow.run_console()  # 手動貼上授權碼

# 寫入 token.json
with open('token.json', 'w') as token:
    token.write(creds.to_json())

print("✅ 授權完成，token.json 已建立！")
