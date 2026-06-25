import LandingLayout from '../layouts/LandingLayout.vue'
import StudentLayout from '../layouts/StudentLayout.vue'

export default [
  {
    path: '/',
    component: LandingLayout,
    children: [
      { path: '', name: 'Landing', component: () => import('../views/landing/LandingPage.vue') },
    ],
  },
  {
    path: '/',
    component: StudentLayout,
    children: [
      { path: 'dashboard', name: 'Dashboard', meta: { requiresAuth: true, roles: ['student'] }, component: () => import('../views/student/Dashboard.vue') },
      { path: 'points', name: 'Points', meta: { requiresAuth: true, roles: ['student'] }, component: () => import('../views/student/PointsCenter.vue') },
      { path: 'practice', name: 'Practice', meta: { requiresAuth: true, roles: ['student'] }, component: () => import('../views/student/Practice.vue') },
      { path: 'courses', name: 'Courses', component: () => import('../views/student/Courses.vue') },
      { path: 'courses/:id', name: 'CourseDetail', component: () => import('../views/student/CourseDetail.vue') },
      { path: 'courses/:id/learn/:lessonId', name: 'CourseLearn', meta: { requiresAuth: true, roles: ['student'] }, component: () => import('../views/student/CourseLearn.vue') },
      { path: 'wrong-book', name: 'WrongBook', meta: { requiresAuth: true, roles: ['student'] }, component: () => import('../views/student/WrongBook.vue') },
      { path: 'teachers/:slug', name: 'TeacherPage', component: () => import('../views/student/TeacherPage.vue') },
      { path: 'profile', name: 'Profile', meta: { requiresAuth: true, roles: ['student'] }, component: () => import('../views/student/Profile.vue') },
      { path: 'orders', name: 'Orders', meta: { requiresAuth: true, roles: ['student'] }, component: () => import('../views/student/Orders.vue') },
      { path: 'orders/:id', name: 'OrderDetail', meta: { requiresAuth: true, roles: ['student'] }, component: () => import('../views/student/OrderDetail.vue') },
    ],
  },
]
