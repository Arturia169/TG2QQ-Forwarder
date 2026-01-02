TG2QQ-Forwarder
基于 Telethon 和 NapCat (OneBot v11) 的 Telegram 消息转发 QQ 群工具。专为监控 TG 频道并实时同步情报至 QQ 群而设计。

✨ 功能特性
消息聚合转发：自动识别 Telegram 的媒体组（Album），将多张图片或视频合并为一条转发消息，避免刷屏。

表情回应展示：同步展示 TG 消息下的 Emoji 回应（Reactions）。

状态实时查询：在 QQ 群发送“状态”关键词，机器人会回复当前的运行状态及服务器剩余磁盘空间。

全自动化管理：支持 24 小时自动清理下载的缓存媒体文件，保持系统清爽。

高度安全脱敏：所有敏感 API 密钥均通过环境变量加载，核心代码与隐私数据完全隔离。

容器化部署：提供 Docker 和 Docker Compose 支持，实现一键部署。

🚀 快速开始
1. 准备工作
获取 Telegram API_ID 和 API_HASH（前往 my.telegram.org）。

部署好 NapCatQQ 并开启 WebSocket 服务。

准备一个 SOCKS5 代理（由于 TG 网络限制）。

2. 配置环境
克隆仓库后，将 .env.example 复制并重命名为 .env，填入你的参数：

Ini, TOML

TG_API_ID=你的API_ID
TG_API_HASH=你的API_HASH
TG_CHANNELS=https://t.me/频道A,https://t.me/频道B
QQ_GROUP=接收消息的QQ群号
NAPCAT_WS=ws://127.0.0.1:3001
PROXY_HOST=172.17.0.1
PROXY_PORT=7890
3. Docker 部署
使用 Docker Compose 启动：

Bash

docker-compose up -d
📂 项目结构
main.py: 核心逻辑处理。

Dockerfile: 镜像构建定义。

docker-compose.yml: 多容器定义。

.env.example: 环境变量模板。

.gitignore: 隐私过滤清单。

⚖️ 许可证
本项目采用 MIT License 开源协议。
