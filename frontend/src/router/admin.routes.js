import AdminLayout from '../layouts/AdminLayout.vue'

export default [
  {
    path: '/admin',
    component: AdminLayout,
    meta: { requiresAuth: true, roles: ['admin'] },
    children: [
      { path: '', name: 'AdminDashboard', component: () => import('../views/admin/Dashboard.vue') },
      { path: 'users', name: 'AdminUsers', component: () => import('../views/admin/Users.vue') },
      { path: 'teachers', name: 'AdminTeachers', component: () => import('../views/admin/Teachers.vue') },
      { path: 'courses', name: 'AdminCourses', component: () => import('../views/admin/Courses.vue') },
      { path: 'orders', name: 'AdminOrders', component: () => import('../views/admin/Orders.vue') },
      { path: 'questions', name: 'AdminQuestions', component: () => import('../views/admin/Questions.vue') },
      { path: 'analytics', name: 'AdminAnalytics', component: () => import('../views/admin/Analytics.vue') },
      { path: 'settings', name: 'AdminSettings', component: () => import('../views/admin/Settings.vue') },
    ],
  },
]
