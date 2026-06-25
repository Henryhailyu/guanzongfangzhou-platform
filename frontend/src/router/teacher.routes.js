import TeacherLayout from '../layouts/TeacherLayout.vue'

export default [
  {
    path: '/teacher',
    component: TeacherLayout,
    meta: { requiresAuth: true, roles: ['teacher'] },
    children: [
      { path: '', name: 'TeacherDashboard', component: () => import('../views/teacher/Dashboard.vue') },
      { path: 'courses', name: 'TeacherCourses', component: () => import('../views/teacher/Courses.vue') },
      { path: 'courses/:id', name: 'TeacherCourseEdit', component: () => import('../views/teacher/TeacherCourseEdit.vue') },
      { path: 'students', name: 'TeacherStudents', component: () => import('../views/teacher/Students.vue') },
      { path: 'marketing', name: 'TeacherMarketing', component: () => import('../views/teacher/Marketing.vue') },
    ],
  },
]
