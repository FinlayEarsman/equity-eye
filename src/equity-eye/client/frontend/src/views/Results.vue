<template>
    <div class="p-8 mx-20">
         <div>
            <span class="text-xl font-bold" >Search Results for: "{{ query }}"</span>
        </div>
        <div v-if="searchSuccess">
            <div
                v-for="(asset, i) in allAssets"
                v-bind:key="i"
                class="wrapper flex flex-col p-2 mb-4 bg-[#D9D9D9] rounded mt-2 w-3/4"
            >
                <span @click="routeAsset(asset.ticker)" class="text-xl font-bold cursor-pointer" >{{ asset.name }}</span>
                <span @click="routeAsset(asset.ticker)" class="text-l cursor-pointer" >{{ asset.summary }}</span>
            </div>
        </div>
        <div v-if="searchSuccess && allArticles.length > 0" class="flex flex-col">
            <span class="text-l font-bold mt-4" >Related articles:</span>
            <div
                class="p-3 bg-[#D9D9D9] grid grid-cols-2 max-w-fit"
            >
                <div
                    v-for="(article, i) in allArticles"
                    v-bind:key="i"
                    class="p-2 cursor-pointer"
                >
                        <article-card
                            :title="article.title"
                            :body="article.body"
                            :date="article.published"
                            :id="article.id"
                        />
                </div>
                <div
                    v-if="allArticles.length === 25 || page > 1"
                    class="flex flex-row gap-x-2 my-2 place-self-end"
                >
                    <button @click="showLast" class="outline-1 outline p-2 rounded bg-[#E6E6E6]">&lt; Last</button>
                    <button @click="showNext" class="outline-1 outline p-2 rounded bg-[#E6E6E6]">Next &gt;</button>
                </div>
            </div>
        </div>
    </div>

</template>

<script>
import axios from "axios";
import ArticleCard from "@/components/ArticleCard";
import router from "@/router";
export default {
    name: "ResultsView",
    components: {
        ArticleCard
    },
    data() {
        return {
            allArticles: [],
            allAssets: [],
            query: "",
            page: 1,
            searchSuccess: false
        }
    },
    mounted() {
        if (this.$route.query) {
            this.query = this.$route.query.asset
            this.completeSearch()
        }
    },
    methods: {
        async completeSearch() {
            await axios
                .post('search/', {'query': this.query, 'page': this.page})
                .then(response => {
                    this.allArticles = response.data.articles
                    this.allAssets = response.data.assets
                    this.searchSuccess = true
                    this.$forceUpdate();
                })
                .catch(error => {
                    console.log(error)
                })
        },
        routeAsset(ticker) {
            router.push({name: 'asset', params: {'ticker': ticker}})
        },
        showNext() {
            this.page += 1;
            this.completeSearch()
        },
        showLast() {
            if (this.page > 1) {
                this.page -= 1;
                this.completeSearch()
            }
        }
    }
}
</script>

<style scoped>
.wrapper:hover {
    box-shadow: 0 0 11px rgba(35, 35, 35, 0.2);
}
</style>