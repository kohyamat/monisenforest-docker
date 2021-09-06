<template>
  <v-row align="center">
    <v-col cols="6">
      <div class="text-h4 mb-3 grey--text text--darken-3">
        Litterfall Data Summary
      </div>
    </v-col>

    <v-col cols="6">
      <v-select
        v-model="selectPlot"
        color="deep-purple"
        :items="plots"
        :item-text="text"
        :hint="`${selectPlot.name_jp}`"
        label="Select Forest Plot"
        item-value="id"
        single-line
        persistent-hint
        return-object
        @change="readPlotData"
      ></v-select>
    </v-col>

    <v-col cols="12">
      <v-card>
        <v-toolbar flat>
          <v-toolbar-title>Annual Variation in Litterfall</v-toolbar-title>

          <v-spacer></v-spacer>

          <v-btn-toggle
            v-model="toggleChart1"
            color="deep-purple accent-3"
            mandatory
            dense
          >
            <v-btn :value="true">
              <v-icon>mdi-chart-line</v-icon>
            </v-btn>
            <v-btn :value="false">
              <v-icon>mdi-table</v-icon>
            </v-btn>
          </v-btn-toggle>
        </v-toolbar>

        <v-card class="px-2" v-if="toggleChart1" flat>
          <v-card-subtitle v-html="subtitle1"></v-card-subtitle>

          <line-chart
            v-if="loaded1"
            :chart-data="chartData1"
            :options="options1"
            height="288px"
          ></line-chart>
        </v-card>

        <v-card v-if="!toggleChart1" flat>
          <v-data-table
            :headers="headers1"
            :items="litterAnnual"
            class="elevation-0"
          >
            <template v-slot:item.wdry_all="{ item }">
              {{ Math.round(item.wdry_all * 1000) / 1000 }}
            </template>
            <template v-slot:item.wdry_leaf="{ item }">
              {{ Math.round(item.wdry_leaf * 1000) / 1000 }}
            </template>
            <template v-slot:item.wdry_branch="{ item }">
              {{ Math.round(item.wdry_branch * 1000) / 1000 }}
            </template>
            <template v-slot:item.wdry_rep="{ item }">
              {{ Math.round(item.wdry_rep * 1000) / 1000 }}
            </template>
          </v-data-table>
        </v-card>

        <v-card-actions class="px-2">
          <v-btn color="deep-purple" text @click="showCaption1 = !showCaption1">
            Show Caption
          </v-btn>

          <v-spacer></v-spacer>

          <v-btn icon @click="showCaption1 = !showCaption1">
            <v-icon>{{
              showCaption ? "mdi-chevron-up" : "mdi-chevron-down"
            }}</v-icon>
          </v-btn>
        </v-card-actions>

        <v-expand-transition>
          <v-list class="px-2" v-show="showCaption1" dense>
            <v-divider></v-divider>
            <template v-for="(item, index) in headers1">
              <v-list-item :key="index">
                <v-list-item-content>
                  <v-list-item-subtitle
                    v-html="item.text + ' &mdash; ' + item.caption"
                  ></v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
            </template>
          </v-list>
        </v-expand-transition>
      </v-card>
    </v-col>

    <v-col cols="12">
      <v-card>
        <v-toolbar flat>
          <v-toolbar-title>Seasonal Variation in Litterfall</v-toolbar-title>

          <v-spacer></v-spacer>

          <v-btn-toggle
            v-model="toggleChart2"
            color="deep-purple accent-3"
            mandatory
            dense
          >
            <v-btn :value="true">
              <v-icon>mdi-chart-line</v-icon>
            </v-btn>
            <v-btn :value="false">
              <v-icon>mdi-table</v-icon>
            </v-btn>
          </v-btn-toggle>
        </v-toolbar>

        <v-card class="px-2" v-if="toggleChart2" flat>
          <v-card-subtitle v-html="subtitle2"></v-card-subtitle>

          <line-chart
            v-if="loaded2"
            :chart-data="chartData2"
            :options="options2"
            height="288px"
          ></line-chart>
        </v-card>

        <v-card v-if="!toggleChart2" flat>
          <v-data-table
            :headers="headers2"
            :items="litterEach"
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
          <v-btn color="deep-purple" text @click="showCaption2 = !showCaption2">
            Show Caption
          </v-btn>

          <v-spacer></v-spacer>

          <v-btn icon @click="showCaption2 = !showCaption2">
            <v-icon>{{
              showCaption ? "mdi-chevron-up" : "mdi-chevron-down"
            }}</v-icon>
          </v-btn>
        </v-card-actions>

        <v-expand-transition>
          <v-list class="px-2" v-show="showCaption2" dense>
            <v-divider></v-divider>
            <template v-for="(item, index) in headers2">
              <v-list-item :key="index">
                <v-list-item-content>
                  <v-list-item-subtitle
                    v-html="item.text + ' &mdash; ' + item.caption"
                  ></v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
            </template>
          </v-list>
        </v-expand-transition>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
import LineChart from "../components/LineChart.js";
import axios from "axios";

const BASE_URL = "http://localhost:8000/api";

export default {
  components: {
    LineChart,
  },

  data() {
    return {
      plots: [{ id: "", pid: "", name: "", name_jp: "", text: "No Data" }],
      selectPlot: null,

      // Chart1: Litter annual
      subtitle1:
        "Litterfall dry mass (Mg&nbsp;ha<sup>&minus;1</sup>&nbsp;year<sup>&minus;1</sup>)",
      litterAnnual: [],
      chartData1: null,
      options1: {
        responsive: true,
        maintainAspectRatio: false,
        legend: {
          position: "top",
        },
        scales: {
          xAxes: [
            {
              type: "linear",
              ticks: {
                stepSize: 1,
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
              return tooltipItem.yLabel;
            },
          },
        },
        plugins: {
          colorschemes: {
            scheme: "brewer.DarkTwo4",
          },
        },
      },
      loaded1: false,
      toggleChart1: true,
      showCaption1: false,

      headers1: [
        {
          text: "Year",
          value: "year",
          label: "Year",
          caption: "Calender year",
        },
        {
          text: "Start date",
          value: "t1",
          label: "Start date of the trap installation period",
          caption: "Start date of the trap installation period",
        },
        {
          text: "End Date",
          value: "t2",
          label: "End date of the trap installation period",
          caption: "End date of the trap installation period",
        },
        {
          text: "Leaves",
          value: "wdry_leaf",
          label: "Annual litterfall dry mass of leaves",
          caption:
            "Annual litterfall dry mass of leaves (Mg&nbsp;ha<sup>&minus;1</sup>&nbsp;year<sup>&minus;1</sup>)",
        },
        {
          text: "Branches",
          value: "wdry_branch",
          label: "Annual litterfall dry mass of branches",
          caption:
            "Annual litterfall dry mass of branches (Mg&nbsp;ha<sup>&minus;1</sup>&nbsp;year<sup>&minus;1</sup>)",
        },
        {
          text: "Reproductive parts",
          value: "wdry_rep",
          label: "Annual litterfall dry mass of reproductive parts",
          caption:
            "Annual litterfall dry mass of reproductive parts (flowers, fruits, seeds, etc.) (Mg&nbsp;ha<sup>&minus;1</sup>&nbsp;year<sup>&minus;1</sup>)",
        },
        {
          text: "Total",
          value: "wdry_all",
          label: "Annual total litterfall dry mass",
          caption:
            "Annual total litterfall dry mass (Mg&nbsp;ha<sup>&minus;1</sup>&nbsp;year<sup>&minus;1</sup>)",
        },
      ],

      // Chart2: Litter each sampling
      subtitle2:
        "Litterfall dry mass (Mg&nbsp;ha<sup>&minus;1</sup>&nbsp;day<sup>&minus;1</sup>)",
      litterEach: [],
      chartData2: null,
      options2: {
        responsive: true,
        maintainAspectRatio: false,
        legend: {
          position: "top",
        },
        scales: {
          xAxes: [
            {
              type: "time",
              gridLines: {
                zeroLineColor: "rgba(0, 0, 0, 0.1)",
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
              return tooltipItem.yLabel;
            },
          },
        },
        plugins: {
          colorschemes: {
            scheme: "brewer.DarkTwo4",
          },
        },
      },
      loaded2: false,
      toggleChart2: true,
      showCaption2: false,
      headers2: [
        {
          text: "Year",
          value: "year",
          label: "Year",
          caption: "Calender year",
        },
        {
          text: "Start date",
          value: "t1",
          label: "Start date of the trap installation period",
          caption: "Start date of the trap installation period",
        },
        {
          text: "End Date",
          value: "t2",
          label: "End date of the trap installation period",
          caption: "End date of the trap installation period",
        },
        {
          text: "Leaves",
          value: "wdry_leaf",
          label: "Daily litterfall dry mass of leaves",
          caption:
            "Daily litterfall dry mass of leaves (Mg&nbsp;ha<sup>&minus;1</sup>&nbsp;day<sup>&minus;1</sup>)",
        },
        {
          text: "Branches",
          value: "wdry_branch",
          label: "Daily litterfall dry mass of branches",
          caption:
            "Daily litterfall dry mass of branches (Mg&nbsp;ha<sup>&minus;1</sup>&nbsp;day<sup>&minus;1</sup>)",
        },
        {
          text: "Reproductive parts",
          value: "wdry_rep",
          label: "Daily litterfall dry mass of reproductive parts",
          caption:
            "Daily litterfall dry mass of reproductive parts (flowers, fruits, seeds, etc.) (Mg&nbsp;ha<sup>&minus;1</sup>&nbsp;day<sup>&minus;1</sup>)",
        },
        {
          text: "Total",
          value: "wdry_all",
          label: "Daily total litterfall dry mass",
          caption:
            "Daily total litterfall dry mass (Mg&nbsp;ha<sup>&minus;1</sup>&nbsp;day<sup>&minus;1</sup>)",
        },
      ],
    };
  },

  watch: {
    litterAnnual() {
      this.fillData1();
    },
    litterEach() {
      this.fillData2();
    },
  },

  mounted() {
    this.selectPlot = this.plots[0];
    this.readPlots();
  },

  methods: {
    readPlots() {
      axios
        .get(BASE_URL + "/plots/?skip=0&dtype=litter&no_load=true")
        .then((response) => {
          if (response.data.length > 0) {
            this.plots = response.data.map((o) => {
              return {
                id: o.id,
                pid: o.pid,
                name_jp: o.name_jp,
                text: o.pid + " – " + o.name,
              };
            });
            this.plots.sort(function (a, b) {
              var pidA = a.pid.toUpperCase();
              var pidB = b.pid.toUpperCase();
              if (pidA < pidB) {
                return -1;
              }
              if (pidA > pidB) {
                return 1;
              }
              return 0;
            });
            this.selectPlot = this.plots[0];
            this.readPlotData();
            console.log(this.plots);
          }
        });
    },

    readPlotData() {
      axios
        .get(BASE_URL + "/plots/" + this.selectPlot.id + "/")
        .then((response) => {
          this.litterAnnual = response.data.litter_annual;
          this.litterEach = response.data.litter_each.map((o) => {
            return {
              year: o.year,
              t1: o.t1,
              t2: o.t2,
              wdry_leaf: o.wdry_leaf / o.inst_period,
              wdry_branch: o.wdry_branch / o.inst_period,
              wdry_rep: o.wdry_rep / o.inst_period,
              wdry_all: o.wdry_all / o.inst_period,
            };
          });
          console.log(this.litterAnnual);
        });
    },

    fillData1() {
      this.chartData1 = {
        labels: this.litterAnnual.map((o) => Math.round(o.year * 10) / 10),
        datasets: [
          {
            label: "Leaves",
            fill: false,
            data: this.litterAnnual.map((o) => {
              return {
                x: Math.round(o.year * 10) / 10,
                y: o.wdry_leaf,
              };
            }),
          },
          {
            label: "Branches",
            fill: false,
            data: this.litterAnnual.map((o) => {
              return {
                x: Math.round(o.year * 10) / 10,
                y: o.wdry_branch,
              };
            }),
          },
          {
            label: "Reproductive parts",
            fill: false,
            data: this.litterAnnual.map((o) => {
              return {
                x: Math.round(o.year * 10) / 10,
                y: o.wdry_rep,
              };
            }),
          },
          {
            label: "Total",
            fill: false,
            data: this.litterAnnual.map((o) => {
              return {
                x: Math.round(o.year * 10) / 10,
                y: o.wdry_all,
              };
            }),
          },
        ],
      };
      this.loaded1 = true;
    },

    fillData2() {
      this.chartData2 = {
        datasets: [
          {
            label: "Leaves",
            fill: false,
            steppedLine: "after",
            data: this.litterEach.map((o) => {
              return {
                x: o.t2,
                y: o.wdry_leaf,
              };
            }),
          },
          {
            label: "Branches",
            fill: false,
            steppedLine: "after",
            data: this.litterEach.map((o) => {
              return {
                x: o.t2,
                y: o.wdry_branch,
              };
            }),
          },
          {
            label: "Reproductive parts",
            fill: false,
            steppedLine: "after",
            data: this.litterEach.map((o) => {
              return {
                x: o.t2,
                y: o.wdry_rep,
              };
            }),
          },
          {
            label: "Total",
            fill: false,
            steppedLine: "after",
            data: this.litterEach.map((o) => {
              return {
                x: o.t2,
                y: o.wdry_all,
              };
            }),
          },
        ],
      };
      this.loaded2 = true;
    },
  },
};
</script>

<style lang="scss"></style>
