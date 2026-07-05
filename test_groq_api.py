import requests
import json
import os

# 環境変数からAPIキーを取得
api_key = os.environ.get('GROQ_API_KEY', '')

if not api_key:
    print("❌ 環境変数 GROQ_API_KEY が設定されていません")
    exit(1)

# Groq API endpoint
url = "https://api.groq.com/openai/v1/chat/completions"

# リクエストヘッダー
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# 最小限のリクエストペイロード
payload = {
    "model": "llama-3.1-8b-instant",
    "messages": [
        {"role": "user", "content": "Hello"}
    ],
    "max_tokens": 10
}

print("📡 Groq APIに接続テスト中...")
print(f"🔑 APIキー: {api_key[:20]}... (先頭20文字)")
print(f"🌐 エンドポイント: {url}")
print()

try:
    response = requests.post(url, headers=headers, json=payload, timeout=30)
    
    print(f"📊 ステータスコード: {response.status_code}")
    print()
    
    if response.status_code == 200:
        print("✅ 接続成功！APIキーは有効です。")
        result = response.json()
        print(f"📝 レスポンス: {result['choices'][0]['message']['content']}")
    elif response.status_code == 401:
        print("❌ 401 Unauthorized - APIキーが無効または期限切れです")
        print(f"🔍 エラー詳細: {response.text}")
        print()
        print("💡 解決策:")
        print("1. Groq Consoleで新しいAPIキーを作成: https://console.groq.com/keys")
        print("2. 環境変数を更新:")
        print("   [Environment]::SetEnvironmentVariable('GROQ_API_KEY', '新しいキー', 'User')")
    else:
        print(f"⚠️ 予期しないステータスコード: {response.status_code}")
        print(f"🔍 レスポンス: {response.text}")
        
except requests.exceptions.Timeout:
    print("⏱️ タイムアウト: Groq APIへの接続がタイムアウトしました")
except requests.exceptions.RequestException as e:
    print(f"❌ 接続エラー: {e}")
