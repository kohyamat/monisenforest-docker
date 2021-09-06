<template>
  <v-row align="center">
    <v-col cols="6">
      <div class="text-h4 mb-3 grey--text text--darken-3">
        Seedfall Data Summary
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
        single-line
        item-value="id"
        persistent-hint
        return-object
        @change="readPlotData"
      ></v-select>
    </v-col>

    <v-col cols="12">
      <v-card>
        <v-toolbar flat>
          <v-toolbar-title>Annual Variation in Seed Production</v-toolbar-title>

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
          <v-col cols="6">
            <v-select
              v-model="selectSpecies"
              label="Select Species"
              :items="speciesList"
              :item-text="(item) => `${item.species} – ${item.species_jp}`"
              :hint="`${selectSpecies.order}: ${selectSpecies.family}`"
              clearable
              persistent-hint
              return-object
              color="deep-purple"
            >
            </v-select>
          </v-col>

          <bar-chart
            v-if="loaded1"
            :chart-data="chartData1"
            :options="options1"
            height="288px"
          ></bar-chart>
        </v-card>

        <v-card v-if="!toggleChart1" flat>
          <v-card-text>
            <v-text-field
              v-model="searchSpecies"
              append-icon="mdi-magnify"
              label="Search"
              single-line
              hide-details
              color="deep-purple"
              class="ma-0 pa-0"
            ></v-text-field>
          </v-card-text>

          <v-data-table
            :headers="headers1"
            :items="seedAnnual"
            :search="searchSpecies"
            class="elevation-0"
          >
            <template v-slot:item.number="{ item }">
              {{ Math.round(item.number * 10) / 10 }}
            </template>
            <template v-slot:item.wdry="{ item }">
              {{ Math.round(item.wdry * 1000) / 1000 }}
            </template>
            <template v-slot:item.prop_viable="{ item }">
              {{ Math.round(item.prop_viable * 1000) / 10 }}
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
  </v-row>
</template>

<script>
import BarChart from "../components/BarChart.js";
import axios from "axios";

const BASE_URL = "http://localhost:8000/api";

export default {
  components: {
    BarChart,
  },

  data() {
    return {
      plots: [{ id: "", pid: "", name: "", name_jp: "", text: "No Data" }],
      selectPlot: null,

      // Chart1: Seedfall annual
      seedAnnual: [],
      chartData1: null,
      options1: {
        responsive: true,
        maintainAspectRatio: false,
        legend: {
          position: "top",
          // reverse: true,
        },
        scales: {
          xAxes: [
            //{
            //  type: 'linear',
            //  ticks: {
            //    stepSize: 1,
            //  },
            //},
          ],
          yAxes: [
            {
              id: "y-axis-1",
              type: "linear",
              position: "left",
              ticks: {
                beginAtZero: true,
              },
            },
            {
              id: "y-axis-2",
              type: "linear",
              position: "right",
              ticks: {
                beginAtZero: true,
              },
              gridLines: {
                drawOnChartArea: false,
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

      speciesList: [],
      years: [],
      searchSpecies: "",
      filters: { species: [], year: [] },
      selectSpecies: null,

      headers1: [
        {
          text: "Year",
          value: "year",
          label: "Year",
          caption: "Calender year",
        },
        {
          text: "Name",
          value: "species_jp",
          label: "Name",
          caption: "Japanese name",
        },
        {
          text: "Species",
          value: "species",
          label: "Species",
          caption: "Scientific name",
        },
        {
          text: "Family",
          value: "family",
          label: "Family",
          caption: "Family name",
        },
        {
          text: "Number",
          value: "number",
          label: "Number of seeds or fruits",
          caption: "Number of seeds or fruits (m<sup>&minus;2</sup>)",
        },
        {
          text: "Dry mass",
          value: "wdry",
          label: "Dry mass of seeds or fruits",
          caption: "Dry mass of seeds or fruits (g&nbsp;m<sup>&minus;2</sup>)",
        },
        {
          text: "%Viable",
          value: "prop_viable",
          label: "Pecentage of viable seeds",
          caption: "Pecentage of viable seeds",
        },
      ],
    };
  },

  watch: {
    selectSpecies() {
      this.fillData1();
    },
  },

  computed: {},

  mounted() {
    this.selectPlot = this.plots[0];
    this.readPlots();
  },

  methods: {
    readPlots() {
      axios
        .get(BASE_URL + "/plots/?skip=0&dtype=seed&no_load=true")
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
              // sort by plot name
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
          this.seedAnnual = response.data.seed_annual;
          this.speciesList = this.seedAnnual
            .map((o) => {
              return {
                species_jp: o["species_jp"],
                species: o["species"],
                family: o["family"],
                order: o["order"],
              };
            })
            .filter(
              // unique
              (element, index, self) =>
                self.findIndex(
                  (e) =>
                    e.species_jp === element.species_jp &&
                    e.species === element.species
                ) === index
            );
          this.selectSpecies = this.speciesList[0];
          this.filters["species"] = this.speciesList
            .map((o) => o["species"])
            .slice(0, 1);
          this.years = this.uniq(this.seedAnnual.map((o) => o["year"]));
          this.filters["year"] = this.years.slice();
        });
    },

    toggleSpecies() {
      this.$nextTick(() => {
        if (this.selectAllSpecies) {
          this.filters["species"] = [];
        } else {
          this.filters["species"] = this.speciesList
            .map((o) => o["species"])
            .slice();
        }
      });
    },

    toggleYear() {
      this.$nextTick(() => {
        if (this.selectAllYear) {
          this.filters["year"] = [];
        } else {
          this.filters["year"] = this.years.slice();
        }
      });
    },

    uniq(array) {
      const uniquedArray = [];
      for (const e of array) {
        if (!uniquedArray.includes(e)) uniquedArray.push(e);
      }
      return uniquedArray;
    },

    makeDatasetsSpecies() {
      let subItems = this.seedAnnual.filter(
        (e) => e.species === this.selectSpecies["species"]
      );
      let resArray = [
        {
          type: "line",
          label: "Number (left axis)",
          borderColor: "rgba(103, 58, 183, 0.8)",
          pointBorderColor: "rgba(103, 58, 183, 0.8)",
          pointBackgroundColor: "rgba(103, 58, 183,) 0.8",
          fill: false,
          data: subItems.map((o) => o.number),
          yAxisID: "y-axis-1",
          order: 1,
        },
        {
          type: "bar",
          label: "Dry mass (right axis)",
          backgroundColor: "rgba(0, 150, 136, 0.8)",
          borderColor: "rgba(0, 150, 136, 0.8)",
          data: Array.from(
            subItems.map((o) => o.wdry),
            (i) => (i !== null ? i : NaN)
          ),
          yAxisID: "y-axis-2",
          order: 2,
        },
      ];
      return resArray;
    },

    fillData1() {
      this.chartData1 = {
        labels: this.years,
        datasets: this.makeDatasetsSpecies(),
      };
      this.loaded1 = true;
    },
  },
};
</script>

<style lang="scss"></style>
