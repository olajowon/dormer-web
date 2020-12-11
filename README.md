## 准备
### PgSQL
    create database dormer_web

## 开发运行
### 创建环境文件
	cd dormer_web
	echo development > env # manage.py 同级目录

### 修改配置文件
    cd configure
    cp example.ini development.ini # 与env同名
    vim development.ini

### 创建日志目录
	mkdir /var/log/dormer-web

### 创建python虚拟环境
    python3 -m venv venv

### 初始化数据库
    source venv/bin/activate
    python3 manage.py migrate

### 启动前端开发
	cd frontend && npm run dev
	
### 启动后端服务
    source venv/bin/activate
	python3 manage.py runserver:8000

### 浏览器访问
	http://localhost:9090


## 生产运行
### 创建环境文件
	cd dormer_web
	echo production > env # manage.py 同级目录

### 修改配置文件
    cd configure
    cp example.ini production.ini # 与env同名
    vim production.ini

### 创建日志目录
	mkdir /var/log/dormer-web

### 初始化数据库
    python3 server.py migrate

### 启动、停止、重启服务
	python3 server.py start|stop|restart

### 浏览器访问
	http://ip:9090