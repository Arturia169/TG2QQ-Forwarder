# 🚀 TG2QQ-Forwarder

> **基于 Telethon + NapCat 的 Telegram 消息高效转发工具**

[![Python Version](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Docker Support](https://img.shields.io/badge/Docker-Supported-cyan.svg)](docker-compose.yml)

本项目专注于将 Telegram 频道情报实时、整洁地转发至 QQ 群，支持媒体聚合与系统状态监控。

---

## ✨ 核心功能

* **📦 消息聚合转发**：智能识别 Telegram 媒体组 (Album)，将多张图文合并转发，告别消息刷屏。
* **📊 回应展示**：完美同步展示 Telegram 消息下的 Emoji 回应 (Reactions)。
* **🤖 状态监控**：群内发送 `状态` 即可获取机器人运行详情及服务器磁盘空间。
* **🧹 自动清理**：内置 24 小时定时任务，自动清空下载缓存，保持硬盘清爽。
* **🔐 安全隔离**：核心代码与配置完全分离，通过环境变量加载敏感信息，确保隐私安全。

---

## 🚀 快速开始

### 1. 环境准备
1.  **Telegram API**: 前往 [my.telegram.org](https://my.telegram.org) 获取 `API_ID` 和 `API_HASH`。
2.  **QQ 服务端**: 部署并开启 [NapCatQQ](https://github.com/NapNeko/NapCatQQ) 的 WebSocket 服务。
3.  **网络环境**: 准备一个 SOCKS5 代理用于连接 Telegram。

### 2. 配置文件
复制 `.env.example` 并重命名为 `.env`，填入相应参数：

```env
TG_API_ID=1234567
TG_API_HASH=your_hash_string
TG_CHANNELS=[https://t.me/channel_a,https://t.me/channel_b](https://t.me/channel_a,https://t.me/channel_b)
QQ_GROUP=987654321
NAPCAT_WS=ws://127.0.0.1:3001
PROXY_HOST=172.17.0.1
PROXY_PORT=7890

### 3. 部署
docker-compose up -d

### 4.📂 项目结构说明
文件,描述
main.py,核心逻辑处理程序
Dockerfile,容器镜像构建脚本
docker-compose.yml,容器编排定义
.env.example,环境变量模板文件
.gitignore,隐私与缓存过滤清单

看到你的预览图了，现在的文字确实挤在一起，缺乏视觉重点。在 GitHub 上，良好的排版（Markdown）能让项目看起来专业度倍增。

既然你的项目已经成功上传，我为你重新设计了一个高颜值、结构化的 README.md。这个版本加入了图标、代码块和清晰的层次结构。

🎨 建议替换的 README 内容
你可以直接点击 GitHub 页面上的编辑图标，将内容全部替换为：

Markdown
# 🚀 TG2QQ-Forwarder

> **基于 Telethon + NapCat 的 Telegram 消息高效转发工具**

[![Python Version](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Docker Support](https://img.shields.io/badge/Docker-Supported-cyan.svg)](docker-compose.yml)

本项目专注于将 Telegram 频道情报实时、整洁地转发至 QQ 群，支持媒体聚合与系统状态监控。

---

## ✨ 核心功能

* **📦 消息聚合转发**：智能识别 Telegram 媒体组 (Album)，将多张图文合并转发，告别消息刷屏。
* **📊 回应展示**：完美同步展示 Telegram 消息下的 Emoji 回应 (Reactions)。
* **🤖 状态监控**：群内发送 `状态` 即可获取机器人运行详情及服务器磁盘空间。
* **🧹 自动清理**：内置 24 小时定时任务，自动清空下载缓存，保持硬盘清爽。
* **🔐 安全隔离**：核心代码与配置完全分离，通过环境变量加载敏感信息，确保隐私安全。

---

## 🚀 快速开始

### 1. 环境准备
1.  **Telegram API**: 前往 [my.telegram.org](https://my.telegram.org) 获取 `API_ID` 和 `API_HASH`。
2.  **QQ 服务端**: 部署并开启 [NapCatQQ](https://github.com/NapNeko/NapCatQQ) 的 WebSocket 服务。
3.  **网络环境**: 准备一个 SOCKS5 代理用于连接 Telegram。

### 2. 配置文件
复制 `.env.example` 并重命名为 `.env`，填入相应参数：

```env
TG_API_ID=1234567
TG_API_HASH=your_hash_string
TG_CHANNELS=[https://t.me/channel_a,https://t.me/channel_b](https://t.me/channel_a,https://t.me/channel_b)
QQ_GROUP=987654321
NAPCAT_WS=ws://127.0.0.1:3001
PROXY_HOST=172.17.0.1
PROXY_PORT=7890
3. 一键部署
使用 Docker Compose 启动服务：

Bash
docker-compose up -d
📂 项目结构说明
文件	描述
main.py	核心逻辑处理程序
Dockerfile	容器镜像构建脚本
docker-compose.yml	容器编排定义
.env.example	环境变量模板文件
.gitignore	隐私与缓存过滤清单

### 5.📜 许可证
本项目采用 MIT License 开源协议。
