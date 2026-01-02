# 使用轻量级的 Python 镜像
FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 复制依赖清单并安装
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制你的程序代码
COPY main.py .

# 运行程序
CMD ["python", "main.py"]