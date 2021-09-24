<template>
  <v-row justify="center">
    <v-col cols="12" sm="12" md="6" lg="6" xl="4" align-self="center">
      <v-card flat>
        <v-card-text v-if="plotSelected" class="text-center">
          <div class="text-h4 text--primary pb-2">
            {{ plotSelected ? plotSelected.site_name : '' }}
          </div>
          <div class="pb-4" style="font-size: 1.25em">
            {{ plotSelected ? plotSelected.plot_name_jp : '' }}
          </div>
          <div>
            {{
              plotSelected
                ? 'N' +
                  Math.round(plotSelected.lat * 1000) / 1000 +
                  '˚, E' +
                  Math.round(plotSelected.long * 1000) / 1000 +
                  '˚, ' +
                  plotSelected.ele +
                  ' m a.s.l.'
                : ''
            }}
          </div>
          <div>
            {{ plotSelected ? plotSelected.age : '' }}
          </div>
        </v-card-text>

        <v-card-text v-if="!plotSelected" class="text-center">
          <div class="text-h4 text--primary pb-4">MoniSenForest</div>
          <div>Application for analysing permanent forest plot</div>
          <div>observation data of the Monitoring Sites 1000.</div>
        </v-card-text>

        <v-select
          v-model="plotSelected"
          color="teal"
          :items="plotData"
          item-value="plot_id"
          label="Select Forest Plot"
          class="pa-4"
          clearable
          return-object
        >
          <template slot="item" slot-scope="data">
            {{ data.item.plot_id }} — {{ data.item.site_name }}
          </template>
          <template slot="selection" slot-scope="data">
            {{ data.item.plot_id }}
          </template>
        </v-select>

        <div v-if="plotSelected" class="text-center">
          <v-btn
            class="mx-2"
            outlined
            fab
            small
            color="teal"
            v-if="plotSelected.dtype.includes('treeGBH')"
            @click="$vuetify.goTo('#treeCensus')"
            v-bind="attrs"
            v-on="on"
          >
            <v-icon> mdi-pine-tree </v-icon>
          </v-btn>

          <v-btn
            class="mx-2"
            fab
            outlined
            small
            color="orange"
            v-if="plotSelected.dtype.includes('litter')"
            @click="$vuetify.goTo('#litterfall')"
            v-bind="attrs"
            v-on="on"
          >
            <v-icon> mdi-leaf </v-icon>
          </v-btn>

          <v-btn
            class="mx-2"
            fab
            outlined
            small
            color="deep-purple"
            v-if="plotSelected.dtype.includes('seed')"
            @click="$vuetify.goTo('#seedfall')"
          >
            <v-icon> mdi-seed </v-icon>
          </v-btn>
        </div>
      </v-card>
    </v-col>

    <v-col cols="12" sm="12" md="6" lg="6" xl="4" align-self="center">
      <v-card flat>
        <map-jp
          :plotSelected="plotSelected"
          :plotData="plotData"
          @plotMouseOver="onPlotMouseOver"
          @plotMouseOut="onPlotMouseOut"
          @plotClicked="onPlotClicked"
        ></map-jp>
        <v-tooltip
          bottom
          v-model="tooltip"
          :activator="`#${plotMouseOver ? plotMouseOver.plot_id : null}`"
        >
          <span class="font-weight-bold">
            {{ plotMouseOver ? plotMouseOver.plot_id : '' }}
          </span>
          <br />
          <span>{{ plotMouseOver ? plotMouseOver.site_name : '' }}</span>
        </v-tooltip>
      </v-card>
    </v-col>

    <v-col
      cols="12"
      v-if="plotSelected ? plotSelected.dtype.includes('treeGBH') : false"
    >
      <v-card flat tile class="grey lighten-4" id="treeCensus">
        <v-toolbar color="teal" dark>
          <v-toolbar-title>Tree Census Data Summary </v-toolbar-title>
          <v-spacer></v-spacer>
          <v-btn-toggle
            v-model="toggleSingleColTree"
            v-if="$vuetify.breakpoint.mdAndUp"
            dense
            group
          >
            <v-btn :value="true">
              <v-icon>mdi-view-sequential</v-icon>
            </v-btn>
            <v-btn :value="false">
              <v-icon>mdi-view-grid</v-icon>
            </v-btn>
          </v-btn-toggle>
        </v-toolbar>
        <v-container fluid>
          <v-subheader v-if="treeComSummaryData">Community Scale</v-subheader>
          <v-row>
            <v-col
              cols="12"
              sm="12"
              :md="toggleSingleColTree ? 12 : 6"
              :lg="toggleSingleColTree ? 12 : 6"
              :xl="toggleSingleColTree ? 12 : 6"
            >
              <v-card>
                <tree-com-summary
                  v-if="treeComSummaryData"
                  :data="treeComSummaryData"
                ></tree-com-summary>
              </v-card>
            </v-col>

            <v-col
              cols="12"
              sm="12"
              :md="toggleSingleColTree ? 12 : 6"
              :lg="toggleSingleColTree ? 12 : 6"
              :xl="toggleSingleColTree ? 12 : 6"
            >
              <v-card>
                <tree-com-turnover
                  v-if="treeComTurnoverData"
                  :data="treeComTurnoverData"
                ></tree-com-turnover>
              </v-card>
            </v-col>
          </v-row>

          <v-subheader v-if="treeSpSummaryData">Species Scale</v-subheader>
          <v-row>
            <v-col
              cols="12"
              sm="12"
              :md="toggleSingleColTree ? 12 : 6"
              :lg="toggleSingleColTree ? 12 : 6"
              :xl="toggleSingleColTree ? 12 : 6"
            >
              <v-card>
                <tree-sp-summary
                  v-if="treeSpSummaryData"
                  :data="treeSpSummaryData"
                  :toggleSingleCol="toggleSingleColTree"
                ></tree-sp-summary>
              </v-card>
            </v-col>

            <v-col
              cols="12"
              sm="12"
              :md="toggleSingleColTree ? 12 : 6"
              :lg="toggleSingleColTree ? 12 : 6"
              :xl="toggleSingleColTree ? 12 : 6"
            >
              <v-card>
                <tree-sp-turnover
                  v-if="treeSpTurnoverData"
                  :data="treeSpTurnoverData"
                  :toggleSingleCol="toggleSingleColTree"
                ></tree-sp-turnover>
              </v-card>
            </v-col>
          </v-row>
        </v-container>
      </v-card>
    </v-col>

    <v-col
      cols="12"
      v-if="plotSelected ? plotSelected.dtype.includes('litter') : false"
    >
      <v-card flat tile class="grey lighten-4" id="litterfall">
        <v-toolbar color="orange" dark>
          <v-toolbar-title>Litterfall Data Summary </v-toolbar-title>
          <v-spacer></v-spacer>
          <v-btn-toggle
            v-model="toggleSingleColLitter"
            v-if="$vuetify.breakpoint.mdAndUp"
            dense
            group
          >
            <v-btn :value="true">
              <v-icon>mdi-view-sequential</v-icon>
            </v-btn>
            <v-btn :value="false">
              <v-icon>mdi-view-grid</v-icon>
            </v-btn>
          </v-btn-toggle>
        </v-toolbar>
        <v-container fluid>
          <v-row>
            <v-col
              cols="12"
              sm="12"
              :md="toggleSingleColLitter ? 12 : 6"
              :lg="toggleSingleColLitter ? 12 : 6"
              :xl="toggleSingleColLitter ? 12 : 6"
            >
              <v-card>
                <litter-annual
                  v-if="litterAnnualData"
                  :data="litterAnnualData"
                ></litter-annual>
              </v-card>
            </v-col>

            <v-col
              cols="12"
              sm="12"
              :md="toggleSingleColLitter ? 12 : 6"
              :lg="toggleSingleColLitter ? 12 : 6"
              :xl="toggleSingleColLitter ? 12 : 6"
            >
              <v-card>
                <litter-each
                  v-if="litterEachData"
                  :data="litterEachData"
                ></litter-each>
              </v-card>
            </v-col>
          </v-row>
        </v-container>
      </v-card>
    </v-col>

    <v-col
      cols="12"
      v-if="plotSelected ? plotSelected.dtype.includes('seed') : false"
    >
      <v-card flat tile class="grey lighten-4" id="seedfall">
        <v-toolbar color="deep-purple" dark>
          <v-toolbar-title>Seedfall Data Summary </v-toolbar-title>
          <v-spacer></v-spacer>
          <v-btn-toggle
            v-model="toggleSingleColSeed"
            v-if="$vuetify.breakpoint.mdAndUp"
            dense
            group
          >
            <v-btn :value="true">
              <v-icon>mdi-view-sequential</v-icon>
            </v-btn>
            <v-btn :value="false">
              <v-icon>mdi-view-grid</v-icon>
            </v-btn>
          </v-btn-toggle>
        </v-toolbar>
        <v-container fluid>
          <v-row>
            <v-col
              cols="12"
              sm="12"
              :md="toggleSingleColSeed ? 12 : 6"
              :lg="toggleSingleColSeed ? 12 : 6"
              :xl="toggleSingleColSeed ? 12 : 6"
            >
              <v-card>
                <seed-annual
                  v-if="seedAnnualData"
                  :data="seedAnnualData"
                  :toggleSingleCol="toggleSingleColSeed"
                ></seed-annual>
              </v-card>
            </v-col>

            <v-col
              cols="12"
              sm="12"
              :md="toggleSingleColSeed ? 12 : 6"
              :lg="toggleSingleColSeed ? 12 : 6"
              :xl="toggleSingleColSeed ? 12 : 6"
            >
              <v-card> </v-card>
            </v-col>
          </v-row>
        </v-container>
      </v-card>
    </v-col>

    <div class="text-center">
      <v-bottom-sheet v-model="sheetEmpty">
        <v-sheet class="text-center" height="200px">
          <div class="py-6">No data has been loaded.</div>
          <v-btn text color="red" @click="$router.push('data')">
            Add Data
          </v-btn>
        </v-sheet>
      </v-bottom-sheet>
    </div>
  </v-row>
</template>

<script>
import axios from 'axios'

// Import components
import MapJp from '../components/Map'
import TreeComSummary from '../components/TreeComSummary.vue'
import TreeComTurnover from '../components/TreeComTurnover.vue'
import TreeSpSummary from '../components/TreeSpSummary.vue'
import TreeSpTurnover from '../components/TreeSpTurnover.vue'
import LitterAnnual from '../components/LitterAnnual.vue'
import LitterEach from '../components/LitterEach.vue'
import SeedAnnual from '../components/SeedAnnual.vue'

import plotInfo from '../assets/plot_info.json'
const BASE_URL = 'http://localhost:8000/api'

export default {
  components: {
    MapJp,
    TreeComSummary,
    TreeComTurnover,
    TreeSpSummary,
    TreeSpTurnover,
    LitterAnnual,
    LitterEach,
    SeedAnnual,
  },

  data: () => ({
    plotSelected: null,
    plotMouseOver: undefined,
    tooltip: false,
    dtypeIcons: {
      treeGBH: 'mdi-pine-tree',
      litter: 'mdi-leaf',
      seed: 'mdi-seed',
    },

    toggleSingleColTree: false,
    treeComSummaryData: null,
    treeComTurnoverData: null,
    treeSpSummaryData: null,
    treeSpTurnoverData: null,

    toggleSingleColLitter: false,
    litterAnnualData: null,
    litterEachData: null,

    toggleSingleColSeed: true,
    seedAnnualData: null,
    seedEachData: null,
  }),

  computed: {
    showGoToTop() {
      return this.offsetTop > 20
    },
    datafiles() {
      return this.$store.getters.allDatafiles
    },
    plotIdList() {
      // sort alphabetically
      return this.datafiles
        .map((e) => e.plot_id)
        .filter((element, index, self) => self.indexOf(element) === index)
        .sort()
    },
    plotDataType() {
      let arr = {}
      for (let i = 0; i < this.plotIdList.length; i++) {
        arr[this.plotIdList[i]] = this.datafiles
          .filter((e) => e.plot_id === this.plotIdList[i])
          .map((e) => e.dtype)
      }
      return arr
    },
    plotData() {
      return this.plotIdList.map((e) => {
        return {
          plot_id: e,
          site_name: plotInfo[e].site_name,
          plot_name_jp: plotInfo[e].plot_name,
          long: plotInfo[e].long,
          lat: plotInfo[e].lat,
          ele: plotInfo[e].ele,
          age: plotInfo[e].age,
          dtype: this.plotDataType[e],
        }
      })
    },
    sheetEmpty() {
      return this.$store.getters.getEmpty
    },
  },

  watch: {
    plotSelected() {
      this.readData()
    },
  },

  methods: {
    readData() {
      if (this.plotSelected) {
        if (this.plotSelected.dtype.includes('treeGBH')) {
          this.readTreeCensusData()
        }

        if (this.plotSelected.dtype.includes('litter')) {
          this.readLitterfallData()
        }
        if (this.plotSelected.dtype.includes('seed')) {
          this.readSeedfallData()
        }
      }
    },

    async readTreeComSummary() {
      axios
        .get(
          BASE_URL + '/tree_com_summary/?plot_id=' + this.plotSelected.plot_id
        )
        .then((response) => {
          this.treeComSummaryData =
            response.data.length > 0 ? response.data : null
        })
        .catch((error) => {
          this.treeComSummaryData = null
          console.log(error)
        })
    },

    async readTreeComTurnover() {
      axios
        .get(
          BASE_URL + '/tree_com_turnover/?plot_id=' + this.plotSelected.plot_id
        )
        .then((response) => {
          this.treeComTurnoverData =
            response.data.length > 0 ? response.data : null
        })
        .catch((error) => {
          this.treeComTurnoverData = null
          console.log(error)
        })
    },

    async readTreeSpSummary() {
      axios
        .get(
          BASE_URL + '/tree_sp_summary/?plot_id=' + this.plotSelected.plot_id
        )
        .then((response) => {
          this.treeSpSummaryData =
            response.data.length > 0 ? response.data : null
        })
        .catch((error) => {
          this.treeSpSummaryData = null
          console.log(error)
        })
    },

    async readTreeSpTurnover() {
      axios
        .get(
          BASE_URL + '/tree_sp_turnover/?plot_id=' + this.plotSelected.plot_id
        )
        .then((response) => {
          this.treeSpTurnoverData =
            response.data.length > 0 ? response.data : null
        })
        .catch((error) => {
          this.treeSpTurnoverData = null
          console.log(error)
        })
    },

    async readLitterEach() {
      axios
        .get(BASE_URL + '/litter_each/?plot_id=' + this.plotSelected.plot_id)
        .then((response) => {
          this.litterEachData = response.data.length > 0 ? response.data : null
        })
        .catch((error) => {
          this.litterEachData = null
          console.log(error)
        })
    },

    async readLitterAnnual() {
      axios
        .get(BASE_URL + '/litter_annual/?plot_id=' + this.plotSelected.plot_id)
        .then((response) => {
          this.litterAnnualData =
            response.data.length > 0 ? response.data : null
        })
        .catch((error) => {
          this.litterAnnualData = null
          console.log(error)
        })
    },

    async readSeedEach() {
      axios
        .get(BASE_URL + '/seed_each/?plot_id=' + this.plotSelected.plot_id)
        .then((response) => {
          this.seedEachData = response.data.length > 0 ? response.data : null
        })
        .catch((error) => {
          this.seedEachData = null
          console.log(error)
        })
    },

    async readSeedAnnual() {
      axios
        .get(BASE_URL + '/seed_annual/?plot_id=' + this.plotSelected.plot_id)
        .then((response) => {
          this.seedAnnualData = response.data.length > 0 ? response.data : null
        })
        .catch((error) => {
          this.seedAnnualData = null
          console.log(error)
        })
    },

    async readTreeCensusData() {
      await this.readTreeComSummary()
      await this.readTreeComTurnover()
      await this.readTreeSpSummary()
      await this.readTreeSpTurnover()
    },

    async readLitterfallData() {
      await this.readLitterEach()
      await this.readLitterAnnual()
    },

    async readSeedfallData() {
      await this.readSeedEach()
      await this.readSeedAnnual()
    },

    onPlotMouseOver(plot_id) {
      this.tooltip = true
      this.plotMouseOver = this.plotData.filter((e) => e.plot_id === plot_id)[0]
    },

    onPlotMouseOut() {
      this.tooltip = false
      this.plotMouseOver = undefined
    },

    onPlotClicked(plot_id) {
      this.plotSelected = this.plotData.filter((e) => e.plot_id === plot_id)[0]
    },
  },
}
</script>

<style lang="scss">
.v-data-table {
  white-space: nowrap;
}
.fade-enter-active,
.fade-leave-active {
  transition: 0.5s;
}
.fade-enter,
.fade-leave-to {
  opacity: 0;
  transform: scale(0);
}
</style>
