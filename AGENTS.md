# 管理类联考备考平台 — 项目全局说明文档

> 供 **Cursor Agent** 阅读。每次开始编码任务前必须先读取本文件。
>
> 版本：v1.5 | 维护人：Hai Lyu | 创建日期：2026-06-23

---

## 0. 文档说明与使用方式

### 用途

本文件是项目的**唯一权威上下文**，供：

1. **Cursor Agent** — 编码前必读，严格遵守技术栈与业务规则
2. **人类开发者** — 项目全景说明与决策参考
3. **后续对话** — 增量更新的载体，每次变更记录在文末「变更记录」

### 源文件关系

由以下两份文档合并规整而来（内容相同，已去重）：

- `管理类联考教学平台.md`
- `cursor.md`

原有两个 md 文件暂不删除，待 `AGENTS.md` 确认满意后可归档。

### 维护方式

- 通过对话迭代完善，**有新想法先记入第十章「后续想法记录区」，确认后迁入正文**
- 每次重要变更更新版本号与「变更记录」
- 部署相关改动必须同步更新第三章与 `docker/` 目录

### 0.1 文档目录速查

| 章节 | 内容 |
|---|---|
| §1 | 产品与业务（定位、三端、营销、考试结构、促销） |
| §2 | 技术架构（技术栈、云服务、教师 AI 知识库） |
| §3 | 腾讯云 + Docker 部署 |
| §4 | 开发路线图（MVP / 二期 / 三期） |
| §5 | 核心业务规则（积分、错题、视频、AI 批改） |
| §6 | 数据与 API |
| §7 | 前端三端路由与设计系统 |
| §8 | 工程目录结构 |
| §9 | Cursor Agent 工作指令 |
| 附录 A/B | 促销详细规格与数据库表 |
| §10 | 后续想法记录区（待讨论的新点子） |
| 文末 | 变更记录、待确认清单 |

### 0.2 已确认产品决策总览

> 截至 v1.5，以下决策已确认，编码时以本表为准。

| 类别 | 决策项 | 结论 |
|---|---|---|
| **平台模式** | 定位 | 商用多教师入驻平台（类小鹅通） |
| **三端** | 端口划分 | 学生端 + 教师端 + 管理员端 |
| **三端** | 访问方式 | 子域名：`www` / `teacher` / `admin` |
| **三端** | 技术方案 | 单 Vue 3 项目 + 三套路由布局 |
| **教师** | 入驻方式 | 开放申请 + 管理员审核 |
| **教师** | 课程分成 | 教师 70%，平台 30% |
| **教师** | 学员管理范围 | 仅自己课程的已购学员 |
| **AI** | 大模型 | 全部使用腾讯混元，不用境外 API |
| **AI** | 答疑定价 | 平台统一定价（消耗积分） |
| **AI** | 教师知识库 | 第二期上线 |
| **营销** | 三层体系 | 平台促销 + 教师自主营销 + 学员分销 |
| **营销** | 学员佣金来源 | 从教师 70% 份额中扣除，平台不贴钱 |
| **营销** | 学员佣金默认值 | 默认 **10%**，管理员上限 **20%** |
| **营销** | 分销层级 | **仅一级**，不做多级分销 |
| **营销** | 佣金结算基数 | 按实付金额（先扣平台优惠券再算分成） |
| **营销** | 提现门槛 | 满 ¥50 可提现 |
| **营销** | 推广归因窗口 | 首访/注册后 **7 天**内购课有效 |
| **基础设施** | 部署 | Lighthouse + Docker Compose |
| **基础设施** | 生产数据库 | 全部腾讯云托管，不进 Docker |

---

## 1. 产品与业务

### 1.1 产品定位

针对中国考研**管理类联考**（199 综合能力 + 英语二）的**商用在线学习平台**。目标用户为备考 MBA、MPA、MPAcc、MEM、MAud 等管理类专业硕士的在职人员和应届生。

**平台模式：多教师入驻（类小鹅通/知识店铺）**

- 平台提供基础设施：题库、支付、积分、视频、AI 工具
- **教师**在平台内开设自己的课程空间，上传内容、定价、运营学员
- 每位教师可配置**个性化 AI 助教**（第二期上线，基于自有知识库 + 教学风格）
- 平台面向**商用场景**，需支撑大量并发用户与多租户数据隔离

### 1.5 三端架构与角色体系

平台分为**三个独立端口**，共用同一后端 API，按角色权限隔离数据与功能。

```mermaid
flowchart TB
  subgraph portals [三端入口]
    student[学生端]
    teacher[教师端]
    admin[管理员端]
  end
  subgraph api [统一后端 API]
    flask[Flask + FastAPI]
  end
  subgraph data [数据层]
    mysql[(MySQL)]
    mongo[(MongoDB)]
  end
  student -->|"role=student"| flask
  teacher -->|"role=teacher"| flask
  admin -->|"role=admin"| flask
  flask --> mysql
  flask --> mongo
```

| 端口 | 访问路径 | 角色 | 核心职责 |
|---|---|---|---|
| **学生端** | `www.domain.com` | `student` | 刷题、看课、购课、积分、学习进度、推广赚佣金 |
| **教师端** | `teacher.domain.com` | `teacher` | 课程运营、学员管理、自主营销、收入查看 |
| **管理员端** | `admin.domain.com` | `admin` | 管控全平台：用户、教师、题库、订单、促销、系统配置 |

**权限层级（自上而下）：**

```
管理员（admin）  →  可见并管控全平台所有数据
    ↓
教师（teacher）  →  仅可见 teacher_id = 自己的课程、学员、订单、数据
    ↓
学生（student）  →  仅可见自己的学习数据、已购课程、积分
```

**已确认的产品决策：**

| 决策项 | 结论 |
|---|---|
| AI 答疑定价 | **平台统一定价**，学员消耗积分，教师不可自行定价 |
| 教师知识库 + 个性化 AI | **第二期**上线，MVP 仅平台级混元 AI |
| 教师学员管理范围 | 教师只能管理**购买了该教师课程**的学员，不能看到全平台学生 |
| 教师入驻 | **开放申请 + 管理员审核**（`teacher_profiles.status`） |
| 三端访问方式 | **子域名**：`www` / `teacher` / `admin` |
| 课程销售分成 | 教师 **70%**，平台 **30%**（`teacher_profiles.commission_rate` 默认 0.70） |
| 教师自主营销 | 教师可自行配置推广方式，学员帮推可得佣金/优惠（见 §1.6） |
| 学员分销默认值 | 佣金比例默认 **10%**，管理员上限 **20%**（见 §1.6.3） |
| 分销层级 | **仅一级分销**，禁止多级（合规与复杂度考量） |

### 1.6 教师自主营销与学员分销体系

> 营销能力下放给每位教师，教师自行决定如何推销自己的课程；学员（及任何推广者）通过专属链接推广可获佣金或优惠。

#### 1.6.1 设计理念

```
平台促销（管理员配置）     →  全平台活动（优惠券、秒杀、限时折扣）
        +
教师自主营销（教师配置）   →  专属链接/海报/店铺页，适配抖音/小红书/微信等
        +
学员分销（教师开启后）     →  学员帮老师推广课程，成交后获佣金或积分奖励
```

**三层分工：**

| 层级 | 谁配置 | 谁推广 | 典型场景 |
|---|---|---|---|
| 平台促销 | 管理员 | 平台统一运营 | 考研季大促、新人券 |
| 教师营销 | 教师 | 教师本人 + 外部渠道 | 抖音短视频挂课程链接、朋友圈海报 |
| 学员分销 | 教师开启并设比例 | 已注册学员/粉丝 | 老学员推荐新学员报课，获现金或积分 |

#### 1.6.2 教师端营销工具箱

教师在 `teacher.domain.com` 的营销中心可自助完成：

| 工具 | 说明 | 分期 |
|---|---|---|
| **教师主页** | 学生端公开页 `/teachers/:slug`，展示简介、课程、评价 | MVP |
| **专属推广链接** | 按课程或全店生成带参链接 `?ref=T123_C456` | MVP |
| **二维码 / 海报** | 一键生成可转发至微信、抖音简介的课程海报 | 第二期 |
| **学员分销开关** | 开启/关闭；设置佣金比例与奖励形式 | 第二期 |
| **推广数据看板** | 点击量、注册量、成交量、佣金支出 | 第二期 |
| **短视频落地页** | 精简课程介绍页，适配抖音/快手外链 | 第三期 |

**外链场景示例：**

- 抖音/小红书主页 Bio → 教师专属链接 → 学生端教师主页 → 购课
- 微信朋友圈 → 课程海报二维码 → 直达课程详情页
- 学员分享 → 带 `ref=学员ID` 的链接 → 新用户注册购课 → 学员获佣金

#### 1.6.3 学员分销机制（教师可配置）

教师开启学员分销后，**已注册学生**可在学生端「推广中心」推广该教师的课程。

**奖励形式（教师可选一种或组合，管理员设上限）：**

| 奖励类型 | 说明 | 示例 |
|---|---|---|
| **现金佣金** | 成交后按课程价百分比结算，可提现 | 课程 ¥199，佣金 10% → 推广者得 ¥19.9 |
| **积分奖励** | 成交后获赠平台积分 | 成功推荐一人 +200 积分 |
| **优惠券** | 推广者本人获得下次购课折扣券 | 推荐成功得 8 折券 |

**佣金来源与分成逻辑（¥100 课程成交示例）：**

```
订单金额           ¥100
├── 平台抽成 30%    ¥30
└── 教师收入 70%    ¥70
        ├── 若有学员推广佣金 10%（¥10）→ 从教师 70% 中扣除，给推广学员
        └── 教师实际到手           ¥60
```

> **原则**：学员推广佣金从**教师收入份额**中支出，不额外增加平台成本。平台管理员设置全局佣金上限，教师在上限内自行配置。

**默认参数（已确认）：**

| 参数 | 默认值 | 说明 |
|---|---|---|
| `referral_commission_rate` | **10%** | 教师开启学员分销时的默认佣金比例 |
| `max_commission_rate` | **20%** | 管理员可设的全局上限，教师不可超过 |
| `referral_points` | **200 分** | 选择积分奖励时的默认赠送量 |
| `referral_bind_days` | **7 天** | 推广关系有效窗口 |
| `withdraw_min_amount` | **¥50** | 推广佣金提现门槛 |

**防作弊规则（必须实现）：**

- 推广关系绑定：新用户首次通过推广链接注册/访问后 7 天内购课有效
- 自推自买无效：推广者 ID ≠ 购买者 ID
- 同设备/同支付账号限购一次佣金
- 佣金满 ¥50 可提现（与平台推广员规则一致）
- 退款订单自动追回已发佣金

**分销层级限制（已确认）：**

- **仅支持一级分销**：学员 A 推广 → 新用户 B 购课 → A 得佣金
- **禁止多级**：B 不能再发展下级 C 并产生二级佣金
- 原因：降低合规风险、逻辑简单、避免传销式结构

#### 1.6.4 学生端相关页面

| 路由 | 说明 |
|---|---|
| `/teachers/:slug` | 教师公开主页（课程列表、简介、可购课） |
| `/courses/:id?ref=xxx` | 课程详情（带推广参数，下单时记录推广关系） |
| `/profile/promote` | 学员推广中心：我的推广链接、收益、已推荐人数 |
| `/profile/earnings` | 推广收益明细与提现 |

#### 1.6.5 与平台促销的关系

- **平台促销**（优惠券、限时折扣）与**教师分销**可叠加，但需管理员配置叠加规则
- **已确认**：先应用平台优惠券，再按**实付金额**计算教师分成与学员佣金
- 教师不可修改平台级促销，仅可叠加自己的学员分销

#### 1.6.6 实施分期

| 阶段 | 营销能力 |
|---|---|
| **MVP** | 教师主页 + 专属推广链接/二维码；平台级邀请码积分；订单记录 `referrer_id` |
| **第二期** | 学员分销（教师可配置佣金/积分）；海报生成；推广数据看板 |
| **第三期** | 短视频落地页；渠道效果分析（仍仅一级分销） |

#### 1.6.7 架构设计要点（备忘）

```mermaid
flowchart LR
  subgraph channels [推广渠道]
    douyin[抖音/小红书]
    wechat[微信/朋友圈]
    studentRef[学员分销]
  end
  subgraph platform [平台]
    teacherPage[教师主页]
    coursePage[课程详情]
    order[订单系统]
  end
  subgraph settlement [结算]
    platformFee[平台30%]
    teacherIncome[教师70%]
    referrerFee[学员佣金从教师份额扣]
  end
  douyin --> teacherPage
  wechat --> coursePage
  studentRef --> coursePage
  coursePage --> order
  order --> platformFee
  order --> teacherIncome
  teacherIncome --> referrerFee
```

**关键设计原则：**

1. **营销下放但不失控** — 教师自主推广，平台设上限与防作弊规则
2. **平台不做贴钱分销** — 学员佣金从教师份额出，平台只收 30%
3. **MVP 轻量启动** — 先做链接追踪 + 教师主页，学员分销放第二期
4. **管理端保留终审权** — 可下架违规课程、暂停教师、调整全局佣金上限
5. **管理端安全加固** — `admin.domain.com` 建议 IP 白名单或二次验证

### 1.2 考试结构（影响题库和模块设计）

| 科目 | 题型 | 分值 |
|---|---|---|
| **数学基础** | 问题求解×15（五选一）+ 条件充分性判断×10（五选一） | 75分 |
| **逻辑推理** | 单选×30（形式推理/论证推理/综合推理） | 60分 |
| **写作** | 论证有效性分析×1（30分）+ 论说文×1（35分） | 65分 |
| **英语二** | 完形填空+阅读理解+翻译+小作文+大作文 | 100分 |
| **总计** | | 300分 |

### 1.3 考生核心痛点（产品设计出发点）

1. **做题速度慢** — 题量大，时间紧（管综 3 小时）
2. **条件充分性判断**难，市面专项训练少
3. **逻辑阅读量大**（2025 年约 8500 字），近年持续增加
4. **写作思辨能力弱**，很多人不会找论证漏洞
5. **在职人员时间碎片**，需要高效利用通勤/午休时间
6. **英语基础差**，词汇量不足

### 1.4 促销体系摘要

本平台将实现小鹅通营销中心的全部促销功能，分六大类共 28 种玩法，按 MVP→第二期→第三期分批上线。所有促销功能需在管理后台提供可视化配置界面。

| 类别 | 包含玩法 | 数量 |
|---|---|---|
| 价格促销 | 划线价、普通优惠券、有价优惠券、限时折扣、秒杀、弹窗广告 | 6 |
| 社交裂变 | 邀请码/卡、兑换码、请好友免费看、涨粉神器、裂变海报、普通/邀新/阶梯拼团 | 7 |
| 留存激励 | 打卡系统、打卡返学费、支付有礼、成长任务+勋章、排行榜、结课证书、送好友 | 7 |
| 分销推广 | 推广员计划、批量兑换码、内容分销市场 | 3 |
| 智能运营 | 兴趣转换、未付款唤回、新客复购、高活维系、流失召回、收藏未购 | 6 |
| 店铺展示 | 销售弹幕、划线价展示、首页轮播+微页面、商品分组推荐位 | 4 |

**实施优先级：**

```
【MVP 第一期】— 核心转化工具
  ✅ 划线价展示
  ✅ 普通优惠券（新人券 + 满减券）
  ✅ 限时折扣（带倒计时）
  ✅ 邀请码注册（双向积分）
  ✅ 请好友免费看（单节试看）
  ✅ 打卡签到 + 连续打卡奖励
  ✅ 打卡返学费（VIP 年卡用户）
  ✅ 批量兑换码（机构合作）
  ✅ 弹窗广告（大促期间手动开关）

【第二期】— 裂变与自动化
  ⬜ 秒杀、有价优惠券、三种拼团、裂变海报、涨粉神器
  ⬜ 推广员分销、支付有礼、成长任务+勋章、排行榜
  ⬜ 结课证书、送好友、智能自动化运营、销售弹幕

【第三期】— 生态完善
  ⬜ 内容分销市场、付费打卡、活动微页面
  ⬜ 商品分组推荐位、积分商城、二级推广员佣金
```

> 28 种促销玩法详细规格见**附录 A**。

---

## 2. 技术架构总览

### 2.1 技术栈（必须严格遵守，不得随意替换）

#### 前端

- **Vue.js 3**（Composition API）+ Element Plus + Axios
- **uni-app**（第二期，编译为微信小程序 + H5）
- React（特定复杂交互场景可用）

#### 后端

- **Flask**（Python）— 主要 API 服务
- **Node.js / Express** — 实时功能（WebSocket、直播信令）
- **FastAPI** — AI 相关接口（异步处理）

#### 数据库（商用级，全部腾讯云托管）

- **MySQL**（TencentDB 高可用版）— 主数据库，读写分离，自动备份
- **Redis**（腾讯云 Redis 集群版）— 缓存、Session、积分实时计算、刷题状态
- **MongoDB**（腾讯云数据库 MongoDB）— 题库、答题记录、学习行为日志
- **VectorDB**（腾讯云向量数据库）— 教师知识库向量检索（RAG）

> **原则：生产环境禁止将数据库放进 Docker Compose。** 商用场景必须走腾讯云托管，保障稳定性与可扩展性。

#### AI 集成（全部使用腾讯云混元，不使用境外 API）

- **腾讯混元大模型**（Hunyuan）— **唯一大模型供应商**
  - 题目智能解析、AI 练习题生成
  - 写作批改、论证分析评分
  - 教师个性化 AI 答疑（结合知识库 RAG）
- **腾讯云知识引擎 / 向量检索** — 教师知识库构建与检索增强（RAG）
- **不使用 Anthropic Claude API**（中国大陆网络不稳定，已废弃）

### 2.2 服务关系图

```mermaid
flowchart LR
  subgraph lighthouse [Lighthouse轻量服务器]
    nginx[Nginx反向代理]
    flask[Flask API]
    node[Node Express实时]
    fastapi[FastAPI AI]
    frontend[Vue静态资源]
  end
  subgraph tencent [腾讯云托管服务]
    tdb[(TencentDB MySQL HA)]
    redis[(Redis集群)]
    mongo[(MongoDB)]
    vectordb[(VectorDB)]
    cos[COS]
    vod[VOD]
    css[CSS直播]
    sms[SMS]
    hunyuan[混元大模型]
  end
  user[用户浏览器] --> nginx
  nginx --> frontend
  nginx --> flask
  nginx --> node
  nginx --> fastapi
  flask --> tdb
  flask --> redis
  flask --> mongo
  flask --> cos
  fastapi --> hunyuan
  fastapi --> vectordb
  flask --> vod
  node --> css
```

### 2.3 层级分工

| 层级 | 组件 | 说明 |
|---|---|---|
| 计算 | Lighthouse + Docker | 跑应用容器，Ubuntu 22.04 |
| 关系数据 | TencentDB MySQL 高可用版 | 用户/订单/积分/教师/课程，读写分离 |
| 缓存 | 腾讯云 Redis 集群版 | Session、积分、刷题状态、热点缓存 |
| 文档数据 | 腾讯云 MongoDB | 题库、答题日志、行为数据 |
| 向量数据 | 腾讯云 VectorDB | 教师知识库 embedding 存储与检索 |
| 媒体 | COS + VOD + CSS | 纯腾讯云 SaaS，容器通过 SDK 调用 |
| AI | 混元大模型 + RAG | 全部 AI 能力统一走腾讯云，密钥通过 `.env` 注入 |

### 2.4 商用数据库架构（必须遵守）

本平台为**商用多租户系统**，数据库设计须满足高可用、可扩展、数据隔离。

#### 2.4.1 生产环境推荐配置

| 组件 | 腾讯云产品 | 推荐规格（起步） | 关键配置 |
|---|---|---|---|
| 关系数据库 | TencentDB MySQL | 高可用版，4核8G 起 | 自动备份、binlog、读写分离（1 主 1 从） |
| 缓存 | 云数据库 Redis | 集群版，4G 起 | 持久化开启、主从切换 |
| 文档数据库 | 云数据库 MongoDB | 副本集，4核8G 起 | 三节点副本集、自动备份 |
| 向量数据库 | 向量数据库 VectorDB | 按教师数量扩展 | 按 `teacher_id` 分 Collection/Namespace |
| 对象存储 | COS | 标准存储 | 版本控制、跨 AZ 冗余 |

#### 2.4.2 多租户数据隔离策略

```
平台层（platform）
  ├── 用户、订单、积分、支付 — MySQL，全局共享
  ├── 平台公共题库 — MongoDB，subject/tag 索引
  └── 平台级 AI（写作批改、公共出题）— 混元 API

教师层（tenant = teacher_id）
  ├── 课程、课时、定价 — MySQL，courses.teacher_id 隔离
  ├── 教师私有题库 — MongoDB，teacher_id 字段隔离
  ├── 教师知识库 — VectorDB，每教师独立 Collection
  ├── 教师 AI 配置 — MySQL，人设/风格/答疑规则
  └── 学员 AI 对话记录 — MongoDB，按 teacher_id + user_id 隔离
```

#### 2.4.3 扩展路径

| 阶段 | 用户规模 | 架构调整 |
|---|---|---|
| MVP | < 1 万注册用户 | 单 Lighthouse + 托管数据库起步规格 |
| 成长期 | 1–10 万 | MySQL 升配 + 读写分离；Redis 集群扩容；CDN 全开 |
| 规模期 | 10 万+ | Lighthouse 迁 CVM 多节点；MongoDB 分片；VectorDB 按教师扩容 |

### 2.5 腾讯云产品清单

**云平台：腾讯云（cloud.tencent.com）— 唯一云平台**

| 腾讯云产品 | 用途 |
|---|---|
| **轻量应用服务器 Lighthouse** | 应用宿主，运行 Docker Compose（**当前选用**） |
| **CVM** | 用户量达 10 万+ 时迁移扩容 |
| **TencentDB MySQL 高可用版** | 用户/订单/积分/教师/课程（商用核心） |
| **云数据库 Redis 集群版** | 缓存、Session、积分实时计算 |
| **云数据库 MongoDB** | 题库、答题日志、AI 对话记录 |
| **向量数据库 VectorDB** | 教师知识库 RAG 向量检索 |
| **COS**（对象存储） | 图片、PDF、题目附件、知识库原始文件 |
| **VOD**（云点播） | 录播课视频（防盗链签名 URL） |
| **CSS**（云直播）+ **TRTC** | 直播课（教师端推流，学生端播放） |
| **IM**（即时通信） | 直播课聊天室、师生消息 |
| **SMS**（短信服务） | OTP 验证码 |
| **混元大模型**（Hunyuan） | **全部 AI 能力**（出题、批改、答疑、解析） |
| **ASR**（语音识别） | 直播课自动字幕、知识库音视频转文字 |
| **CDN** | 全国加速 |
| **SSL 证书** | HTTPS |

### 2.6 教师个性化 AI 知识库架构

> 每位教师可训练自己的 AI 助教，按自身教学思路和答疑方法服务学员。

#### 2.6.1 核心概念

| 概念 | 说明 |
|---|---|
| **教师 AI Agent** | 绑定 `teacher_id` 的个性化 AI 助教，有独立人设与知识库 |
| **知识库** | 教师上传的教学资料（课件、讲义、录播字幕、历年答疑记录） |
| **人设配置** | 教师的答疑风格、语气、方法论（如"先引导再给答案"） |
| **RAG 检索** | 学员提问时，先从该教师知识库检索相关内容，再交给混元生成回答 |

#### 2.6.2 知识库构建流程

```mermaid
flowchart TD
  upload[教师上传资料] --> parse[文档解析与分块]
  parse --> embed[混元 Embedding向量化]
  embed --> store[存入VectorDB按teacher_id隔离]
  store --> ready[知识库就绪]
  ready --> config[教师配置AI人设与答疑规则]
  config --> agent[教师AI Agent上线]
```

**支持的知识库来源：**

- Word / PDF / PPT 课件
- 课程录播字幕（ASR 自动转写）
- 教师手动录入的 FAQ、解题套路
- 历史答疑记录（经教师审核后入库）

#### 2.6.3 学员答疑流程

```
学员在课程页提问
  ↓
鉴权：是否为该教师课程的付费学员
  ↓
加载该教师的 AI 人设配置（system prompt）
  ↓
VectorDB 检索该教师知识库 Top-K 相关片段
  ↓
拼装 Prompt：人设 + 检索上下文 + 学员问题
  ↓
调用混元大模型生成回答
  ↓
记录对话到 MongoDB（teacher_id + user_id + course_id）
  ↓
可选：学员评价回答质量，教师可审核并补充到知识库
```

#### 2.6.4 实施分期

| 阶段 | 能力 |
|---|---|
| **MVP** | 平台级混元 AI（写作批改、题目解析、公共出题）；三端框架；教师端学员管理 |
| **第二期** | 教师知识库上传 → 自动建库 → 课程内 AI 答疑（RAG）；教师 AI 人设配置 |
| **第三期** | 教师 AI 多轮记忆、答疑质量反馈闭环、知识库增量更新 |

---

## 3. 腾讯云与 Docker 部署

### 3.1 部署方案

**选用：腾讯云轻量应用服务器（Lighthouse）+ Docker Compose**

- 操作系统：Ubuntu 22.04 LTS
- 地域推荐：`ap-guangzhou`（广州，与 TencentDB/混元同区域降低延迟）
- 所有应用服务容器化部署在 Lighthouse 上
- MySQL、Redis 使用腾讯云托管实例，通过内网/公网连接

### 3.2 Docker Compose 服务规划

```
guanlian-learning/
├── docker/
│   ├── docker-compose.yml          # 基础配置（开发+生产共用）
│   ├── docker-compose.prod.yml     # 生产覆盖配置
│   ├── docker-compose.dev.yml      # 开发覆盖（含本地 MySQL/Redis）
│   ├── nginx/
│   │   └── nginx.conf              # 反向代理 + SSL 终止
│   ├── flask/Dockerfile
│   ├── node/Dockerfile
│   ├── fastapi/Dockerfile
│   └── frontend/Dockerfile         # 多阶段构建 Vue
```

**Compose 服务定义：**

| 服务名 | 镜像/构建 | 端口 | 职责 |
|---|---|---|---|
| `nginx` | nginx:alpine + 自定义配置 | 80, 443 | 入口，SSL 终止，静态资源 |
| `backend` | docker/flask | 5000 | Flask 主 API |
| `realtime` | docker/node | 3001 | WebSocket、直播信令 |
| `ai-service` | docker/fastapi | 8000 | 异步 AI 接口 |
| `frontend` | docker/frontend | — | Vue 构建产物（挂载到 nginx） |
| `mongodb` | mongo:7 | 27017 | **仅开发环境**，生产用腾讯云 MongoDB |

**Nginx 路由规则：**

- `/` → frontend 静态资源
- `/api/*` → `backend:5000`
- `/ws/*` → `realtime:3001`（WebSocket upgrade）
- `/ai/*` → `ai-service:8000`

**不包含在 Compose 中（生产必须腾讯云托管）：**

- MySQL（TencentDB 高可用版）
- Redis（腾讯云 Redis 集群版）
- MongoDB（腾讯云数据库 MongoDB）
- VectorDB（腾讯云向量数据库）

### 3.3 环境分层

| 环境 | 运行方式 | 数据库 | 说明 |
|---|---|---|---|
| `development` | 本地 `docker compose -f docker-compose.yml -f docker-compose.dev.yml up` | 可用 Compose 内 MySQL/Redis 简化开发 | 热重载、调试友好 |
| `production` | Lighthouse 上 `docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d` | 全部连腾讯云托管实例 | 正式商用对外服务 |

### 3.4 部署流程

1. **Lighthouse 初始化**
   - 购买轻量应用服务器（Ubuntu 22.04）
   - 开放端口：22（SSH）、80、443
   - 安装 Docker + Docker Compose Plugin

2. **腾讯云控制台开通托管服务**
   - TencentDB MySQL（高可用版）、Redis（集群版）、MongoDB、VectorDB、COS、VOD、混元 API、SMS 等
   - 记录连接地址、端口、账号（写入 `.env.production`）

3. **域名与 SSL**
   - 域名 A 记录解析到 Lighthouse 公网 IP
   - 腾讯云免费 SSL 证书，挂载到 nginx 容器

4. **配置环境变量**
   - 复制 `.env.example` 为 `.env.production`
   - 填入真实密钥（**不提交 git**）

5. **启动服务**

   ```bash
   docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
   ```

6. **健康检查与日志**

   ```bash
   docker compose ps
   docker compose logs -f backend
   curl https://yourdomain.com/api/health
   ```

### 3.5 安全与运维要点

- 所有密钥仅存 `.env`，通过 Compose `env_file` 注入容器
- VOD 播放 URL 必须签名，有效期 2 小时
- 微信支付/支付宝回调必须验签
- Lighthouse 防火墙 + 腾讯云安全组最小开放（仅 22/80/443）
- TencentDB 开启自动备份；COS 开启版本控制
- 定期 `docker compose pull && docker compose up -d` 更新镜像

---

## 4. 开发路线图与优先级

### 4.1 MVP 第一期 — Web 网页版（当前阶段）

> 优先完成，验证核心功能

**必须实现的功能：**

1. 用户注册/登录（邮箱 + 手机号，预留微信登录接口）
2. **三端框架**：学生端 + 教师端 + 管理员端（路由守卫 + 角色权限）
3. 题库浏览（按科目 / 知识点标签）
4. 刷题练习（随机练习 / 专项练习）
5. 答题与即时判分（客观题自动判，写作题 AI 批改）
6. 错题本（收录错题 + 关联同类题目）
7. 积分系统（见第五章）
8. 学习进度看板（每科完成率、连续打卡天数）
9. 基础支付（微信支付/支付宝 购买积分/课程）
10. 视频课程（VOD 点播，免费预览 + 付费完整版）

**三端 MVP 功能分工：**

| 端口 | MVP 必须实现 |
|---|---|
| 学生端 | 刷题、看课、购课、积分、学习进度、写作批改 |
| 教师端 | 课程/课时 CRUD、学员列表、学情查看、收入概览、**教师主页与推广链接** |
| 管理员端 | 全平台用户管理、教师审核、公共题库、订单、促销配置、系统参数、数据看板 |

### 4.2 第二期 — 微信小程序 + 教师 AI

- uni-app 复用第一期核心逻辑
- 微信登录 + 微信支付
- 轻量刷题（碎片时间场景）
- **教师知识库上传 + 个性化 AI 答疑（RAG）**
- 教师后台：课程管理、学员管理、AI 人设配置

### 4.3 第三期 — 原生 APP + AI 生态

- iOS（Xcode / Swift）
- Android（Android Studio / Kotlin）
- 鸿蒙（HarmonyOS）
- 教师 AI 多轮记忆、答疑质量反馈闭环、知识库增量学习

---

## 5. 核心业务规则

> AI Agent 必须严格遵守以下业务逻辑。

### 5.1 积分获得途径

| 行为 | 获得积分 |
|---|---|
| 每日首次登录签到 | +10分 |
| 完成一道题目（答对） | +3分 |
| 完成一道题目（答错） | +1分 |
| 完成一套模拟题 | +50分 |
| 连续登录 7 天 | 额外 +50分 |
| 连续登录 30 天 | 额外 +200分 |
| 分享平台给好友（好友注册） | +30分 |
| 参与社区讨论/答疑 | +5分/次 |
| 购买课程/积分包 | 按金额比例获赠积分 |

### 5.2 积分消耗途径

| 消耗场景 | 消耗积分 |
|---|---|
| 免费额度用尽后继续刷题 | 每道题 -5分（客观题） |
| 查看 AI 视频解析 | -10分/题 |
| AI 写作批改一篇 | -50分 |
| 教师 AI 答疑一次（第二期） | -5分（平台统一定价，管理员可配置） |
| 换购付费课程（部分抵扣） | 按课程定价折算 |
| 解锁真题模拟卷（单套） | -100分 |

### 5.3 免费每日额度限制

```
免费用户：每天免费做 20 道题
- 答对：不扣积分
- 答错一道：扣除当日 5 分"额度"
- 当日错题达到 5 道（累计扣 25 分额度）→ 当日免费额度用尽
- 用尽后选择：① 消耗积分继续 ② 付费购买当日无限次 ③ 等明天刷新

付费/VIP 用户：无限刷题，不受每日限制
```

**核心目的：**

1. 答题准确率高的用户可以一直免费用
2. 答题准确率低的用户更快消耗额度，产生付费动力
3. 长期坚持学习的用户积累积分可兑换服务，增加留存

### 5.4 积分等级体系

| 等级 | 积分区间 | 特权 |
|---|---|---|
| 入门生 | 0–500 | 基础刷题功能 |
| 备考生 | 500–2000 | 解锁部分历年真题 |
| 冲刺生 | 2000–5000 | 每月 1 次免费 AI 写作批改 |
| 上岸生 | 5000+ | 专属学习报告、优先客服 |

### 5.5 收费项目定价参考

| 服务 | 定价参考 | 说明 |
|---|---|---|
| 积分包 | ¥6/100积分，¥30/600积分，¥88/2000积分 | 直接购买积分 |
| VIP 月卡 | ¥39/月 | 无限刷题+文字解析 |
| VIP 年卡 | ¥299/年 | 无限刷题+文字解析+每月 3 次 AI 批改 |
| 单科视频课 | ¥99–¥299/科 | 数学/逻辑/写作/英语二 |
| 全科套餐 | ¥699–¥999 | 四科视频课打包 |
| 视频解析（按题） | 消耗 10 积分 或 ¥1/题 | AI+教师视频讲解 |
| AI 写作批改（单次） | 消耗 50 积分 或 ¥5/次 | 混元大模型批改 |
| 真题模拟卷（单套） | 消耗 100 积分 或 ¥9.9/套 | 历年真题全套 |
| 1 对 1 辅导（在线） | ¥150–¥300/小时 | 预约真人教师 |
| 直播课（单次） | ¥19–¥49/节 | 教师直播讲课 |

### 5.6 错题与智能推荐逻辑

```
用户做错一道题 → 记录错题
  ↓
系统读取该题的 tags（primary/secondary/tertiary）
  ↓
从题库中查找：
  1. 同 tertiary 标签的其他题目（最相关）
  2. 同 secondary 标签的题目（次相关）
  ↓
按以下权重排序推荐：
  - 用户之前未做过的：权重最高
  - 用户做过但答错的：权重次高
  - 用户做过且答对的：权重最低（不推荐）
  ↓
下次练习时，该类题目出现频率提高（艾宾浩斯遗忘曲线间隔）

第 N 次做错同类型题 → 频率继续加大，标记为"重点薄弱点"
```

### 5.7 题目来源

**模块一：教师上传**

- 教师在管理后台上传题目（支持 Word/PDF/图片）
- 系统调用**混元大模型**自动解析题目内容、提取知识点、打标签
- 教师审核后发布

**模块二：AI 生成**

- 基于知识点标签，调用**混元大模型**生成练习题
- 系统标注"AI 生成题目"角标，与真题区分
- 学生可选择：只做真题 / 只做 AI 题 / 混合

### 5.8 视频系统

**录播课（VOD）**

- 存储：腾讯云 VOD，防盗链签名 URL（有效期 2 小时）
- 结构：科目 → 章节 → 课时（每课时 20–45 分钟）
- 收费：部分免费预览（前 5 分钟），全集付费

**题目视频解析**

- 文字解析免费 + 视频解析付费（-10 积分或 VIP 免费）
- 视频时长：3–8 分钟

**直播课**

- 推流：腾讯云 CSS；拉流：HLS
- 互动：TRTC（连麦）+ IM（聊天室）
- 录制：直播结束自动转存 VOD

### 5.9 AI 写作批改

- 论证有效性分析、论说文均使用**腾讯混元大模型**
- 评分维度：漏洞识别准确性、分析深度、语言表达、结构完整性（各 25 分）
- 每次批改消耗 50 积分（VIP 有免费额度）

### 5.10 教师 AI 答疑业务规则（第二期上线）

- 仅**已购课学员**可调用该教师的 AI 助教
- **平台统一定价**：每次 AI 答疑消耗积分，价格由管理员在后台配置，教师不可自行修改
- 积分消耗记入平台账户，教师按课程销售额分成（非按 AI 次数分成）
- AI 回答必须基于该教师知识库检索结果，**禁止跨教师知识库检索**
- 教师可设置：是否允许 AI 直接给答案 / 仅引导思考（人设层面，不影响定价）
- 敏感内容过滤：混元内置 + 平台关键词黑名单
- 对话记录归属：`teacher_id` + `user_id`，教师可在教师端查看本课程答疑记录

---

## 6. 数据与 API

### 6.1 知识点标签体系（树形结构）

```
科目（Subject）
├── 数学基础
│   ├── 代数（整式与分式、函数、方程与不等式、数列）
│   ├── 几何（平面几何、立体几何、解析几何）
│   └── 数据分析（排列组合、概率）
├── 逻辑推理
│   ├── 形式逻辑（命题与推理、假言命题）
│   ├── 论证逻辑（削弱型、支持型、解释型）
│   └── 综合推理（分析推理、数独/符号推理）
├── 写作
│   ├── 论证有效性分析（因果混淆、以偏概全、概念不清、论据不足）
│   └── 论说文（命题作文、材料作文）
└── 英语二
    ├── 完形填空
    ├── 阅读理解（Part A、Part B）
    ├── 翻译（英译汉）
    └── 写作（小作文、大作文）
```

### 6.2 MongoDB 题目数据结构

```json
{
  "_id": "ObjectId",
  "question_id": "MATH_001_001",
  "subject": "math",
  "question_type": "problem_solving",
  "difficulty": 3,
  "tags": {
    "primary": "代数",
    "secondary": "函数",
    "tertiary": "二次函数",
    "tag_ids": ["math_algebra", "math_function", "math_quadratic"]
  },
  "source": {
    "type": "teacher_upload",
    "year": 2024,
    "is_real_exam": true
  },
  "content": {
    "stem": "题目正文...",
    "image_urls": [],
    "options": ["A. ...", "B. ...", "C. ...", "D. ...", "E. ..."],
    "correct_answer": "B",
    "answer_analysis": {
      "text": "文字解析...",
      "video_url": "vod://file_id_xxx",
      "video_is_paid": true
    }
  },
  "ai_generated": false,
  "stats": {
    "total_attempts": 1250,
    "correct_rate": 0.42,
    "avg_time_seconds": 180
  },
  "created_at": "2025-01-01T00:00:00Z"
}
```

### 6.3 MySQL 核心表结构

```sql
-- 用户表
CREATE TABLE users (
  id            BIGINT PRIMARY KEY AUTO_INCREMENT,
  openid        VARCHAR(64) UNIQUE,
  nickname      VARCHAR(100),
  phone         VARCHAR(20) UNIQUE,
  email         VARCHAR(100) UNIQUE,
  password_hash VARCHAR(255),
  role          ENUM('student','teacher','admin') DEFAULT 'student',
  points        INT DEFAULT 0,
  level         ENUM('入门生','备考生','冲刺生','上岸生') DEFAULT '入门生',
  vip_expires_at DATETIME,
  target_school VARCHAR(100),
  target_major  ENUM('MBA','MPA','MPAcc','MEM','MAud','MTA','MLIS'),
  exam_year     INT,
  created_at    DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 积分流水表
CREATE TABLE point_transactions (
  id          BIGINT PRIMARY KEY AUTO_INCREMENT,
  user_id     BIGINT REFERENCES users(id),
  amount      INT NOT NULL,
  type        VARCHAR(50) NOT NULL,
  description VARCHAR(200),
  balance     INT NOT NULL,
  created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 每日刷题额度表（Redis 为主，MySQL 做持久化）
CREATE TABLE daily_quota (
  id          BIGINT PRIMARY KEY AUTO_INCREMENT,
  user_id     BIGINT REFERENCES users(id),
  date        DATE NOT NULL,
  free_done   INT DEFAULT 0,
  wrong_count INT DEFAULT 0,
  quota_used  BOOLEAN DEFAULT FALSE,
  UNIQUE KEY uq_user_date (user_id, date)
);

-- 用户答题记录表
CREATE TABLE answer_records (
  id            BIGINT PRIMARY KEY AUTO_INCREMENT,
  user_id       BIGINT REFERENCES users(id),
  question_id   VARCHAR(50) NOT NULL,
  subject       VARCHAR(20),
  is_correct    BOOLEAN,
  user_answer   VARCHAR(10),
  time_spent    INT,
  points_cost   INT DEFAULT 0,
  created_at    DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 错题本表
CREATE TABLE wrong_questions (
  id            BIGINT PRIMARY KEY AUTO_INCREMENT,
  user_id       BIGINT REFERENCES users(id),
  question_id   VARCHAR(50) NOT NULL,
  wrong_count   INT DEFAULT 1,
  last_wrong_at DATETIME,
  next_review_at DATETIME,
  is_mastered   BOOLEAN DEFAULT FALSE,
  UNIQUE KEY uq_user_question (user_id, question_id)
);

-- 课程表
CREATE TABLE courses (
  id          BIGINT PRIMARY KEY AUTO_INCREMENT,
  title       VARCHAR(200) NOT NULL,
  subject     ENUM('math','logic','writing','english','combo'),
  description TEXT,
  cover_url   VARCHAR(500),
  teacher_id  BIGINT REFERENCES users(id),
  price       DECIMAL(10,2) DEFAULT 0,
  original_price DECIMAL(10,2),
  is_free     BOOLEAN DEFAULT FALSE,
  status      ENUM('draft','published','archived') DEFAULT 'draft',
  total_lessons INT DEFAULT 0,
  student_count INT DEFAULT 0,
  created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 课时表
CREATE TABLE lessons (
  id            BIGINT PRIMARY KEY AUTO_INCREMENT,
  course_id     BIGINT REFERENCES courses(id),
  title         VARCHAR(200),
  vod_file_id   VARCHAR(200),
  duration_sec  INT,
  sort_order    INT,
  is_free       BOOLEAN DEFAULT FALSE,
  preview_sec   INT DEFAULT 300,
  created_at    DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 直播课表
CREATE TABLE live_classes (
  id            BIGINT PRIMARY KEY AUTO_INCREMENT,
  title         VARCHAR(200),
  teacher_id    BIGINT REFERENCES users(id),
  subject       VARCHAR(20),
  scheduled_at  DATETIME,
  duration_min  INT DEFAULT 60,
  price         DECIMAL(10,2) DEFAULT 0,
  stream_key    VARCHAR(200),
  status        ENUM('scheduled','live','ended') DEFAULT 'scheduled',
  replay_vod_id VARCHAR(200),
  created_at    DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 订单表
CREATE TABLE orders (
  id             BIGINT PRIMARY KEY AUTO_INCREMENT,
  order_no       VARCHAR(64) UNIQUE,
  user_id        BIGINT REFERENCES users(id),
  product_type   ENUM('course','live_class','points_pack','vip','question_analysis'),
  product_id     BIGINT,
  amount         DECIMAL(10,2),
  points_granted INT DEFAULT 0,
  referrer_id    BIGINT REFERENCES users(id),       -- 推广人（学员/教师）
  referral_link_id BIGINT REFERENCES referral_links(id),
  payment_method ENUM('wechat','alipay','points'),
  status         ENUM('pending','paid','refunded','cancelled'),
  paid_at        DATETIME,
  created_at     DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 写作批改记录表
CREATE TABLE writing_submissions (
  id              BIGINT PRIMARY KEY AUTO_INCREMENT,
  user_id         BIGINT REFERENCES users(id),
  question_id     VARCHAR(50),
  essay_type      ENUM('critique','argumentative'),
  content         TEXT,
  total_score     INT,
  dimension_scores JSON,
  feedback        TEXT,
  ai_model        VARCHAR(50),
  points_cost     INT DEFAULT 50,
  created_at      DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 教师入驻资料表（审核流程）
CREATE TABLE teacher_profiles (
  id              BIGINT PRIMARY KEY AUTO_INCREMENT,
  user_id         BIGINT REFERENCES users(id) UNIQUE,
  real_name       VARCHAR(50),
  bio             TEXT,
  expertise       VARCHAR(200),
  status          ENUM('pending','approved','rejected','suspended') DEFAULT 'pending',
  commission_rate DECIMAL(4,2) DEFAULT 0.70,
  approved_by     BIGINT REFERENCES users(id),
  approved_at     DATETIME,
  created_at      DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 课程学员关系表（教师管理学员的依据）
CREATE TABLE course_enrollments (
  id              BIGINT PRIMARY KEY AUTO_INCREMENT,
  user_id         BIGINT REFERENCES users(id),
  course_id       BIGINT REFERENCES courses(id),
  teacher_id      BIGINT REFERENCES users(id),
  enrolled_at     DATETIME DEFAULT CURRENT_TIMESTAMP,
  progress_pct    DECIMAL(5,2) DEFAULT 0,
  last_active_at  DATETIME,
  UNIQUE KEY uq_user_course (user_id, course_id)
);

-- 教师营销配置表（学员分销开关与佣金规则）
CREATE TABLE teacher_marketing_configs (
  id                  BIGINT PRIMARY KEY AUTO_INCREMENT,
  teacher_id            BIGINT REFERENCES users(id) UNIQUE,
  slug                  VARCHAR(50) UNIQUE,          -- 教师主页 URL 别名
  student_referral_enabled BOOLEAN DEFAULT FALSE,    -- 是否开启学员分销
  referral_reward_type  ENUM('cash','points','coupon','mixed') DEFAULT 'points',
  referral_commission_rate DECIMAL(4,2) DEFAULT 0.10, -- 佣金比例（占实付金额，从教师份额扣）
  referral_points       INT DEFAULT 200,             -- 积分奖励数量（reward_type 含 points 时）
  max_commission_rate   DECIMAL(4,2) DEFAULT 0.20,   -- 管理员可覆盖的上限
  created_at            DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at            DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 推广链接/渠道表
CREATE TABLE referral_links (
  id              BIGINT PRIMARY KEY AUTO_INCREMENT,
  teacher_id      BIGINT REFERENCES users(id),
  course_id       BIGINT REFERENCES courses(id),     -- NULL = 全店推广
  referrer_id     BIGINT REFERENCES users(id),       -- 推广人（教师本人或学员）
  referrer_type   ENUM('teacher','student','platform') DEFAULT 'teacher',
  code            VARCHAR(32) UNIQUE,                -- 短码，如 T8X2K9
  channel         VARCHAR(50),                       -- douyin / wechat / poster 等
  click_count     INT DEFAULT 0,
  convert_count   INT DEFAULT 0,
  created_at      DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 推广佣金记录表
CREATE TABLE referral_commissions (
  id              BIGINT PRIMARY KEY AUTO_INCREMENT,
  order_id        BIGINT REFERENCES orders(id) UNIQUE,
  teacher_id      BIGINT REFERENCES users(id),
  referrer_id     BIGINT REFERENCES users(id),
  order_amount    DECIMAL(10,2),
  commission_rate DECIMAL(4,2),
  commission_amount DECIMAL(10,2),
  reward_type     ENUM('cash','points','coupon'),
  status          ENUM('pending','settled','withdrawn','revoked') DEFAULT 'pending',
  settled_at      DATETIME,
  created_at      DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 教师 AI 人设配置表（第二期启用）
CREATE TABLE teacher_ai_configs (
  id              BIGINT PRIMARY KEY AUTO_INCREMENT,
  teacher_id      BIGINT REFERENCES users(id) UNIQUE,
  display_name    VARCHAR(100),           -- AI 助教显示名（如"张老师的小助手"）
  system_prompt   TEXT,                   -- 人设与答疑风格
  answer_mode     ENUM('guide','direct') DEFAULT 'guide',
  is_enabled      BOOLEAN DEFAULT FALSE,
  created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
-- 注：points_per_chat 已移除，AI 答疑积分由平台 admin 在系统配置表统一设定

-- 教师知识库文档表
CREATE TABLE teacher_knowledge_docs (
  id              BIGINT PRIMARY KEY AUTO_INCREMENT,
  teacher_id      BIGINT REFERENCES users(id),
  title           VARCHAR(200),
  file_url        VARCHAR(500),           -- COS 存储路径
  file_type       ENUM('pdf','docx','pptx','txt','subtitle','faq'),
  status          ENUM('uploading','processing','ready','failed') DEFAULT 'uploading',
  chunk_count     INT DEFAULT 0,
  vector_collection VARCHAR(100),         -- VectorDB 中的 Collection 名
  created_at      DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

**MongoDB 集合（教师 AI 对话，存 MongoDB）：**

```json
{
  "collection": "ai_chat_sessions",
  "document": {
    "session_id": "uuid",
    "teacher_id": 123,
    "user_id": 456,
    "course_id": 789,
    "messages": [
      { "role": "user", "content": "这道题怎么做？", "created_at": "..." },
      { "role": "assistant", "content": "...", "rag_sources": ["doc_id_1"], "created_at": "..." }
    ],
    "created_at": "...",
    "updated_at": "..."
  }
}
```

> 促销功能扩展表（优惠券、限时活动、拼团、推广员等）见**附录 B**。

### 6.4 API 设计规范

**统一响应格式：**

```json
{
  "success": true,
  "data": {},
  "message": "操作成功",
  "pagination": { "page": 1, "page_size": 20, "total": 100 }
}
```

**错误响应：**

```json
{
  "success": false,
  "error": { "code": "QUOTA_EXCEEDED", "message": "今日免费额度已用完，请消耗积分继续或升级VIP" }
}
```

**关键接口列表：**

```
# 用户认证
POST /api/auth/register
POST /api/auth/login
POST /api/auth/wechat          # 预留
POST /api/auth/refresh

# 题目
GET  /api/questions            # ?subject=math&tag=函数&page=1
GET  /api/questions/:id
POST /api/questions/:id/submit # 触发积分/额度逻辑
GET  /api/questions/recommend
POST /api/questions/generate   # 管理员

# 积分
GET  /api/points/balance
GET  /api/points/transactions
POST /api/points/checkin
GET  /api/points/quota/today

# 错题本
GET  /api/wrong-book           # ?subject=math
DELETE /api/wrong-book/:id

# 课程
GET  /api/courses
GET  /api/courses/:id
GET  /api/lessons/:id/play-url # VOD 签名 URL

# 直播
GET  /api/live-classes
POST /api/live-classes/:id/join
GET  /api/live-classes/:id/token

# 写作批改
POST /api/writing/critique
POST /api/writing/argument

# 教师端（teacher 角色，数据按 teacher_id 隔离）
GET  /api/teacher/dashboard              # 教师工作台概览
GET  /api/teacher/courses                # 我的课程列表
POST /api/teacher/courses                # 创建课程
PUT  /api/teacher/courses/:id            # 编辑课程
GET  /api/teacher/students               # 我的学员列表（已购课）
GET  /api/teacher/students/:id/progress  # 某学员学情详情
GET  /api/teacher/orders                 # 我的课程订单与收入
GET  /api/teacher/questions              # 我的题库
POST /api/teacher/questions              # 上传题目
GET  /api/teacher/marketing              # 营销配置
PUT  /api/teacher/marketing              # 更新分销开关、佣金比例
POST /api/teacher/marketing/links        # 生成推广链接
GET  /api/teacher/marketing/stats        # 推广数据（第二期）
GET  /api/teacher/marketing/commissions   # 佣金支出明细

# 学生端推广
GET  /api/teachers/:slug                 # 教师公开主页
GET  /api/referral/resolve/:code         # 解析推广短码，记录点击
POST /api/referral/bind                  # 绑定推广关系（注册/首访时）
GET  /api/student/promote                # 我的可推广课程与链接
GET  /api/student/earnings               # 推广收益与提现

# 管理员端（admin 角色，全平台数据）
GET  /api/admin/dashboard                # 平台数据看板
GET  /api/admin/users                    # 全平台用户
PUT  /api/admin/users/:id/role           # 修改用户角色
GET  /api/admin/teachers                 # 教师列表
PUT  /api/admin/teachers/:id/approve     # 审核教师入驻
PUT  /api/admin/teachers/:id/suspend     # 暂停教师
GET  /api/admin/questions                # 公共题库
GET  /api/admin/orders                   # 全平台订单
GET  /api/admin/settings                 # 系统配置（含 AI 答疑积分定价）
PUT  /api/admin/settings                 # 更新系统配置
PUT  /api/admin/settings/referral        # 全局分销规则（佣金上限、提现门槛）
GET  /api/admin/analytics                # 数据分析

# 教师 AI（第二期起）
GET  /api/teacher/ai/config              # 获取教师 AI 配置
PUT  /api/teacher/ai/config              # 更新 AI 人设
POST /api/teacher/knowledge/upload       # 上传知识库文档
GET  /api/teacher/knowledge/docs         # 知识库文档列表
DELETE /api/teacher/knowledge/docs/:id   # 删除文档
POST /api/teacher/ai/chat                # 学员向教师 AI 提问（RAG）
GET  /api/teacher/ai/sessions            # 教师查看答疑记录

# 支付
POST /api/orders
GET  /api/orders/:id
POST /api/webhooks/wechat-pay
```

### 6.5 环境变量

#### 本地开发（docker-compose.dev.yml）

```env
# 应用
FLASK_ENV=development
SECRET_KEY=dev-secret-key
JWT_SECRET=dev-jwt-secret-64-chars

# MySQL（开发可用 Compose 内 mysql 服务）
DB_HOST=mysql
DB_PORT=3306
DB_NAME=guanlian_db
DB_USER=guanlian_user
DB_PASS=dev-password

# MongoDB（Compose 内 mongodb 服务）
MONGO_URI=mongodb://mongodb:27017/guanlian_questions

# Redis（开发可用 Compose 内 redis 服务）
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_PASS=

# 腾讯云（开发可用测试密钥）
TENCENT_SECRET_ID=AKIDxxx
TENCENT_SECRET_KEY=xxx
TENCENT_REGION=ap-guangzhou

# 前端
VUE_APP_API_BASE=http://localhost/api
```

#### Lighthouse 生产（.env.production，不提交 git）

```env
# 应用
FLASK_ENV=production
SECRET_KEY=<强随机密钥>
JWT_SECRET=<强随机密钥-64字符>

# MySQL（TencentDB 托管）
DB_HOST=gz-cdb-xxx.sql.tencentcdb.com
DB_PORT=3306
DB_NAME=guanlian_db
DB_USER=guanlian_user
DB_PASS=<生产密码>

# MongoDB（腾讯云托管）
MONGO_URI=mongodb://user:pass@gz-mongo-xxx.mongodb.tencentcloudapi.com:27017/guanlian_questions

# Redis（腾讯云 Redis 集群版）
REDIS_HOST=gz-redis-xxx.redis.tencentcdb.com
REDIS_PORT=6379
REDIS_PASS=<生产密码>

# 腾讯云
TENCENT_SECRET_ID=AKIDxxx
TENCENT_SECRET_KEY=xxx
TENCENT_REGION=ap-guangzhou

# COS
COS_BUCKET=guanlian-assets-1234567890
COS_REGION=ap-guangzhou

# VOD
VOD_APP_ID=your-vod-appid
VOD_SUB_APP_ID=your-subapp-id

# CSS 直播
CSS_PUSH_DOMAIN=push.your-domain.com
CSS_PLAY_DOMAIN=play.your-domain.com
CSS_KEY=your-css-key

# TRTC / IM
TRTC_APP_ID=your-trtc-appid
TRTC_SECRET_KEY=xxx
IM_SDK_APP_ID=your-im-appid
IM_ADMIN_KEY=xxx

# SMS
SMS_APP_ID=xxx
SMS_SIGN=管理联考学习
SMS_OTP_TEMPLATE_ID=xxx

# 混元大模型（全部 AI 能力）
HUNYUAN_SECRET_ID=xxx
HUNYUAN_SECRET_KEY=xxx
HUNYUAN_MODEL=hunyuan-pro

# 向量数据库（教师知识库 RAG）
VECTORDB_HOST=xxx.vectordb.tencentcloudapi.com
VECTORDB_API_KEY=xxx

# 微信（第二期）
WX_APPID=wx...
WX_SECRET=xxx
WECHAT_PAY_MCH_ID=xxx
WECHAT_PAY_NOTIFY_URL=https://api.yourdomain.com/api/webhooks/wechat-pay

# 前端
VUE_APP_API_BASE=https://yourdomain.com/api
VUE_APP_TRTC_APP_ID=your-trtc-appid
```

---

## 7. 前端与设计

### 7.1 三端技术实现方案（推荐）

**MVP 推荐：单 Vue 3 项目 + 三套路由布局**（而非三个独立项目）

```
frontend/src/
├── layouts/
│   ├── StudentLayout.vue      # 学生端壳（底部导航、学习氛围）
│   ├── TeacherLayout.vue      # 教师端壳（侧边栏、工作台风格）
│   └── AdminLayout.vue        # 管理端壳（侧边栏、数据密集）
├── views/
│   ├── student/               # 学生端页面
│   ├── teacher/               # 教师端页面
│   └── admin/                 # 管理员端页面
├── router/
│   ├── index.js               # 主路由 + 全局守卫
│   ├── student.routes.js
│   ├── teacher.routes.js
│   └── admin.routes.js
└── stores/
    └── auth.js                # 角色、Token、权限
```

**理由：**

- 共享组件（QuestionCard、VideoPlayer、积分模块）避免重复开发
- 统一设计系统，三端风格一致但有差异化布局
- 一套构建部署，nginx 按路径或子域名分发
- 后期若教师端/管理端体量极大，可拆为独立项目

**访问方式：子域名（已确认）**

| 学生端 | 教师端 | 管理端 |
|---|---|---|
| `www.domain.com` | `teacher.domain.com` | `admin.domain.com` |

三个子域名 nginx 同指向一个 frontend 构建产物；管理端建议 IP 白名单或二次验证。

**登录与路由守卫：**

```
用户登录 → JWT 含 role 字段
  ↓
role=student  → 只能访问 / 下学生路由，访问 /teacher 或 /admin 自动跳转
role=teacher  → 只能访问 /teacher/*，且 API 层强制 teacher_id = 当前用户
role=admin    → 可访问 /admin/*，可见全平台数据
```

**后端权限中间件（必须实现）：**

```python
# 伪代码 — 每个教师端/管理端 API 必须过此检查
def teacher_only(fn):
    # 1. 验证 JWT role == 'teacher'
    # 2. 验证 teacher_profiles.status == 'approved'
    # 3. 查询参数强制注入 current_teacher_id，忽略客户端传的 teacher_id

def admin_only(fn):
    # 验证 JWT role == 'admin'
```

### 7.2 学生端路由

```
/                     → 首页（产品介绍 + CTA）
/login                → 登录/注册
/dashboard            → 学习中心
/practice/*           → 刷题（数学/逻辑/写作/英语/综合）
/wrong-book           → 错题本
/mock-exam/*          → 真题模拟
/courses/*            → 课程中心 + 播放
/teachers/:slug       → 教师公开主页（可购课、看简介）
/writing-lab/*        → 写作训练室
/profile/*            → 个人中心、积分、订单、VIP
/profile/promote      → 推广中心（我的推广链接与收益，第二期完整）
/profile/earnings     → 推广收益明细与提现（第二期）
/shop                 → 商城
```

### 7.3 教师端路由

```
/teacher                      → 教师工作台（数据概览）
/teacher/login                → 教师登录（可与学生共用登录页，按角色跳转）
/teacher/courses              → 我的课程列表
/teacher/courses/:id          → 课程编辑（课时、定价、封面）
/teacher/courses/:id/lessons  → 课时管理
/teacher/students             → 我的学员（已购课学生列表）
/teacher/students/:id         → 学员学情详情（进度、错题、活跃度）
/teacher/questions            → 我的题库
/teacher/orders               → 收入与订单
/teacher/marketing            → 营销中心（推广链接、分销配置、数据看板）
/teacher/marketing/links      → 推广链接管理
/teacher/marketing/poster     → 海报生成（第二期）
/teacher/profile              → 教师资料、入驻信息
/teacher/ai                   → AI 助教配置（第二期）
/teacher/ai/knowledge         → 知识库管理（第二期）
/teacher/ai/sessions          → 答疑记录（第二期）
```

### 7.4 管理员端路由

```
/admin                        → 平台数据看板
/admin/users                  → 全平台用户管理
/admin/teachers               → 教师管理（审核/暂停/分成比例）
/admin/teachers/:id           → 教师详情
/admin/questions              → 公共题库管理
/admin/courses                → 全平台课程（可下架违规课程）
/admin/orders                 → 全平台订单
/admin/promotions/*           → 促销配置（优惠券、限时折扣等）
/admin/settings               → 系统配置（AI 积分定价、免费额度等）
/admin/analytics              → 数据分析报表
/admin/content                → 首页轮播、弹窗广告等内容运营
```

### 7.5 三端 UI 差异化建议

| 端口 | 布局 | 色调 | 体验重点 |
|---|---|---|---|
| 学生端 | 移动优先，底部 Tab 导航 | 品牌蓝 #4F6EF7，科目彩色标签 | 学习沉浸感，减少干扰 |
| 教师端 | 左侧边栏 + 内容区，偏桌面 | 品牌蓝 + 中性灰，偏专业 | 效率优先，数据卡片清晰 |
| 管理端 | 左侧边栏 + 宽表格/图表 | 深蓝灰 #1A1A2E 侧边栏 | 信息密度高，操作可追溯 |

### 7.6 设计系统（UI 规范，三端共用）

**配色：**

```css
--color-primary:    #4F6EF7;
--color-primary-hover: #3B54D4;
--color-primary-light: #EEF1FE;
--color-bg:         #FFFFFF;
--color-surface:    #F7F8FA;
--color-border:     #E8EAED;
--color-text-main:  #1A1A2E;
--color-text-muted: #6B7280;
--color-success:    #10B981;
--color-warning:    #F59E0B;
--color-error:      #EF4444;
--color-math:       #6C63FF;
--color-logic:      #F97316;
--color-writing:    #EC4899;
--color-english:    #14B8A6;
```

**字体：**

```css
font-family: 'Inter', 'PingFang SC', 'Microsoft YaHei', sans-serif;
line-height: 1.7;
```

**间距（8px 网格）：** xs:4px sm:8px md:16px lg:24px xl:32px 2xl:48px 3xl:64px

**Wix 风格设计原则：**

1. 大量留白，节间距最少 64px
2. 一个页面只有一个主要强调色（#4F6EF7）
3. Hero 区大标题粗体（48–64px, font-weight: 700）
4. 卡片极简，薄边框+轻阴影，无渐变
5. 所有可交互元素 `transition: all 0.2s`
6. 移动优先响应式（375px 起）
7. 布局不规则有变化，体现设计感

---

## 8. 工程规范与目录

### 8.1 项目目录结构

```
guanlian-learning/
├── AGENTS.md                   # 本文件（项目全局说明）
├── .env.example                # 环境变量模板（不含真实密钥）
├── docker/                     # Docker 部署配置
│   ├── docker-compose.yml
│   ├── docker-compose.prod.yml
│   ├── docker-compose.dev.yml
│   ├── nginx/nginx.conf
│   ├── flask/Dockerfile
│   ├── node/Dockerfile
│   ├── fastapi/Dockerfile
│   └── frontend/Dockerfile
├── backend/                    # Flask 后端
│   ├── app.py
│   ├── config.py
│   ├── models/
│   ├── routes/
│   ├── services/
│   └── requirements.txt
├── frontend/                   # Vue.js 前端
│   ├── src/
│   │   ├── views/
│   │   ├── components/
│   │   ├── router/
│   │   ├── store/
│   │   ├── api/
│   │   └── utils/
│   ├── package.json
│   └── vite.config.js
└── ai-service/                 # FastAPI AI 服务
    ├── main.py
    ├── services/
    │   ├── hunyuan_service.py  # 混元 API 调用
    │   ├── rag_service.py      # 知识库 RAG 检索
    │   └── embedding_service.py
    └── requirements.txt
```

### 8.2 后端服务职责

| 目录/服务 | 技术 | 职责 |
|---|---|---|
| `backend/` | Flask | 主 API：用户、题目、积分、课程、订单、支付、教师管理 |
| `realtime/` 或 `backend/ws/` | Node.js Express | WebSocket、直播信令 |
| `ai-service/` | FastAPI | 混元出题/批改/答疑、知识库 RAG（异步） |

---

## 9. AI Agent 工作指令

每次接到编码任务时，Cursor Agent 必须遵守以下规则：

1. **技术选型** — 严格按照第二章技术栈，不得引入未列出的框架
2. **云服务** — 所有云功能必须使用腾讯云，不用 AWS/阿里云/境外 API
3. **AI 接口** — **全部 AI 能力统一使用腾讯混元大模型**，禁止使用 Anthropic Claude 等境外 API
4. **数据库** — 生产环境全部腾讯云托管（MySQL HA + Redis 集群 + MongoDB + VectorDB），禁止生产数据库进 Docker
5. **多租户隔离** — 教师数据按 `teacher_id` 隔离；教师只能访问自己课程的学员；AI 知识库检索不得跨教师
6. **三端权限** — 学生/教师/管理员三端严格按 `role` 路由守卫 + 后端中间件双重校验
7. **积分逻辑** — 任何涉及答题的接口都必须触发积分/额度判断（见第五章）
8. **设计风格** — 三端共用设计系统，布局按 §7.5 差异化
9. **响应格式** — 所有 API 统一使用第六章 JSON 格式
10. **错题推荐** — 做题后必须更新错题本，并基于标签体系计算推荐
11. **安全** — 所有视频 URL 必须用腾讯 VOD 签名，支付回调必须验签
12. **注释** — 关键逻辑用中文注释，方便团队阅读
13. **部署同步** — 部署相关改动必须同步更新 `docker/` 配置与本文件第三章
14. **密钥管理** — 云服务调用一律走腾讯云 SDK，密钥从环境变量读取，禁止硬编码
15. **教师 AI** — RAG 答疑（第二期）必须先检索该教师 VectorDB Collection，再调用混元生成
16. **AI 定价** — 所有 AI 消耗积分由平台管理员统一配置，教师不可自行定价
17. **分销佣金** — 学员推广佣金从教师收入份额扣除；须校验推广绑定与防作弊规则（见 §1.6.3）
18. **订单归因** — 任何购课订单必须记录 `referrer_id` 与 `referral_link_id`（若有），作为分成与佣金结算依据

---

## 附录 A：促销功能详细规格

### 【第一类】价格促销工具（6 种）

**① 划线价** — 付费商品页显示划掉原价+现售价；字段 `courses.original_price`

**② 普通优惠券** — 满减券/折扣券/指定商品券；新人注册自动发放、活动期间发放、后台群发

**③ 有价优惠券** — 优惠券当商品出售，大促预热锁客（如 ¥9.9 购 ¥50 券）

**④ 限时折扣** — 指定时间段折扣价，前端倒计时，结束自动恢复原价

**⑤ 秒杀** — 限时限量极低价，支持预热和预约提醒

**⑥ 弹窗广告** — 首页/课程页促销浮层，可配置展示频率和时间段

### 【第二类】社交裂变工具（7 种）

**⑦ 邀请码/卡** — 专属邀请码，双向各得 50 积分；邀请卡带参数图片

**⑧ 兑换码** — 后台批量生成，兑换课程/VIP/积分

**⑨ 请好友免费看** — 已购课用户分享试看链接，好友注册后奖励积分

**⑩ 涨粉神器** — 分享公众号/注册链接，新用户关注后分享者得奖励

**⑪ 裂变海报** — 带专属二维码海报，他人注册/购课后得佣金 10%–20%

**⑫ 普通拼团** — 48 小时内凑够人数享 7 折，未成团全额退款

**⑬ 邀新拼团** — 仅新用户可参团，老用户作团长拉新

**⑭ 阶梯拼团** — 人越多越便宜（3 人 7 折 → 5 人 6 折 → 10 人 5 折）

### 【第三类】留存与激励工具（7 种）

**⑮ 打卡系统** — 日历打卡、闯关打卡、付费打卡（保证金）、作业打卡

**⑯ 打卡返学费** — VIP 年卡连续打卡 100 天返 ¥50 现金券

**⑰ 支付有礼** — 支付后自动赠送关联课程折扣券

**⑱ 成长任务+勋章** — 里程碑任务解锁勋章（数感觉醒、坚持不懈等）

**⑲ 学习排行榜** — 周/月/总榜，刷题量、时长、正确率、打卡天数

**⑳ 结课证书** — 完成课时+测验后生成电子证书，可分享朋友圈

**㉑ 送好友** — 购课后可将课程赠送给好友

### 【第四类】分销推广工具（3 种）

**㉒ 推广员计划** — 一级佣金 15%–30%，二级 5%，满 ¥50 可提现

**㉓ 批量兑换码** — B 端渠道合作，可配置兑换内容和有效期

**㉔ 内容分销市场** — 课程开放给外部渠道分销，平台设定分成比例

### 【第五类】智能自动化运营（6 种触发场景）

| 场景 | 触发条件 | 自动动作 | 渠道 |
|---|---|---|---|
| 兴趣转换 | 浏览商品 >3 次未购且超 1 天 | 限时优惠+9 折券 | 站内信+短信 |
| 未付款唤回 | 订单未支付超 24 小时 | 订单即将过期提醒 | 站内信+短信 |
| 新客复购 | 首购后 30 天未二次购买 | 搭配课程推荐+折扣券 | 站内信+微信 |
| 高活维系 | 近 7 天每天登录 | 学习报告+积分奖励 | 站内信 |
| 流失召回 | 有消费但 30 天未登录 | 距考研 XX 天+积分补贴 | 短信+微信 |
| 收藏未购 | 收藏超 3 天未购 | 即将恢复原价提醒 | 站内信 |

### 【第六类】店铺展示与氛围工具（4 种）

**㉕ 销售弹幕** — 课程页滚动显示最近购买记录

**㉖ 划线价展示** — 列表卡片和详情页双处展示，配合倒计时

**㉗ 首页轮播+活动微页面** — 可视化拖拽配置 Landing Page

**㉘ 商品分组与推荐位** — 冲刺必备、高分套餐等分组置顶

---

## 附录 B：促销功能数据库表

```sql
CREATE TABLE coupon_templates (
  id            BIGINT PRIMARY KEY AUTO_INCREMENT,
  name          VARCHAR(100),
  type          ENUM('fixed','percent','product_specific'),
  discount_value DECIMAL(10,2),
  min_amount    DECIMAL(10,2) DEFAULT 0,
  applicable_to ENUM('all','specific_course','vip'),
  course_ids    JSON,
  total_count   INT,
  per_user_limit INT DEFAULT 1,
  valid_days    INT,
  start_at      DATETIME,
  end_at        DATETIME,
  is_paid       BOOLEAN DEFAULT FALSE,
  paid_price    DECIMAL(10,2),
  created_at    DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE user_coupons (
  id            BIGINT PRIMARY KEY AUTO_INCREMENT,
  user_id       BIGINT REFERENCES users(id),
  template_id   BIGINT REFERENCES coupon_templates(id),
  code          VARCHAR(32) UNIQUE,
  status        ENUM('unused','used','expired') DEFAULT 'unused',
  used_order_id BIGINT,
  expires_at    DATETIME,
  received_at   DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE flash_sales (
  id            BIGINT PRIMARY KEY AUTO_INCREMENT,
  name          VARCHAR(100),
  type          ENUM('discount','seckill'),
  start_at      DATETIME,
  end_at        DATETIME,
  status        ENUM('preview','active','ended') DEFAULT 'preview',
  created_at    DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE flash_sale_items (
  id            BIGINT PRIMARY KEY AUTO_INCREMENT,
  sale_id       BIGINT REFERENCES flash_sales(id),
  product_type  ENUM('course','vip','points_pack'),
  product_id    BIGINT,
  original_price DECIMAL(10,2),
  sale_price    DECIMAL(10,2),
  stock_limit   INT,
  sold_count    INT DEFAULT 0,
  UNIQUE KEY uq_sale_product (sale_id, product_type, product_id)
);

CREATE TABLE group_buy_activities (
  id            BIGINT PRIMARY KEY AUTO_INCREMENT,
  product_type  ENUM('course','vip'),
  product_id    BIGINT,
  type          ENUM('normal','invite_new','ladder'),
  time_limit_hours INT DEFAULT 48,
  start_at      DATETIME,
  end_at        DATETIME,
  ladder_prices JSON,
  group_size    INT,
  group_price   DECIMAL(10,2),
  leader_price  DECIMAL(10,2),
  status        ENUM('active','ended') DEFAULT 'active'
);

CREATE TABLE group_buy_orders (
  id            BIGINT PRIMARY KEY AUTO_INCREMENT,
  activity_id   BIGINT REFERENCES group_buy_activities(id),
  leader_id     BIGINT REFERENCES users(id),
  status        ENUM('open','success','failed') DEFAULT 'open',
  current_size  INT DEFAULT 1,
  expires_at    DATETIME,
  created_at    DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE group_buy_members (
  id            BIGINT PRIMARY KEY AUTO_INCREMENT,
  group_id      BIGINT REFERENCES group_buy_orders(id),
  user_id       BIGINT REFERENCES users(id),
  is_leader     BOOLEAN DEFAULT FALSE,
  is_new_user   BOOLEAN DEFAULT FALSE,
  order_id      BIGINT REFERENCES orders(id),
  joined_at     DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE promoters (
  id            BIGINT PRIMARY KEY AUTO_INCREMENT,
  user_id       BIGINT REFERENCES users(id) UNIQUE,
  status        ENUM('pending','approved','rejected','banned') DEFAULT 'pending',
  level         ENUM('basic','senior') DEFAULT 'basic',
  commission_rate1 DECIMAL(4,2) DEFAULT 0.15,
  commission_rate2 DECIMAL(4,2) DEFAULT 0.05,
  parent_promoter_id BIGINT,
  total_earned  DECIMAL(10,2) DEFAULT 0,
  withdrawable  DECIMAL(10,2) DEFAULT 0,
  applied_at    DATETIME DEFAULT CURRENT_TIMESTAMP,
  approved_at   DATETIME
);

CREATE TABLE promoter_commissions (
  id            BIGINT PRIMARY KEY AUTO_INCREMENT,
  promoter_id   BIGINT REFERENCES promoters(id),
  order_id      BIGINT REFERENCES orders(id),
  level         TINYINT,
  amount        DECIMAL(10,2),
  status        ENUM('pending','settled','withdrawn') DEFAULT 'pending',
  created_at    DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE redeem_codes (
  id            BIGINT PRIMARY KEY AUTO_INCREMENT,
  batch_name    VARCHAR(100),
  code          VARCHAR(32) UNIQUE,
  reward_type   ENUM('course','vip_days','points'),
  reward_id     BIGINT,
  reward_value  INT,
  is_used       BOOLEAN DEFAULT FALSE,
  used_by       BIGINT REFERENCES users(id),
  used_at       DATETIME,
  expires_at    DATETIME,
  created_at    DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE auto_marketing_logs (
  id            BIGINT PRIMARY KEY AUTO_INCREMENT,
  user_id       BIGINT REFERENCES users(id),
  scene         VARCHAR(50),
  triggered_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY uq_user_scene_day (user_id, scene, DATE(triggered_at))
);

CREATE TABLE checkin_activities (
  id            BIGINT PRIMARY KEY AUTO_INCREMENT,
  name          VARCHAR(100),
  type          ENUM('daily','challenge','paid'),
  target_days   INT,
  reward_type   ENUM('points','coupon','cashback'),
  reward_value  DECIMAL(10,2),
  deposit_amount DECIMAL(10,2) DEFAULT 0,
  start_at      DATETIME,
  end_at        DATETIME
);
```

---

## 10. 后续想法记录区

> **使用说明**：对话中产生的新想法先记录在此，经确认后迁入正文对应章节，并更新「变更记录」版本号。本节只放**尚未确认**或**待细化**的内容。

### 待讨论

（暂无 — 有新想法时在此追加）

### 已迁入正文（备忘索引）

| 想法 | 确认版本 | 迁入位置 |
|---|---|---|
| 腾讯云混元替代 Claude | v1.2 | §2.1 |
| 商用托管数据库 | v1.2 | §2.4 |
| 教师 AI 知识库 | v1.2 | §2.6 |
| 三端架构 | v1.3 | §1.5、§7 |
| 教师自主营销 + 学员分销 | v1.4 | §1.6 |
| 子域名 / 分成 70/30 / 开放审核 | v1.4 | §0.2、§1.5 |
| 佣金默认 10%/上限 20%、仅一级分销 | v1.5 | §0.2、§1.6.3、§1.6.7 |

---

## 变更记录

| 版本 | 日期 | 变更摘要 |
|---|---|---|
| v1.0 | 2026-06-22 | 初版（`管理类联考教学平台.md` / `cursor.md`） |
| v1.1 | 2026-06-23 | 合并两份文档为 `AGENTS.md`；新增 Lighthouse + Docker Compose 部署架构 |
| v1.2 | 2026-06-23 | AI 全面切换腾讯混元；商用数据库架构；多教师 AI 知识库/RAG |
| v1.3 | 2026-06-23 | 确认三端架构；AI 答疑平台统一定价；教师知识库第二期 |
| v1.4 | 2026-06-23 | 确认子域名访问、教师分成 70/30、开放申请+审核；新增 §1.6 教师自主营销与学员分销体系 |
| v1.5 | 2026-06-23 | 固化营销默认参数（佣金 10%/上限 20%）；确认仅一级分销；新增 §0.1 目录、§0.2 决策总览、§10 后续想法记录区、§1.6.7 设计要点 |

---

## 待确认清单

- [ ] Lighthouse 具体配置（CPU/内存/带宽，建议 2核4G 起）
- [ ] TencentDB MySQL 起步规格（建议高可用版 4核8G）
- [ ] 腾讯云 VectorDB 选型与 Embedding 模型（第二期前确认）
- [ ] 是否已有域名、ICP 备案状态
- [ ] MVP 是否包含直播课（CSS/TRTC 复杂度高，可降级到二期）
- [ ] 微信支付/支付宝商户号是否已申请
- [ ] 平台品牌名称与 Logo 定稿
- [ ] 首期题库内容来源（自建 / 合作机构）
- [x] 三端访问方式 → **子域名**
- [x] 教师分成比例 → **教师 70% / 平台 30%**
- [x] 教师注册方式 → **开放申请 + 管理员审核**
- [x] AI 答疑定价策略 → **平台统一定价（消耗积分）**
- [x] 教师知识库上线时间 → **第二期**
- [x] 三端架构 → **学生端 + 教师端 + 管理员端**
- [x] 教师自主营销 → **教师配置推广工具 + 学员分销（佣金从教师份额扣）**
- [x] 学员分销佣金 → **默认 10%，上限 20%，仅一级分销**
