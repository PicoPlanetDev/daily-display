import './assets/main.css'

import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.min.js'

import 'bootstrap-icons/font/bootstrap-icons.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

import axios from 'axios'
axios.defaults.baseURL = window.location.href.split(':5173')[0] + ":5000/api";

const app = createApp(App)

app.use(router)

app.mount('#app')
