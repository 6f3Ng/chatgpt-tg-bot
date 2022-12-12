#!/usr/bin/python3.9
import os
from telethon import TelegramClient, events, Button
from data import *
from revChatGPT.revChatGPT import AsyncChatbot as Chatbot
from cache import *

# yum install gcc libffi-devel python3-devel openssl-devel -y

cache = Cache()

if os.path.exists("chatgpt_session.txt"):
    with open("chatgpt_session.txt") as f:
        sessionStrs = f.readline().strip().split("|")
        config["cf_clearance"] = sessionStrs[0]
        config["session_token"] = sessionStrs[1]
        config["user_agent"] = sessionStrs[2]

# chatbot = Chatbot(config, conversation_id=None)

# response = chatbot.get_chat_response("你是谁", output="text")
# print(response)

# Initialize bot and... just the bot!
# bot = TelegramClient('bot_id_'+str(api_id), api_id, api_hash, proxy=sock_server).start(bot_token=bot_token)
bot = TelegramClient('bot_id_'+str(api_id), api_id, api_hash).start(bot_token=bot_token)

@bot.on(events.NewMessage(pattern='(?:/start)|(?:/Reset Thread)'))
async def send_welcome(event):
    if "session_token" in config and "cf_clearance" in config and config["cf_clearance"] and config["session_token"]:
        cache.reset(str(event.sender.id))
        await event.reply('重置成功，请发送第一条对话', parse_mode="Markdown")
    else :
        await event.reply('请联系作者设置chatgpt session，格式/session cf_clearance|session_token|user_agent', parse_mode="Markdown")

@bot.on(events.NewMessage(pattern='(?:/bye)|(?:/Log out)'))
async def send_end(event):
    cache.clear(str(event.sender.id))
    await event.reply('退出成功', parse_mode="Markdown")

@bot.on(events.NewMessage(pattern='(?:/session.*)'))
async def set_session(event):
    sessionStrs = event.text[8:].split("|")
    length = len(sessionStrs)
    if length == 3:
        with open("chatgpt_session.txt", 'w') as f:
            f.write(event.text[8:])
        config["cf_clearance"] = sessionStrs[0]
        config["session_token"] = sessionStrs[1]
        config["user_agent"] = sessionStrs[2]
        await event.reply('设置chatgpt session成功', parse_mode="Markdown")
    else :
        await event.reply('设置chatgpt session失败，需联系作者设置，格式/session cf_clearance|session_token|user_agent', parse_mode="Markdown")

@bot.on(events.NewMessage(pattern='(?:/try again)'))
async def try_again(event):
    markup = event.client.build_reply_markup([[Button.text('/Reset Thread')],[Button.text('/try again')],[Button.text('/session')],[Button.text('/Log out')]])
    conversation_id,parent_id,lastConv = cache.getLastConv(str(event.sender.id))
    if conversation_id == None or conversation_id == "conversation_id" or conversation_id == "":
        await event.reply("无历史会话，请点击/Reset Thread", buttons=markup, parse_mode="Markdown")
        return
    elif conversation_id and parent_id == None:
        conversation_id = None
        parent_id = None
        chatbot = Chatbot(config, conversation_id=None)
    else :
        chatbot = Chatbot(config, conversation_id=conversation_id, parent_id=parent_id)
    with open("chatgpt_session.txt", 'w') as f:
        f.write(config["cf_clearance"] + "|" + config["session_token"] + "|" + config["user_agent"])
    try :
        response = await chatbot.get_chat_response(lastConv, output="text", conversation_id=conversation_id, parent_id=parent_id)
        print(response)
        cache.set(str(event.sender.id), conversation_id=response["conversation_id"], parent_id=response["parent_id"], lastConv=lastConv)
        await event.reply(response['message'], buttons=markup, parse_mode="Markdown")
    except :
        await event.reply("请求失败，请手动输入以上问题重试。", buttons=markup, parse_mode="Markdown")

@bot.on(events.NewMessage(pattern='(?!/start|/end|/Reset Thread|/Log out|/try again|/session)'))
async def echo_all(event):
    markup = event.client.build_reply_markup([[Button.text('/Reset Thread')],[Button.text('/try again')],[Button.text('/session')],[Button.text('/Log out')]])
    conversation_id,parent_id = cache.get(str(event.sender.id))
    # print(config["user_agent"])
    if conversation_id == None:
        await event.reply("请点击/Reset Thread", buttons=markup, parse_mode="Markdown")
        return
    elif conversation_id == "conversation_id" :
        conversation_id = None
        parent_id = None
        chatbot = Chatbot(config, conversation_id=None)
    else:
        chatbot = Chatbot(config, conversation_id=conversation_id, parent_id=parent_id)
    with open("chatgpt_session.txt", 'w') as f:
        f.write(config["cf_clearance"] + "|" + config["session_token"] + "|" + config["user_agent"])
    try :
        response = await chatbot.get_chat_response(event.text, output="text", conversation_id=conversation_id, parent_id=parent_id)
        # print(response)
        cache.set(str(event.sender.id), conversation_id=response["conversation_id"], parent_id=response["parent_id"], lastConv=event.text)
        await event.reply(response['message'], buttons=markup, parse_mode="Markdown")
    except Exception as r:
        await event.reply(str(r) , buttons=markup, parse_mode="Markdown")

def main():
    try:
        print('(Press Ctrl+C to stop this)')
        bot.run_until_disconnected()
    finally:
        bot.disconnect()
        os.remove('bot_id_'+str(api_id)+".session")

if __name__ == '__main__':
    main()