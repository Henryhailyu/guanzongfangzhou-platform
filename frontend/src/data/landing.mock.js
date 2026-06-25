export const navLinks = [
  { label: '首页', href: '#top' },
  { label: '课程体系', href: '#courses' },
  { label: '智能题库', href: '#features' },
  { label: 'AI 批改', href: '#ai' },
  { label: '名师入驻', href: '#teacher-join' },
  { label: '上岸计划', href: '#solution' },
]

export const footerLinks = [
  { label: '关于我们', href: '#' },
  { label: '课程体系', href: '#courses' },
  { label: '教师入驻', href: '#teacher-join' },
  { label: '商务合作', href: '#' },
  { label: '用户协议', href: '#' },
  { label: '隐私政策', href: '#' },
  { label: '联系我们', href: '#' },
]

export const heroTags = [
  { icon: '📘', text: '199 管综 + 英语二全覆盖' },
  { icon: '🤖', text: 'AI 写作批改与错题诊断' },
  { icon: '🎯', text: '名师课程 + 个性化学习路径' },
  { icon: '👨‍🏫', text: '教师可开课、售课、运营学员' },
]

export const painPoints = [
  { title: '做题很多，但不知道错在哪里', desc: '错题堆积，知识点混乱，复习没有优先级。' },
  { title: '管综时间太紧，速度练不上来', desc: '数学、逻辑、写作都要在有限时间内完成，单靠刷题很难形成考试节奏。' },
  { title: '条件充分性判断总是卡住', desc: '题型特殊，判断路径复杂，缺少专项训练和可视化解析。' },
  { title: '逻辑阅读量大，题干越看越乱', desc: '形式推理、论证推理、综合推理混在一起，缺少结构化训练。' },
  { title: '写作不知道怎么提分', desc: '论证有效性分析不会找漏洞，论说文缺少结构、素材和反馈。' },
  { title: '在职备考时间碎片化', desc: '通勤、午休、晚上学习时间有限，需要更精准的每日任务安排。' },
]

export const solutionSteps = [
  { step: '测', title: '入学诊断', desc: '入学诊断，找到真实短板。' },
  { step: '学', title: '系统学习', desc: '跟随名师课程，系统完成基础、强化、冲刺学习。' },
  { step: '练', title: '智能刷题', desc: '智能题库按知识点、题型、难度、正确率和耗时推送练习。' },
  { step: '改', title: 'AI + 老师批改', desc: 'AI 批改与老师反馈结合，提升写作、英语作文和论证分析能力。' },
  { step: '冲', title: '冲刺模考', desc: '阶段模考、错题回炉、冲刺计划和数据报告，形成考前节奏。' },
]

export const studentFeatures = [
  { title: '智能题库', desc: '覆盖数学基础、逻辑推理、写作、英语二，支持专项练习、随机练习、限时训练和错题回炉。', link: '/practice' },
  { title: 'AI 解析与错题诊断', desc: '不只告诉学生答案，更解释为什么错、错因属于哪类、下一步该练什么。', link: '/practice' },
  { title: '写作批改中心', desc: '支持论证有效性分析、论说文、英语小作文、英语大作文，从结构、逻辑、语言、论证和表达方面给出反馈。', link: '/practice' },
  { title: '每日上岸计划', desc: '把长期备考目标拆解为每日任务，支持打卡、提醒、进度条和阶段目标。', link: '/dashboard' },
  { title: '学习报告与成长曲线', desc: '展示正确率、耗时、薄弱知识点、错题掌握率、模考表现和学习趋势。', link: '/dashboard' },
  { title: '名师课程', desc: '学生可以查看老师主页、课程介绍、试看内容、学员评价和课程优惠。', link: '/courses' },
]

export const examSubjects = [
  { key: 'math', name: '数学基础', score: 75, color: '#4F6EF7', desc: '问题求解 + 条件充分性判断。重点解决公式不会用、题型反应慢、条件判断混乱的问题。' },
  { key: 'logic', name: '逻辑推理', score: 60, color: '#8B5CF6', desc: '形式推理 + 论证推理 + 综合推理。训练题干拆解、推理路径、选项排除和限时阅读能力。' },
  { key: 'writing', name: '写作', score: 65, color: '#F97316', desc: '论证有效性分析 + 论说文。从找漏洞、搭结构、积累素材到表达优化，形成可复用写作方法。' },
  { key: 'english', name: '英语二', score: 100, color: '#14B8A6', desc: '完形、阅读、翻译、小作文、大作文。围绕词汇、长难句、阅读速度和写作表达进行分层训练。' },
]

export const aiFeatures = [
  { title: 'AI 题目解析', desc: '看懂答案背后的解题路径。' },
  { title: 'AI 写作批改', desc: '快速定位结构、逻辑、语言和论证问题。' },
  { title: 'AI 学习诊断', desc: '根据正确率、耗时和错因生成能力画像。' },
  { title: 'AI 练习推荐', desc: '自动推荐相似题、薄弱题和冲刺题。' },
  { title: '教师个性化 AI 助教', desc: '第二期支持老师上传讲义、课件、答疑记录，训练自己的课程 AI 助教。', badge: '第二期' },
]

export const dashboardMetrics = [
  { label: '今日完成率', value: '76%', icon: '✅', trend: '' },
  { label: '本周刷题', value: '328 题', icon: '📝', trend: '+15% 较上周' },
  { label: '错题掌握率', value: '61%', icon: '🔄', trend: '+8%' },
  { label: '写作修改', value: '4 次', icon: '✍️', trend: '' },
  { label: '英语阅读正确率', value: '72%', icon: '📖', trend: '+6%' },
  { label: '逻辑平均耗时', value: '下降 18%', icon: '⏱️', trend: '' },
  { label: '上岸进度', value: '67%', icon: '🎯', trend: '距目标 98 天' },
]

export const heroTasks = [
  { name: '数学基础 20 题', done: true },
  { name: '逻辑推理 15 题', done: true },
  { name: '写作训练 1 篇', done: false },
  { name: '英语阅读 2 篇', done: false },
]

export const teacherCardsFallback = [
  { name: '陈老师', subject: 'math', course: '199 数学基础系统班', tags: ['基础强化', '在职友好'], avatar: '陈' },
  { name: '林老师', subject: 'logic', course: '逻辑阅读提速班', tags: ['限时训练', '冲刺提分'], avatar: '林' },
  { name: '周老师', subject: 'writing', course: '论证分析与论说文写作班', tags: ['写作提分', 'AI 批改'], avatar: '周' },
]

export const teacherBenefits = [
  { title: '快速搭建个人课程主页', desc: '展示教师介绍、课程体系、试看内容、学员评价和购买入口。' },
  { title: '课程上传与售卖', desc: '支持录播课、直播课、资料包、题库训练营、冲刺班等课程形态。' },
  { title: '学员管理与学习数据', desc: '老师只管理自己课程的已购学员，查看进度、作业、题库表现和反馈记录。' },
  { title: '专属推广链接', desc: '每位老师可生成课程推广链接，适配微信、朋友圈、小红书、抖音等渠道。' },
  { title: '收入结算清晰', desc: '课程销售默认教师 70%，平台 30%，后续可支持学员推广佣金从教师份额中扣除。' },
  { title: '个性化 AI 助教', desc: '第二期支持老师上传讲义、课件、答疑记录，训练自己的 AI 助教。', badge: '第二期' },
]

export const marketingTools = [
  { title: '新人优惠券', desc: '新用户注册即可领取备考课程优惠。' },
  { title: '限时折扣', desc: '暑期强化、考前冲刺、开班活动均可配置限时优惠。' },
  { title: '课程试看', desc: '支持单节试看，降低学生购买决策门槛。' },
  { title: '打卡奖励', desc: '连续学习、完成任务、参加训练营可获得积分和奖励。' },
  { title: '邀请有礼', desc: '学员邀请好友注册或购课，可获得积分、优惠券或佣金。' },
  { title: '教师推广链接', desc: '老师可在微信、抖音、小红书等渠道推广自己的课程。' },
]

export const audiences = [
  { title: '在职备考人群', desc: '时间少、压力大，需要高效率每日计划和碎片化学习。', emoji: '💼' },
  { title: '基础薄弱考生', desc: '需要从基础概念、题型方法、英语词汇和写作结构开始补齐。', emoji: '📚' },
  { title: '二战 / 三战考生', desc: '需要精准定位旧问题，避免重复低效刷题。', emoji: '🎯' },
  { title: '冲刺阶段考生', desc: '需要模考、限时训练、错题回炉和高频考点突破。', emoji: '🚀' },
]

export const testimonials = [
  { type: 'student', content: '以前我每天都在刷题，但不知道自己到底有没有进步。现在平台会告诉我数学哪类题最弱、逻辑哪类题最耗时，复习方向清楚很多。', author: 'MBA 备考生' },
  { type: 'student', content: '写作批改很有帮助，尤其是论证有效性分析。AI 先帮我指出漏洞类型，老师再给我改结构，效率比以前高很多。', author: 'MPAcc 在职考生' },
  { type: 'teacher', content: '我不需要自己搭建网站，也不用手动统计学生进度。课程、资料、作业、学员数据都在一个后台里，运营轻松很多。', author: '数学主讲老师' },
  { type: 'teacher', content: '教师主页和推广链接很适合我做私域和短视频转化，学生报名后还能继续在平台内学习和提交作业。', author: '逻辑主讲老师' },
]

export const faqs = [
  { q: '管综方舟适合哪些考生？', a: '适合备考 MBA、MPA、MPAcc、MEM、MAud 等管理类专业硕士的考生，包括在职、应届、二战及冲刺阶段学员。' },
  { q: '平台覆盖哪些考试科目？', a: '覆盖 199 管理类综合能力（数学、逻辑、写作）与英语二，总分 300 分全科备考。' },
  { q: 'AI 批改能代替老师吗？', a: 'AI 负责快速反馈与结构化诊断，老师负责深度点评与方法论指导，两者结合效率更高。' },
  { q: '老师如何申请入驻？', a: '注册账号后选择教师身份，提交资料后由平台管理员审核，通过即可开课。' },
  { q: '老师入驻后可以自己设置课程吗？', a: '可以。教师可在教师端创建课程、设置定价、上传课时和管理学员。' },
  { q: '学生可以试看课程吗？', a: '支持。部分课程提供免费试看章节，降低购买决策门槛。' },
  { q: '平台是否支持移动端或微信小程序？', a: 'Web 版已上线，微信小程序规划在第二期，支持碎片时间刷题。' },
  { q: '后续是否支持教师自己的 AI 助教？', a: '是的，第二期将支持教师上传知识库，为付费学员提供个性化 AI 答疑。' },
]

export const subjectLabels = { math: '数学', logic: '逻辑', writing: '写作', english: '英语', combo: '综合' }
