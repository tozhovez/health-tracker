
//////<template>
//////<Line :data="data" :options="options" />
//////<HealthDashboard />
//////
//////</template>
//////
//////<script lang="ts">
//////import {
//////  Chart as ChartJS,
//////  CategoryScale,
//////  LinearScale,
//////  PointElement,
//////  LineElement,
//////  Title,
//////  Tooltip,
//////  Legend
//////} from 'chart.js'
//////import { Line } from 'vue-chartjs'
//////import * as chartConfig from './chartConfig.js'
//////
//////ChartJS.register(
//////  CategoryScale,
//////  LinearScale,
//////  PointElement,
//////  LineElement,
//////  Title,
//////  Tooltip,
//////  Legend
//////)
//////
//////export default {
//////  name: 'App',
//////  components: {
//////    Line
//////  },
//////  data() {
//////    return chartConfig
//////  }
//////}
//////
//////
//////import HealthDashboard from './components/HealthDashboard.vue';
//////
//////export default {
//////  components: {
//////    HealthDashboard,
//////  },
//////};
//////
//////
//////</script>
