import python_socks

# https://my.telegram.org/apps
api_id = 1234567 # tg API ID
api_hash = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa' # tg API hash
bot_token = '123456:ABcderfg' # tg bot token
sock_server = (python_socks.ProxyType.SOCKS5, '127.0.0.1', 1080) # tg proxy
# For the chatgpt config please go here:
# https://github.com/acheong08/ChatGPT/wiki/Setup
config = {
    # "ema#il": "<YOUR_EMAIL>",
    # "password": "<YOUR_PASSWORD>",
    # "session_token": "<YOUR_SESSIO_TOKEN>", # token保存在文件chatgpt_session.txt中
    # "proxy": "socks5://127.0.0.1:1080"
}