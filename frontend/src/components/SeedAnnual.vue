<template>
  <v-flex>
    <v-toolbar flat>
      <v-toolbar-title>Annual Variation in Seed Production</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn-toggle
        v-model="toggleChart"
        color="deep-purple accent-3"
        group
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

    <v-container fluid>
      <v-row align="center">
        <v-col cols="6" sm="12" :md="toggleSingleCol ? 6 : 12">
          <v-select
            v-if="toggleChart"
            v-model="spSelected1"
            label="Select Species"
            :items="spList"
            item-value="species"
            clearable
            color="deep-purple"
            class="my-0 py-0"
          >
            <template slot="item" slot-scope="data">
              {{ data.item.species }} - {{ data.item.species_jp }}
            </template>
            <template slot="selection" slot-scope="data">
              {{ data.item.species }}
            </template>
          </v-select>

          <v-select
            v-else
            v-model="spSelected2"
            label="Select Species"
            :items="spList"
            item-value="species"
            :item-text="(item) => `${item.species} – ${item.species_jp}`"
            multiple
            clearable
            color="deep-purple"
            class="my-0 py-0"
          >
            <template v-slot:selection="{ item, index }">
              <v-chip
                v-if="index === 0 && spSelected2.length === spList.length"
                small
                color="deep-purple lighten-4"
              >
                <span>All</span>
              </v-chip>
              <v-chip v-else-if="index === 0" small>
                <span>{{ item.species }}</span>
              </v-chip>
              <span
                v-if="index === 1 && spSelected2.length < spList.length"
                class="grey--text caption"
              >
                (+{{ spSelected2.length - 1 }} others)
              </span>
            </template>
            <template v-slot:prepend-item>
              <v-list-item ripple @click="toggleSpecies">
                <v-list-item-action>
                  <v-icon
                    :color="spSelected2.length > 0 ? 'indigo darken-4' : ''"
                  >
                    {{ iconSpecies }}
                  </v-icon>
                </v-list-item-action>
                <v-list-item-content>
                  <v-list-item-title> Select All </v-list-item-title>
                </v-list-item-content>
              </v-list-item>
              <v-divider class="mt-2"></v-divider>
            </template>
          </v-select>
        </v-col>

        <v-col cols="6" sm="12" :md="toggleSingleCol ? 6 : 12">
          <v-text-field
            v-if="!toggleChart"
            v-model="search"
            append-icon="mdi-magnify"
            label="Search"
            color="deep-purple"
            class="my-0 py-0"
          ></v-text-field>
        </v-col>
      </v-row>
    </v-container>

    <v-card class="mt-0 pt-0 px-2" v-if="toggleChart" flat>
      <v-card-subtitle v-html="subtitle"></v-card-subtitle>
      <bar-chart
        v-if="loaded"
        :chart-data="chartData"
        :options="options"
        height="288px"
      ></bar-chart>
    </v-card>

    <v-card v-if="!toggleChart" flat>
      <v-data-table
        :headers="headers"
        :items="filteredData2"
        :search="search"
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
      <v-btn color="deep-purple" text @click="showCaption = !showCaption">
        Show Caption
      </v-btn>

      <v-spacer></v-spacer>

      <v-btn icon @click="showCaption = !showCaption">
        <v-icon>
          {{ showCaption ? "mdi-chevron-up" : "mdi-chevron-down" }}
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
import BarChart from "../components/BarChart.js";

export default {
  components: {
    BarChart,
  },

  props: ["data", "toggleSingleCol"],

  data: () => ({
    search: "",
    spList: [],
    spSelected1: null,
    spSelected2: [],
    chartData: null,
    subtitle: "Amount of seeds or fruits per square meter",
    options: {
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

    loaded: false,
    toggleChart: true,
    showCaption: false,

    headers: [
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
        text: "N",
        value: "number",
        label: "Number of seeds or fruits",
        caption: "Number of seeds or fruits (m<sup>&minus;2</sup>)",
      },
      {
        text: "W",
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
  }),

  mounted() {
    this.getSpList();
  },

  computed: {
    filteredData1() {
      return this.data.filter((d) => d.species === this.spSelected1);
    },
    filteredData2() {
      return this.data.filter((d) => this.spSelected2.includes(d.species));
    },
    selectAllSpecies() {
      return this.spSelected2.length === this.spList.length;
    },
    selectSomeSpecies() {
      return this.spSelected2.length > 0 && !this.selectAllSpecies;
    },
    iconSpecies() {
      if (this.selectAllSpecies) return "mdi-close-box";
      if (this.selectSomeSpecies) return "mdi-minus-box";
      return "mdi-checkbox-blank-outline";
    },
  },

  watch: {
    data() {
      this.getSpList();
    },

    filteredData1() {
      this.fillData();
    },
  },

  methods: {
    getSpList() {
      this.spList = this.data
        .map((e) => {
          return {
            species_jp: e.species_jp,
            species: e.species,
          };
        })
        .filter(
          (element, index, self) =>
            self.findIndex(
              (e) =>
                e.species_jp === element.species_jp &&
                e.species === element.species
            ) === index
        );
      this.spSelected1 = this.spList.map((o) => o.species)[0];
      this.spSelected2 = this.spList.map((o) => o.species).slice();
    },

    toggleSpecies() {
      this.$nextTick(() => {
        if (this.selectAllSpecies) {
          this.spSelected2 = [];
        } else {
          this.spSelected2 = this.spList.map((e) => e.species).slice();
        }
      });
    },

    fillData() {
      this.chartData = {
        labels: this.filteredData1.map((e) => Math.round(e.year * 10) / 10),
        datasets: [
          {
            type: "line",
            label: "Number (left axis)",
            borderColor: "rgba(103, 58, 183, 0.8)",
            pointBorderColor: "rgba(103, 58, 183, 0.8)",
            pointBackgroundColor: "rgba(103, 58, 183,) 0.8",
            fill: false,
            data: this.filteredData1.map((e) => e.number),
            yAxisID: "y-axis-1",
            order: 1,
          },
          {
            type: "bar",
            label: "Dry mass (right axis)",
            backgroundColor: "rgba(0, 150, 136, 0.8)",
            borderColor: "rgba(0, 150, 136, 0.8)",
            data: Array.from(
              this.filteredData1.map((e) => e.wdry),
              (i) => (i !== null ? i : NaN)
            ),
            yAxisID: "y-axis-2",
            order: 2,
          },
        ],
      };
      this.loaded = true;
    },
  },
};
</script>
