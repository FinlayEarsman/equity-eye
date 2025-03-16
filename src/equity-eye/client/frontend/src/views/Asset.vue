<template>
    <div class="flex flex-col gap-y-2 m-10 p-6 bg-[#D9D9D9]">
        <div
            class="text-4xl p-4 bg-[#E6E6E6] flex gap-x-8 w-fit"
        >
            <span>{{ name }}</span>
            <span>({{ ticker }})</span>
        </div>
        <div
            class="p-4 bg-[#E6E6E6] w-fit max-w-[60%]"
        >
            <span>{{ summary }}</span>
        </div>
        <div class="w-full">
            <chart
              :options="chartOptions"
              :constructor-type="'stockChart'"
            />
            <div v-if="!fetchedRange" class="font-bold pt-1">
                <span>Select a window of time to view articles from</span>
            </div>
        </div>
        <div v-if="allRelatedArticles.length > 0" class="flex flex-row gap-x-6">
            <div
                v-if="fetchedAll"
                class="p-4"
            >
                <span class="font-bold">Most recent articles:</span>
                <div class="overflow-auto max-h-screen pr-1 flex flex-col gap-y-1">
                    <div
                        v-for="(article, i) in allRelatedArticles"
                        v-bind:key="i"
                    >
                        <article-card
                            :title="article.title"
                            :body="article.body"
                            :date="article.published"
                            :id="article.id"
                        />
                    </div>
                </div>
            </div>
            <div
                v-if="fetchedRange"
                class="p-4"
            >
                <span class="font-bold">Related articles from {{ window[0] }} to {{ window[1] }}:</span>
                <div v-if="dateRangeArticles.length > 0" class="flex flex-col gap-y-1 overflow-auto max-h-screen pr-1">
                    <div
                        v-for="(article, i) in dateRangeArticles"
                        v-bind:key="i"
                    >
                        <article-card
                            :title="article.title"
                            :body="article.body"
                            :date="article.published"
                            :id="article.id"
                        />
                    </div>
                </div>
                <div
                    v-else
                    class="pt-3"
                >
                    <span>No articles found in this period D:</span>
                </div>
            </div>
        </div>
        <div
            v-else
            class="pt-3"
        >
            <span>No articles found for this asset.</span>
        </div>
    </div>
</template>

<script>
import axios from "axios";
import { Chart } from 'highcharts-vue'
import articleCard from "@/components/ArticleCard.vue";

export default {
    name: "AssetView",
    components: {
        chart: Chart,
        articleCard
    },
    data() {
        let vm = this;
        return {
            ticker: "",
            name: "",
            summary: "",
            aggregates: [],
            window: [],
            fetchedAll: false,
            fetchedRange: false,
            allRelatedArticles: [],
            dateRangeArticles: [],
            assetSearchSuccess: false,
            aggregatesSearchSuccess: false,
            chartOptions: {
                chart: {
                    events: {
                        load: (function(self) {
                            return function () {
                                self.chart = this;
                            };
                        })(this)
                    }
                },
                xAxis: {
                    events: {
                        setExtremes: function(e) {
                            vm.changeDetected(e);
                        },
                    }
                },
                rangeSelector: {
                    selected: 0
                },

                title: {
                    text: ''
                },
                series: [{
                    type: 'candlestick',
                    name: '',
                    data: this.data,
                    dataGrouping: {
                        units: [
                            [
                                'week', // unit name
                                [1] // allowed multiples
                            ], [
                                'month',
                                [1, 2, 3, 4, 6]
                            ]
                        ]
                    }
                }]
            }
        }
    },
    mounted() {
        this.ticker = this.$route.params.ticker
        this.fetchAsset()
        this.fetchAggregates()

    },
    methods: {
        async fetchAsset() {
            await axios
                .get(`assets/${this.ticker}`)
                .then(response => {
                    if (response.data['not-found']) {
                        this.$router.push({
                          name: 'NotFound',
                        })
                    }
                    let asset = response.data.asset
                    this.name = asset.name
                    this.summary = asset.summary
                    this.assetSearchSuccess = true
                })
                .catch(error => {
                    console.log(error)
                })
        },
        async fetchAggregates() {
            await axios
                .get(`prices/${this.ticker}`)
                .then(response => {
                    if (response.data['not-found']) {
                        return
                    }
                    let aggregates = response.data.aggregates
                    let arr = aggregates.map(agg => ([
                        new Date(agg['time']).getTime(),
                        parseFloat(agg['open']),
                        parseFloat(agg['high']),
                        parseFloat(agg['low']),
                        parseFloat(agg['close'])
                    ]))
                    this.aggregates = arr
                    this.chartOptions.series[0].data = arr;
                    this.chartOptions.series[0].name = `${this.ticker} Price`;
                    this.chartOptions.title.text = `${this.ticker} Stock Price Chart`;

                    this.aggregatesSearchSuccess = true
                })
                .catch(error => {
                    console.log(error)
                })
        },
        changeDetected(e) {
            if (e.trigger === "navigator" && e.DOMEvent.type !== "mouseup") {
                return
            }
            let vals = this.chart.xAxis[0].getExtremes()
            let min = vals.min
            let max = vals.max
            if (isNaN(min)) {
                min = 0
            } else {
                this.window[0] = new Date(min).toISOString().substring(0,10);
            }
            if (isNaN(max)) {
                max = 0
            } else {
                this.window[1] = new Date(max).toISOString().substring(0,10);
            }
            console.log(min, max)
            this.fetchRelatedArticles(Math.floor(parseInt(min)/1000), Math.floor(parseInt(max) / 1000))
        },
        async fetchRelatedArticles(min, max) {
            await axios
                .get(`articles/${min}-${max}-${this.ticker}`)
                .then(response => {
                    if (response.data['invalid-request']) {
                        return
                    }
                    if (min === 0 || max === 0){
                        this.allRelatedArticles = response.data.articles;
                        this.fetchedAll = true;
                    } else {
                        this.dateRangeArticles = response.data.articles;
                        this.fetchedRange = true;
                    }

                    console.log(response.data)
                })
                .catch(error => {
                    console.log(error)
                })
        }
    }
}
</script>

<style scoped>

</style>