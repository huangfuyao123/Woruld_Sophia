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

## 当前待完善内容

这个项目目前更接近一个“前端原型 / 开发版”，如果要继续完善，建议优先做：

1. 补全 `loginWithBackend`，接入真实后端登录接口（store 与组件无需改动）
2. 增加 token 过期处理
3. 将各业务分组页面从占位页改为正式页面，并按 `canViewGroup` / `canEditGroup` 控制工作项的查看与编辑
4. 丰富首页内容
5. 增加统一的 API 请求封装
6. 完善 README、部署说明与项目文档

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
