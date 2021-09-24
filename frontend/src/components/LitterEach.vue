<template>
  <v-flex>
    <v-toolbar flat>
      <v-toolbar-title>Seasonal Variation in Litterfall</v-toolbar-title>

      <v-spacer></v-spacer>

      <v-btn-toggle v-model="toggleChart" color="orange" group dense>
        <v-btn :value="true">
          <v-icon>mdi-chart-line</v-icon>
        </v-btn>
        <v-btn :value="false">
          <v-icon>mdi-table</v-icon>
        </v-btn>
      </v-btn-toggle>
    </v-toolbar>

    <v-card class="px-2" v-if="toggleChart" flat>
      <v-card-subtitle v-html="subtitle"></v-card-subtitle>

      <line-chart
        v-if="loaded"
        :chart-data="chartData"
        :options="options"
        height="288px"
      ></line-chart>
    </v-card>

    <v-card v-if="!toggleChart" flat>
      <v-data-table
        :headers="headers"
        :items="modifiedData"
        class="elevation-0"
      >
        <template v-slot:item.wdry_all="{ item }">
          {{ Math.round(item.wdry_all * 100000) / 100000 }}
        </template>
        <template v-slot:item.wdry_leaf="{ item }">
          {{ Math.round(item.wdry_leaf * 100000) / 100000 }}
        </template>
        <template v-slot:item.wdry_branch="{ item }">
          {{ Math.round(item.wdry_branch * 100000) / 100000 }}
        </template>
        <template v-slot:item.wdry_rep="{ item }">
          {{ Math.round(item.wdry_rep * 100000) / 100000 }}
        </template>
      </v-data-table>
    </v-card>

    <v-card-actions class="px-2">
      <v-btn color="deep-orange" text @click="showCaption = !showCaption">
        Show Caption
      </v-btn>

      <v-spacer></v-spacer>

      <v-btn icon @click="showCaption = !showCaption">
        <v-icon>
          {{ showCaption ? 'mdi-chevron-up' : 'mdi-chevron-down' }}
        </v-icon>
      </v-btn>
    </v-card-actions>

    <v-list class="px-2" v-show="showCaption" dense>
      <v-divider></v-divider>
      <template v-for="(item, index) in headers">
        <v-list-item :key="index">
          <v-list-item-content>
            <v-list-item-subtitle
              v-html="item.text + ' &mdash; ' + item.caption"
            ></v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
      </template>
    </v-list>
  </v-flex>
</template>

<script>
import LineChart from './LineChart.js'

export default {
  components: {
    LineChart,
  },

  props: ['data'],

  data: () => ({
    toggleChart: true,
    showCaption: false,
    loaded: false,
    chartData: null,
    subtitle:
      'Dry mass (Mg&nbsp;ha<sup>&minus;1</sup>&nbsp;day<sup>&minus;1</sup>)',
    options: {
      responsive: true,
      maintainAspectRatio: false,
      legend: {
        position: 'top',
      },
      scales: {
        xAxes: [
          {
            type: 'time',
            gridLines: {
              zeroLineColor: 'rgba(0, 0, 0, 0.1)',
            },
          },
        ],
        yAxes: [
          {
            ticks: {
              beginAtZero: true,
            },
          },
        ],
      },
      tooltips: {
        callbacks: {
          label: function (tooltipItem) {
            return tooltipItem.yLabel
          },
        },
      },
      plugins: {
        colorschemes: {
          scheme: 'brewer.DarkTwo4',
        },
      },
    },

    headers: [
      {
        text: 'Year',
        value: 'year',
        label: 'Year',
        caption: 'Calender year',
      },
      {
        text: 'Start date',
        value: 't1',
        label: 'Start date of the trap installation period',
        caption: 'Start date of the trap installation period',
      },
      {
        text: 'End Date',
        value: 't2',
        label: 'End date of the trap installation period',
        caption: 'End date of the trap installation period',
      },
      {
        text: 'Leaves',
        value: 'wdry_leaf',
        label: 'Daily litterfall dry mass of leaves',
        caption:
          'Daily litterfall dry mass of leaves (Mg&nbsp;ha<sup>&minus;1</sup>&nbsp;day<sup>&minus;1</sup>)',
      },
      {
        text: 'Branches',
        value: 'wdry_branch',
        label: 'Daily litterfall dry mass of branches',
        caption:
          'Daily litterfall dry mass of branches (Mg&nbsp;ha<sup>&minus;1</sup>&nbsp;day<sup>&minus;1</sup>)',
      },
      {
        text: 'Reproductive parts',
        value: 'wdry_rep',
        label: 'Daily litterfall dry mass of reproductive parts',
        caption:
          'Daily litterfall dry mass of reproductive parts (flowers, fruits, seeds, etc.) (Mg&nbsp;ha<sup>&minus;1</sup>&nbsp;day<sup>&minus;1</sup>)',
      },
      {
        text: 'Total',
        value: 'wdry_all',
        label: 'Daily total litterfall dry mass',
        caption:
          'Daily total litterfall dry mass (Mg&nbsp;ha<sup>&minus;1</sup>&nbsp;day<sup>&minus;1</sup>)',
      },
    ],
  }),

  mounted() {
    this.fillData()
  },

  computed: {
    modifiedData() {
      return this.data.map((e) => {
        return {
          year: e.year,
          t1: e.t1,
          t2: e.t2,
          wdry_leaf: e.wdry_leaf / e.inst_period,
          wdry_branch: e.wdry_branch / e.inst_period,
          wdry_rep: e.wdry_rep / e.inst_period,
          wdry_all: e.wdry_all / e.inst_period,
        }
      })
    },
  },

  watch: {
    data() {
      this.fillData()
    },
  },

  methods: {
    fillData() {
      this.chartData = {
        datasets: [
          {
            label: 'Leaves',
            fill: false,
            steppedLine: 'after',
            data: this.modifiedData.map((e) => {
              return {
                x: e.t2,
                y: e.wdry_leaf,
              }
            }),
          },
          {
            label: 'Branches',
            fill: false,
            steppedLine: 'after',
            data: this.modifiedData.map((e) => {
              return {
                x: e.t2,
                y: e.wdry_branch,
              }
            }),
          },
          {
            label: 'Reproductive parts',
            fill: false,
            steppedLine: 'after',
            data: this.modifiedData.map((e) => {
              return {
                x: e.t2,
                y: e.wdry_rep,
              }
            }),
          },
          {
            label: 'Total',
            fill: false,
            steppedLine: 'after',
            data: this.modifiedData.map((e) => {
              return {
                x: e.t2,
                y: e.wdry_all,
              }
            }),
          },
        ],
      }
      this.loaded = true
    },
  },
}
</script>
