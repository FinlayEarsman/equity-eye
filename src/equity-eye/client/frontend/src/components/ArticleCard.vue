<template>
    <div
        class="wrapper flex flex-col rounded max-w-md bg-[#E6E6E6] pt-3 px-4 pb-2 cursor-pointer" @click="routeArticle(id)"
    >
        <div class="flex flex-col">
            <div id="date" class="text-xs self-end">
                {{ formattedDate }}
            </div>
            <div id="title" class="line-clamp-2">
                {{ title }}
            </div>
        </div>
        <div id="body" class="p-2 h-20 ">
            <p class=" text-xs line-clamp-4">
                <span
                    v-for="(p, i) in JSON.parse(body)"
                    v-bind:key="i"
                >
                    {{ p }}
                </span>
            </p>
        </div>
    </div>
</template>

<script>
import router from "@/router";

export default {
    name: "ArticleCard",
    props: {
        id: Number,
        title: String,
        body: String,
        date: String
    },
    computed: {
        formattedDate() {
            const options = { year: 'numeric', month: 'numeric', day: 'numeric' };
            if (this.date !== null) {
                let dateObj = new Date(this.date);
                return dateObj.toLocaleDateString('en-GB', options)
            }
            return ""
        },
    },
    methods: {
        routeArticle(id) {
            router.push({name: 'article', params: {'id': id}})
        },
    }
}
</script>

<style scoped>
.wrapper:hover {
    box-shadow: 0 0 11px rgba(33, 33, 33, .2);
}
</style>