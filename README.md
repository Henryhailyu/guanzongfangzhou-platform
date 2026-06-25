# 管理类联考备考平台

## 本地开发（Docker）

```bash
cd docker
docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build
```

访问：http://localhost

## 本地开发（前端热重载）

```bash
# 终端1：仅启动数据库与后端
cd docker && docker compose -f docker-compose.yml -f docker-compose.dev.yml up mysql redis mongodb backend

# 终端2：前端
cd frontend && npm install && npm run dev
```

访问：http://localhost:5173

## 测试账号

| 角色 | 邮箱 | 密码 |
|---|---|---|
| 管理员 | admin@guanlian.com | admin123 |
| 教师 | teacher@guanlian.com | teacher123 |
| 学生 | student@guanlian.com | student123 |

教师主页示例：/teachers/zhang-math
