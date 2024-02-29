<template>
    <div ref="lyechartmain" style="width: 100%;height: 280px"></div>
</template>

<script setup>
    import {onMounted, nextTick, watch, onUnmounted, onBeforeUnmount, ref} from "vue";
    // import * as echarts from 'echarts'
    // 按需引入echarts
    import echarts from "@/components/analysis/echartsInstall";

    const props = defineProps({
        postbarchart: Array  // Define the type of the prop
    });
    console.log("1111111111111111111111111")
    console.log(props.postbarchart)
    console.log("1111111111111111111111111")
    let myChart = null

    let option = {
        xAxis: {

            type: 'category',
            data: ['市场营销', '产品运营', '设计师', '财务', '项目主管', '开发工程师', '文员', '电商运营', '人力资源管理', '风控专员'],
            axisLabel: {
                rotate: 45, // 设置标签旋转角度
                overflow: 'truncate' // 如果标签过长，截断显示
            }
        },
        yAxis: {
            type: 'value',
            min: 0,  // 设置纵轴的最小值
            max: 1   // 设置纵轴的最大值
        },
        tooltip: {
            trigger: 'axis', // 触发类型为坐标轴触发
            axisPointer: {
                // 坐标轴指示器配置项
                type: 'shadow' // 阴影指示器，显示在轴的反方向
            }
        },
        series: [
            {
                // data: [0.999420166015625, 0.28789597749710083, 0.02924545854330063, 0.2536962926387787, 0.281377911567688, 0.22694765031337738, 0.2784091830253601, 0.31068167090415955, 0.26311373710632324, 0.29395151138305664],
                data: props.postbarchart,
                type: 'bar',
                showBackground: true,
                backgroundStyle: {
                    color: 'rgba(180, 180, 180, 0.2)'
                }
            }
        ]
    };

    let lyechartmain = ref(null)

    onMounted(async () => {//需要获取到element,所以是onMounted的Hook

        setTimeout(() => {
            nextTick(() => {
                myChart = echarts.init(lyechartmain.value);
                myChart.setOption(option);
            })
        }, 300)

        window.onresize = function () {//自适应大小
            myChart.resize();
        };

    });
    onBeforeUnmount(() => {
        window.onresize = null;
    })
</script>

<style scoped>

</style>