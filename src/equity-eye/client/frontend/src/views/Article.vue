<template>
    <div v-if="article" class="flex flex-row">
        <div class="mx-24 my-12 py-10 px-20 flex flex-col gap-y-6 bg-[#D9D9D9] items-center">
            <div class="p-4 flex flex-col bg-[#E6E6E6] w-fit">
                <span class="text-l">{{ formattedDate }}</span>
                <a
                    :href="article.url"
                    target="_blank" rel="noopener noreferrer"
                ><span class="text-4xl">{{ article.title }}</span></a>
                <a
                    :href="article.url"
                    target="_blank" rel="noopener noreferrer"
                ><span class="pt-2">{{ article.url }}</span></a>
            </div>
            <div class="flex flex-row w-full justify-between">
                <div class="bg-[#E6E6E6] max-w-3xl ml-32">
                    <div class="py-6 px-32 ">
                        <p
                            v-for="(p, i) in JSON.parse(article.body)"
                            v-bind:key="i"
                            class="my-2"
                        >
                            {{ p }}
                        </p>
                    </div>
                </div>
                <div
                    class="flex flex-col mt-10 ml-6 p-4 gap-y-2 border border-black rounded h-fit"
                >
                    <span class="text-l font-bold">Related assets:</span>
                    <asset-card
                        v-for="(asset, i) in article.assets" v-bind:key="i"
                        :name="asset"
                        :ticker="''"
                        class="cursor-pointer"
                    />
                </div>
            </div>
        </div>
    </div>
</template>
<script>

import axios from "axios";
import AssetCard from "@/components/AssetCard.vue";

export default {
    name: 'ArticleView',
    components: {
        AssetCard
    },
    data() {
        return {
            article: null
        }
    },
    mounted() {
        this.fetchArticle()
    },
    computed: {
        formattedDate() {
            const options = {weekday: 'long', year: 'numeric', month: 'long', day: 'numeric'};
            let date = new Date(this.article.published);
            return date.toLocaleDateString('en-GB', options)
        }
    },
    methods: {
        async fetchArticle() {
            await axios
                .get(`articles/${this.$route.params.id}`)
                .then(response => {
                    if (response.data['not-found']) {
                        this.$router.push({
                            name: 'NotFound',
                        })
                    }
                    this.article = response.data.article
                })
                .catch(error => {
                    console.log(error)
                })
        },
    }
}
</script>

<style>

</style>