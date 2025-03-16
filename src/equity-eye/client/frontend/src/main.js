import { createApp } from 'vue'
import '../index.css'
import App from './App.vue'
import router from './router'
import axios from 'axios'

import Highcharts from "highcharts"
import Stock from "highcharts/modules/stock";
import HighchartsVue from 'highcharts-vue'

Stock(Highcharts)

axios.defaults.baseURL = "http://localhost:8000"

// for testing the cluster
//axios.defaults.baseURL = "http://django-l422finlayproject.ida.dcs.gla.ac.uk"

createApp(App).use(router, axios, (HighchartsVue, {tagName: 'charts'})).mount('#app')
