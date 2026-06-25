import { defineStore } from 'pinia'
import request from '../api/request'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: JSON.parse(localStorage.getItem('user') || 'null'),
    token: localStorage.getItem('token') || '',
  }),
  getters: {
    isLoggedIn: (s) => !!s.token,
    role: (s) => s.user?.role || 'student',
    teacherStatus: (s) => s.user?.teacher_profile?.status || null,
    isApprovedTeacher: (s) => s.user?.role === 'teacher' && s.user?.teacher_profile?.status === 'approved',
  },
  actions: {
    _persist(user, token) {
      this.user = user
      this.token = token
      localStorage.setItem('user', JSON.stringify(user))
      localStorage.setItem('token', token)
    },
    async login(account, password) {
      const res = await request.post('/auth/login', { account, password })
      this._persist(res.data.user, res.data.token)
      await this.fetchMe()
      return this.user
    },
    async register(payload) {
      const res = await request.post('/auth/register', payload)
      this._persist(res.data.user, res.data.token)
      await this.fetchMe()
      return this.user
    },
    async fetchMe() {
      if (!this.token) return null
      try {
        const res = await request.get('/auth/me')
        this.user = res.data
        localStorage.setItem('user', JSON.stringify(this.user))
        return this.user
      } catch {
        this.logout()
        return null
      }
    },
    logout() {
      this.user = null
      this.token = ''
      localStorage.removeItem('user')
      localStorage.removeItem('token')
    },
    redirectByRole(router) {
      const map = { student: '/dashboard', teacher: '/teacher', admin: '/admin' }
      router.push(map[this.role] || '/dashboard')
    },
  },
})
