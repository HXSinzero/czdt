import { appConfig } from '../config'

const localGuide = {
  profile: {
    title: '职页成长指引',
    summary: '围绕职业画像、能力补齐、项目实践和求职转化，帮助用户把成长路线拆成可执行的阶段任务。',
    ownerPath: appConfig.basePath
  },
  stages: [
    {
      id: 'discover',
      name: '探索定位',
      duration: '第 1-2 周',
      description: '明确目标岗位、行业方向和当前差距，形成个人成长基线。',
      tasks: ['梳理过往项目与岗位偏好', '完成 1 份能力自评', '选定 2-3 个目标岗位']
    },
    {
      id: 'build',
      name: '能力建设',
      duration: '第 3-6 周',
      description: '按岗位要求补齐核心技能，并沉淀可以展示的学习成果。',
      tasks: ['拆解岗位 JD 高频技能', '完成主题学习清单', '输出作品或复盘文章']
    },
    {
      id: 'practice',
      name: '项目实践',
      duration: '第 7-10 周',
      description: '用真实项目强化能力证据，让简历和作品集更有说服力。',
      tasks: ['选择一个业务场景', '完成可演示项目', '整理项目指标与亮点']
    },
    {
      id: 'convert',
      name: '求职转化',
      duration: '第 11-12 周',
      description: '优化简历、面试表达和投递节奏，把成长成果转化为机会。',
      tasks: ['打磨一页式简历', '准备 STAR 面试素材', '建立投递与复盘表']
    }
  ],
  capabilities: [
    { name: '职业定位', value: 78 },
    { name: '专业技能', value: 64 },
    { name: '项目表达', value: 58 },
    { name: '简历包装', value: 72 },
    { name: '面试沟通', value: 61 }
  ],
  actions: [
    '本周完成一次岗位样本分析，至少对比 10 条招聘信息。',
    '选择一个能体现目标能力的小项目，控制在两周内完成首版。',
    '把项目经历改写成“背景、动作、结果、反思”的结构。'
  ],
  resources: [
    { title: '岗位能力地图', type: '模板', tag: '定位' },
    { title: '项目复盘清单', type: '清单', tag: '实践' },
    { title: '面试素材库', type: '表格', tag: '转化' }
  ]
}

export async function getGrowthGuide() {
  // 后续接入真实接口时，可替换为 fetch(`${appConfig.apiBaseUrl}/growth-guide`)
  return localGuide
}
