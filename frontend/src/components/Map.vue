<template>
  <div id="container" class="svg-container"></div>
</template>

<script>
import * as d3 from "d3";
import feature from "topojson-client/src/feature";

export default {
  props: ["plotData", "plotSelected"],

  data: () => ({
    width: 400,
    height: 400,
  }),

  mounted() {
    this.scale = this.width * 2;
    this.projection = d3
      .geoMercator()
      .center([135.5, 35.4])
      .translate([this.width / 2, this.height / 2])
      .scale(this.scale);

    this.svg = d3
      .select("div#container")
      .append("svg")
      .attr("preserveAspectRatio", "xMinYMin meet")
      .attr("viewBox", "0 0 400 400")
      .classed("svg-content", true)
      .attr("height", "100%")
      .attr("id", "map-svg");

    this.generateMap();
  },

  watch: {
    plotSelected() {
      this.onPlotSelected();
    },

    plotData() {
      this.updatePlotData();
    },
  },

  methods: {
    async generateMap() {
      this.path_g = await this.addPaths();
      this.circle_g = await this.addCircles();
    },

    async addPaths() {
      let path = d3.geoPath().projection(this.projection);
      let path_g = this.svg.append("g").attr("id", "path-g");
      d3.json("/static/data/jpn.json").then((jpn) => {
        path_g
          .selectAll("#path-g path")
          .data(feature(jpn, jpn.objects.subunits).features)
          .enter()
          .append("path")
          .attr("d", path)
          .style("stroke", null)
          .style("fill", "rgba(176, 190, 197, 1)");
      });
      return path_g;
    },

    async addCircles() {
      let circle_g = this.svg.append("g").attr("id", "circle-g");
      circle_g
        .selectAll("#circle-g circle")
        .data(this.plotData)
        .enter()
        .append("circle")
        .attr("cx", (d) => this.projection([d.long, d.lat])[0])
        .attr("cy", (d) => this.projection([d.long, d.lat])[1])
        .attr("r", (d) => d.circleSize || 2)
        .style("fill", (d) => d.circleColor || "rgba(69, 90, 100, 0.7)")
        .attr("class", "plot")
        .attr("id", (d) => d.plot_id)
        .on("mouseover", (event, d) => {
          this.$emit("plotMouseOver", d.plot_id);
        })
        .on("mouseout", (event, d) => {
          this.$emit("plotMouseOut", d.plot_id);
        })
        .on("click", (event, d) => {
          this.$emit("plotClicked", d.plot_id);
        });
      return circle_g;
    },

    onPlotSelected() {
      this.svg
        .selectAll("circle")
        .attr("r", 2)
        .style("fill", "rgba(69, 90, 100, 0.7)");
      this.svg
        .select("circle#" + this.plotSelected.plot_id)
        .attr("r", 4)
        .style("fill", "rgba(244, 67, 54, 0.9)")
        .raise();
    },

    updatePlotData() {
      this.svg.selectAll("#circle-g circle").remove();
      this.addCircles();
    },
  },
};
</script>

<style>
.plot:hover {
  fill: rgba(244, 67, 54, 0.7) !important;
}
.svg-container {
  display: inline-block;
  position: relative;
  width: 100%;
  /* text-align: center; */
  vertical-align: middle;
  padding-bottom: 100%;
  overflow: hidden;
}
.svg-content {
  display: inline-block;
  position: absolute;
  top: 0;
  left: 0;
}
</style>
