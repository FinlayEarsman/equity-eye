<template>
    <div id="app" class="h-full flex flex-col">
        <nav class="p-4 bg-[#B5C2C7] flex flex-row items-center justify-between h-14">
            <div>
                <router-link to="/" class="px-7">Home</router-link>
            </div>
            <div
                v-if="$route.name !== 'home' && $route.name !== 'results'"
                class="w-1/4 flex flex-row items-center gap-x-4"
            >
                <div class="w-full">
                    <multiselect
                        v-model="chosenAsset"
                        :options="allAssets"
                        placeholder="Search for an asset..."
                        label="name"
                        :select-label="''"
                        track-by="name"
                        :resetAfter="true"
                        @select="submit"
                        class="w-full rounded-lg drop-shadow-lg border-black border-solid border text-sm text-slate-600 h-11"
                    />
                </div>
                <div class="grid grid-cols-2 items-center">
                    <img
                        v-bind:src="'http://localhost:8000/static/images/eye_logo.svg'"
                        class="scale-50"
                    />
                    <span class="text-xl font-semibold">
                        Equity Eye
                    </span>
                </div>
            </div>
        </nav>
        <div id="content">
          <router-view/>
        </div>

<!--        <footer-->
<!--            class="fixed bottom-0 left-0 border-t-2 border-grey-400 p-4 w-full"-->
<!--        >-->
<!--        </footer>-->
    </div>
</template>

<script>
import Multiselect from "vue-multiselect";
import router from "@/router";
import axios from "axios";
export default {
    components: { Multiselect },
    data() {
        return {
            allAssets: [],
            chosenAsset: null
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
            router.push({name: 'results', query: {'asset': this.chosenAsset.name}})
        }
    }
}
</script>

<style>
/*.multiselect__tags {*/
/*    font-size: 14px;*/
/*}*/

/*.multiselect__option {*/
/*    font-size: 14px;*/
/*}*/

/*.multiselect {*/
/*    width: 12rem;*/
/*}*/

#app {
    font-family: 'Roboto Serif',sans-serif;
    background-color: #F8F8F8;
    min-height: 100%;
    min-height: 100vh;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}
nav a {
    font-weight: bold;
    font-style: italic;
    color: #000000;
}
nav a.router-link-exact-active {
  text-decoration: underline;
}
</style>