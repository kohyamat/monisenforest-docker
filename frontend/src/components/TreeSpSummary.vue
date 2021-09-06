<template>
  <v-flex>
    <v-toolbar flat>
      <v-toolbar-title>Tree Population Dynamics</v-toolbar-title>
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

    <v-container fluid>
      <v-row align="center">
        <v-col cols="6" sm="12" :md="toggleSingleCol ? 6 : 12">
          <v-select
            v-model="spSelected"
            label="Select Species"
            :items="spList"
            item-value="species"
            :item-text="(item) => `${item.species} – ${item.species_jp}`"
            multiple
            clearable
            color="teal"
            class="my-0 py-0"
          >
            <template v-slot:selection="{ item, index }">
              <v-chip
                v-if="index === 0 && spSelected.length === spList.length"
                small
                color="teal lighten-4"
              >
                <span>All</span>
              </v-chip>
              <v-chip v-else-if="index === 0" small color="teal lighten-4">
                <span>{{ item.species }}</span>
              </v-chip>
              <span
                v-if="index === 1 && spSelected.length < spList.length"
                class="grey--text caption"
              >
                (+{{ spSelected.length - 1 }} others)
              </span>
            </template>
            <template v-slot:prepend-item>
              <v-list-item ripple @click="toggleSpecies">
                <v-list-item-action>
                  <v-icon
                    :color="spSelected.length > 0 ? 'indigo darken-4' : ''"
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
            color="teal"
            class="my-0 py-0"
          ></v-text-field>
        </v-col>
      </v-row>
    </v-container>

    <v-card class="mt-0 pt-0 px-2" v-if="toggleChart" flat>
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
      <v-data-table
        :headers="headers"
        :items="filteredData"
        :search="search"
        class="elevation-0"
      >
        <template v-slot:item.year="{ item }">
          {{ Math.round(item.year * 10) / 10 }}
        </template>
        <template v-slot:item.n="{ item }">
          {{ Math.round(item.n * 10) / 10 }}
        </template>
        <template v-slot:item.b="{ item }">
          {{ Math.round(item.b * 100) / 100 }}
        </template>
        <template v-slot:item.ba="{ item }">
          {{ Math.round(item.ba * 100) / 100 }}
        </template>
        <template v-slot:item.n_prop="{ item }">
          {{ Math.round(item.n_prop * 100) / 100 }}
        </template>
        <template v-slot:item.b_prop="{ item }">
          {{ Math.round(item.b_prop * 100) / 100 }}
        </template>
        <template v-slot:item.ba_prop="{ item }">
          {{ Math.round(item.ba_prop * 100) / 100 }}
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
import LineChart from "./LineChart.js";

export default {
  components: {
    LineChart,
  },

  props: ["data", "toggleSingleCol"],

  data: () => ({
    search: "",
    spList: [],
    spSelected1: [],
    spSelected: [],
    chartData: null,
    options: {
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
      plugins: {
        colorschemes: {
          scheme: "brewer.Paired12",
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
        caption:
          "Census year (calendar year - 1 for plots surveyed in the early spring)",
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
        value: "n",
        label: "N",
        caption: "Number of stems (ha<sup>&minus;1</sup>)",
      },
      {
        text: "B",
        value: "b",
        label: "B",
        caption: "Above ground biomass (Mg&nbsp;ha<sup>&minus;1</sup>)",
      },
      {
        text: "BA",
        value: "ba",
        label: "BA",
        caption: "Basal area (m<sup>2</sup>&nbsp;ha<sup>&minus;1</sup>)",
      },
      {
        text: "%N",
        value: "n_prop",
        label: "%N",
        caption: "Proportion of species based on number of stems (%)",
      },
      {
        text: "%B",
        value: "b_prop",
        label: "%B",
        caption: "Proportion of species based on above ground biomass (%)",
      },
      {
        text: "%BA",
        value: "ba_prop",
        label: "%BA",
        caption: "Proportion of species based on basal area (%)",
      },
    ],

    btn: [
      {
        text: "N",
        value: "n",
        label: "Number of Stems (ha<sup>&minus;1</sup>)",
      },
      {
        text: "B",
        value: "b",
        label: "Above ground biomass (Mg&nbsp;ha<sup>&minus;1</sup>)",
      },
      {
        text: "BA",
        value: "ba",
        label: "Basal Area (m<sup>2</sup>&nbsp;ha<sup>&minus;1</sup>)",
      },
      {
        text: "%N",
        value: "n_prop",
        label: "Proportion of species based on number of stems (%)",
      },
      {
        text: "%B",
        value: "b_prop",
        label: "Proportion of species based on above ground biomass (%)",
      },
      {
        text: "%BA",
        value: "ba_prop",
        label: "Proportion of species based on basal area (%)",
      },
    ],

    select: {
      text: "N",
      value: "n",
      label: "Number of Stems (ha<sup>&minus;1</sup>)",
    },
  }),

  mounted() {
    this.getSpList();
  },

  computed: {
    filteredData() {
      return this.data.filter((d) => this.spSelected.includes(d.species));
    },
    selectAllSpecies() {
      return this.spSelected.length === this.spList.length;
    },
    selectSomeSpecies() {
      return this.spSelected.length > 0 && !this.selectAllSpecies;
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

    filteredData() {
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
      this.spSelected = this.spList.map((o) => o.species).slice(0, 3);
    },

    toggleSpecies() {
      this.$nextTick(() => {
        if (this.selectAllSpecies) {
          this.spSelected = [];
        } else {
          this.spSelected = this.spList.map((o) => o.species).slice();
        }
      });
    },

    makeDatasets() {
      let resArray = [];
      for (let i = 0; i < this.spSelected.length; i++) {
        let subItems = this.filteredData.filter(
          (e) => e.species === this.spSelected[i]
        );
        resArray.push({
          label: this.spSelected[i],
          fill: false,
          data: subItems.map((o) => {
            return {
              x: Math.round(o.year * 10) / 10,
              y: o[this.select.value],
            };
          }),
        });
      }
      return resArray;
    },

    fillData() {
      this.chartData = {
        // labels: this.years,
        datasets: this.makeDatasets(),
      };
      this.loaded = true;
    },
  },
};
</script>
