# Woruld Sophia

基于 Vue 3、TypeScript、Django REST Framework、MySQL 的前后端分离式协会门户与成员权限管理系统。

## 项目概览

当前项目包含以下能力：

- 前端门户与个人中心
- 登录鉴权与登录态持久化
- 基于角色与作用域的权限控制（RBAC）
- 账户管理、资料修改、密码修改
- 分组工作表与组内协作编辑
- Django API + Gunicorn + Nginx + Supervisor 的线上部署链路

## 技术栈

前端：

- Vue 3
- Vite
- TypeScript
- Pinia
- Vue Router

后端：

- Django
- Django REST Framework
- JWT
- MySQL

工程化：

- ESLint
- Oxlint
- Prettier
- Supervisor
- Nginx

## 目录结构

```text
src/
├── assets/          # 图片等静态资源
├── components/      # 公共组件
├── composables/     # 组合式逻辑
├── constants/       # 常量配置
├── layouts/         # 页面布局
├── router/          # 路由配置与守卫
├── services/        # 请求与服务层
├── stores/          # Pinia 状态管理
├── types/           # 类型定义
├── utils/           # 工具函数
├── views/           # 页面视图
├── App.vue          # 根组件
└── main.ts          # 入口文件

backend/
├── accounts/        # 用户、角色、认证相关
├── netclub/         # Django 项目配置
├── requirements.txt # 后端依赖
└── manage.py        # Django 管理入口
```

## 本地开发

### 前端

安装依赖：

```bash
npm install
```

启动开发服务器：

```bash
npm run dev
```

构建生产包：

```bash
npm run build
```

本地预览构建结果：

```bash
npm run preview
```

### 后端

进入后端目录并创建虚拟环境：

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

初始化环境变量：

```bash
cp .env.example .env
```

执行迁移并启动：

```bash
python manage.py migrate
python manage.py runserver
```

## 常用命令

前端：

```bash
npm run dev
npm run build
npm run preview
npm run lint
npm run format
```

后端：

```bash
cd backend
source venv/bin/activate
python manage.py migrate
python manage.py runserver
```

## 生产部署与更新流程

当前线上环境：Vue 3 前端静态文件 + Django/Gunicorn API + Nginx 反向代理 + 宝塔面板 + Supervisor。

### 线上目录约定

- 前端站点目录：`/www/wwwroot/netclub`
- 后端项目目录：`/root/Woruld_Sophia/backend`
- 后端虚拟环境：`/root/Woruld_Sophia/backend/venv`
- Gunicorn 监听地址：`127.0.0.1:8000`
- Nginx 站点配置：`/www/server/panel/vhost/nginx/47.116.119.51.conf`
- Supervisor 配置：`/etc/supervisor/conf.d/netclub_gunicorn.conf`

### 前端更新

本地构建：

```bash
npm run build
```

上传到服务器临时目录：

```bash
scp -r dist root@47.116.119.51:/root/upload/
```

执行前端部署脚本：

```bash
bash /root/deploy_frontend.sh
```

该脚本已包含：

- `dist` 完整性校验
- 自动备份
- 自动失败回滚
- 仅替换前端构建文件
- 自动保留最近 5 份备份

### 后端更新

后端代码推送到仓库后，在服务器执行：

```bash
bash /root/deploy_backend.sh
```

该脚本会执行：

1. `git pull origin main`
2. 激活虚拟环境
3. `pip install -r requirements.txt`
4. `python manage.py migrate`
5. `python manage.py collectstatic --noinput`
6. `supervisorctl restart netclub_gunicorn`

### 前后端一起更新

如果前后端都改了：

1. 本地构建前端并上传 `dist`
2. 推送后端代码到仓库
3. 在服务器执行：

```bash
bash /root/deploy_all.sh
```

## Gunicorn 与 Supervisor

Supervisor 配置文件路径：

```bash
/etc/supervisor/conf.d/netclub_gunicorn.conf
```

配置内容：

```ini
[program:netclub_gunicorn]
command=/root/Woruld_Sophia/backend/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:8000 netclub.wsgi:application
directory=/root/Woruld_Sophia/backend
user=root
autostart=true
autorestart=true
startsecs=5
stopwaitsecs=10
stdout_logfile=/root/Woruld_Sophia/backend/logs/gunicorn_stdout.log
stderr_logfile=/root/Woruld_Sophia/backend/logs/gunicorn_stderr.log
stdout_logfile_maxbytes=20MB
stdout_logfile_backups=5
stderr_logfile_maxbytes=20MB
stderr_logfile_backups=5
environment=PYTHONUNBUFFERED="1"
```

创建日志目录并加载配置：

```bash
mkdir -p /root/Woruld_Sophia/backend/logs
supervisorctl reread
supervisorctl update
supervisorctl start netclub_gunicorn
```

常用命令：

```bash
supervisorctl status
supervisorctl status netclub_gunicorn
supervisorctl restart netclub_gunicorn
supervisorctl stop netclub_gunicorn
supervisorctl start netclub_gunicorn
```

查看日志：

```bash
tail -f /root/Woruld_Sophia/backend/logs/gunicorn_stdout.log
tail -f /root/Woruld_Sophia/backend/logs/gunicorn_stderr.log
```

## Nginx 配置

当前站点采用保守版配置，HTTP 与 HTTPS 并行可访问，不强制跳转。

可直接用于宝塔站点配置：

```nginx
server {
    listen 80;
    server_name 47.116.119.51;

    #CERT-APPLY-CHECK--START
    location ~ \.well-known {
        root /www/wwwroot/netclub;
    }
    #CERT-APPLY-CHECK--END

    location = /index.html {
        root /www/wwwroot/netclub;
        add_header Cache-Control "no-cache, no-store, must-revalidate";
    }

    location / {
        root /www/wwwroot/netclub;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    location /assets/ {
        alias /www/wwwroot/netclub/assets/;
        expires 30d;
        access_log off;
    }

    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-Host $host;
        proxy_set_header X-Forwarded-Port $server_port;

        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    location /static/ {
        alias /www/wwwroot/netclub/static/;
        expires 30d;
        access_log off;
    }

    location /media/ {
        alias /www/wwwroot/netclub/media/;
        expires 30d;
        access_log off;
    }
}

server {
    listen 443 ssl;
    http2 on;
    server_name 47.116.119.51;

    ssl_certificate /www/server/panel/vhost/cert/47.116.119.51/fullchain.pem;
    ssl_certificate_key /www/server/panel/vhost/cert/47.116.119.51/privkey.pem;

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;

    location = /index.html {
        root /www/wwwroot/netclub;
        add_header Cache-Control "no-cache, no-store, must-revalidate";
    }

    location / {
        root /www/wwwroot/netclub;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    location /assets/ {
        alias /www/wwwroot/netclub/assets/;
        expires 30d;
        access_log off;
    }

    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto https;
        proxy_set_header X-Forwarded-Host $host;
        proxy_set_header X-Forwarded-Port $server_port;

        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    location /static/ {
        alias /www/wwwroot/netclub/static/;
        expires 30d;
        access_log off;
    }

    location /media/ {
        alias /www/wwwroot/netclub/media/;
        expires 30d;
        access_log off;
    }
}
```

修改后执行：

```bash
nginx -t
systemctl reload nginx
```

## 服务器首次部署

### 1. 准备基础环境

确保服务器已安装：

- Nginx
- MySQL
- Python 3
- `python3-venv`
- Supervisor
- 宝塔面板

### 2. 初始化后端

```bash
cd /root/Woruld_Sophia/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

根据实际数据库信息修改 `.env`。

执行迁移与静态文件收集：

```bash
python manage.py migrate
python manage.py collectstatic --noinput
```

### 3. 配置 Supervisor

```bash
mkdir -p /root/Woruld_Sophia/backend/logs
supervisorctl reread
supervisorctl update
supervisorctl start netclub_gunicorn
```

### 4. 配置 Nginx

使用上面的保守版配置，保存后执行：

```bash
nginx -t
systemctl reload nginx
```

### 5. 首次发布前端

```bash
npm install
npm run build
scp -r dist root@47.116.119.51:/root/upload/
ssh root@47.116.119.51 "bash /root/deploy_frontend.sh"
```

### 6. 验证

建议检查：

- 首页可正常访问
- `/api/login` 可连通
- 登录与个人中心正常
- `supervisorctl status netclub_gunicorn` 为 `RUNNING`

## 脚本文件

服务器上建议保留：

- `/root/deploy_frontend.sh`
- `/root/deploy_backend.sh`
- `/root/deploy_all.sh`

## Git 常用命令

```bash
git add .
git commit -m "update"
git push
```

拉取远程更新：

```bash
git  pull
```
