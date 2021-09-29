<template>
  <v-row justify="center">
    <v-col cols="12" sm="10" md="8" lg="8" xl="8">
      <v-sheet>
        <v-layout justify-center>
          <v-img src="@/assets/logo.png" max-width="144"> </v-img>
        </v-layout>
        <div class="text-h2 py-6" style="text-align: center">MoniSenForest</div>
        <p class="text-body-1" style="text-align: center">
          Data summarization and visualization tool for permanent forest plot
          observations (tree census and litterfall survey) of the Monitoring
          Site 1000.
        </p>

        <div class="text-h4 py-6">About Monitoring Sites 1000</div>
        <p class="text-body-1">
          The
          <a
            href="https://www.biodic.go.jp/moni1000/"
            target="_blank"
            style="text-decoration: none"
          >
            <span class="font-weight-bold teal--text"
              >Monitoring Sites 1000</span
            >
            <v-icon x-small color="teal">mdi-open-in-new</v-icon> </a
          >, also called 'moni1000' or 'moni-sen', is a nationwide ecosystem
          monitoring project in Japan led by the Ministry of the Environment.
          The monitoring covers a wide range of ecosystems, including alpine
          areas, forests, grasslands, satoyama, lakes, marshes, coastal areas,
          coral reefs, and small islands. Since the launch of the project in
          2003, a massive amount of observation data has been accumulated with
          the cooperation of researchers and citizens. Permanent forest plot
          observations have been conducted as part of the
          <a
            href="http://moni1000-forest.jwrc.or.jp"
            target="_blank"
            style="text-decoration: none"
          >
            <span class="font-weight-bold teal--text"
              >Forests & Grasslands Survey</span
            >
            <v-icon x-small color="teal">mdi-open-in-new</v-icon>
          </a>
          of the project.
        </p>

        <div class="text-h5 py-6">Datasets of the Monitoring Sites 1000</div>
        <p class="text-body-1">
          The data collected by the Monitoring Sites 1000 project is publicly
          available and can be be found
          <a
            href="https://www.biodic.go.jp/moni1000/findings/data/"
            target="_blank"
            style="text-decoration: none"
            ><span class="font-weight-bold teal--text">here</span
            ><v-icon x-small color="teal">mdi-open-in-new</v-icon></a
          >. Tree census data and litterfall monitoring data can be obtained
          from the following:
        </p>
        <ul class="text-body-1">
          <li class="py-2">
            <a
              href="https://www.biodic.go.jp/moni1000/findings/data/index_file.html"
              target="_blank"
              style="text-decoration: none"
            >
              <span class="font-weight-bold teal--text">Tree census data</span>
              <v-icon x-small color="teal"> mdi-open-in-new </v-icon>
            </a>
            from 61 forest plots (ca. 1 ha each) in 49 sites in Japan (Ishihara
            et al. 2011).
          </li>
          <li class="py-2">
            <a
              href="https://www.biodic.go.jp/moni1000/findings/data/index_file_LitterSeed.html"
              target="_blank"
              style="text-decoration: none"
            >
              <span class="font-weight-bold teal--text"
                >Litterfall and seedfall monitoring data</span
              >

              <v-icon x-small color="teal"> mdi-open-in-new </v-icon>
            </a>
            from 21 forest plots in 20 sites in Japan (Suzuki et al. 2012).
          </li>
        </ul>

        <div class="text-h4 py-6">Technical Notes</div>
        <p class="text-body-1">
          <span class="font-weight-bold">Biomass estimaion</span> — Above ground
          biomass of trees was estimated using the generic allometric equations
          of Ishihara et al. (2015). Basically, stem diameter at breast height
          and species-specific wood density (Aiba et al. 2016; Zanne et al.
          2009) were used for estimation. Genus or family averages of wood
          density were used when species-specific data were not available, and
          when even these were not available, life form-specific allometric
          equations were fitted.
        </p>

        <p class="text-body-1">
          <span class="font-weight-bold">Turnover rates estimaion</span> —
          Species-level turnover rates (mortality, recruitment, aboveground
          biomass productivity and loss rates) were estimated based on the
          biomass of trees at each census and their inter-census fates
          (survival, recruitment, or death). Community-wide turnover rates were
          then calculated as a weighted average of the species turnover rates as
          described in Kohyama et al. (2018, 2019).
        </p>

        <div class="text-h4 py-6">References</div>
        <ol>
          <li class="py-2" v-for="(item, index) in references" :key="index">
            {{ item.author }} ({{ item.year }}) {{ item.title }}.
            <span class="font-italic">{{ item.journal }}</span
            >{{ item.pages ? ', ' + item.pages : '' }}.
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

        <p class="text-body-1 py-6"></p>
      </v-sheet>
    </v-col>
  </v-row>
</template>

<script>
export default {
  data() {
    return {
      references: [
        {
          author:
            'Ishihara MI, Suzuki SN, Nakamura M, Enoki T, Fujiwara A, Hiura T, Homma K, Hoshino D, Hoshizaki K, Ida H, Ishida K, Itoh A, Kaneko T, Kubota K, Kuraji K, Kuramoto S, Makita A, Masaki T, Namikawa K, Niiyama K, Noguchi M, Nomiya H, Ohkubo T, Saito S, Sakai T, Sakimoto M, Sakio H, Shibano H, Sugita H, Suzuki M, Takashima A, Tanaka N, Tashiro N, Tokuchi N, Yakushima Forest Environment Conservation Center, Yoshida T & Yoshida Y',
          year: '2011',
          title:
            'Forest stand structure, composition, and dynamics in 34 sites over Japan',
          journal: 'Ecological Research',
          pages: '26: 1007-1008',
          doi: 'https://doi.org/10.1007/s11284-011-0847-y',
        },
        {
          author:
            'Suzuki SN, Ishihara MI, Nakamura M, Abe S, Hiura T, Homma K, Higa M, Hoshino D, Hoshizaki K, Ida H, Ishida K, Kawanishi M, Kobayashi K, Kuraji K, Kuramoto S, Masaki T, Niiyama K, Noguchi M, Nomiya H, Saito S, Sakai T, Sakimoto M, Sakio H, Sato T, Shibano H, Shibata M, Suzuki M, Takashima A, Tanaka H, Takagi M, Tashiro N, Tokuchi N, Yoshida T & Yoshida Y',
          year: '2012',
          title:
            'Nation‐wide litter fall data from 21 forests of the Monitoring Sites 1000 Project in Japan',
          journal: 'Ecological Research',
          pages: '27: 989-990',
          doi: 'https://doi.org/10.1007/s11284-012-0980-2',
        },
        {
          author:
            'Ishihara MI, Utsugi H, Tanouchi H, Aiba M, Kurokawa H, Onoda Y, Nagano M, Umehara T, Ando M, Miyata R & Hiura T',
          year: '2015',
          title:
            'Efficacy of generic allometric equations for estimating biomass: a test in Japanese natural forests',
          journal: 'Ecological Applications',
          pages: '25: 1433-1446',
          doi: 'https://doi.org/10.1890/14-0175.1',
        },
        {
          author:
            'Aiba M, Kurokawa H, Onoda Y, Oguro M, Nakashizuka T & Masaki T',
          year: '2016',
          title:
            'Context‐dependent changes in the functional composition of tree communities along successional gradients after land‐use change',
          journal: 'Journal of Ecology',
          pages: '104: 1347-1356',
          doi: 'https://doi.org/10.1111/1365-2745.12597',
        },
        {
          author:
            'Zanne AE, Lopez-Gonzalez G, Coomes, DA, Ilic J, Jansen S, Lewis SL, Miller RB, Swenson NG, Wiemann MC & Chave J',
          year: '2009',
          title: 'Data from: Towards a worldwide wood economics spectrum',
          journal: 'Dryad, Dataset',
          pages: '',
          doi: 'https://doi.org/10.5061/dryad.234',
        },
        {
          author: 'Kohyama TS, Kohyama TI & Sheil D',
          year: '2018',
          title:
            'Definition and estimation of vital rates from repeated censuses: Choices, comparisons and bias corrections focusing on trees',
          journal: 'Methods in Ecology and Evolution',
          pages: '9: 809-821',
          doi: 'https://doi.org/10.1111/2041-210X.12929',
        },
        {
          author: 'Kohyama TS, Kohyama TI & Sheil D',
          year: '2019',
          title:
            'Estimating net biomass production and loss from repeated measurements of trees in forests and woodlands: Formulae, biases and recommendations',
          journal: 'Forest Ecology and Management',
          pages: '433: 729-740',
          doi: 'https://doi.org/10.1016/j.foreco.2018.11.010',
        },
      ],
    }
  },
}
</script>
