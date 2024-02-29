<template>
    <div ref="lyechartmain" style="width: 100%;height: 600px"></div>
</template>

<script setup>
    import {nextTick, onBeforeUnmount, onMounted, ref} from "vue";
    // 按需引入echarts
    import echarts from "@/components/analysis/echartsInstall";

    let myChart = null
    let option = {
        title: {
            text: '简历学历分布',
            left: "center"
        },
        tooltip: {
            trigger: "item",
            formatter: "{a} <br/>{b} : {c} ({d}%)",
        },
        legend: {
            top: "bottom",
            data: ["小学", "初中", "高中", "中专", "大专", "本科", "硕士", "博士"],
        },
        toolbox: {
            show: true,
            feature: {
                mark: {show: true},
                dataView: {show: true, readOnly: false},
                restore: {show: true},
                saveAsImage: {show: true}
            }
        },
        series: [
            {
                name: "学历分布",
                type: "pie",
                radius: [50, 250],
                center: ["50%", "50%"],
                roseType: 'area',
                itemStyle: {
                    borderRadius: 8
                },
                data: [
                    {value: 1, name: "小学"},
                    {value: 0, name: "初中"},
                    {value: 0, name: "高中"},
                    {value: 2, name: "中专"},
                    {value: 3, name: "大专"},
                    {value: 7, name: "本科"},
                    {value: 5, name: "硕士"},
                    {value: 2, name: "博士"},
                ],
                emphasis: {
                    itemStyle: {
                        shadowBlur: 10,
                        shadowOffsetX: 0,
                        shadowColor: "rgba(0, 0, 0, 0.5)",
                    },
                },
            },
        ],

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