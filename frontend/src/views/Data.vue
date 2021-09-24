<template>
  <v-row>
    <v-col cols="12">
      <v-card>
        <v-toolbar flat>
          <v-card-title>Data Manager</v-card-title>
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

          <v-progress-linear
            :active="loading"
            :indeterminate="loading"
            absolute
            bottom
            color="teal accent-4"
          ></v-progress-linear>
        </v-toolbar>

        <v-data-table
          v-model="selectedData"
          :headers="headers"
          :items="datafiles"
          :search="search"
          class="elevation-0"
          sort-by="plot_id"
          show-select
        >
          <template v-slot:top>
            <v-dialog
              v-model="dialogDelete"
              max-width="550px"
              v-if="selectedData.length > 0"
            >
              <template v-slot:activator="{ on, attrs }">
                <v-btn
                  color="pink"
                  class="ma-3 white--text"
                  :disabled="loading"
                  v-bind="attrs"
                  v-on="on"
                >
                  <v-icon left dark>mdi-delete</v-icon>
                  Delete
                </v-btn>
              </template>
              <v-card>
                <v-card-title class="justify-center">
                  Are you sure you want to delete
                  {{ selectedData.length > 1 ? 'these files?' : 'this file?' }}
                </v-card-title>
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn color="teal" text @click="closeDialogDelete">
                    Cancel
                  </v-btn>
                  <v-btn color="teal" text @click="deleteFiles"> OK </v-btn>
                  <v-spacer></v-spacer>
                </v-card-actions>
              </v-card>
            </v-dialog>

            <v-dialog v-model="dialog" max-width="550px" v-else>
              <template v-slot:activator="{ on, attrs }">
                <v-btn
                  color="teal"
                  class="ma-3 white--text"
                  :disabled="loading"
                  v-bind="attrs"
                  v-on="on"
                >
                  <v-icon left dark> mdi-plus </v-icon>
                  Add
                </v-btn>
              </template>
              <v-card class="pa-2">
                <v-card-text>
                  <template>
                    <v-file-input
                      v-model="selectedFiles"
                      label="File input"
                      color="teal"
                      multiple
                    ></v-file-input>
                  </template>
                  <small class="grey--text">
                    * Acceptable file format is .xlsx and .csv
                  </small>
                </v-card-text>

                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn color="teal" text @click="closeDialog"> Cancel </v-btn>
                  <v-btn text color="teal" @click="submitFiles"> Submit </v-btn>
                  <v-spacer></v-spacer>
                </v-card-actions>
              </v-card>
            </v-dialog>
          </template>

          <template v-slot:item.dtype="{ item }">
            {{ item.dtype.charAt(0).toUpperCase() + item.dtype.slice(1) }}
          </template>
        </v-data-table>

        <v-dialog v-model="dialogUpdate" persistent max-width="550px">
          <v-card>
            <v-card-title class="justify-center">
              {{ updateData ? updateData.message : '' }}
            </v-card-title>
            <v-card-text class="text-center">
              Do you want to update?
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="teal darken-1" text @click="updateDataCancel">
                Cancel
              </v-btn>
              <v-btn color="teal darken-1" text @click="updateDataConfirm">
                OK
              </v-btn>
              <v-checkbox
                class="my-checkbox"
                v-if="updateList.length > 0"
                v-model="applyToAll"
                label="Apply to all"
                color="teal darken-1"
              ></v-checkbox>

              <v-spacer></v-spacer>
            </v-card-actions>
          </v-card>
        </v-dialog>

        <v-dialog v-model="dialogError" max-width="550px">
          <v-card>
            <v-card-title class="justify-center">{{
              errorMessage
            }}</v-card-title>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="teal darken-1" text @click="closeDialogError"
                >OK</v-btn
              >
              <v-spacer></v-spacer>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
import axios from 'axios'

const BASE_URL = 'http://localhost:8000/api'

export default {
  data() {
    return {
      dialog: false,
      dialogDelete: false,
      dialogUpdate: false,
      dialogError: false,
      loading: false,
      applyToAll: false,
      headers: [
        {
          text: 'Plot ID',
          align: 'start',
          value: 'plot_id',
        },
        { text: 'Site Name', value: 'name' },
        { text: 'File Name', value: 'filename' },
        { text: 'Data Type', value: 'dtype' },
        { text: 'Date Created', value: 'date' },
        { text: 'File Size (KB)', value: 'size' },
      ],
      updateData: null,
      updateList: [],
      errorMessage: '',
      errorList: [],
      selectedFiles: [],
      selectedData: [],
      search: '',
      onSearch: false,
    }
  },

  computed: {
    datafiles() {
      return this.$store.getters.allDatafiles
    },
  },

  watch: {
    dialog(val) {
      val || this.closeDialog()
    },

    dialogDelete(val) {
      val || this.closeDialogDelete()
    },

    dialogError(val) {
      val || this.closeDialogError()
    },

    loading(val) {
      if (!val) return
    },
  },

  methods: {
    async submitFile(formData) {
      return axios
        .post(BASE_URL + '/datafiles/upload/', formData)
        .then((response) => {
          console.log(response.data.filename + ' has been successfully loaded.')
          return 0
        })
        .catch((err) => {
          console.log(err)
          if (err.response.status == 400) {
            this.updateList.push(err.response.data)
            return 1
          } else {
            this.errorList.push(err.response.data.detail)
            return 2
          }
        })
    },

    async submitFiles() {
      this.dialog = false
      if (this.selectedFiles.length > 0) {
        this.loading = true
        let promiseArray = this.selectedFiles.map((file) => {
          let formData = new FormData()
          formData.append('file', file)
          return this.submitFile(formData)
        })
        await Promise.all(promiseArray)
        this.$store.dispatch('getDatafiles')
        this.loading = false
        if (this.updateList.length > 0) {
          this.updateDataAsk()
        } else if (this.errorList.length > 0) {
          this.showDialogError()
        }
      }
    },

    closeDialog() {
      this.dialog = false
      this.selectedFiles = []
    },

    deleteFile(index) {
      return axios.delete(BASE_URL + '/datafiles/' + index + '/')
    },

    async deleteFiles() {
      this.dialogDelete = false
      if (this.selectedData.length > 0) {
        this.loading = true
        let promiseArray = this.selectedData.map((e) => {
          return this.deleteFile(e.id)
        })
        let results = await Promise.all(promiseArray)
        results.forEach((e) => console.log(e.data.message))
        this.$store.dispatch('getDatafiles')
        this.selectedData = []
        this.loading = false
      }
    },

    closeDialogDelete() {
      this.dialogDelete = false
    },

    updateDataAsk() {
      this.updateData = this.updateList.pop()
      if (this.applyToAll) {
        this.updateDataConfirm()
      } else {
        this.dialogUpdate = true
      }
    },

    async updateDataConfirm() {
      this.loading = true
      this.dialogUpdate = false
      let response = await axios.put(
        BASE_URL + '/datafiles/' + this.updateData.id + '/',
        this.updateData.data
      )
      console.log(response.data.message)
      this.$store.dispatch('getDatafiles')
      this.loading = false
      if (this.updateList.length > 0) {
        this.updateDataAsk()
      } else {
        this.updateData = null
        this.applyToAll = false
        if (this.errorList.length > 0) {
          this.showDialogError()
        }
      }
    },

    updateDataCancel() {
      this.dialogUpdate = false
      if (this.applyToAll) {
        this.updateData = null
        this.updateList = []
        this.applyToAll = false
        if (this.errorList.length > 0) {
          this.showDialogError()
        }
      } else if (this.updateList.length > 0) {
        this.updateDataAsk()
      } else {
        this.updateData = null
        if (this.errorList.length > 0) {
          this.showDialogError()
        }
      }
    },

    showDialogError() {
      this.errorMessage = this.errorList.pop()
      this.dialogError = true
    },

    closeDialogError() {
      this.dialogError = false
      if (this.errorList.length > 0) {
        this.showDialogError()
      } else {
        this.errorMessage = ''
      }
    },
  },
}
</script>

<style>
.my-checkbox .v-label {
  font-size: 14px;
}
</style>
