# 🚀 TG2QQ-Forwarder

> **基于 Telethon + NapCat 的 Telegram 消息高效转发工具**

[![Python Version](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Docker Support](https://img.shields.io/badge/Docker-Supported-cyan.svg)](docker-compose.yml)

本项目专为监控 Telegram 频道并实时同步情报至 QQ 群而设计，支持媒体组聚合、表情回应同步及自动空间清理。

---

## ✨ 功能特性

* **📦 消息聚合转发**：自动识别 Telegram 媒体组 (Album)，将多张图片或视频合并为一条转发消息，拒绝刷屏。
* **📊 表情回应同步**：实时展示 Telegram 消息下的 Emoji 回应 (Reactions) 统计。
* **🤖 运行状态查询**：在 QQ 群发送 `状态` 关键词，机器人自动回复运行详情及服务器剩余空间。
* **🧹 自动空间清理**：内置 24 小时定时清理任务，自动清空下载缓存文件夹，保持系统清爽。
* **🔐 高度安全脱敏**：敏感 API 密钥完全通过环境变量加载，核心代码与隐私数据严格隔离。

---

## 🚀 快速开始

### 1. 环境准备
1. **Telegram API**: 前往 [my.telegram.org](https://my.telegram.org) 获取 `API_ID` 和 `API_HASH`。
2. **QQ 服务端**: 部署并开启 [NapCatQQ](https://github.com/NapNeko/NapCatQQ) 的 WebSocket 服务。


### 2. 配置文件
复制 `.env.example` 并重命名为 `.env`，填入相应参数：

```env
# 基础鉴权
TG_API_ID=1234567
TG_API_HASH=your_hash_string
QQ_GROUP=987654321

# 监控频道 (多个请用英文逗号分隔)
TG_CHANNELS=[https://t.me/example_a,https://t.me/example_b](https://t.me/example_a,https://t.me/example_b)

# 服务地址与代理
NAPCAT_WS=ws://172.17.0.1:3001
PROXY_HOST=172.17.0.1
PROXY_PORT=7890

