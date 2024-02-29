<template>
    <div ref="lyechartmain" style="width: 100%;height: 400px"></div>
</template>

<script setup>
    import {nextTick, onBeforeUnmount, onMounted, ref} from "vue";
    // 按需引入echarts
    import echarts from "@/components/analysis/echartsInstall";

    const props = defineProps({
        myData: Array  // Define the type of the prop
    });

    // console.log("===============props")
    // console.log(props.myData)
    // console.log("===============props")

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
            top: "10%",
            data: ["小学", "初中", "高中", "中专", "大专", "本科", "硕士", "博士"],
        },
        series: [
            {
                name: "学历",
                type: "pie",
                radius: ['40%', '70%'],
                avoidLabelOverlap: false,
                itemStyle: {
                    borderRadius: 10,
                    borderColor: '#fff',
                    borderWidth: 2
                },
                center: ["50%", "60%"],
                data: props.myData,
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
    });


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