import axios from 'axios'

const request = axios.create({
  baseURL: import.meta.env.VITE_API_BASE || '/api',
  timeout: 30000,
})

request.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

request.interceptors.response.use(
  (res) => {
    const data = res.data
    if (data.success === false) {
      return Promise.reject(new Error(data.error?.message || '请求失败'))
    }
    return data
  },
  (err) => Promise.reject(err)
)

export default request
