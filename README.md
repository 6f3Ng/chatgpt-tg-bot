# chatGPT tg bot
## 说明
无聊注册了个chatgpt账号，想给朋友一起玩，本来想写个wxbot，但是网页版登陆不上去了，所以就写了telegram版的。目前除了常规的聊天，session过期了还可以直接重新设置，但是由于session是共享的，所以一旦设置错误，就会导致所有人用不了。另外cache搞了个字典在内存里好像问题也挺大，不过自己玩玩应该没啥问题。

### 20221213
20221212 chatgpt增加了cf防护，现在需要保证`cf_clearance|session_token|user_agent|ip`四个参数完全一致才能正常访问，所以做了一版更新

## 启动
```shell
pip3 install -r requirements.txt
python3 chatGPT.py
```

## 使用
1. 如果没有在`chatgpt_session.txt`文件中配置session，则先发送`/session cf_clearance|session_token|user_agent`设置，注意，获取session的ip要与机器人部署的ip保持一致
2. 发送`/Reset Thread`重置会话
3. 正常聊天，`/try again`不太好用
4. 结束发送`/Log out`清除缓存

## todo
- [ ] 公共session和私人session可分开配置(做不了了，加cf限制了)
- [ ] 配置文件独立出来（再说吧看心情）