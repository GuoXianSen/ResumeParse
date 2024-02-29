<template>
    <div ref="lyechartmain" style="width: 100%;height: 400px"></div>
</template>

<script setup>
    import {nextTick, onBeforeUnmount, onMounted, ref} from "vue";
    // 按需引入echarts
    import echarts from "@/components/analysis/echartsInstall";

    let myChart = null
    const props = defineProps({
        myname: String  // Define the type of the prop
    });
    let option = {
        tooltip: {
            trigger: 'axis',
        },
        radar: [
            {
                indicator: [

                    {name: '教育背景', max: 10},
                    {name: '经验值', max: 10},
                    {name: '信息完整性', max: 10},
                    {name: '工作技能', max: 10},
                    {name: '发展潜力', max: 10},
                ],
            },
        ],
        series: [
            {
                type: 'radar',
                tooltip: {
                    trigger: 'item'
                },
                areaStyle: {},
                data: [
                    {
                        value: [10, 7, 10, 7, 8],
                        name: '求职者雷达图（满分为10分）'
                    }
                ]
            },
        ]
    };
    let lyechartmain = ref(null)
    onMounted(() => {//需要获取到element,所以是onMounted的Hook
        setTimeout(() => {
            nextTick(() => {
                myChart = echarts.init(lyechartmain.value);
                myChart.setOption(option);
            })
        }, 300)
        // myChart = echarts.init(document.getElementById("lyechartmain"));
        // // 绘制图表
        // myChart.setOption(option);
        window.onresize = function () {//自适应大小
            if (myChart) {
                myChart.resize();
            }
        };
    });
    onBeforeUnmount(() => {
        window.onresize = null;
    })

    function handleResize() {
        if (myChart) {
            myChart.resize();
        }
    }

    defineExpose({
        handleResize
    })
</script>

<style scoped>

</style>