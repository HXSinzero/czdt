import { createRouter, createWebHistory } from 'vue-router'
import { appConfig } from '../config'
import HomeView from '../views/HomeView.vue'
import DirectionView from '../views/DirectionView.vue'
import IntakeView from '../views/IntakeView.vue'
import DashboardView from '../views/DashboardView.vue'
import StageDetailView from '../views/StageDetailView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
    meta: { title: '主页', pageTitle: '职业成长', subtitle: '' }
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
    meta: { title: '资质选择', pageTitle: '选择资质', subtitle: '选择你的修行起点', rightLabel: '总览' }
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: DashboardView,
    meta: { title: '路线总览', pageTitle: '修行年限', subtitle: '修行岁月，境界可期', rightLabel: '总览' }
  },
  {
    path: '/stage-detail',
    name: 'stage-detail',
    component: StageDetailView,
    meta: { title: '详情展示', pageTitle: '详情展示', subtitle: '阶段卷宗', rightLabel: '总览' }
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
