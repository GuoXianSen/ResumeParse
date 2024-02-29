<template>
    <el-row :gutter="20">
        <el-col :span="24">
            <div class="space-inner">
                <el-tabs type="border-card" class="lycard" v-model="activeName" @tab-change="handleTabChage">
                    <el-skeleton :rows="rows" :animated="animated" :count="count" :loading="loading"
                                 style="padding: 20px;width: auto;overflow: hidden;">
                        <template #default>
                            <el-tab-pane label="简历学历分布" name="tab1">
                                <ly-pie-echart ref="lyecharts1" v-if="activeName == 'tab1'"
                                               :my-data="this.myData"></ly-pie-echart>
                            </el-tab-pane>
                            <el-tab-pane label="新版学历分布" name="tab2">
                                <gyz-new-pie-echart ref="lyecharts2" v-if="activeName == 'tab2'"></gyz-new-pie-echart>
                            </el-tab-pane>
<!--                            <el-tab-pane label="工作年限统计" name="tab3">-->
<!--                                <ly-bar-echart ref="lyecharts3" v-if="activeName == 'tab3'"></ly-bar-echart>-->
<!--                            </el-tab-pane>-->
<!--                            <el-tab-pane label="雷达图" name="tab4">-->
<!--                                <gyz-radar-echart ref="lyecharts4" v-if="activeName == 'tab4'"></gyz-radar-echart>-->
<!--                            </el-tab-pane>-->
                        </template>
                    </el-skeleton>
                </el-tabs>
            </div>
        </el-col>
    </el-row>
</template>

<script>
    import LyBarEchart from "./barEchart";
    import LyPieEchart from "./pieEchart";
    import GyzNewPieEchart from "./newPieEchart"
    import GyzRadarEchart from "./radarEchart"


    export default {
        name: "LyEchartcard",
        components: {LyPieEchart, LyBarEchart, GyzNewPieEchart, GyzRadarEchart},
        data() {
            return {
                activeName: "tab1",
                dataList: "",
                myData: [],
            }
        },
        async created() {
            this.dataList = this.modelValue;
            console.log("===============dataList");
            console.log(this.dataList);
            console.log("===============dataList");

            for (let item of this.dataList) {
                // console.log("===============item.nums");
                // console.log(item.nums);
                // console.log("===============item.nums");

                // 异步等待数据处理完成后再继续
                await this.processItem(item);
            }
        },
        props: {
            loading: {
                type: Boolean,
                default: true
            },
            count: {
                type: Number,
                default: 1,
            },
            rows: {
                type: Number,
                default: 4,
            },
            animated: {
                type: Boolean,
                default: true,
            },
            modelValue: {
                type: Array,
                default: []
            },
            chartData: {
                type: Array,
                default: []
            },
            height: {
                type: Number,
                default: 300,
            }
        },
        watch: {
            modelValue: function (nval) {
                this.dataList = nval;
            },
            dataList: function (nval) {
                this.$emit('update:modelValue', nval);
            },
        },
        methods: {
            handleTabChage(e) {
            },
            async processItem(item) {
                // 模拟异步操作，实际可能是接口请求等异步操作
                await new Promise(resolve => setTimeout(resolve, 100));

                this.myData.push({
                    value: item.nums,
                    name: item.title
                });
            }
        },
    }
</script>

<style scoped>
    .space-inner {
    }

    .lycard {
        background: var(--el-bg-color);
        box-shadow: var(--el-box-shadow-light);
        border: 1px solid var(--el-border-color-light);
    }
</style>