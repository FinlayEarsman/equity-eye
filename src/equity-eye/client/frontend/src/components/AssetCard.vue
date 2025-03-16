<template>
    <div v-if="assetSearchSuccess"
         class="wrapper flex flex-col rounded max-w-md bg-[#E6E6E6] pt-3 px-4 pb-2"
         @click="routeAsset(this.ticker)"
    >
        <div class="text-l">
            <div>
                {{ name }} - {{ticker}}
            </div>
        </div>
    </div>
</template>

<script>
import axios from "axios";
import router from "@/router";

export default {
    name: "AssetCard",
    props: {
        name: String,
    },
    data() {
        return {
            assetSearchSuccess: false,
            ticker: null,
        }
    },
    mounted() {
        this.fetchAsset()
    },
    methods: {
        async fetchAsset() {
            await axios
                .get(`assets/${this.name}`)
                .then(response => {
                    if (response.data['not-found']) {
                        this.$router.push({
                            name: 'NotFound',
                        })
                    }
                    let asset = response.data.asset
                    this.ticker = asset.ticker
                    this.assetSearchSuccess = true
                })
                .catch(error => {
                    console.log(error)
                })
        },
        routeAsset(ticker) {
            router.push({name: 'asset', params: {'ticker': ticker}})
        },
    },
}
</script>

<style scoped>
.wrapper:hover {
    box-shadow: 0 0 11px rgba(33, 33, 33, .2);
}
</style>