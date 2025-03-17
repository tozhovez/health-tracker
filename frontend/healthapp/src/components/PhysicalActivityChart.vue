<template>
    <div v-if="activityData.length">
      <h2>Физическая активность</h2>
      <Line :data="chartData" :options="chartOptions" />
    </div>
  </template>
  
  <script>
  import { fetchPhysicalActivityData } from "../services/PhysicalActivityService.js";
  import { Line } from "vue-chartjs";
  import {
    ArcElement,
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
  } from "chart.js";
  
  ChartJS.register(  ArcElement, 
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend);
  
  export default {
    components: {
        Line
        
    },
    props: {
      userUuid: String,
    },
    data() {
      return {
        activityData: [],
      };
    },
    computed: {
      chartData() {
        return {
          labels: this.activityData.map(a => new Date(a.start_time).toLocaleDateString()),
          datasets: [
            {
              label: "Шаги",
              data: this.activityData.map(a => a.steps),
              borderColor: "blue",
              fill: false,
            },
            {
              label: "Сожженные калории",
              data: this.activityData.map(a => a.calories_burned),
              borderColor: "red",
              fill: false,
            },
            {
              label: "Activity duration",
              data: this.activityData.map(a => a.activity_duration),
              borderColor: "green",
              fill: false,
            },
            {
              label: "heart rate",
              data: this.activityData.map(a => a.heart_rate_avg),
              borderColor: "#7acbf9",
              fill: false,
            }
          ],
        };
      },
      chartOptions() {
        return {
          responsive: true,
          plugins: {
            legend: {
              position: "top",
            },
          },
        };
      },
    },
    watch: {
      async userUuid(newUuid) {
        if (newUuid) {
          this.activityData = await fetchPhysicalActivityData(newUuid);
        }
      },
    },
  };
  </script>
  