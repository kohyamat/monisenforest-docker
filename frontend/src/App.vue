<template>
  <v-app>
    <v-app-bar app color="teal" dark>
      <!-- App bar -->
      <v-app-bar-nav-icon @click.stop="drawer = !drawer"></v-app-bar-nav-icon>

      <v-toolbar-title>
        <router-link
          to="/"
          class="toolbar-title"
          style="text-decoration: none; color: inherit"
        >
          MoniSenForest
        </router-link>
      </v-toolbar-title>

      <v-spacer></v-spacer>

      <v-btn icon href="https://github.com/MoniSenNC/MoniSenForest">
        <v-icon> mdi-github </v-icon>
      </v-btn>
    </v-app-bar>

    <!-- Navigation drawer -->
    <v-navigation-drawer v-model="drawer" app temporary bottom>
      <v-list>
        <v-list-item two-line>
          <v-list-item-avatar>
            <img src="@/assets/logo.png" />
          </v-list-item-avatar>

          <v-list-item-content>
            <v-list-item-title class="title"> MoniSenForest </v-list-item-title>
            <v-list-item-subtitle> version 0.1.0 </v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>

        <v-divider></v-divider>

        <v-list-item
          v-for="item in items"
          :key="item.title"
          :to="item.path"
          link
          color="teal"
        >
          <v-list-item-icon>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            {{ item.title }}
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-main>
      <!-- Provides the application the proper gutter -->
      <v-container fluid>
        <router-view></router-view>
      </v-container>
    </v-main>

    <v-footer padless>
      <v-card flat tile width="100%" class="text-center pt-4">
        <v-row class="pa-0 ma-0 justify-center">
          <v-col class="text-center" cols="12">
            <v-btn
              v-for="item in items"
              :key="item"
              :to="item.path"
              color="teal"
              text
              dense
              rounded
              class="px-4"
            >
              {{ item.title }}
            </v-btn>
          </v-col>
        </v-row>
        <v-card-text class="py-4 text-center">
          Released under the
          <a
            class="teal--text"
            href="https://github.com/MoniSenNC/MoniSenForest/blob/main/LICENSE"
            style="text-decoration: none"
            >MIT license</a
          ><br />
          Copyright © 2020–{{ new Date().getFullYear() }} Tetsuo Kohyama
        </v-card-text>
      </v-card>
    </v-footer>
  </v-app>
</template>

<script>
export default {
  data() {
    return {
      drawer: null,
      items: [
        {
          title: "Overview",
          icon: "mdi-view-dashboard",
          path: "/",
        },
        {
          title: "Data Manager",
          icon: "mdi-file-table",
          path: "/Data",
        },
        {
          title: "Species List",
          icon: "mdi-view-list",
          path: "/Species",
        },
        {
          title: "About",
          icon: "mdi-information",
          path: "/about",
        },
      ],
    };
  },

  mounted() {
    try {
      this.$store.dispatch("getPlots");
    } catch (e) {
      (e) => console.log("Error" + e.message);
    }
  },

  methods: {},
};
</script>

<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}
</style>