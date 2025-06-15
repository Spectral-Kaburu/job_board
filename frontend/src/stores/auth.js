import { defineStore } from 'pinia'
import axios from 'axios'

const API_BASE = 'http://127.0.0.1:8000/api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    accessToken: localStorage.getItem('access') || null,
    refreshToken: localStorage.getItem('refresh') || null,
  }),

  actions: {
    async login(email, password) {
      try {
        const response = await axios.post(`${API_BASE}/token/`, {
          email,
          password,
        })

        this.accessToken = response.data.access
        this.refreshToken = response.data.refresh
        localStorage.setItem('access', this.accessToken)
        localStorage.setItem('refresh', this.refreshToken)

        await this.fetchUser() // Optional: auto-fetch user profile
        return true
      } catch (error) {
        console.error('Login failed:', error)
        return false
      }
    },

    async fetchUser() {
      try {
        const response = await axios.get(`${API_BASE}/user/`, {
          headers: {
            Authorization: `Bearer ${this.accessToken}`,
          },
        })
        this.user = response.data
      } catch (error) {
        console.error('Fetching user failed:', error)
      }
    },

    logout() {
      this.user = null
      this.accessToken = null
      this.refreshToken = null
      localStorage.removeItem('access')
      localStorage.removeItem('refresh')
    },
  },
})
