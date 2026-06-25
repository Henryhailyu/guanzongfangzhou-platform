# 管理类联考在线学习系统 — 项目全局说明文档
> 供 Claude Code 阅读。每次开始编码任务前必须先读取本文件。

---

## 一、项目概述

### 产品定位
针对中国考研**管理类联考**（199综合能力 + 英语二）的在线学习系统。目标用户为备考 MBA、MPA、MPAcc、MEM、MAud 等管理类专业硕士的在职人员和应届生。

### 考试结构（必须了解，影响题库和模块设计）

| 科目 | 题型 | 分值 |
|---|---|---|
| **数学基础** | 问题求解×15（五选一）+ 条件充分性判断×10（五选一） | 75分 |
| **逻辑推理** | 单选×30（形式推理/论证推理/综合推理） | 60分 |
| **写作** | 论证有效性分析×1（30分）+ 论说文×1（35分） | 65分 |
| **英语二** | 完形填空+阅读理解+翻译+小作文+大作文 | 100分 |
| **总计** | | 300分 |

### 考生核心痛点（产品设计的出发点）
1. **做题速度慢** — 题量大，时间紧（管综3小时）
2. **条件充分性判断**难，市面专项训练少
3. **逻辑阅读量大**（2025年约8500字），近年持续增加
4. **写作思辨能力弱**，很多人不会找论证漏洞
5. **在职人员时间碎片**，需要高效利用通勤/午休时间
6. **英语基础差**，词汇量不足

---

## 二、技术栈（必须严格遵守，不得随意替换）

### 前端
- **Vue.js 3**（Composition API）+ Element Plus + Axios
- **uni-app**（第二期，编译为微信小程序 + H5）
- React（特定复杂交互场景可用）

### 后端
- **Flask**（Python）— 主要 API 服务
- **Node.js / Express** — 实时功能（WebSocket、直播信令）
- **FastAPI** — AI 相关接口（异步处理）

### 数据库
- **MySQL**（腾讯云 TencentDB）— 主数据库
- **Redis** — 缓存、Session、积分实时计算、刷题状态
- **MongoDB** — 题库内容（支持复杂标签结构和嵌套查询）

### 云平台：**腾讯云（cloud.tencent.com）— 唯一云平台**

| 腾讯云产品 | 用途 |
|---|---|
| **CVM** | 服务器（Ubuntu 22.04 LTS） |
| **TencentDB MySQL** | 用户/订单/积分数据 |
| **COS**（对象存储） | 图片、PDF、题目附件 |
| **VOD**（云点播） | 录播课视频（防盗链签名URL） |
| **CSS**（云直播）+ **TRTC** | 直播课（教师端推流，学生端播放） |
| **IM**（即时通信） | 直播课聊天室、师生消息 |
| **SMS**（短信服务） | OTP验证码 |
| **混元大模型**（Hunyuan） | 写作批改、AI解题、题目生成 |
| **ASR**（语音识别） | 直播课自动字幕 |
| **CDN** | 全国加速 |
| **SSL证书** | HTTPS |

### AI 集成
- **Anthropic Claude API**（嵌入平台）— 题目智能解析、AI 练习题生成
  - 模型：`claude-sonnet-4-6`
  - 用于：教师上传资料后 AI 自动提取知识点、生成练习题
- **腾讯混元大模型**（Hunyuan）— 写作批改、论证分析评分
  - 用于：论证有效性分析批改、论说文评分反馈

---

## 三、开发路线图

### MVP 第一期 — Web 网页版（当前阶段）
> 优先完成，验证核心功能

**必须实现的功能：**
1. 用户注册/登录（邮箱 + 手机号，预留微信登录接口）
2. 题库浏览（按科目 / 知识点标签）
3. 刷题练习（随机练习 / 专项练习）
4. 答题与即时判分（客观题自动判，写作题 AI 批改）
5. 错题本（收录错题 + 关联同类题目）
6. 积分系统（见第四章详细说明）
7. 学习进度看板（每科完成率、连续打卡天数）
8. 基础支付（微信支付/支付宝 购买积分/课程）
9. 视频课程（VOD 点播，免费预览 + 付费完整版）
10. 管理后台（题库录入、用户管理、订单管理）

### 第二期 — 微信小程序
- uni-app 复用第一期核心逻辑
- 微信登录 + 微信支付
- 轻量刷题（碎片时间场景）

### 第三期 — 原生 APP
- iOS（Xcode / Swift）
- Android（Android Studio / Kotlin）
- 鸿蒙（HarmonyOS）

---

## 四、积分与商业模式系统（核心设计，必须严格实现）

### 4.1 积分规则

#### 获得积分途径

| 行为 | 获得积分 |
|---|---|
| 每日首次登录签到 | +10分 |
| 完成一道题目（答对） | +3分 |
| 完成一道题目（答错） | +1分 |
| 完成一套模拟题 | +50分 |
| 连续登录7天 | 额外+50分 |
| 连续登录30天 | 额外+200分 |
| 分享平台给好友（好友注册） | +30分 |
| 参与社区讨论/答疑 | +5分/次 |
| 购买课程/积分包 | 按金额比例获赠积分 |

#### 消耗积分途径（免费额度机制）

| 消耗场景 | 消耗积分 |
|---|---|
| **免费额度用尽后继续刷题** | 每道题-5分（客观题） |
| **查看 AI 视频解析** | -10分/题 |
| **AI 写作批改一篇** | -50分 |
| **换购付费课程（部分抵扣）** | 按课程定价折算 |
| **解锁真题模拟卷（单套）** | -100分 |

#### 免费每日额度限制
```
免费用户：每天免费做20道题
- 答对：不扣积分
- 答错一道：扣除当日5分"额度"
- 当日错题达到5道（累计扣25分额度）→ 当日免费额度用尽
- 用尽后选择：① 消耗积分继续 ② 付费购买当日无限次 ③ 等明天刷新

付费/VIP用户：无限刷题，不受每日限制
```

**重要逻辑说明：**
> 这个机制的核心目的：
> 1. 答题准确率高的用户（学习效果好）可以一直免费用
> 2. 答题准确率低的用户会更快消耗额度，产生付费动力
> 3. 长期坚持学习的用户积累积分可兑换服务，增加留存

#### 积分等级体系

| 等级 | 积分区间 | 特权 |
|---|---|---|
| 入门生 | 0–500 | 基础刷题功能 |
| 备考生 | 500–2000 | 解锁部分历年真题 |
| 冲刺生 | 2000–5000 | 每月1次免费AI写作批改 |
| 上岸生 | 5000+ | 专属学习报告、优先客服 |

### 4.2 商业模式

#### 收费项目清单

| 服务 | 定价参考 | 说明 |
|---|---|---|
| **积分包** | ¥6/100积分，¥30/600积分，¥88/2000积分 | 直接购买积分 |
| **VIP月卡** | ¥39/月 | 无限刷题+文字解析 |
| **VIP年卡** | ¥299/年 | 无限刷题+文字解析+每月3次AI批改 |
| **单科视频课** | ¥99–¥299/科 | 数学/逻辑/写作/英语二 |
| **全科套餐** | ¥699–¥999 | 四科视频课打包 |
| **视频解析（按题）** | 消耗10积分 或 ¥1/题 | AI+教师视频讲解 |
| **AI写作批改（单次）** | 消耗50积分 或 ¥5/次 | 混元大模型批改 |
| **真题模拟卷（单套）** | 消耗100积分 或 ¥9.9/套 | 历年真题全套 |
| **1对1辅导（在线）** | ¥150–¥300/小时 | 预约真人教师 |
| **直播课（单次）** | ¥19–¥49/节 | 教师直播讲课 |

#### 4.3 完整促销模式体系（全面对标小鹅通，全部实现）

> 本平台将实现小鹅通营销中心的全部促销功能，分六大类共28种玩法，按MVP→第二期→第三期分批上线。所有促销功能需在管理后台提供可视化配置界面，运营人员无需开发即可自助配置。

---

##### 【第一类】价格促销工具（6种）

**① 划线价（原价显示）**
- 所有付费商品页均显示"划掉的原价 + 现售价"
- 管理后台可单独设置每个商品的原价（划线价）和现价
- 前端展示：~~¥399~~ **¥199**，红色强调现价
- 数据库字段：`courses.original_price`（已在建表中包含）

**② 普通优惠券**
- 三种类型：满减券（满X减Y）、折扣券（X折）、指定商品券
- 发放方式：新人注册自动发放 / 活动期间手动发放 / 后台指定用户群发
- 使用限制：有效期、每人限领次数、是否可叠加
- 适用场景示例：新人券（-¥20，7天有效）、全科满减券（满500减100）

**③ 有价优惠券（预售券）**
- 把优惠券当商品出售，用于大促预热锁客
- 示例：¥9.9购买价值¥50的课程优惠券，在指定大促日使用
- 使用场景：考研报名季前2周上线，提前锁定转化意向用户

**④ 限时折扣**
- 指定一个或多个商品，在设定时间段内以折扣价售卖
- 前端展示倒计时（时:分:秒），营造紧迫感
- 支持批量设置多个商品同时打折
- 折扣结束后自动恢复原价，无需人工操作
- 典型节点：每年12月考研季、618、双11、元旦

**⑤ 秒杀**
- 限时（如2小时）限量（如前100名）极低价出售
- 支持"活动预热"：提前发布预告，营造期待感
- 支持"预约提醒"：用户点击预约，活动开始时自动推送通知
- 活动结束或售完自动关闭，剩余库存自动恢复正价
- 典型玩法：¥1秒杀单节数学精讲课，引流新用户

**⑥ 弹窗广告（促销弹窗）**
- 用户进入首页/课程页时，弹出促销活动浮层
- 管理后台可设置：弹窗图片、跳转链接、展示频率（每天最多1次）、展示时间段
- 用于大促期间强化曝光，提升活动转化率

---

##### 【第二类】社交裂变工具（7种）

**⑦ 邀请码 / 邀请卡**
- 每个用户拥有专属邀请码
- 新用户注册时填写邀请码：邀请人+被邀请人各得50积分
- 邀请卡：生成带参数的图片邀请卡，可转发至微信群/朋友圈
- 后台可查看每个用户的邀请人数和邀请带来的订单数

**⑧ 兑换码（批量发放）**
- 管理后台批量生成一次性兑换码，可兑换指定课程/VIP/积分
- 使用场景：与考研机构/院校合作，线下发放体验码；节假日活动奖品
- 支持设置：总数量、兑换内容、有效期、每人限用次数

**⑨ 请好友免费看**
- 已购课用户可生成"好友免费试看"链接，分享给尚未注册的好友
- 好友点击链接可免费试看指定课程的前N节（如前3节）
- 好友注册后，原用户获得积分奖励
- 每个用户每天可发出N次（管理后台配置）

**⑩ 涨粉神器（关注送课）**
- 用户分享公众号二维码或注册链接，新用户扫码关注/注册后，分享者获得奖励（积分或免费课）
- 核心逻辑：老用户邀请新粉丝→裂变式拉新
- 适用于平台冷启动阶段，快速积累种子用户

**⑪ 裂变海报**
- 用户一键生成带个人专属二维码的精美海报（考研主题设计）
- 他人扫码注册/购课后，海报发布者获得佣金（按成交金额10%-20%）
- 海报样式可在后台自定义（背景图、文案、头像位置）
- 购课前和购课后均可生成

**⑫ 普通拼团**
- 用户发起拼团，在设定时限内（如48小时）凑够人数享受优惠价
- 成团价通常为原价7折
- 未成团则全额退款（24小时内到账）
- 支持查看"我的拼团进度"，可一键催促好友参团

**⑬ 邀新拼团**
- 只有新用户（从未在平台下过单）才能作为参团者
- 专门用于拉新场景，老用户作为团长，拉来的必须是新用户
- 成团后老用户享受团长优惠价，新用户享受参团优惠价

**⑭ 阶梯拼团**
- 设置多档人数对应多档价格，人越多越便宜
- 示例：3人成团7折 → 5人成团6折 → 10人成团5折
- 极大刺激用户主动拉人，形成自发传播

---

##### 【第三类】留存与激励工具（7种）

**⑮ 打卡系统（多模式）**

| 打卡类型 | 规则 |
|---|---|
| 日历打卡 | 每日完成指定任务打卡，日历上显示打卡记录 |
| 闯关打卡 | 完成当日任务才能解锁下一关，游戏化体验 |
| 付费打卡 | 用户缴纳保证金，完成打卡可全额取回，否则扣除 |
| 作业打卡 | 提交作业截图/文字作业，老师审核后标记完成 |

**⑯ 打卡返学费（打卡奖学金）**
- 购买VIP年卡/指定课程后，连续完成N天打卡，返还部分学费
- 示例：购买VIP年卡¥299，连续打卡100天，返¥50现金券（可抵扣下次续费）
- 未完成打卡则不返还，激励长期使用

**⑰ 支付有礼（购后赠券）**
- 用户完成支付后，系统自动弹出赠送优惠权益
- 示例：购买数学单科课后，自动赠送"逻辑课8折券"（3天有效）
- 配置：管理后台设定触发商品→赠送内容→有效期
- 目的：提升连带购买率和复购率

**⑱ 成长任务 + 勋章体系**
- 预设学习里程碑任务，完成后解锁专属勋章
- 示例任务：
  - 完成100道数学题 → 解锁「数感觉醒」勋章
  - 连续打卡30天 → 解锁「坚持不懈」勋章
  - 完成首次写作AI批改 → 解锁「思辨新手」勋章
  - 模拟考综合成绩超过150分 → 解锁「冲刺达人」勋章
- 勋章可在个人主页展示，满足用户的荣誉感和分享欲

**⑲ 学习排行榜**
- 周榜 / 月榜 / 总榜，多维度排名：
  - 刷题数量榜
  - 学习时长榜
  - 正确率榜（仅限做题数≥50道的用户）
  - 连续打卡天数榜
- 前3名获得积分奖励，榜单在首页和社区显示
- 增加竞争感，激励用户持续学习

**⑳ 结课证书**
- 完成全部课时+通过结课测验后，自动生成精美电子证书
- 证书包含：姓名、完成课程名称、完成日期、平台Logo
- 支持一键分享至微信朋友圈（带平台水印，免费品牌曝光）
- 全科完成后颁发"管理类联考全科通关证书"

**㉑ 送好友（赠课功能）**
- 用户购买课程后，可将课程作为礼物赠送给指定好友
- 好友收到赠课通知，点击领取后自动解锁课程
- 节日营销场景：生日、考研冲刺、元旦等节点赠课

---

##### 【第四类】分销推广工具（3种）

**㉒ 推广员计划（内容分销员）**
- 用户/机构申请成为推广员，审核通过后获得专属推广链接
- 推广规则：
  - 一级佣金：他人通过推广员链接购课，推广员得成交额15%-30%
  - 二级佣金（可选）：推广员发展的下级推广员产生销售，上级得5%
- 佣金实时到账至平台钱包，满¥50可提现至微信
- 管理后台查看：推广员列表、各推广员带来的订单数和佣金总额

**㉓ 批量兑换码（渠道合作码）**
- 面向B端合作渠道（考研机构、院校、企业）批量生成兑换码
- 兑换内容可配置：指定课程、N天VIP体验、积分包
- 支持设置：总数量、有效期、每码限用次数（通常1次）
- 后台实时查看兑换率，评估渠道合作效果

**㉔ 内容分销市场**
- 将平台部分课程开放给外部渠道（考研博主/其他平台）上架分销
- 内容方（本平台）设定分成比例，渠道方获得对应佣金
- 渠道方可在自己的平台/公众号/小程序中展示并售卖课程
- 管理后台：审核分销申请、查看各渠道销售数据、结算佣金

---

##### 【第五类】智能自动化运营（6种触发场景）

> 基于用户行为自动触发，通过腾讯云SMS（短信）+ 站内消息 + 微信服务号推送 实现，管理后台可开关和配置每个场景。

| # | 触发场景 | 触发条件 | 自动动作 | 发送渠道 |
|---|---|---|---|---|
| ① | **兴趣转换** | 浏览商品详情页 > 3次但未购买，且超过1天 | 发送「您关注的课程有限时优惠」+9折券 | 站内信+短信 |
| ② | **未付款订单唤回** | 创建订单未支付超过24小时 | 发送「您的订单即将过期，限时再享折扣」 | 站内信+短信 |
| ③ | **新客复购激励** | 首次购买后30天内未二次购买 | 推送「已完成XX课，搭配YY课效果更佳」+折扣券 | 站内信+微信推送 |
| ④ | **高活跃用户维系** | 近7天每天登录的用户 | 推送专属学习报告+积分奖励通知 | 站内信 |
| ⑤ | **流失用户召回** | 有过消费记录但30天未登录 | 发送「距考研还有XX天，回来继续备考」+积分补贴 | 短信+微信推送 |
| ⑥ | **收藏未购提醒** | 收藏商品超过3天未购买 | 推送「您收藏的课程即将恢复原价」制造紧迫感 | 站内信 |

---

##### 【第六类】店铺展示与氛围工具（4种）

**㉕ 销售弹幕（实时购买提示）**
- 课程页面底部滚动显示：「XX同学刚刚购买了本课程」
- 后台可设置是否开启，增加购买热度氛围，提升转化信心
- 数据来源：真实最近购买记录（可设置最近N小时内的订单）

**㉖ 划线价展示（原价对比）**
- 与第①条价格促销中划线价配合，在商品列表卡片和详情页双处展示
- 配合限时折扣时，在折扣价旁显示倒计时

**㉗ 首页轮播 + 活动微页面**
- 管理后台可视化拖拽配置首页轮播图，链接到活动页
- 活动微页面（Landing Page）：专为大促设计的活动落地页，支持组件搭配（轮播图、倒计时、课程卡片、优惠券领取按钮等）
- 运营人员无需开发，自助配置发布

**㉘ 商品分组与推荐位**
- 管理后台可将课程分组（如"冲刺必备"、"高分套餐"、"限时特惠"），在首页和课程列表特殊展示
- 支持手动排序推荐位，将重点促销商品置顶

---

##### 促销功能数据库支撑（新增表）

```sql
-- 优惠券模板表
CREATE TABLE coupon_templates (
  id            BIGINT PRIMARY KEY AUTO_INCREMENT,
  name          VARCHAR(100),
  type          ENUM('fixed','percent','product_specific'),
  discount_value DECIMAL(10,2),     -- 固定减免金额 或 折扣率(0.8=8折)
  min_amount    DECIMAL(10,2) DEFAULT 0, -- 最低消费门槛
  applicable_to ENUM('all','specific_course','vip'),
  course_ids    JSON,               -- 指定课程ID列表
  total_count   INT,                -- 发放总数，NULL=不限
  per_user_limit INT DEFAULT 1,
  valid_days    INT,                -- 领取后N天有效
  start_at      DATETIME,
  end_at        DATETIME,
  is_paid       BOOLEAN DEFAULT FALSE, -- 是否有价优惠券
  paid_price    DECIMAL(10,2),
  created_at    DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 用户领取优惠券记录
CREATE TABLE user_coupons (
  id            BIGINT PRIMARY KEY AUTO_INCREMENT,
  user_id       BIGINT REFERENCES users(id),
  template_id   BIGINT REFERENCES coupon_templates(id),
  code          VARCHAR(32) UNIQUE, -- 唯一券码
  status        ENUM('unused','used','expired') DEFAULT 'unused',
  used_order_id BIGINT,
  expires_at    DATETIME,
  received_at   DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 限时活动表（覆盖限时折扣、秒杀）
CREATE TABLE flash_sales (
  id            BIGINT PRIMARY KEY AUTO_INCREMENT,
  name          VARCHAR(100),
  type          ENUM('discount','seckill'),
  start_at      DATETIME,
  end_at        DATETIME,
  status        ENUM('preview','active','ended') DEFAULT 'preview',
  created_at    DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 限时活动商品表
CREATE TABLE flash_sale_items (
  id            BIGINT PRIMARY KEY AUTO_INCREMENT,
  sale_id       BIGINT REFERENCES flash_sales(id),
  product_type  ENUM('course','vip','points_pack'),
  product_id    BIGINT,
  original_price DECIMAL(10,2),
  sale_price    DECIMAL(10,2),
  stock_limit   INT,               -- NULL=不限量；秒杀时必填
  sold_count    INT DEFAULT 0,
  UNIQUE KEY uq_sale_product (sale_id, product_type, product_id)
);

-- 拼团活动表
CREATE TABLE group_buy_activities (
  id            BIGINT PRIMARY KEY AUTO_INCREMENT,
  product_type  ENUM('course','vip'),
  product_id    BIGINT,
  type          ENUM('normal','invite_new','ladder'),
  time_limit_hours INT DEFAULT 48, -- 成团时限
  start_at      DATETIME,
  end_at        DATETIME,
  -- 阶梯拼团价格档次（JSON: [{people:3,price:199},{people:5,price:169}]）
  ladder_prices JSON,
  -- 普通/邀新拼团
  group_size    INT,               -- 需要几人
  group_price   DECIMAL(10,2),
  leader_price  DECIMAL(10,2),     -- 团长价
  status        ENUM('active','ended') DEFAULT 'active'
);

-- 拼团记录表
CREATE TABLE group_buy_orders (
  id            BIGINT PRIMARY KEY AUTO_INCREMENT,
  activity_id   BIGINT REFERENCES group_buy_activities(id),
  leader_id     BIGINT REFERENCES users(id),
  status        ENUM('open','success','failed') DEFAULT 'open',
  current_size  INT DEFAULT 1,
  expires_at    DATETIME,
  created_at    DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 拼团参与记录
CREATE TABLE group_buy_members (
  id            BIGINT PRIMARY KEY AUTO_INCREMENT,
  group_id      BIGINT REFERENCES group_buy_orders(id),
  user_id       BIGINT REFERENCES users(id),
  is_leader     BOOLEAN DEFAULT FALSE,
  is_new_user   BOOLEAN DEFAULT FALSE,
  order_id      BIGINT REFERENCES orders(id),
  joined_at     DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 推广员表
CREATE TABLE promoters (
  id            BIGINT PRIMARY KEY AUTO_INCREMENT,
  user_id       BIGINT REFERENCES users(id) UNIQUE,
  status        ENUM('pending','approved','rejected','banned') DEFAULT 'pending',
  level         ENUM('basic','senior') DEFAULT 'basic',
  commission_rate1 DECIMAL(4,2) DEFAULT 0.15, -- 一级佣金率
  commission_rate2 DECIMAL(4,2) DEFAULT 0.05, -- 二级佣金率
  parent_promoter_id BIGINT,       -- 上级推广员
  total_earned  DECIMAL(10,2) DEFAULT 0,
  withdrawable  DECIMAL(10,2) DEFAULT 0,
  applied_at    DATETIME DEFAULT CURRENT_TIMESTAMP,
  approved_at   DATETIME
);

-- 推广员佣金记录
CREATE TABLE promoter_commissions (
  id            BIGINT PRIMARY KEY AUTO_INCREMENT,
  promoter_id   BIGINT REFERENCES promoters(id),
  order_id      BIGINT REFERENCES orders(id),
  level         TINYINT,           -- 1=直接佣金 2=间接佣金
  amount        DECIMAL(10,2),
  status        ENUM('pending','settled','withdrawn') DEFAULT 'pending',
  created_at    DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 兑换码表
CREATE TABLE redeem_codes (
  id            BIGINT PRIMARY KEY AUTO_INCREMENT,
  batch_name    VARCHAR(100),      -- 批次名称（如"某机构合作码"）
  code          VARCHAR(32) UNIQUE,
  reward_type   ENUM('course','vip_days','points'),
  reward_id     BIGINT,            -- course_id 或 NULL
  reward_value  INT,               -- VIP天数 或 积分数量
  is_used       BOOLEAN DEFAULT FALSE,
  used_by       BIGINT REFERENCES users(id),
  used_at       DATETIME,
  expires_at    DATETIME,
  created_at    DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 智能运营触发记录（防重复触发）
CREATE TABLE auto_marketing_logs (
  id            BIGINT PRIMARY KEY AUTO_INCREMENT,
  user_id       BIGINT REFERENCES users(id),
  scene         VARCHAR(50),       -- 触发场景编码
  triggered_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY uq_user_scene_day (user_id, scene, DATE(triggered_at))
);

-- 打卡活动表
CREATE TABLE checkin_activities (
  id            BIGINT PRIMARY KEY AUTO_INCREMENT,
  name          VARCHAR(100),
  type          ENUM('daily','challenge','paid'),
  target_days   INT,               -- 目标天数（如100天）
  reward_type   ENUM('points','coupon','cashback'),
  reward_value  DECIMAL(10,2),
  deposit_amount DECIMAL(10,2) DEFAULT 0, -- 付费打卡保证金
  start_at      DATETIME,
  end_at        DATETIME
);
```

---

##### 促销功能实施优先级

```
【MVP第一期】— 核心转化工具（先上线）
  ✅ 划线价展示
  ✅ 普通优惠券（新人券 + 满减券）
  ✅ 限时折扣（带倒计时）
  ✅ 邀请码注册（双向积分）
  ✅ 请好友免费看（单节试看）
  ✅ 打卡签到 + 连续打卡奖励
  ✅ 打卡返学费（VIP年卡用户）
  ✅ 批量兑换码（用于机构合作）
  ✅ 弹窗广告（大促期间手动开关）

【第二期】— 裂变与自动化
  ⬜ 秒杀（含预热和预约）
  ⬜ 有价优惠券（预售券）
  ⬜ 三种拼团（普通/邀新/阶梯）
  ⬜ 裂变海报（带参二维码海报）
  ⬜ 涨粉神器（关注送课）
  ⬜ 推广员分销计划（含佣金结算）
  ⬜ 支付有礼（购后自动赠券）
  ⬜ 成长任务 + 勋章体系
  ⬜ 学习排行榜
  ⬜ 结课证书（可分享朋友圈）
  ⬜ 送好友（赠课功能）
  ⬜ 智能自动化运营（6个触发场景）
  ⬜ 销售弹幕（实时购买提示）

【第三期】— 生态完善
  ⬜ 内容分销市场（对外渠道分销）
  ⬜ 付费打卡（保证金模式）
  ⬜ 活动微页面（Landing Page可视化编辑）
  ⬜ 商品分组推荐位管理
  ⬜ 积分商城完整版（积分兑换实物周边）
  ⬜ 二级推广员佣金体系
```

---

## 五、题库系统设计（数据库核心）

### 5.1 知识点标签体系（树形结构）

```
科目（Subject）
├── 数学基础
│   ├── 代数
│   │   ├── 整式与分式
│   │   ├── 函数（一次/二次/幂函数）
│   │   ├── 方程与不等式
│   │   └── 数列（等差/等比）
│   ├── 几何
│   │   ├── 平面几何（三角形/四边形/圆）
│   │   ├── 立体几何（椎体/球）
│   │   └── 解析几何（直线/圆/抛物线）
│   └── 数据分析
│       ├── 排列组合
│       └── 概率（古典概型）
├── 逻辑推理
│   ├── 形式逻辑
│   │   ├── 命题与推理
│   │   └── 假言命题
│   ├── 论证逻辑
│   │   ├── 削弱型
│   │   ├── 支持型
│   │   └── 解释型
│   └── 综合推理
│       ├── 分析推理
│       └── 数独/符号推理
├── 写作
│   ├── 论证有效性分析
│   │   ├── 因果混淆
│   │   ├── 以偏概全
│   │   ├── 概念不清
│   │   └── 论据不足
│   └── 论说文
│       ├── 命题作文
│       └── 材料作文
└── 英语二
    ├── 完形填空
    ├── 阅读理解
    │   ├── Part A（精读）
    │   └── Part B（新题型）
    ├── 翻译（英译汉）
    └── 写作
        ├── 小作文
        └── 大作文
```

### 5.2 题目数据结构（MongoDB）

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

### 5.3 错题与智能推荐逻辑

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

第N次做错同类型题 → 频率继续加大，标记为"重点薄弱点"
```

### 5.4 题目来源两种模块

**模块一：教师上传**
- 教师在管理后台上传题目（支持 Word/PDF/图片）
- 系统调用 Claude API 自动解析题目内容、提取知识点、打标签
- 教师审核后发布

**模块二：AI生成**
- 基于知识点标签，调用 Claude API 生成练习题
- 系统标注"AI生成题目"角标，与真题区分
- 学生可选择：只做真题 / 只做AI题 / 混合

```python
# AI生成题目示例（Flask接口）
@app.route('/api/questions/generate', methods=['POST'])
def generate_question():
    tag = request.json['tag']  # e.g. "二次函数"
    difficulty = request.json['difficulty']  # 1-5
    count = request.json.get('count', 3)

    prompt = f"""
    请为管理类联考数学基础生成{count}道关于"{tag}"的练习题。
    难度等级：{difficulty}/5
    题型：问题求解（五选一）
    要求：符合管理类联考出题风格，选项干扰项设计合理
    输出JSON格式：[{{"stem":..., "options":[...], "correct":"X", "analysis":...}}]
    """

    response = anthropic_client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}]
    )
    return jsonify(json.loads(response.content[0].text))
```

---

## 六、视频系统设计

### 6.1 两类视频

**类型一：录播课（系统讲解）**
- 存储：腾讯云 VOD（云点播）
- 防盗链：签名URL，有效期2小时
- 结构：科目 → 章节 → 课时（每课时20-45分钟）
- 功能：
  - 学生可先"预习做题"，再看视频讲解
  - 或直接看视频
  - 记录观看进度（watched_seconds）
- 收费：部分免费预览（前5分钟），全集付费

**类型二：题目视频解析**
- 每道题配备文字解析（免费）+ 视频解析（付费/消耗积分）
- 视频时长：3-8分钟（精讲单题）
- 存储：腾讯云 VOD
- 收费规则：消耗10积分 或 VIP会员免费

### 6.2 直播课
- 推流：腾讯云 CSS（云直播）教师端
- 拉流：学生端 HLS 播放
- 互动：腾讯云 TRTC（互动连麦）+ 腾讯 IM（聊天室）
- 录制：直播结束自动转存 VOD，变为回放

```javascript
// 腾讯云直播推流（教师端）
const pusher = new TXLivePusher();
pusher.startCamera();
pusher.startPush('rtmp://push.your-domain.com/live/room_' + roomId + '?txSecret=xxx&txTime=xxx');

// 学生端拉流
const player = TCPlayer('player-container', {
  fileID: '',
  appID: '',
  sources: [{ src: 'https://play.your-domain.com/live/room_' + roomId + '.m3u8' }]
});
```

---

## 七、AI 写作批改系统

### 论证有效性分析批改流程

```python
@app.route('/api/writing/critique', methods=['POST'])
def critique_essay():
    user_essay = request.json['essay']        # 用户写的批改文章
    original_material = request.json['material']  # 题目原材料

    # 调用腾讯混元大模型
    from tencentcloud.hunyuan.v20230901 import hunyuan_client, models

    client = hunyuan_client.HunyuanClient(cred, 'ap-guangzhou')
    req = models.ChatCompletionsRequest()
    req.Messages = [{
        "Role": "user",
        "Content": f"""
        你是管理类联考写作评分专家。请对以下论证有效性分析作文进行批改：

        【原材料】：{original_material}
        【学生作文】：{user_essay}

        请从以下维度评分（各25分）：
        1. 论证漏洞识别准确性（是否找到主要问题）
        2. 分析深度（是否说清楚为什么是漏洞）
        3. 语言表达（逻辑性、准确性）
        4. 结构完整性（开头/主体/结尾）

        输出格式：JSON
        {{
          "total_score": X,
          "dimension_scores": {{"accuracy":X, "depth":X, "language":X, "structure":X}},
          "found_issues": ["找到的漏洞1", "找到的漏洞2"],
          "missed_issues": ["遗漏的漏洞1"],
          "feedback": "具体改进建议...",
          "sample_paragraph": "示范段落..."
        }}
        """
    }]
    response = client.ChatCompletions(req)
    return jsonify(json.loads(response.Choices[0].Message.Content))
```

---

## 八、数据库表结构（MySQL）

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
  amount      INT NOT NULL,           -- 正数=获得，负数=消耗
  type        VARCHAR(50) NOT NULL,   -- 'daily_checkin','correct_answer','purchase'等
  description VARCHAR(200),
  balance     INT NOT NULL,           -- 变动后余额
  created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 每日刷题额度表（Redis为主，MySQL做持久化）
CREATE TABLE daily_quota (
  id          BIGINT PRIMARY KEY AUTO_INCREMENT,
  user_id     BIGINT REFERENCES users(id),
  date        DATE NOT NULL,
  free_done   INT DEFAULT 0,          -- 今日已做免费题数
  wrong_count INT DEFAULT 0,          -- 今日答错题数
  quota_used  BOOLEAN DEFAULT FALSE,  -- 免费额度是否已耗尽
  UNIQUE KEY uq_user_date (user_id, date)
);

-- 用户答题记录表
CREATE TABLE answer_records (
  id            BIGINT PRIMARY KEY AUTO_INCREMENT,
  user_id       BIGINT REFERENCES users(id),
  question_id   VARCHAR(50) NOT NULL,  -- MongoDB题目ID
  subject       VARCHAR(20),
  is_correct    BOOLEAN,
  user_answer   VARCHAR(10),
  time_spent    INT,                   -- 答题用时（秒）
  points_cost   INT DEFAULT 0,         -- 本题消耗积分
  created_at    DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 错题本表
CREATE TABLE wrong_questions (
  id            BIGINT PRIMARY KEY AUTO_INCREMENT,
  user_id       BIGINT REFERENCES users(id),
  question_id   VARCHAR(50) NOT NULL,
  wrong_count   INT DEFAULT 1,         -- 错误次数
  last_wrong_at DATETIME,
  next_review_at DATETIME,             -- 下次复习时间（艾宾浩斯）
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
  vod_file_id   VARCHAR(200),          -- 腾讯云VOD文件ID
  duration_sec  INT,
  sort_order    INT,
  is_free       BOOLEAN DEFAULT FALSE, -- 是否可免费预览
  preview_sec   INT DEFAULT 300,       -- 免费预览秒数
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
  stream_key    VARCHAR(200),          -- 腾讯云CSS推流Key
  status        ENUM('scheduled','live','ended') DEFAULT 'scheduled',
  replay_vod_id VARCHAR(200),          -- 结束后转存VOD
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
  ai_model        VARCHAR(50),         -- 'hunyuan'
  points_cost     INT DEFAULT 50,
  created_at      DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

---

## 九、前端页面结构

### Web 端路由规划（Vue Router）

```
/                     → 首页（产品介绍 + CTA）
/login                → 登录/注册
/dashboard            → 学习中心（登录后首页）
  /dashboard/today    → 今日任务
  /dashboard/progress → 学习进度报告

/subjects             → 科目选择页
/practice             → 刷题页面
  /practice/math      → 数学练习
  /practice/logic     → 逻辑练习
  /practice/writing   → 写作练习
  /practice/english   → 英语练习
  /practice/mixed     → 综合练习

/question/:id         → 单题详情 + 解析页

/wrong-book           → 错题本
  /wrong-book/math    → 数学错题
  /wrong-book/logic   → 逻辑错题

/mock-exam            → 真题模拟
  /mock-exam/select   → 选择年份
  /mock-exam/:year    → 模拟考试
  /mock-exam/result   → 成绩报告

/courses              → 课程中心
  /courses/:id        → 课程详情
  /courses/:id/learn  → 课程播放页（视频）

/live                 → 直播课列表
  /live/:id           → 直播课间
  /live/:id/replay    → 回放

/writing-lab          → 写作训练室
  /writing-lab/critique   → 论证有效性分析练习+批改
  /writing-lab/argument   → 论说文练习+批改

/profile              → 个人中心
  /profile/points     → 积分明细
  /profile/orders     → 订单记录
  /profile/vip        → VIP开通

/shop                 → 商城（积分兑换 / 课程购买）

/admin                → 管理后台（role=admin/teacher可见）
  /admin/questions    → 题库管理
  /admin/courses      → 课程管理
  /admin/users        → 用户管理
  /admin/orders       → 订单管理
  /admin/analytics    → 数据分析
```

---

## 十、设计系统（UI规范，所有页面必须遵守）

### 配色
```css
--color-primary:    #4F6EF7;  /* 品牌蓝，主按钮/链接 */
--color-primary-hover: #3B54D4;
--color-primary-light: #EEF1FE;
--color-bg:         #FFFFFF;
--color-surface:    #F7F8FA;
--color-border:     #E8EAED;
--color-text-main:  #1A1A2E;
--color-text-muted: #6B7280;
--color-text-hint:  #9CA3AF;
--color-success:    #10B981;
--color-warning:    #F59E0B;
--color-error:      #EF4444;
--color-math:       #6C63FF;  /* 数学科目标识色 */
--color-logic:      #F97316;  /* 逻辑科目标识色 */
--color-writing:    #EC4899;  /* 写作科目标识色 */
--color-english:    #14B8A6;  /* 英语科目标识色 */
```

### 字体
```css
font-family: 'Inter', 'PingFang SC', 'Microsoft YaHei', sans-serif;
/* 中文段落额外加 */
line-height: 1.7;
```

### 间距（8px网格）
```
xs:4px  sm:8px  md:16px  lg:24px  xl:32px  2xl:48px  3xl:64px
```

### 组件规范
```css
/* 主按钮 */
.btn-primary {
  background: #4F6EF7; color: #fff;
  border-radius: 10px; padding: 12px 28px;
  font-size: 15px; font-weight: 500;
  transition: all 0.2s;
}

/* 卡片 */
.card {
  background: #fff;
  border: 1px solid #E8EAED;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.06);
}

/* 科目标签 */
.tag-math    { background: #EEF0FF; color: #6C63FF; }
.tag-logic   { background: #FFF4EE; color: #F97316; }
.tag-writing { background: #FFF0F6; color: #EC4899; }
.tag-english { background: #EFFAF8; color: #14B8A6; }
```

### Wix 风格设计原则（必须遵守）
1. 大量留白，节间距最少64px
2. 一个页面只有一个主要强调色（#4F6EF7）
3. Hero区大标题粗体（font-size: 48-64px, font-weight: 700）
4. 卡片极简，薄边框+轻阴影，无渐变
5. 所有可交互元素 `transition: all 0.2s`
6. 移动优先响应式（375px起）
7. 布局不规则有变化（非等宽grid），体现设计感

---

## 十一、API 设计规范

### 统一响应格式
```json
{
  "success": true,
  "data": {},
  "message": "操作成功",
  "pagination": { "page": 1, "page_size": 20, "total": 100 }
}
```

### 错误响应
```json
{
  "success": false,
  "error": { "code": "QUOTA_EXCEEDED", "message": "今日免费额度已用完，请消耗积分继续或升级VIP" }
}
```

### 关键接口列表
```
# 用户认证
POST /api/auth/register          # 注册（邮箱/手机）
POST /api/auth/login             # 登录
POST /api/auth/wechat            # 微信登录（预留）
POST /api/auth/refresh           # 刷新Token

# 题目
GET  /api/questions              # 题目列表（?subject=math&tag=函数&page=1）
GET  /api/questions/:id          # 题目详情
POST /api/questions/:id/submit   # 提交答案（触发积分/额度逻辑）
GET  /api/questions/recommend    # 获取推荐题目（基于错题标签）
POST /api/questions/generate     # AI生成题目（管理员）

# 积分
GET  /api/points/balance         # 当前积分余额
GET  /api/points/transactions    # 积分流水
POST /api/points/checkin         # 每日签到
GET  /api/points/quota/today     # 今日剩余免费额度

# 错题本
GET  /api/wrong-book             # 错题列表（?subject=math）
DELETE /api/wrong-book/:id       # 移出错题本（标记已掌握）

# 课程
GET  /api/courses                # 课程列表
GET  /api/courses/:id            # 课程详情
GET  /api/lessons/:id/play-url   # 获取视频播放签名URL（VOD）

# 直播
GET  /api/live-classes           # 直播课列表
POST /api/live-classes/:id/join  # 加入直播间
GET  /api/live-classes/:id/token # 获取TRTC token

# 写作批改
POST /api/writing/critique       # 提交论证有效性分析批改
POST /api/writing/argument       # 提交论说文批改

# 支付
POST /api/orders                 # 创建订单
GET  /api/orders/:id             # 订单状态
POST /api/webhooks/wechat-pay    # 微信支付回调
```

---

## 十二、环境变量（.env 模板）

```env
# Flask
FLASK_ENV=development
SECRET_KEY=your-secret-key
JWT_SECRET=your-jwt-secret-64-chars

# MySQL (腾讯云TencentDB)
DB_HOST=gz-cdb-xxx.sql.tencentcdb.com
DB_PORT=3306
DB_NAME=guanlian_db
DB_USER=guanlian_user
DB_PASS=your-db-password

# MongoDB (题库)
MONGO_URI=mongodb://localhost:27017/guanlian_questions

# Redis
REDIS_HOST=gz-redis-xxx.redis.tencentcdb.com
REDIS_PORT=6379
REDIS_PASS=your-redis-password

# 腾讯云
TENCENT_SECRET_ID=AKIDxxx
TENCENT_SECRET_KEY=xxx
TENCENT_REGION=ap-guangzhou

# 腾讯云COS（文件存储）
COS_BUCKET=guanlian-assets-1234567890
COS_REGION=ap-guangzhou

# 腾讯云VOD（视频点播）
VOD_APP_ID=your-vod-appid
VOD_SUB_APP_ID=your-subapp-id

# 腾讯云CSS（直播）
CSS_PUSH_DOMAIN=push.your-domain.com
CSS_PLAY_DOMAIN=play.your-domain.com
CSS_KEY=your-css-key

# 腾讯云TRTC（实时音视频）
TRTC_APP_ID=your-trtc-appid
TRTC_SECRET_KEY=xxx

# 腾讯云IM（即时通信）
IM_SDK_APP_ID=your-im-appid
IM_ADMIN_KEY=xxx

# 腾讯云SMS（短信）
SMS_APP_ID=xxx
SMS_SIGN=管理联考学习
SMS_OTP_TEMPLATE_ID=xxx

# 腾讯混元大模型（写作批改）
HUNYUAN_SECRET_ID=xxx
HUNYUAN_SECRET_KEY=xxx

# Anthropic Claude API（AI题目生成与解析）
ANTHROPIC_API_KEY=sk-ant-xxx
ANTHROPIC_MODEL=claude-sonnet-4-6

# 微信小程序（第二期）
WX_APPID=wx...
WX_SECRET=xxx

# 微信支付
WECHAT_PAY_MCH_ID=xxx
WECHAT_PAY_NOTIFY_URL=https://api.yourdomain.com/api/webhooks/wechat-pay

# 前端
VUE_APP_API_BASE=http://localhost:5000
VUE_APP_TRTC_APP_ID=your-trtc-appid
```

---

## 十三、项目目录结构（建议）

```
guanlian-learning/
├── backend/                    # Flask 后端
│   ├── app.py                  # 入口
│   ├── config.py               # 配置加载
│   ├── models/                 # SQLAlchemy 模型
│   │   ├── user.py
│   │   ├── order.py
│   │   ├── points.py
│   │   └── writing.py
│   ├── routes/                 # API 路由
│   │   ├── auth.py
│   │   ├── questions.py
│   │   ├── points.py
│   │   ├── courses.py
│   │   ├── writing.py
│   │   ├── live.py
│   │   └── payment.py
│   ├── services/               # 业务逻辑
│   │   ├── ai_service.py       # Claude API 调用
│   │   ├── hunyuan_service.py  # 混元大模型调用
│   │   ├── vod_service.py      # 腾讯云VOD
│   │   ├── points_service.py   # 积分计算逻辑
│   │   └── question_service.py # 题目推荐逻辑
│   └── requirements.txt
│
├── frontend/                   # Vue.js 前端
│   ├── src/
│   │   ├── views/              # 页面组件
│   │   │   ├── Home.vue
│   │   │   ├── Dashboard.vue
│   │   │   ├── Practice.vue
│   │   │   ├── Question.vue
│   │   │   ├── WrongBook.vue
│   │   │   ├── MockExam.vue
│   │   │   ├── Courses.vue
│   │   │   ├── Live.vue
│   │   │   ├── WritingLab.vue
│   │   │   ├── Profile.vue
│   │   │   ├── Shop.vue
│   │   │   └── Admin/
│   │   ├── components/         # 公共组件
│   │   │   ├── QuestionCard.vue
│   │   │   ├── ProgressRing.vue
│   │   │   ├── PointsBadge.vue
│   │   │   ├── SubjectTag.vue
│   │   │   └── VideoPlayer.vue
│   │   ├── router/index.js
│   │   ├── store/index.js      # Pinia
│   │   ├── api/                # API调用模块
│   │   └── utils/
│   │       ├── request.js      # Axios 拦截器
│   │       └── auth.js
│   ├── package.json
│   └── vite.config.js
│
└── CLAUDE.md                   # 本文件（Claude Code 全局指令）
```

---

## 十四、给 Claude Code 的工作指令

每次接到编码任务时，请遵守以下规则：

1. **技术选型** — 严格按照本文件第二章技术栈，不得引入未列出的框架
2. **云服务** — 所有云功能必须使用腾讯云，不用 AWS/Alibaba
3. **AI接口** — 题目生成用 Claude API，写作批改用混元大模型
4. **数据库** — 用户/订单/积分用 MySQL；题库用 MongoDB
5. **积分逻辑** — 任何涉及答题的接口都必须触发积分/额度判断（见第四章）
6. **设计风格** — 所有前端组件遵守第十章设计系统，Wix简洁现代风格
7. **响应格式** — 所有API统一使用第十一章的JSON格式
8. **错题推荐** — 做题后必须更新错题本，并基于标签体系计算推荐（见第五章）
9. **安全** — 所有视频URL必须用腾讯VOD签名，支付回调必须验签
10. **注释** — 关键逻辑用中文注释，方便团队阅读

---

*文档版本：v1.0 | 创建日期：2026-06-22 | 维护人：Hai Lyu*
*下次更新：待商业模式促销细节确认后补充第四章4.3节*
