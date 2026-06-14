import { createApp } from 'vue'
import './shared/styles/index.css'
import App from './App.vue'
import { router } from './app/router'
import { pinia } from './app/providers/pinia'

const app = createApp(App)

app.use(pinia)
app.use(router)

app.mount('#app')
