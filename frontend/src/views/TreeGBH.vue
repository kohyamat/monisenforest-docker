<template>
  <v-row align="center">
    <v-col cols="6">
      <div class="text-h4 mb-3 grey--text text--darken-3">
        Tree Census Data Summary
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
          <v-toolbar-title>Density, Biomass and Diversity</v-toolbar-title>

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
          <v-card-subtitle v-html="select1.label"></v-card-subtitle>

          <line-chart
            v-if="loaded1"
            :chart-data="chartData1"
            :options="options1"
            height="288px"
          ></line-chart>

          <v-card-actions>
            <v-btn-toggle
              v-model="select1"
              color="deep-purple accent-3"
              tile
              group
              mandatory
              dense
              @change="fillData1()"
            >
              <v-btn
                v-for="(btn, index) in btn1"
                :key="index"
                :value="btn"
                v-html="btn.text"
              ></v-btn>
            </v-btn-toggle>
          </v-card-actions>
        </v-card>

        <v-card v-if="!toggleChart1" flat>
          <v-data-table
            :headers="headers1"
            :items="treeComSummary"
            class="elevation-0"
          >
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
          <v-toolbar-title>Community-wide Turnover</v-toolbar-title>

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
          <v-card-subtitle v-html="select2.label"></v-card-subtitle>

          <line-chart
            v-if="loaded2"
            :chart-data="chartData2"
            :options="options2"
            height="288px"
          ></line-chart>

          <v-card-actions>
            <v-btn-toggle
              v-model="select2"
              color="deep-purple accent-3"
              tile
              group
              mandatory
              dense
              @change="fillData2()"
            >
              <v-btn
                v-for="(btn, index) in btn2"
                :key="index"
                :value="btn"
                v-html="btn.text"
                id="btnGroup2"
              ></v-btn>
            </v-btn-toggle>
          </v-card-actions>
        </v-card>

        <v-card v-if="!toggleChart2" flat>
          <v-data-table
            :headers="headers2"
            :items="treeComTurnover"
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

    <v-col cols="12">
      <v-card>
        <v-toolbar flat>
          <v-toolbar-title>Tree Population Dynamics</v-toolbar-title>
          <v-spacer></v-spacer>
          <v-btn-toggle
            v-model="toggleChart3"
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

        <v-container fluid flat>
          <v-row dense>
            <v-col>
              <v-select
                v-model="filters['species']"
                label="Select Species"
                :items="speciesList"
                :item-text="(item) => `${item.species} – ${item.species_jp}`"
                item-value="species"
                multiple
                clearable
                color="deep-purple"
                class="my-0 py-0"
              >
                <template v-slot:selection="{ item, index }">
                  <v-chip
                    v-if="
                      index === 0 &&
                      filters['species'].length === speciesList.length
                    "
                    small
                    color="deep-purple lighten-4"
                  >
                    <span>All</span>
                  </v-chip>
                  <v-chip v-else-if="index === 0" small>
                    <span>{{ item.species }}</span>
                  </v-chip>
                  <span
                    v-if="
                      index === 1 &&
                      filters['species'].length < speciesList.length
                    "
                    class="grey--text caption"
                  >
                    (+{{ filters["species"].length - 1 }} others)
                  </span>
                </template>
                <template v-slot:prepend-item>
                  <v-list-item ripple @click="toggleSpecies">
                    <v-list-item-action>
                      <v-icon
                        :color="
                          filters['species'].length > 0 ? 'indigo darken-4' : ''
                        "
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

            <v-col>
              <v-select
                v-model="filters['year']"
                v-if="!toggleChart3"
                label="Select Year"
                :items="years"
                multiple
                clearable
                color="deep-purple"
                class="my-0 py-0"
              >
                <template v-slot:selection="{ item, index }">
                  <v-chip
                    v-if="
                      index === 0 && filters['year'].length === years.length
                    "
                    small
                    color="deep-purple lighten-4"
                  >
                    <span>All</span>
                  </v-chip>
                  <v-chip
                    v-if="index < 3 && filters['year'].length < years.length"
                    small
                  >
                    <span>{{ item }}</span>
                  </v-chip>
                  <span
                    v-if="index === 3 && filters['year'].length < years.length"
                    class="grey--text caption"
                  >
                    (+{{ filters["year"].length - 3 }} others)
                  </span>
                </template>
                <template v-slot:prepend-item>
                  <v-list-item ripple @click="toggleYear">
                    <v-list-item-action>
                      <v-icon
                        :color="
                          filters['year'].length > 0 ? 'indigo darken-4' : ''
                        "
                      >
                        {{ iconYear }}
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
          </v-row>
        </v-container>

        <v-card class="mt-0 pt-0 px-2" v-if="toggleChart3" flat>
          <v-card-subtitle v-html="select3.label"></v-card-subtitle>

          <line-chart
            v-if="loaded3"
            :chart-data="chartData3"
            :options="options3"
            height="288px"
          ></line-chart>

          <v-card-actions>
            <v-btn-toggle
              v-model="select3"
              color="deep-purple accent-3"
              tile
              group
              mandatory
              dense
              @change="fillData3()"
            >
              <v-btn
                v-for="(btn, index) in btn3"
                :key="index"
                :value="btn"
                v-html="btn.text"
              ></v-btn>
            </v-btn-toggle>
          </v-card-actions>
        </v-card>

        <v-card v-if="!toggleChart3" flat>
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
            :headers="headers3"
            :items="filteredSpecies"
            :search="searchSpecies"
            class="elevation-0"
          >
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
          <v-btn color="deep-purple" text @click="showCaption3 = !showCaption3">
            Show Caption
          </v-btn>

          <v-spacer></v-spacer>

          <v-btn icon @click="showCaption3 = !showCaption3">
            <v-icon>{{
              showCaption ? "mdi-chevron-up" : "mdi-chevron-down"
            }}</v-icon>
          </v-btn>
        </v-card-actions>

        <v-expand-transition>
          <v-list class="px-2" v-show="showCaption3" dense>
            <v-divider></v-divider>
            <template v-for="(item, index) in headers3">
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
      plots: [{ id: "", plot_id: "", name: "", name_jp: "", text: "No Data" }],
      selectPlot: null,

      // Chart1: Biomass and Diversity
      treeComSummary: [],
      // treeComSummary: [
      //   { year: '', nstem: 0, nsp: 0, b: 0, ba: 0, richness: 0, shannon: 0 },
      // ],
      chartData1: null,
      options1: {
        responsive: true,
        maintainAspectRatio: false,
        legend: {
          display: false,
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
                // beginAtZero: true,
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
      },
      loaded1: false,
      select1: null,
      toggleChart1: true,
      showCaption1: false,

      headers1: [
        {
          text: "Year",
          value: "year",
          label: "Year",
          caption:
            "Census year (calendar year - 1 for plots surveyed in the early spring)",
        },
        {
          text: "N<sub>stem</sub>",
          value: "nstem",
          label: "N stem",
          caption: "Number of stems (ha<sup>&minus;1</sup>)",
        },
        {
          text: "N<sub>species</sub>",
          value: "nsp",
          label: "N species",
          caption: "Number of species",
        },
        {
          text: "B",
          value: "b",
          label: "Above ground biomass",
          caption: "Above ground biomass (Mg&nbsp;ha<sup>&minus;1</sup>)",
        },
        {
          text: "BA",
          value: "ba",
          label: "BA",
          caption: "Basal area (m<sup>2</sup>&nbsp;ha<sup>&minus;1</sup>)",
        },
        {
          text: "Richness",
          value: "richness",
          label: "Richness",
          caption:
            "Expected number of species in a sample of 100 stems (rarefaction species richness)",
        },
        {
          text: "Diversity",
          value: "shannon",
          label: "Diversity",
          caption: "Shannon index",
        },
      ],

      btn1: [
        {
          text: "N",
          value: "nstem",
          label: "Number of Stems (ha<sup>&minus;1</sup>)",
        },
        {
          text: "B",
          value: "b",
          label: "Above Ground Biomass (Mg&nbsp;ha<sup>&minus;1</sup>)",
        },
        {
          text: "BA",
          value: "ba",
          label: "Basal Area (m<sup>2</sup>&nbsp;ha<sup>&minus;1</sup>)",
        },
        {
          text: "Richness",
          value: "richness",
          label: "Rarefaction Species Richness (n = 100 stems)",
        },
        {
          text: "Diversity",
          value: "shannon",
          label: "Shannon Index",
        },
      ],

      // Chart2: Tree turnover rates
      treeComTurnover: [],
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
              type: "linear",
              ticks: {
                stepSize: 1,
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
      loaded2: false,
      select2: null,
      toggleChart2: true,
      showCaption2: false,

      headers2: [
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

      btn2: [
        {
          text: "<i>r</i>&nbsp;&amp;&nbsp;<i>m</i>",
          value: 4,
          label: "Relative Density Turnover Rates (year<sup>&minus;1</sup>)",
        },
        {
          text: "<i>p</i>&nbsp;&amp;&nbsp;<i>l</i>",
          value: 6,
          label: "Relative Biomass Turnover Rates (year<sup>&minus;1</sup>)",
        },
        {
          text: "<i>R</i>&nbsp;&amp;&nbsp;<i>M</i>",
          value: 8,
          label:
            "Absolute Density Turnover Rates (ha<sup>&minus;1</sup>&nbsp;year<sup>&minus;1</sup>)",
        },
        {
          text: "<i>P</i>&nbsp;&amp;&nbsp;<i>L</i>",
          value: 10,
          label:
            "Absolute Biomass Turnover Rates (Mg&nbsp;ha<sup>&minus;1</sup>&nbsp;year<sup>&minus;1</sup>)",
        },
      ],

      // Chart3: Tree species dynamics
      treeSpSummary: [],
      speciesList: [],
      years: [],
      searchSpecies: "",
      filters: { species: [], year: [] },

      chartData3: null,
      options3: {
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
      loaded3: false,
      select3: null,
      toggleChart3: true,
      showCaption3: false,

      headers3: [
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

      btn3: [
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
    };
  },

  watch: {
    treeComSummary() {
      this.fillData1();
    },

    treeComTurnover() {
      this.fillData2();
    },

    filteredSpecies() {
      this.fillData3();
    },
  },

  computed: {
    filteredSpecies() {
      return this.treeSpSummary.filter((d) => {
        return Object.keys(this.filters).every((f) => {
          return this.filters[f].includes(d[f]);
          // return this.filters[f].length < 1 || this.filters[f].includes(d[f])
        });
      });
    },
    selectAllSpecies() {
      return this.filters["species"].length === this.speciesList.length;
    },
    selectSomeSpecies() {
      return this.filters["species"].length > 0 && !this.selectAllSpecies;
    },
    iconSpecies() {
      if (this.selectAllSpecies) return "mdi-close-box";
      if (this.selectSomeSpecies) return "mdi-minus-box";
      return "mdi-checkbox-blank-outline";
    },
    selectAllYear() {
      return this.filters["year"].length === this.years.length;
    },
    selectSomeYear() {
      return this.filters["year"].length > 0 && !this.selectAllYear;
    },
    iconYear() {
      if (this.selectAllYear) return "mdi-close-box";
      if (this.selectSomeYear) return "mdi-minus-box";
      return "mdi-checkbox-blank-outline";
    },
  },

  mounted() {
    this.select1 = this.btn1[0];
    this.select2 = this.btn2[0];
    this.select3 = this.btn3[0];
    this.selectPlot = this.plots[0];
    this.readPlots();
  },

  methods: {
    readPlots() {
      axios
        .get(BASE_URL + "/plots/?skip=0&dtype=treeGBH&no_load=true")
        .then((response) => {
          if (response.data.length > 0) {
            this.plots = response.data.map((o) => {
              return {
                id: o.id,
                plot_id: o.plot_id,
                name_jp: o.name_jp,
                text: o.plot_id + " – " + o.name,
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
          this.treeComSummary = response.data.tree_com_summary;
          this.treeComTurnover = response.data.tree_com_turnover;
          this.treeSpSummary = response.data.tree_sp_summary.map(function (e) {
            return Object.keys(e).reduce(function (p, n) {
              if (n.startsWith("year")) p[n] = Math.round(e[n] * 10) / 10;
              else p[n] = e[n];
              return p;
            }, {});
          });
          this.speciesList = this.treeSpSummary
            .map((o) => {
              return {
                species_jp: o["species_jp"],
                species: o["species"],
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
          this.filters["species"] = this.speciesList
            .map((o) => o["species"])
            .slice(0, 3);
          this.years = this.uniq(this.treeSpSummary.map((o) => o["year"]));
          this.filters["year"] = this.years.slice();
          console.log(this.treeComSummary);
        });
    },

    fillData1() {
      this.chartData1 = {
        labels: this.treeComSummary.map((o) => Math.round(o.year * 10) / 10),
        datasets: [
          {
            label: this.select1.label,
            backgroundColor: "rgba(103, 58, 183, 0.2)",
            borderColor: "rgba(103, 58, 183, 0.8)",
            pointBorderColor: "rgba(103, 58, 183, 0.8)",
            pointBackgroundColor: "rgba(103, 58, 183, 0.4)",
            data: this.treeComSummary.map((o) => {
              return {
                x: Math.round(o.year * 10) / 10,
                y: o[this.select1.value],
              };
            }),
          },
        ],
      };
      this.loaded1 = true;
    },

    fillData2() {
      let idx = this.select2.value;
      this.chartData2 = {
        labels: this.treeComTurnover.map(
          (o) =>
            String(Math.round(o.t1 * 10) / 10) +
            "–" +
            String(Math.round(o.t2 * 10) / 10)
        ),
        datasets: [
          {
            label: this.headers2[idx].label,
            fill: false,
            data: this.treeComTurnover.map((o) => {
              return {
                x: Math.round(o.t2 * 10) / 10,
                y: o[this.headers2[idx].value],
              };
            }),
          },
          {
            label: this.headers2[idx + 1].label,
            fill: false,
            data: this.treeComTurnover.map((o) => {
              return {
                x: Math.round(o.t2 * 10) / 10,
                y: o[this.headers2[idx + 1].value],
              };
            }),
          },
          {
            label:
              this.headers2[idx].label + " - " + this.headers2[idx + 1].label,
            fill: false,
            data: this.treeComTurnover.map((o) => {
              return {
                x: Math.round(o.t2 * 10) / 10,
                y:
                  o[this.headers2[idx].value] - o[this.headers2[idx + 1].value],
              };
            }),
          },
        ],
      };
      this.loaded2 = true;
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
      let resArray = [];
      for (let i = 0; i < this.filters["species"].length; i++) {
        let subItems = this.treeSpSummary.filter(
          (e) => e.species === this.filters["species"][i]
        );
        resArray.push({
          label: this.filters["species"][i],
          fill: false,
          data: subItems.map((o) => {
            return {
              x: Math.round(o.year * 10) / 10,
              y: o[this.select3.value],
            };
          }),
        });
      }
      return resArray;
    },

    fillData3() {
      this.chartData3 = {
        labels: this.years,
        datasets: this.makeDatasetsSpecies(),
      };
      this.loaded3 = true;
    },
  },
};
</script>

<style lang="scss">
#btnGroup2 {
  text-transform: none;
}
</style>
