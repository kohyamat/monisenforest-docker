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
                  {{ selectedData.length > 1 ? "these files?" : "this file?" }}
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
                  <v-btn color="teal" text @click="closeDialog"> Cancel </v-btn>
                  <v-btn text color="teal" @click="submitFiles"> Submit </v-btn>
                </v-card-actions>
              </v-card>
            </v-dialog>
          </template>

          <template v-slot:item.dtype="{ item }">
            {{ item.dtype.charAt(0).toUpperCase() + item.dtype.slice(1) }}
          </template>
        </v-data-table>

        <v-dialog v-model="dialogUpdate" max-width="550px">
          <v-card>
            <v-card-title class="justify-center">
              {{ updateMessage }}
            </v-card-title>
            <v-card-text class="text-center">
              Do you want to update?
            </v-card-text>
            <v-card-actions>
              <v-btn color="teal darken-1" text @click="closeDialogUpdate">
                Cancel
              </v-btn>
              <v-btn color="teal darken-1" text @click="updateDataConfirm">
                OK
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>

        <v-dialog v-model="dialogError" max-width="550px">
          <v-card>
            <v-card-text class="text-center">{{ errorMessage }}</v-card-text>
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
import axios from "axios";

const BASE_URL = "http://localhost:8000/api";

export default {
  data() {
    return {
      dialog: false,
      dialogDelete: false,
      dialogUpdate: false,
      dialogError: false,
      loading: false,
      headers: [
        {
          text: "Plot ID",
          align: "start",
          value: "plot_id",
        },
        { text: "Site Name", value: "name" },
        { text: "File Name", value: "filename" },
        { text: "Data Type", value: "dtype" },
        { text: "Date Created", value: "date" },
        { text: "File Size (KB)", value: "size" },
      ],
      editIndex: -1,
      updateData: null,
      updateMessage: "",
      errorMessage: "",
      selectedFiles: [],
      selectedData: [],
      search: "",
      onSearch: false,
    };
  },

  computed: {
    datafiles() {
      return this.$store.getters.allDatafiles;
    },
  },

  watch: {
    dialog(val) {
      val || this.closeDialog();
    },

    dialogDelete(val) {
      val || this.closeDialogDelete();
    },

    dialogUpdate(val) {
      val || this.closeDialogUpdate();
    },

    loading(val) {
      if (!val) return;
    },
  },

  methods: {
    async submitFile(formData) {
      return axios
        .post(BASE_URL + "/datafiles/upload/", formData)
        .then((response) => {
          console.log(response.data.message);
        })
        .catch((err) => {
          console.log(err);
          if (err.response.status == 400) {
            this.updateMessage = err.response.data["message"];
            this.editIndex = err.response.data["id"];
            this.updateData = err.response.data["data"];
            this.dialogUpdate = true;
          } else {
            this.dialogError = true;
            this.errorMessage = err.response.data["detail"];
          }
        });
    },

    submitFiles() {
      this.dialog = false;
      if (this.selectedFiles.length > 0) {
        this.loading = true;
        Promise.all(
          this.selectedFiles.map(async (file) => {
            let formData = new FormData();
            formData.append("file", file);
            await this.submitFile(formData);
          })
        ).then(() => {
          this.$store.dispatch("getDatafiles");
          this.loading = false;
        });
      }
    },

    closeDialog() {
      this.dialog = false;
      this.selectedFiles = [];
    },

    async deleteFile(index) {
      axios.delete(BASE_URL + "/datafiles/" + index + "/").then((response) => {
        console.log(response.data.message);
      });
    },

    deleteFiles() {
      this.dialogDelete = false;
      if (this.selectedData.length > 0) {
        this.loading = true;
        Promise.all(
          this.selectedData.map(async (d) => {
            await this.deleteFile(d.id);
          })
        ).then(() => {
          this.$store.dispatch("getDatafiles");
          this.selectedData = [];
          this.loading = false;
        });
      }
    },

    closeDialogDelete() {
      this.dialogDelete = false;
    },

    updateDataConfirm() {
      this.dialogUpdate = false;
      this.loading = true;
      axios
        .put(BASE_URL + "/datafiles/" + this.editIndex + "/", this.updateData)
        .then((response) => {
          console.log(response.data.message);
          this.$store.dispatch("getDatafiles");
          this.closeDialogUpdate();
          this.loading = false;
        });
    },

    closeDialogUpdate() {
      this.dialogUpdate = false;
      this.$nextTick(() => {
        this.updateData = null;
        this.updateMessage = "";
        this.editIndex = -1;
      });
    },

    closeDialogError() {
      this.dialogError = false;
      this.$nextTick(() => {
        this.errorMessage = "";
      });
    },
  },
};
</script>
