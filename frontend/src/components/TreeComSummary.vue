<template>
  <v-flex>
    <v-toolbar flat>
      <v-toolbar-title>Density, Biomass and Diversity</v-toolbar-title>

      <v-spacer></v-spacer>

      <v-btn-toggle v-model="toggleChart" color="teal" group dense>
        <v-btn :value="true">
          <v-icon>mdi-chart-line</v-icon>
        </v-btn>
        <v-btn :value="false">
          <v-icon>mdi-table</v-icon>
        </v-btn>
      </v-btn-toggle>
    </v-toolbar>

    <v-card class="px-2" v-if="toggleChart" flat>
      <v-card-subtitle v-html="select.label"></v-card-subtitle>

      <line-chart
        v-if="loaded"
        :chart-data="chartData"
        :options="options"
        height="288px"
      ></line-chart>

      <v-card-actions>
        <v-btn-toggle
          v-model="select"
          color="teal"
          tile
          group
          mandatory
          dense
          @change="fillData()"
        >
          <v-btn
            v-for="(btn, index) in btn"
            :key="index"
            :value="btn"
            v-html="btn.text"
          ></v-btn>
        </v-btn-toggle>
      </v-card-actions>
    </v-card>

    <v-card v-if="!toggleChart" flat>
      <v-data-table :headers="headers" :items="data" class="elevation-0">
        <template v-slot:header.nstem="{ header }">
          <span v-html="header.text"></span>
        </template>
        <template v-slot:header.nsp="{ header }">
          <span v-html="header.text"></span>
        </template>
        <template v-slot:item.year="{ item }">
          {{ Math.round(item.year * 10) / 10 }}
        </template>
        <template v-slot:item.nstem="{ item }">
          {{ Math.round(item.nstem * 10) / 10 }}
        </template>
        <template v-slot:item.richness="{ item }">
          {{ Math.round(item.richness * 100) / 100 }}
        </template>
        <template v-slot:item.shannon="{ item }">
          {{ Math.round(item.shannon * 100) / 100 }}
        </template>
        <template v-slot:item.b="{ item }">
          {{ Math.round(item.b * 100) / 100 }}
        </template>
        <template v-slot:item.ba="{ item }">
          {{ Math.round(item.ba * 100) / 100 }}
        </template>
      </v-data-table>
    </v-card>

    <v-card-actions class="px-2">
      <v-btn color="teal" text @click="showCaption = !showCaption">
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
    options: {
      responsive: true,
      maintainAspectRatio: false,
      legend: {
        display: false,
      },
      scales: {
        xAxes: [
          {
            type: 'linear',
            ticks: {
              stepSize: 1,
            },
          },
        ],
        yAxes: [
          {
            ticks: {
              // beginAtZero: true,
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
    },

    headers: [
      {
        text: 'Year',
        value: 'year',
        label: 'Year',
        caption:
          'Census year (calendar year - 1 for plots surveyed in the early spring)',
      },
      {
        text: 'N<sub>stem</sub>',
        value: 'nstem',
        label: 'N stem',
        caption: 'Number of stems (ha<sup>&minus;1</sup>)',
      },
      {
        text: 'N<sub>species</sub>',
        value: 'nsp',
        label: 'N species',
        caption: 'Number of species',
      },
      {
        text: 'B',
        value: 'b',
        label: 'Above ground biomass',
        caption: 'Above ground biomass (Mg&nbsp;ha<sup>&minus;1</sup>)',
      },
      {
        text: 'BA',
        value: 'ba',
        label: 'BA',
        caption: 'Basal area (m<sup>2</sup>&nbsp;ha<sup>&minus;1</sup>)',
      },
      {
        text: 'Richness',
        value: 'richness',
        label: 'Richness',
        caption:
          'Expected number of species in a sample of 100 stems (rarefaction species richness)',
      },
      {
        text: 'Diversity',
        value: 'shannon',
        label: 'Diversity',
        caption: 'Shannon index',
      },
    ],

    btn: [
      {
        text: 'N',
        value: 'nstem',
        label: 'Number of Stems (ha<sup>&minus;1</sup>)',
      },
      {
        text: 'B',
        value: 'b',
        label: 'Above Ground Biomass (Mg&nbsp;ha<sup>&minus;1</sup>)',
      },
      {
        text: 'BA',
        value: 'ba',
        label: 'Basal Area (m<sup>2</sup>&nbsp;ha<sup>&minus;1</sup>)',
      },
      {
        text: 'Richness',
        value: 'richness',
        label: 'Rarefaction Species Richness (n = 100 stems)',
      },
      {
        text: 'Diversity',
        value: 'shannon',
        label: 'Shannon Index',
      },
    ],

    select: {
      text: 'N',
      value: 'nstem',
      label: 'Number of Stems (ha<sup>&minus;1</sup>)',
    },
  }),

  mounted() {
    this.fillData()
  },

  watch: {
    data() {
      this.fillData()
    },
  },

  methods: {
    fillData() {
      this.chartData = {
        labels: this.data.map((o) => Math.round(o.year * 10) / 10),
        datasets: [
          {
            label: this.select.label,
            backgroundColor: 'rgba(103, 58, 183, 0.2)',
            borderColor: 'rgba(103, 58, 183, 0.8)',
            pointBorderColor: 'rgba(103, 58, 183, 0.8)',
            pointBackgroundColor: 'rgba(103, 58, 183, 0.4)',
            data: this.data.map((o) => {
              return {
                x: Math.round(o.year * 10) / 10,
                y: o[this.select.value],
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
