# Woruld Sophia

一个基于 **Vue 3 + Vite + TypeScript + Pinia + Vue Router** 的前端项目原型站点。

当前版本已经实现了：
- 首页与基础视觉风格
- 顶部导航栏与移动端汉堡菜单
- 登录页
- 前端 mock 登录
- 登录态持久化（localStorage）
- 路由鉴权（未登录时拦截受保护页面）
- 基于角色作用域的权限系统（RBAC，区分查看与编辑）
- 404 页面
- 多个业务分组入口页（当前为占位页）

---

## 技术栈

- Vue 3
- Vite
- TypeScript
- Pinia
- Vue Router
- ESLint / Oxlint / Prettier

---

## 当前已实现功能

### 1. 首页
- 展示项目标题与简介文案
- 使用自定义字体与图片资源
- 已有基础视觉风格

### 2. 导航栏
- 固定顶部导航
- 页面滚动时切换样式
- 支持移动端汉堡菜单
- 登录后显示用户名与退出按钮

### 3. 登录系统（开发阶段）
- 登录表单
- 用户名/密码非空校验
- 登录失败提示
- 登录成功后保存登录态
- 刷新页面后恢复登录态
- 支持退出登录

### 4. 路由鉴权
以下页面当前要求登录后访问：
- `/conference`
- `/hardware`
- `/software`
- `/network`
- `/woruld-sophia`

未登录访问这些页面时，会自动跳转到 `/login?redirect=<原路径>`，登录成功后自动回到目标页。

#### 登录态 ≠ 分组权限
路由守卫只做**登录校验**：只要已登录，就能进入任一业务分组页面（`/conference`、`/hardware` 等）。

分组页面内的**工作项目查看**与**编辑**由权限系统控制（在页面/组件内部判断，不在路由层拦截）：

- 登录用户都能进入任意分组页面
- 但每个分组的「工作项目」只有该组成员 / 组长 / 相关指导老师 / 会长能查看（`canViewGroup`）
- 编辑权限更严格：只有本组组长、会长可编辑本组内容（`canEditGroup`）
- 个人工作项只能由本人编辑（`canEditOwnWorkItem`）

> 也就是说：**没有其他组权限 ≠ 不能访问其他组页面**，而是看不到、也不能编辑其他组的工作项目。

> 特例：`/woruld-sophia`（寰宇智域）是独立管理模块，非协作分组，路由层要求 `sophia_admin` 角色才能进入。

### 5. 登录弹窗联动
点击导航栏中的 `Sign In` 会打开新窗口登录。
登录成功后会通知主页面刷新登录态，并关闭登录窗口。

### 6. 404 页面
访问不存在的路由时，会进入 404 页面。

---

## 当前路由

| 路径 | 说明 | 是否需登录 |
|---|---|---|
| `/` | 首页 | 否 |
| `/login` | 登录页 | 否 |
| `/conference` | 会议组 | 是 |
| `/hardware` | 硬件组 | 是 |
| `/software` | 软件组 | 是 |
| `/network` | 网络组 | 是 |
| `/woruld-sophia` | 寰宇智域 | 是 |
| `/:pathMatch(.*)*` | 404 页面 | 否 |

---

## 什么是 mock 登录？

**mock 登录** 的意思是：

> 现在这个项目的登录功能，暂时不是连接真实后端接口，而是用本地配置的“模拟账号数据”来假装完成登录流程。

也就是说，目前登录流程是这样的：
1. 你在登录页输入用户名和密码
2. 前端代码读取模拟用户数据：`.env.local` 的 `VITE_MOCK_USERS` 优先，未配置时回退到 `src/mock/users.ts`
3. 如果账号密码匹配，就认为登录成功
4. 然后把用户信息（含角色 `roles`）保存到 `localStorage`

它的作用主要是：
- 在后端还没做好之前，先把前端登录流程跑通
- 方便开发页面、路由守卫、登录态切换等功能
- 让项目在开发阶段可以演示

### 它不是真实登录
当前 mock 登录：
- 不会请求真正的服务器
- 不会校验真实数据库用户
- 不适合正式生产环境

当前项目代码中已经明确限制：
- **开发环境** 下可以使用 mock 登录
- **生产环境** 下不会启用 mock 登录，登录会直接失败，直到你接入真实后端

---

## 权限系统（RBAC）

登录只解决「你是谁」，权限系统决定「你能看到、能改哪些内容」。

### 角色与作用域
权限由「角色 + 作用域」组合表达，定义在 `src/types/auth.ts`：

| 角色 | 含义 | 常见作用域 |
|---|---|---|
| `president` | 会长 | `global`（全局） |
| `group_leader` | 组长 | `group`（某一组） |
| `member` | 组员 | `group`（某一组） |
| `teacher` | 指导老师 | `groups`（多组） |
| `sophia_admin` | 寰宇智域管理员 | `module`（`woruld_sophia`） |

### 权限判定函数（`src/utils/permissions.ts`）
| 函数 | 作用 |
|---|---|
| `canViewGroup(user, groupId)` | 是否可查看某组的工作项目 |
| `canEditGroup(user, groupId)` | 是否可编辑某组内容（组长 / 会长） |
| `canEditOwnWorkItem(user, ownerId)` | 是否可编辑某个工作项（仅本人） |
| `canManageSophia(user)` | 是否可管理寰宇智域模块 |
| `hasRole(user, roleName)` | 是否拥有某角色 |

> 这些函数在页面/组件内部调用，路由守卫不再做分组级拦截。

### 默认 mock 账号（`src/mock/users.ts`，密码均为 `123456`）
| 用户名 | 身份 | 可见分组 |
|---|---|---|
| `president` | 会长 | 全部 |
| `teacher` | 指导老师 | 硬件、会议 |
| `hardwareLeader` / `hardwareMember` | 硬件组组长 / 组员 | 硬件 |
| `conferenceLeader` / `conferenceMember` | 会议组组长 / 组员 | 会议 |
| `softwareLeader` / `softwareMember` | 软件组组长 / 组员 | 软件 |
| `networkLeader` / `networkMember` | 网络组组长 / 组员 | 网络 |
| `woruldSophiaAdmin` | 寰宇智域管理员 | 寰宇智域模块 |
| `multiRoleUser` | 多角色（硬件组长 + 寰宇智域管理员） | 硬件 + 寰宇智域 |

---

## 环境变量说明

项目默认账号来源于 `src/mock/users.ts`；若要覆盖默认账号（如改密码、加账号），用 `.env.local` 的 `VITE_MOCK_USERS`。

请先复制：

```bash
cp .env.example .env.local
```

然后按需修改 `.env.local`。未配置 `VITE_MOCK_USERS` 时，自动回退到 `src/mock/users.ts`。

### 字段说明
- `id`：用户 ID
- `username`：用户名
- `displayName`：页面显示名称
- `email`：邮箱（可选）
- `password`：mock 登录密码（仅开发环境）
- `roles`：角色与作用域分配，结构见 `src/types/auth.ts`

例如自定义一个账号：

```env
VITE_MOCK_USERS={"huangfuyao":{"id":"u99","username":"huangfuyao","displayName":"黄甫尧","password":"123456","roles":[{"role":"group_leader","scope":{"type":"group","groupId":"software"}}]}}
```

这样开发环境下就可以用：
- 用户名：`huangfuyao`
- 密码：`123456`

进行登录测试。

> 注意：`.env.local` 只用于本地开发，已被 `.gitignore` 忽略，不应上传到远程仓库。

---

## 安装与运行

### 1. 安装依赖

```bash
npm install
```

### 2. 配置本地环境变量

```bash
cp .env.example .env.local
```

然后编辑 `.env.local`。

### 3. 启动开发环境

```bash
npm run dev
```

### 4. 构建生产版本

```bash
npm run build
```

### 5. 本地预览生产构建

```bash
npm run preview
```

---

## 常用命令

```bash
npm run dev
```
启动开发服务器

```bash
npm run build
```
类型检查并构建生产包

```bash
npm run preview
```
本地预览构建结果

```bash
npm run lint
```
执行代码检查并自动修复

```bash
npm run format
```
格式化 `src/` 目录代码

---

## 项目结构

```text
src/
├── assets/          # 图片等静态资源
├── components/      # 公共组件（导航栏、首页区块等）
├── constants/       # 权限角色 / 分组 / 模块的中文标签
├── mock/            # mock 数据（默认账号 users.ts）
├── router/          # 路由配置与路由守卫
├── services/        # 服务层（mock / 后端两套登录方法）
├── stores/          # Pinia 状态管理
├── types/           # 类型定义（AuthUser、角色作用域 RBAC）
├── utils/           # 工具函数（权限判定 canViewGroup 等）
├── views/           # 页面视图
├── App.vue          # 根组件
└── main.ts          # 入口文件
```

---

## 生产部署与更新流程

> 当前线上环境：**Vue 3 前端静态文件 + Django/Gunicorn API + Nginx 反向代理 + 宝塔面板**

### 目录约定

线上已确认使用以下目录与服务：

- 前端站点目录：`/www/wwwroot/netclub`
- 后端项目目录：`/root/Woruld_Sophia/backend`
- 后端虚拟环境：`/root/Woruld_Sophia/backend/venv`
- Gunicorn 监听地址：`127.0.0.1:8000`
- Nginx 站点配置：`/www/server/panel/vhost/nginx/47.116.119.51.conf`

### 前端更新流程

当你只修改了 `src/` 下的 Vue 前端代码时，按下面流程更新：

#### 1. 本地构建

```bash
npm run build
```

构建完成后会生成 `dist/`。

#### 2. 上传构建产物到服务器临时目录

```bash
scp -r dist root@47.116.119.51:/root/upload/
```

上传完成后，服务器上应存在：

```bash
/root/upload/dist
```

#### 3. 执行前端部署脚本

```bash
bash /root/deploy_frontend.sh
```

该脚本已实现：

- 检查 `dist` 是否完整（必须包含 `index.html` 和 `assets/`）
- 自动备份当前线上前端文件
- 仅替换 Vue 构建产物，不删除 Django 的 `static/`、`media/`
- 部署失败自动回滚
- 自动只保留最近 5 份前端备份

#### 4. 浏览器强制刷新缓存

部署成功后，如果页面看起来“没变化”，优先强刷缓存：

- `Ctrl + F5`
- 或浏览器开发者工具 → `Network` → 勾选 `Disable cache`

### 后端更新流程

当你修改了 `backend/` 下的 Django 代码时，先将代码推送到远程仓库，再在服务器执行：

```bash
bash /root/deploy_backend.sh
```

该脚本会依次执行：

1. `git pull origin main`
2. 激活虚拟环境
3. `pip install -r requirements.txt`
4. `python manage.py migrate`
5. `python manage.py collectstatic --noinput`
6. `supervisorctl restart netclub_gunicorn`

### 前后端一起更新

如果前后端都改了：

1. 本地先构建前端并上传 `dist`
2. 将后端代码推送到仓库
3. 在服务器执行：

```bash
bash /root/deploy_all.sh
```

### Gunicorn / Supervisor 常用命令

```bash
supervisorctl status
supervisorctl status netclub_gunicorn
supervisorctl restart netclub_gunicorn
supervisorctl stop netclub_gunicorn
supervisorctl start netclub_gunicorn
```

查看 Gunicorn 日志：

```bash
tail -f /root/Woruld_Sophia/backend/logs/gunicorn_stdout.log
tail -f /root/Woruld_Sophia/backend/logs/gunicorn_stderr.log
```

### Nginx 当前配置说明

当前线上 Nginx 的核心结构如下：

- `/`：指向 Vue 前端目录 `/www/wwwroot/netclub`
- `/api/`：反向代理到 `http://127.0.0.1:8000`
- `/static/`：映射到 `/www/wwwroot/netclub/static/`
- `/media/`：映射到 `/www/wwwroot/netclub/media/`

这意味着：

- 前端发布时**不能直接清空整个 `/www/wwwroot/netclub` 目录**
- 因为该目录中还混放了 Django 的 `static` 和 `media`
- 所以前端部署脚本只能替换 `index.html`、`assets/` 及少量前端根文件

### Nginx 可优化建议

当前配置整体可用，但建议后续逐步补充：

1. **先使用保守版 HTTPS/HTTP 并行配置**
   - 当前更推荐 80 和 443 同时可访问
   - 等证书、域名、跳转链路都确认稳定后，再开启 80 → 443 强制跳转

2. **给 `/api/` 增加超时设置**
   - 避免接口慢时过早断开，例如：
   ```nginx
   proxy_connect_timeout 60s;
   proxy_send_timeout 60s;
   proxy_read_timeout 60s;
   ```

3. **补充常见代理头**
   - 当前已有 `Host`、`X-Real-IP`、`X-Forwarded-For`、`X-Forwarded-Proto`
   - 建议额外补上：
   ```nginx
   proxy_set_header X-Forwarded-Host $host;
   proxy_set_header X-Forwarded-Port $server_port;
   ```

4. **为前端静态资源单独加缓存策略**
   - 对 `/assets/` 设置较长缓存时间
   - 对 `index.html` 不做长缓存，减少“前端已更新但页面没变”的概率

5. **生产环境收紧 CORS 来源**
   - 当前后端 `CORS_ALLOWED_ORIGINS` 里包含本地开发地址和公网 IP
   - 后续若正式上线域名，建议只保留真实前端访问域名

### 推荐 Nginx 配置（保守版，可直接粘贴到宝塔）

适合当前阶段直接使用：HTTP 与 HTTPS 并行可访问，不立即做强制跳转。

> 当前服务器 IP：`47.116.119.51`
> 站点根目录：`/www/wwwroot/netclub`
> Django / Gunicorn 反向代理目标：`127.0.0.1:8000`

```nginx
server {
    listen 80;
    server_name 47.116.119.51;

    # === 宝塔 SSL 文件验证专用（不要删除）===
    #CERT-APPLY-CHECK--START
    location ~ \.well-known {
        root /www/wwwroot/netclub;
    }
    #CERT-APPLY-CHECK--END

    # === 首页入口：禁止长缓存 ===
    location = /index.html {
        root /www/wwwroot/netclub;
        add_header Cache-Control "no-cache, no-store, must-revalidate";
    }

    # === 前端（Vue 3 SPA）===
    location / {
        root /www/wwwroot/netclub;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    # === Vue 构建产物缓存 ===
    location /assets/ {
        alias /www/wwwroot/netclub/assets/;
        expires 30d;
        access_log off;
    }

    # === 后端 API（Django DRF）===
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

    # === Django 静态文件 ===
    location /static/ {
        alias /www/wwwroot/netclub/static/;
        expires 30d;
        access_log off;
    }

    # === 上传文件 ===
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

    # === 首页入口：禁止长缓存 ===
    location = /index.html {
        root /www/wwwroot/netclub;
        add_header Cache-Control "no-cache, no-store, must-revalidate";
    }

    # === 前端（Vue 3 SPA）===
    location / {
        root /www/wwwroot/netclub;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    # === Vue 构建产物缓存 ===
    location /assets/ {
        alias /www/wwwroot/netclub/assets/;
        expires 30d;
        access_log off;
    }

    # === 后端 API（Django DRF）===
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

    # === Django 静态文件 ===
    location /static/ {
        alias /www/wwwroot/netclub/static/;
        expires 30d;
        access_log off;
    }

    # === 上传文件 ===
    location /media/ {
        alias /www/wwwroot/netclub/media/;
        expires 30d;
        access_log off;
    }
}
```

修改站点配置后，记得执行：

```bash
nginx -t
systemctl reload nginx
```

### 当前脚本文件

服务器上推荐保留以下脚本：

- `/root/deploy_frontend.sh`：前端部署
- `/root/deploy_backend.sh`：后端部署
- `/root/deploy_all.sh`：前后端一起部署

### 服务器首次部署步骤

如果要在一台新服务器上首次部署当前项目，建议按下面顺序进行。

#### 1. 准备基础环境

确保服务器已具备：

- Nginx
- MySQL
- Python 3
- `python3-venv`
- Supervisor
- 宝塔面板（如果你使用宝塔管理）

#### 2. 准备目录

当前线上目录约定如下：

- 前端站点目录：`/www/wwwroot/netclub`
- 后端项目目录：`/root/Woruld_Sophia/backend`

如目录不存在，请先创建或上传项目代码。

#### 3. 初始化后端环境

```bash
cd /root/Woruld_Sophia/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

然后根据实际数据库信息修改 `.env`。

#### 4. 初始化数据库

确认 MySQL 已启动，并提前创建：

- 数据库
- 数据库用户
- 对应权限

然后执行：

```bash
cd /root/Woruld_Sophia/backend
source venv/bin/activate
python manage.py migrate
python manage.py collectstatic --noinput
```

#### 5. 配置 Gunicorn（推荐 Supervisor 托管）

建议不要再用手工 `nohup` 方式，而是使用 Supervisor 托管 Gunicorn。

推荐将以下内容保存为：

```bash
/etc/supervisor/conf.d/netclub_gunicorn.conf
```

完整配置如下：

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
supervisorctl status
```

常用管理命令：

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

#### 6. 配置 Nginx

Nginx 需要满足以下能力：

- `/` 提供 Vue 前端 SPA
- `/api/` 反向代理 Django / Gunicorn
- `/static/` 映射 Django 静态文件
- `/media/` 映射上传文件

推荐直接参考本 README 上方的“保守版 Nginx 配置”。

修改完成后执行：

```bash
nginx -t
systemctl reload nginx
```

#### 7. 首次发布前端

在本地执行：

```bash
npm install
npm run build
scp -r dist root@47.116.119.51:/root/upload/
```

然后在服务器执行：

```bash
bash /root/deploy_frontend.sh
```

#### 8. 验证部署结果

建议至少检查以下内容：

- 首页能正常打开
- `http://47.116.119.51/api/login` 或 `https://47.116.119.51/api/login` 可连通
- 登录页能正常提交请求
- `supervisorctl status` 中 `netclub_gunicorn` 状态为 `RUNNING`
- 浏览器强刷缓存后，前端页面为最新版本

---

## 当前待完善内容

这个项目目前更接近一个“前端原型 / 开发版”，如果要继续完善，建议优先做：

1. 补全 `loginWithBackend`，接入真实后端登录接口（store 与组件无需改动）
2. 增加 token 过期处理
3. 将各业务分组页面从占位页改为正式页面，并按 `canViewGroup` / `canEditGroup` 控制工作项的查看与编辑
4. 丰富首页内容
5. 增加统一的 API 请求封装
6. 持续完善 README、部署说明与项目文档

---

## 注意事项

- `.env.local` 不应提交到 GitHub（已被 `.gitignore` 忽略）
- 当前业务页大多仍为占位页，权限判定函数已就绪但尚未在页面内调用
- 当前登录仅适用于开发阶段演示；生产环境调用 `loginWithBackend`，未接入后端则登录失败
- 分组页面任何登录用户均可访问，工作项目的查看 / 编辑由角色权限控制

---

## Git 同步常用命令

```bash
git add .
git commit -m "update"
git push
```

拉取远程更新：

```bash
git pull
```
