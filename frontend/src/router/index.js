import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import studentRoutes from './student.routes'
import teacherRoutes from './teacher.routes'
import adminRoutes from './admin.routes'
import AuthLayout from '../layouts/AuthLayout.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    ...studentRoutes,
    ...teacherRoutes,
    ...adminRoutes,
    {
      path: '/',
      component: AuthLayout,
      children: [
        { path: 'login', name: 'Login', component: () => import('../views/shared/Login.vue') },
        { path: 'register/student', name: 'RegisterStudent', component: () => import('../views/shared/RegisterStudent.vue') },
        { path: 'register/teacher', name: 'RegisterTeacher', component: () => import('../views/shared/RegisterTeacher.vue') },
      ],
    },
  ],
})

router.beforeEach(async (to, from, next) => {
  const auth = useAuthStore()

  if (auth.token && !auth.user?.teacher_profile && auth.role === 'teacher') {
    await auth.fetchMe()
  }

  if (to.meta.requiresAuth && !auth.isLoggedIn) {
    return next({ path: '/login', query: { redirect: to.fullPath } })
  }

  if (to.meta.roles && auth.isLoggedIn && !to.meta.roles.includes(auth.role)) {
    if (auth.role === 'teacher') return next('/teacher')
    if (auth.role === 'admin') return next('/admin')
    return next('/dashboard')
  }

  next()
})

export default router
