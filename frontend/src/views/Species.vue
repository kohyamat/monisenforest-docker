<template>
  <v-row justify="center">
    <v-col cols="12" sm="12" md="8" lg="5" xl="4" v-if="showOccurrenceMap">
      <v-card flat>
        <v-card-title class="justify-center"
          >Species Occurrence Map</v-card-title
        >
        <v-card-subtitle class="text-center" pt-2>
          <span class="font-italic">
            {{ spSelected.length > 0 ? spSelected[0].species : "" }}
          </span>
          <span>
            {{
              spSelected.length > 0
                ? " — " + spSelected[0].name_jp
                : "Not selected"
            }}
          </span>
        </v-card-subtitle>
        <map-jp
          :plotData="plotData"
          @plotMouseOver="onPlotMouseOver"
          @plotMouseOut="onPlotMouseOut"
        >
        </map-jp>
        <v-tooltip
          bottom
          v-model="tooltip"
          :activator="`#${plotMouseOver ? plotMouseOver.plot_id : null}`"
        >
          <span class="font-weight-bold">
            {{ plotMouseOver ? plotMouseOver.plot_id : "" }}
          </span>
          <br />
          <span>{{ plotMouseOver ? plotMouseOver.site_name : "" }}</span>
        </v-tooltip>
      </v-card>
    </v-col>

    <v-col
      cols="12"
      sm="12"
      md="12"
      :lg="showOccurrenceMap ? 7 : 12"
      :xl="showOccurrenceMap ? 8 : 12"
    >
      <v-card>
        <v-toolbar flat>
          <v-card-title>Species List</v-card-title>
          <v-spacer></v-spacer>
          <v-text-field
            v-model="search"
            label="Search"
            append-icon="mdi-magnify"
            outlined
            rounded
            flat
            dense
            single-line
            hide-details
          >
          </v-text-field>
        </v-toolbar>

        <v-data-table
          v-model="spSelected"
          :headers="headers"
          :items="spList"
          :search="search"
          class="elevation-0"
          item-key="name_jp"
          :show-select="showOccurrenceMap"
          single-select
          single-expand
        >
          <template v-slot:top>
            <v-switch
              v-model="showOccurrenceMap"
              label="Show occurrence map"
              class="pa-3"
              color="teal"
            ></v-switch>
          </template>
        </v-data-table>

        <v-card-text class="grey--text">
          * This species list is based on tree census data only; it does not
          cover all of the species that may appear in the seedfall data.
        </v-card-text>

        <v-card-actions class="px-2">
          <v-btn color="teal" text @click="showRef = !showRef">
            References
          </v-btn>

          <v-spacer></v-spacer>

          <v-btn icon @click="showRef = !showRef">
            <v-icon>
              {{ showRef ? "mdi-chevron-up" : "mdi-chevron-down" }}
            </v-icon>
          </v-btn>
        </v-card-actions>
        <v-divider v-show="showRef"></v-divider>
        <v-card-text v-show="showRef">
          <ol>
            <li class="py-2" v-for="(item, index) in references" :key="index">
              {{ item.author }} ({{ item.year }}) {{ item.title }}.
              <span class="font-italic">{{ item.journal }}</span
              >{{ item.pages ? ", " + item.pages : "" }}.
              <a
                :href="item.doi"
                target="_blank"
                style="text-decoration: none"
                class="teal--text"
              >
                {{ item.doi }}
              </a>
            </li>
          </ol>
        </v-card-text>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
import axios from "axios";

import MapJp from "../components/Map";

import spInfo from "../assets/species_dict.json";
import plotInfo from "../assets/plot_info.json";

const BASE_URL = "http://localhost:8000/api";

export default {
  components: {
    MapJp,
  },

  data() {
    return {
      spList: [],
      search: "",
      tooltip: false,
      showOccurrenceMap: false,
      headers: [
        { text: "Japanese name", value: "name_jp" },
        { text: "Species", value: "species" },
        { text: "Family", value: "family" },
        { text: "Order", value: "order" },
        { text: "Type", value: "ft" },
        { text: "Wood Density", value: "wd" },
        { text: "Wood Density Ref.", value: "ref" },
      ],

      showRef: false,
      references: [
        {
          author:
            "Aiba M, Kurokawa H, Onoda Y, Oguro M, Nakashizuka T & Masaki T",
          year: "2016",
          title:
            "Context‐dependent changes in the functional composition of tree communities along successional gradients after land‐use change",
          journal: "Journal of Ecology",
          pages: "104: 1347-1356",
          doi: "https://doi.org/10.1111/1365-2745.12597",
        },
        {
          author:
            "Zanne AE, Lopez-Gonzalez G, Coomes, DA, Ilic J, Jansen S, Lewis SL, Miller RB, Swenson NG, Wiemann MC & Chave J",
          year: "2009",
          title: "Data from: Towards a worldwide wood economics spectrum",
          journal: "Dryad, Dataset",
          pages: "",
          doi: "https://doi.org/10.5061/dryad.234",
        },
      ],

      spSelected: [],
      plotData: [],
    };
  },

  mounted() {
    axios.get(BASE_URL + "/species/list/").then((response) => {
      let spListLoaded = response.data.map((e) => e.name_jp);
      Object.keys(spInfo).forEach((key) => {
        let ft = {
          1: "Sub-boreal conifer",
          2: "Temperate conifer",
          4: "Deciduous broadleaf",
          5: "Evergreen broadleaf",
        };
        if (
          spListLoaded.includes(key) &&
          spInfo[key].scientific_name_full != "" &&
          spInfo[key].categ5 == 1
        ) {
          this.spList.push({
            name_jp: key,
            species: spInfo[key].species,
            family: spInfo[key].family,
            order: spInfo[key].order,
            wd: spInfo[key].wood_density
              ? Math.round(spInfo[key].wood_density * 1000) / 1000
              : "n/a",
            ref: spInfo[key].wood_density_ref,
            ft: spInfo[key].categ4 != 1 ? ft[spInfo[key].categ3] : "Tree fern",
          });
        }
      });
    });
  },

  watch: {
    spSelected() {
      if (this.spSelected.length > 0) {
        this.onSelected();
      } else {
        this.plotData = [];
      }
    },
  },

  methods: {
    onSelected() {
      axios
        .get(
          BASE_URL +
            "/species/occurrence/?species=" +
            this.spSelected[0].species
        )
        .then((response) => {
          this.plotData = response.data.map((e) => {
            return {
              plot_id: e,
              site_name: plotInfo[e].site_name,
              plot_name_jp: plotInfo[e].plot_name,
              long: plotInfo[e].long,
              lat: plotInfo[e].lat,
              circleSize: 2.5,
              circleColor: "rgba(0, 121, 107, 0.8)",
            };
          });
        });
    },

    onPlotMouseOver(plot_id) {
      this.tooltip = true;
      this.plotMouseOver = this.plotData.filter(
        (e) => e.plot_id === plot_id
      )[0];
    },

    onPlotMouseOut() {
      this.tooltip = false;
      this.plotMouseOver = undefined;
    },
  },
};
</script>
