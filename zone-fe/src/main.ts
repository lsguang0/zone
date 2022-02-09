// 主入口
import { createApp } from 'vue'

import App from './App.vue'
import router from './router'
import store from './store'
import Axios from 'axios'
import 'element-plus/es/components/message/style/css'
import '@/assets/css/elementPlus.scss'
// 产生实例
const app = createApp(App)
app.config.globalProperties.$axios = Axios;
app.use(store).use(router).mount('#app')