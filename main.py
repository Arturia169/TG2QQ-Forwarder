import shutil
import asyncio
import json
import os
import sys
import websockets

try:
    import socks
except ImportError:
    print("❌ 错误: 未找到 'pysocks' 库，请确保已安装 pysocks。")
    sys.exit(1)

from telethon import TelegramClient, events

# --- 1. 配置加载 (强制环境变量模式) ---
def get_env_or_exit(key):
    val = os.environ.get(key)
    if not val:
        print(f"❌ 启动失败: 缺少环境变量 {key}")
        sys.exit(1)
    return val

# [cite_start]基础鉴权 [cite: 2]
API_ID = int(get_env_or_exit('TG_API_ID'))
API_HASH = get_env_or_exit('TG_API_HASH')
TARGET_QQ_GROUP = int(get_env_or_exit('QQ_GROUP'))

# [cite_start]频道监控列表：强制要求从环境变量读取，不再提供默认值 [cite: 2]
_env_channels = get_env_or_exit('TG_CHANNELS')
MONITOR_CHANNELS = [c.strip() for c in _env_channels.split(',')]

# [cite_start]服务地址与路径 [cite: 2]
NAPCAT_WS_URL = os.environ.get('NAPCAT_WS', 'ws://127.0.0.1:3001')
SESSION_PATH = os.environ.get('SESSION_PATH', '/app/data/session')
DOWNLOAD_PATH = os.environ.get('DOWNLOAD_PATH', '/app/data/temp_media/')

# 代理配置
PHOST = os.environ.get('PROXY_HOST', '172.17.0.1')
PPORT = int(os.environ.get('PROXY_PORT', 7890))
PROXY = (socks.SOCKS5, PHOST, PPORT)

if not os.path.exists(DOWNLOAD_PATH): 
    os.makedirs(DOWNLOAD_PATH)

# --- 2. 全局状态 ---
msg_objects = []          
buffer_lock = asyncio.Lock()
ws_connection = None
pending_task = None      
active_downloads = 0     

# --- 3. 辅助功能 ---
def progress_callback(current, total):
    """实时下载进度条"""
    percentage = 100 * current / total
    sys.stdout.write(f"\r📥 [下载中] 进度: {percentage:.1f}% ({current}/{total} bytes)")
    sys.stdout.flush()
    if current == total: 
        print(flush=True)

def get_reactions_text(message):
    if not message.reactions: return ""
    res = [f"{getattr(count.reaction, 'emoticon', '📊')}{count.count}" for count in message.reactions.results]
    return " ".join(res)

# --- 4. 核心发送逻辑 ---
async def forward_buffer():
    try:
        wait_time = 0
        while active_downloads > 0 and wait_time < 30:
            await asyncio.sleep(1)
            wait_time += 1
        await asyncio.sleep(2) 

        async with buffer_lock:
            if not msg_objects: return
            nodes = []
            for obj in msg_objects:
                header = f"📢 来源频道：{obj['channel']}"
                body = f"\n\n💬 内容：\n{obj['text']}" if obj['text'] else ""
                reactions = f"\n\n📊 回应：{obj['reactions']}" if obj['reactions'] else ""
                
                nodes.append({
                    "type": "node", 
                    "data": {
                        "name": "情报员", 
                        "uin": "2854196310", 
                        "content": f"{header}{body}{reactions}"
                    }
                })
                
                for file_info in obj['files']:
                    if os.path.exists(file_info['path']):
                        tag = "image" if file_info['type'] == 'image' else "video"
                        nodes.append({
                            "type": "node", 
                            "data": {
                                "name": "情报员", 
                                "uin": "2854196310", 
                                "content": f"[CQ:{tag},file=file://{os.path.abspath(file_info['path'])}]"
                            }
                        })

            if nodes and ws_connection:
                payload = {
                    "action": "send_group_forward_msg", 
                    "params": {"group_id": TARGET_QQ_GROUP, "messages": nodes}
                }
                await ws_connection.send(json.dumps(payload))
                print(f"✅ [发送成功] 已投递合并消息包")
            msg_objects.clear()
    except Exception as e: 
        print(f"❌ [发送异常] {e}")

async def handle_tg_message(message):
    global pending_task, active_downloads
    try:
        chat = await message.get_chat()
        channel_title = getattr(chat, 'title', '未知频道')
    except: channel_title = "未知频道"

    text = message.message or ""
    reactions = get_reactions_text(message)
    current_files = []

    if message.media:
        m_type = 'image' if message.photo else 'video' if (message.video or message.gif) else None
        if not m_type and message.document:
            mime = (message.document.mime_type or "").lower()
            m_type = 'video' if 'video' in mime else 'image' if 'image' in mime else None
        
        if m_type:
            active_downloads += 1
            print(f"\n🚀 [触发下载] 来源: {channel_title}")
            try:
                path = await message.download_media(file=DOWNLOAD_PATH, progress_callback=progress_callback)
                if path: current_files.append({'path': path, 'type': m_type})
            finally: 
                active_downloads -= 1

    async with buffer_lock:
        found = False
        if message.grouped_id:
            for obj in msg_objects:
                if obj.get('grouped_id') == message.grouped_id:
                    if text and text not in obj['text']: 
                        obj['text'] = (obj['text'] + "\n" + text).strip()
                    obj['files'].extend(current_files)
                    if reactions: obj['reactions'] = reactions
                    found = True
                    break
        
        if not found:
            msg_objects.append({
                'grouped_id': message.grouped_id, 
                'channel': channel_title, 
                'text': text, 
                'reactions': reactions, 
                'files': current_files
            })
        
        if pending_task: 
            pending_task.cancel()
        pending_task = asyncio.create_task(forward_buffer())

async def auto_cleanup():
    """24小时定时清理缓存"""
    while True:
        await asyncio.sleep(86400)
        try:
            print("🧹 [系统清理] 正在清理旧媒体文件...", flush=True)
            for file in os.listdir(DOWNLOAD_PATH):
                file_path = os.path.join(DOWNLOAD_PATH, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)
            print("✅ [系统清理] 临时文件夹已清空", flush=True)
        except Exception as e:
            print(f"⚠️ [系统清理] 清理失败: {e}", flush=True)

# --- 5. WS 通信与监听 ---
async def listen_ws_messages():
    global ws_connection
    while True:
        if ws_connection:
            try:
                msg = await ws_connection.recv()
                data = json.loads(msg)
                if data.get('post_type') == 'message' and data.get('message_type') == 'group':
                    if data.get('group_id') == TARGET_QQ_GROUP and data.get('raw_message') == '状态':
                        total, used, free = shutil.disk_usage(DOWNLOAD_PATH)
                        free_gb = free / (1024**3)
                        
                        reply = {
                            "action": "send_group_msg",
                            "params": {
                                "group_id": TARGET_QQ_GROUP,
                                "message": f"🤖 系统运行中\n🟢 状态：正常\n📊 监控频道：{len(MONITOR_CHANNELS)}个\n💾 剩余空间：{free_gb:.2f} GB"
                            }
                        }
                        await ws_connection.send(json.dumps(reply))
            except:
                await asyncio.sleep(1)
        else:
            await asyncio.sleep(5)

async def connect_napcat():
    global ws_connection
    while True:
        try:
            async with websockets.connect(NAPCAT_WS_URL) as ws:
                ws_connection = ws
                print("✅ [WS] 已连接至 NapCat 服务")
                await listen_ws_messages()
        except:
            ws_connection = None
            await asyncio.sleep(5)

# --- 6. 主程序 ---
client = TelegramClient(SESSION_PATH, API_ID, API_HASH, proxy=PROXY)

@client.on(events.NewMessage(chats=MONITOR_CHANNELS))
async def handler(event):
    await handle_tg_message(event.message)

async def main():
    asyncio.create_task(connect_napcat())
    await client.start()
    asyncio.create_task(auto_cleanup())
    print(f"🚀 [已启动] 正在监控频道...")
    
    for _ in range(10):
        if ws_connection: break
        await asyncio.sleep(1)

    # 启动自测逻辑
    for channel in MONITOR_CHANNELS:
        try:
            msgs = await client.get_messages(channel, limit=3) 
            if msgs:
                print(f"🔄 [初始化] 检查频道最近消息: {channel}")
                for m in reversed(msgs):
                    await handle_tg_message(m)
                await asyncio.sleep(5)
        except Exception as e: 
            print(f"⚠️ [初始化失败] {e}")

    if ws_connection:
        try:
            msg = {
                "action": "send_group_msg",
                "params": {"group_id": TARGET_QQ_GROUP, "message": "✅ [系统通知] 机器人已上线，实时监控中。"}
            }
            await ws_connection.send(json.dumps(msg))
        except: pass

    await client.run_until_disconnected()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass