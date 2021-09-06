<template>
  <v-flex>
    <v-toolbar flat>
      <v-toolbar-title>Tree Population Turnover</v-toolbar-title>
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
            v-if="toggleChart"
            v-model="spSelected1"
            label="Select Species"
            :items="spList"
            item-value="species"
            clearable
            color="teal"
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
            color="teal"
            class="my-0 py-0"
          >
            <template v-slot:selection="{ item, index }">
              <v-chip
                v-if="index === 0 && spSelected2.length === spList.length"
                small
                color="teal lighten-4"
              >
                <span>All</span>
              </v-chip>
              <v-chip v-else-if="index === 0" small color="teal lighten-4">
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
            id="btnGroup"
          ></v-btn>
        </v-btn-toggle>
      </v-card-actions>
    </v-card>

    <v-card v-if="!toggleChart" flat>
      <v-data-table
        :headers="headers"
        :items="filteredData2"
        :search="search"
        class="elevation-0"
      >
        <template v-slot:header.t1="{ header }">
          <span v-html="header.text"></span>
        </template>
        <template v-slot:header.t2="{ header }">
          <span v-html="header.text"></span>
        </template>
        <template v-slot:header.n_m="{ header }">
          <span v-html="header.text"></span>
        </template>
        <template v-slot:header.b_m="{ header }">
          <span v-html="header.text"></span>
        </template>
        <template v-slot:header.r_rel="{ header }">
          <span v-html="header.text + '&nbsp;(&times;100)'"></span>
        </template>
        <template v-slot:header.m_rel="{ header }">
          <span v-html="header.text + '&nbsp;(&times;100)'"></span>
        </template>
        <template v-slot:header.p_rel="{ header }">
          <span v-html="header.text + '&nbsp;(&times;100)'"></span>
        </template>
        <template v-slot:header.l_rel="{ header }">
          <span v-html="header.text + '&nbsp;(&times;100)'"></span>
        </template>
        <template v-slot:header.r_abs="{ header }">
          <span v-html="header.text"></span>
        </template>
        <template v-slot:header.m_abs="{ header }">
          <span v-html="header.text"></span>
        </template>
        <template v-slot:header.p_abs="{ header }">
          <span v-html="header.text"></span>
        </template>
        <template v-slot:header.l_abs="{ header }">
          <span v-html="header.text"></span>
        </template>
        <template v-slot:item.t2="{ item }">
          {{ Math.round(item.t2 * 10) / 10 }}
        </template>
        <template v-slot:item.t1="{ item }">
          {{ Math.round(item.t1 * 10) / 10 }}
        </template>
        <template v-slot:item.n_m="{ item }">
          {{ Math.round(item.n_m * 10) / 10 }}
        </template>
        <template v-slot:item.b_m="{ item }">
          {{ Math.round(item.b_m * 100) / 100 }}
        </template>
        <template v-slot:item.r_rel="{ item }">
          {{ Math.round(item.r_rel * 10000) / 100 }}
        </template>
        <template v-slot:item.m_rel="{ item }">
          {{ Math.round(item.m_rel * 10000) / 100 }}
        </template>
        <template v-slot:item.p_rel="{ item }">
          {{ Math.round(item.p_rel * 10000) / 100 }}
        </template>
        <template v-slot:item.l_rel="{ item }">
          {{ Math.round(item.l_rel * 10000) / 100 }}
        </template>
        <template v-slot:item.r_abs="{ item }">
          {{ Math.round(item.r_abs * 100) / 100 }}
        </template>
        <template v-slot:item.m_abs="{ item }">
          {{ Math.round(item.m_abs * 100) / 100 }}
        </template>
        <template v-slot:item.p_abs="{ item }">
          {{ Math.round(item.p_abs * 100) / 100 }}
        </template>
        <template v-slot:item.l_abs="{ item }">
          {{ Math.round(item.l_abs * 100) / 100 }}
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
    spSelected1: null,
    spSelected2: [],
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
          scheme: "brewer.DarkTwo3",
        },
      },
    },
    loaded: false,
    toggleChart: true,
    showCaption: false,

    headers: [
      {
        text: "T<sub>1</sub>",
        value: "t1",
        label: "T1",
        caption: "Year of the first census",
      },
      {
        text: "T<sub>2</sub>",
        value: "t2",
        label: "T2",
        caption: "Year of the second census",
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
        text: "N<sub>m</sub>",
        value: "n_m",
        label: "Nm",
        caption: "Period mean number of stems (ha<sup>&minus;1</sup>)",
      },
      {
        text: "B<sub>m</sub>",
        value: "b_m",
        label: "Bm",
        caption:
          "Period mean above ground biomass (Mg &nbsp;ha<sup>&minus;1</sup>)",
      },
      {
        text: "<i>r</i>",
        value: "r_rel",
        label: "r",
        caption:
          "Relative (per-capita) instantneous recruitment rate (year<sup>&minus;1</sup>)",
      },
      {
        text: "<i>m</i>",
        value: "m_rel",
        label: "m",
        caption:
          "Relative (per-capita) instantneous mortality rate (year<sup>&minus;1</sup>)",
      },
      {
        text: "<i>p</i>",
        value: "p_rel",
        label: "p",
        caption:
          "Relative (per-biomass) instantneous productivity rate by tree growth (year<sup>&minus;1</sup>)",
      },
      {
        text: "<i>l</i>",
        value: "l_rel",
        label: "l",
        caption:
          "Relative (per-biomass) instantneous loss rate by tree mortality (year<sup>&minus;1</sup>)",
      },
      {
        text: "<i>R</i>",
        value: "r_abs",
        label: "R",
        caption:
          "Absolute (per-area) instantneous recruitment rate (ha<sup>&minus;1</sup>&nbsp;year<sup>&minus;1</sup>)",
      },
      {
        text: "<i>M</i>",
        value: "m_abs",
        label: "M",
        caption:
          "Absolute (per-area) instantneous mortality rate (ha<sup>&minus;1</sup>&nbsp;year<sup>&minus;1</sup>)",
      },
      {
        text: "<i>P</i>",
        value: "p_abs",
        label: "P",
        caption:
          "Absolute (per-area) instantneous productivity rate by tree growth (Mg&nbsp;ha<sup>&minus;1</sup>&nbsp;year<sup>&minus;1</sup>)",
      },
      {
        text: "<i>L</i>",
        value: "l_abs",
        label: "L",
        caption:
          "Absolute (per-area) instantneous loss rate by tree mortality (Mg&nbsp;ha<sup>&minus;1</sup>&nbsp;year<sup>&minus;1</sup>)",
      },
    ],

    btn: [
      {
        text: "<i>r</i>&nbsp;&amp;&nbsp;<i>m</i>",
        values: [
          { label: "r", value: "r_rel" },
          { label: "m", value: "m_rel" },
        ],
        label: "Relative Density Turnover Rates (year<sup>&minus;1</sup>)",
      },
      {
        text: "<i>p</i>&nbsp;&amp;&nbsp;<i>l</i>",
        values: [
          { label: "p", value: "p_rel" },
          { label: "l", value: "l_rel" },
        ],
        label: "Relative Biomass Turnover Rates (year<sup>&minus;1</sup>)",
      },
      {
        text: "<i>R</i>&nbsp;&amp;&nbsp;<i>M</i>",
        values: [
          { label: "R", value: "r_abs" },
          { label: "M", value: "m_abs" },
        ],
        label:
          "Absolute Density Turnover Rates (ha<sup>&minus;1</sup>&nbsp;year<sup>&minus;1</sup>)",
      },
      {
        text: "<i>P</i>&nbsp;&amp;&nbsp;<i>L</i>",
        values: [
          { label: "P", value: "p_abs" },
          { label: "L", value: "l_abs" },
        ],
        label:
          "Absolute Biomass Turnover Rates (Mg&nbsp;ha<sup>&minus;1</sup>&nbsp;year<sup>&minus;1</sup>)",
      },
    ],

    select: {
      text: "<i>r</i>&nbsp;&amp;&nbsp;<i>m</i>",
      values: [
        { label: "r", value: "r_rel" },
        { label: "m", value: "m_rel" },
      ],
      label: "Relative Density Turnover Rates (year<sup>&minus;1</sup>)",
    },
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
          this.spSelected2 = this.spList.map((o) => o.species).slice();
        }
      });
    },

    fillData() {
      let vals = this.select.values;
      this.chartData = {
        labels: this.filteredData1.map(
          (o) =>
            String(Math.round(o.t1 * 10) / 10) +
            "–" +
            String(Math.round(o.t2 * 10) / 10)
        ),
        datasets: [
          {
            label: vals[0].label,
            fill: false,
            data: this.filteredData1.map((o) => {
              return {
                x: Math.round(o.t2 * 10) / 10,
                y: o[vals[0].value],
              };
            }),
          },
          {
            label: vals[1].label,
            fill: false,
            data: this.filteredData1.map((o) => {
              return {
                x: Math.round(o.t2 * 10) / 10,
                y: o[vals[1].value],
              };
            }),
          },
          {
            label: vals[0].label + " - " + vals[1].label,
            fill: false,
            data: this.filteredData1.map((o) => {
              return {
                x: Math.round(o.t2 * 10) / 10,
                y: o[vals[0].value] - o[vals[1].value],
              };
            }),
          },
        ],
      };
      this.loaded = true;
    },
  },
};
</script>

<style lang="scss">
#btnGroup {
  text-transform: none;
}
</style>
