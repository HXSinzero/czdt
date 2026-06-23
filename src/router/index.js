import { createRouter, createWebHistory } from 'vue-router'
import { appConfig } from '../config'
import HomeView from '../views/HomeView.vue'
import DirectionView from '../views/DirectionView.vue'
import IntakeView from '../views/IntakeView.vue'
import DashboardView from '../views/DashboardView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
    meta: { title: '主页', pageTitle: '职页成长', subtitle: '点击任意位置进入' }
  },
  {
    path: '/directions',
    name: 'directions',
    component: DirectionView,
    meta: { title: '方向选择', pageTitle: '道途抉择', subtitle: '选择你的修行之路', rightLabel: '总览' }
  },
  {
    path: '/intake',
    name: 'intake',
    component: IntakeView,
    meta: { title: '信息收集', pageTitle: '问心录', subtitle: '录入成长信息' }
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: DashboardView,
    meta: { title: '数据展示', pageTitle: '命盘总览', subtitle: '查看成长结果' }
  }
]

const router = createRouter({
  history: createWebHistory(appConfig.basePath),
  routes,
  scrollBehavior() {
    return { top: 0 }
  }
})

router.afterEach((to) => {
  document.title = `${to.meta.title} - 职页成长指引`
})

export default router
