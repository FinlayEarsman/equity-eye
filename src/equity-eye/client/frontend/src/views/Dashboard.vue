<template>
<div class="flex flex-col items-center pt-40">
    <div class="flex flex-row items-center gap-x-6">
        <div>
            <img v-bind:src="'http://localhost:8000/static/images/eye_logo.svg'" />
        </div>
        <span class="text-5xl font-semibold">
            Equity Eye
        </span>
    </div>
    <div class="w-1/4 p-4">
        <multiselect
            v-model="asset"
            :options="allAssets"
            placeholder="Search for an asset..."
            label="name"
            track-by="name"
            class="w-full rounded-lg drop-shadow-lg border-black border-solid border text-sm"
            @select="submit"
            :select-label="''"
        />
    </div>
</div>
</template>

<script>
import Multiselect from "vue-multiselect";
import axios from "axios";
import router from "@/router";

export default {
    name: 'DashboardView',
    components: {
        'multiselect': Multiselect
    },
    data() {
        return {
            allAssets: [],
            asset: null,
        }
    },
    mounted() {
        this.fetchAssets();
    },
    methods: {
        async fetchAssets() {
            await axios
                .get('assets/',)
                .then(response => {
                    this.allAssets = response.data.assets
                })
                .catch(error => {
                    console.log(error)
                })
        },
        submit() {
            router.push({name: 'results', query: {'asset': this.asset.name}})
        }
    }
}
</script>

<style src="vue-multiselect/dist/vue-multiselect.css"></style>
<style scoped>

</style>
