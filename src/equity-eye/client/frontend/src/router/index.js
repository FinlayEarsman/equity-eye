import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/Dashboard.vue'
import ArticleView from '@/views/Article.vue'
import ResultsView from "@/views/Results";
import AssetView from "@/views/Asset";
import NotFound from "@/views/NotFound";

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/article/:id',
    name: 'article',
    component: ArticleView
  },
  {
    path: '/asset/:ticker',
    name: 'asset',
    component: AssetView
  },
  {
    path: '/results',
    name: 'results',
    component: ResultsView
  },
  { path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: NotFound
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router