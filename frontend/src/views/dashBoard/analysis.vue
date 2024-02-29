<template>
    <div class="lycontainer">
        <el-scrollbar>
            <div>
                <ly-growcard :loading="showloading" :rows="2" v-model="growData"></ly-growcard>
            </div>
            <div class="echarts-inner">
                <ly-echartcard :loading="showloading" :rows="3" v-model="growData"></ly-echartcard>
            </div>
        </el-scrollbar>
    </div>
</template>

<script>
    import LyGrowcard from "../../components/analysis/growCard";
    import LyEchartcard from "../../components/analysis/echartCard";
    import {CvUpload} from '@/api/api'

    export default {
        name: "analysis",
        components: {LyEchartcard, LyGrowcard},
        data() {
            // benke_num =
            return {
                showloading: true,
                shuoshi: {
                    xueli: "硕士"
                },
                benke: {
                    xueli: "本科"
                },
                boshi: {
                    xueli: "博士"
                },
                dazhuan: {
                    xueli: "大专"
                },
                zhongzhuan: {
                    xueli: "中专"
                },
                xiaoxue: {
                    xueli: "小学"
                },
                chuzhong: {
                    xueli: "初中"
                },
                gaozhong: {
                    xueli: "高中"
                },
                growData: [
                    {
                        id: 1, title: "小学", nums: 1, icon: {
                            type: "WalletFilled",
                            background: "#f56c6c",
                        },
                        time: {
                            name: "1",
                            type: "danger"
                        }
                    },
                    {
                        id: 2, title: "初中", nums: 0, icon: {
                            type: "WalletFilled",
                            background: "#f56c6c",
                        },
                        time: {
                            name: "2",
                            type: "danger"
                        }
                    },
                    {
                        id: 3, title: "高中", nums: 0, icon: {
                            type: "WalletFilled",
                            background: "#f56c6c",
                        },
                        time: {
                            name: "3",
                            type: "danger"
                        }
                    },
                    {
                        id: 4, title: "中专", nums: 3, icon: {
                            type: "WalletFilled",
                            background: "#f56c6c",
                        },
                        time: {
                            name: "4",
                            type: "danger"
                        }
                    },
                    {
                        id: 5, title: "大专", nums: 4, icon: {
                            type: "WalletFilled",
                            background: "#f56c6c",
                        },
                        time: {
                            name: "5",
                            type: "danger"
                        }
                    },
                    {
                        id: 6, title: "本科", nums: 8, icon: {
                            type: "View",
                            background: "#67c23a",
                        },
                        time: {
                            name: "6",
                            type: "success"
                        }
                    },
                    {
                        id: 7, title: "硕士", nums: 5, icon: {
                            type: "GoodsFilled",
                            background: "#e6a23c",
                        },
                        time: {
                            name: "7",
                            type: "warning"
                        }
                    },
                    {
                        id: 8, title: "博士", nums: 40, icon: {
                            type: "Download",
                            background: "#409eff",
                        },
                        time: {
                            name: "8",
                            type: ""
                        }
                    },
                ],
                echartsData: []
            }
        },
        methods: {
            //获取人数数据
            async getData() {
                // console.log(this.growData[0].nums)
                const educationLevels = [this.xiaoxue, this.chuzhong, this.gaozhong, this.zhongzhuan, this.dazhuan, this.benke, this.shuoshi, this.boshi];

                for (const educationLevel of educationLevels) {
                    try {
                        const res = await CvUpload(educationLevel); // 等待异步请求完成
                        console.log(res.data)
                        this.loadingPage = false;
                        if (res.code == 2000) {
                            this.growData[educationLevels.indexOf(educationLevel)].nums = res.data.total;
                        }
                    } catch (error) {
                        console.error("Error:", error);
                        this.loadingPage = false;
                    }
                }
            },


            timeChange(val) {
                if (val) {
                    this.formInline.beginAt = dateFormats(val[0], 'yyyy-MM-dd hh:mm:ss');
                    this.formInline.endAt = dateFormats(val[1], 'yyyy-MM-dd hh:mm:ss');
                } else {
                    this.formInline.beginAt = null
                    this.formInline.endAt = null
                }
                this.search()
            },
            // 计算搜索栏的高度
            listenResize() {
                this.$nextTick(() => {
                    this.getTheTableHeight()
                })
            },
            getTheTableHeight() {
                let tabSelectHeight = this.$refs.tableSelect ? this.$refs.tableSelect.offsetHeight : 0
                tabSelectHeight = this.isFull ? tabSelectHeight - 110 : tabSelectHeight
                this.tableHeight = getTableHeight(tabSelectHeight)
            }

        },
        created() {

            this.getData()
            setTimeout(() => {
                this.showloading = false
            }, 600)
        },
        mounted() {

        }
    }
</script>
<style lang="scss" scoped>
    .lycontainer {
        width: 100%;
        height: calc(100vh - 130px); //动态计算长度值
        /*overflow-x: hidden;*/
        /*overflow-y:auto;*/
    }

    .echarts-inner {
        margin-top: 1px;
    }

    ::v-deep(.el-scrollbar__bar.is-horizontal) {
        display: none;
    }
</style>