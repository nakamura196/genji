<template>
  <div style="width : 100%; height : 800px; background-color: LightGray;">
    <span style="display:none;">{{ this.id }}</span>
    <span style="display:none;">{{ this.id_modern }}</span>

    <VueDragResize
      :isActive="true"
      :x="0"
      :y="0"
      :w="600"
      :h="750"
      v-on:resizing="resize"
      v-on:dragging="resize"
      class="p-2"
      :sticks="['ml', 'mr']"
    >
      <div class="card">
        <div class="card-body">
          <iframe
            :src="mirador_path"
            seamless
            width="100%"
            height="700px"
            style="border: none;"
          ></iframe>
        </div>
      </div>
    </VueDragResize>

    <VueDragResize
      :isActive="true"
      :x="600"
      :y="0"
      :w="600"
      :h="400"
      v-on:resizing="resize"
      v-on:dragging="resize"
      class="p-2"
    >
      <div class="card scroll" id="org">
        <div class="card-body">
          <h5><b>翻刻文</b></h5>
            <div
                :style="line.selected ? 'background-color : yellow;' : null"
                v-for="(line, line_id) of lines_org"
                v-bind:key="line_id"
                :id="line_id"
                v-on:mouseover="mouseover"
                @click="clickSmoothScroll(line_id)"
            >
                <img
                v-if="line.page"
                @click="mirador_path = line.page"
                src="https://iiif.dl.itc.u-tokyo.ac.jp/images/iiif.png"
                class="m-2"
                />

                <template v-for="node of line.array"
                >{{ node.text }}
                </template>
            </div>
        </div>
      </div>
    </VueDragResize>

    <VueDragResize
      :isActive="true"
      :x="600"
      :y="420"
      :w="600"
      :h="350"
      v-on:resizing="resize"
      v-on:dragging="resize"
      class="p-2"
    >
      <div class="card scroll" id="modern">
        <div class="card-body">
          <h5><b>現代語訳</b></h5>
          <div
            v-for="(line, line_id) of lines_modern"
            v-bind:key="line_id"
            :style="line.selected ? 'background-color : yellow;' : null"
            v-on:mouseover="mouseover_modern"
            :id="line_id"
            @click="clickSmoothScrollModern(line_id)"
          >
            <template v-for="node of line.array">
              {{ node.text }}
            </template>
          </div>
        </div>
      </div>
    </VueDragResize>
  </div>
</template>

<script>
import axios from "axios";

import VueDragResize from "vue-drag-resize";

export default {
  components: {
    VueDragResize
  },
  data() {
    return {
      url: "https://nakamura196.github.io/genji/data/aozora/01.xml",
      url_modern: "https://nakamura196.github.io/genji/data/aozora/yosano_genji_ids.xml",
      url_map: "https://nakamura196.github.io/genji/data/aozora/map.json",
      lines_org: {},
      lines_modern: {},
      id: "", //重要
      id_modern: "",
      modern_org_map: {},
      org_modern_map: {},

      width: 0,
      height: 0,
      top: 0,
      left: 0,

      mirador_path: ""
    };
  },
  created: function() {
    this.url = this.$route.query.left ? this.$route.query.left : this.url;
    this.url_modern = this.$route.query.right
      ? this.$route.query.right
      : this.url_modern;
    this.url_map = this.$route.query.map ? this.$route.query.map : this.url_map;

    this.map();
  },
  methods: {
    resize(newRect) {
      this.width = newRect.width;
      this.height = newRect.height;
      this.top = newRect.top;
      this.left = newRect.left;
    },
    clickSmoothScroll: function(target_id) {
      let modern_ids = this.org_modern_map[target_id];

      if (modern_ids != null) {
        this.$SmoothScroll(
          document.querySelector("#" + modern_ids[0]).getBoundingClientRect()
            .top +
            document.querySelector("#modern").scrollTop -
            document.querySelector("#modern").getBoundingClientRect().top,
          400,
          null,
          document.querySelector("#modern"),
          "y"
        );
      }
    },
    clickSmoothScrollModern: function(target_id) {
      let modern_ids = this.modern_org_map[target_id];

      if (modern_ids != null) {
        this.$SmoothScroll(
          document.querySelector("#" + modern_ids[0]).getBoundingClientRect()
            .top +
            document.querySelector("#org").scrollTop -
            document.querySelector("#org").getBoundingClientRect().top,
          400,
          null,
          document.querySelector("#org"),
          "y"
        );
      }
    },
    map: function() {
      let vm = this;
      axios
        .get(this.url_map)
        .then(response => {
          let modern_org_map = response.data;
          this.modern_org_map = modern_org_map;
          let org_modern_map = {};
          this.org_modern_map = org_modern_map;
          for (let line_modern in modern_org_map) {
            let org_ids = modern_org_map[line_modern];
            for (let i = 0; i < org_ids.length; i++) {
              let org_id = org_ids[i];
              if (!org_modern_map[org_id]) {
                org_modern_map[org_id] = [];
              }
              org_modern_map[org_id].push(line_modern);
            }
          }

          this.org();
          this.modern();
        })
        .catch(err => {
          (vm.errored = true), (vm.error = err);
        })
        .finally(() => (vm.loading = false));
    },
    org: function(data) {
      axios
        .get(this.url, {
          responseType: "document"
        })
        .then(response => {
          let lines_org = {};
          this.lines_org = lines_org;

          let xml = response.data;

          const surfaces = xml.querySelectorAll("surface");

          let manifest = xml.querySelector("surfaceGrp").attributes[0].value;
          this.mirador_path =
            "https://nakamura196.github.io/genji/mirador2/index_params.html?manifest=" +
            manifest;

          for (let s = 0; s < surfaces.length; s++) {
            const surface = surfaces[s];

            const graphic = surface.querySelector("graphic");
            const canvas_id = graphic.getAttribute("n");

            const zones = surface.querySelectorAll("zone");

            for (let z = 0; z < zones.length; z++) {
              const zone = zones[z];

              const x = Number(zone.getAttribute("ulx"));
              const y = Number(zone.getAttribute("uly"));

              const w = Number(zone.getAttribute("lrx")) - x;
              const h = Number(zone.getAttribute("lry")) - y;

              const xywh = x + "," + y + "," + w + "," + h;

              const lines = zone.querySelectorAll("line[*|id]");

              for (let i = 0; i < lines.length; i++) {
                let line = lines[i];
                let line_id = line.getAttribute("xml:id");

                let nodes = line.childNodes;

                let line_obj = {
                  array: [],
                  selected: false
                };

                // <-- 画像との紐付け -->
                if (i == 0) {
                  let param = {};
                  let params = [param];
                  param.manifest = manifest;
                  param.canvas = canvas_id + "#xywh=" + xywh;

                  line_obj["page"] =
                    "https://nakamura196.github.io/genji/mirador2/index_params.html?params=" +
                    encodeURIComponent(JSON.stringify(params));
                }

                // <!-- 画像との紐付け -->

                lines_org[line_id] = line_obj;

                for (let j = 0; j < nodes.length; j++) {
                  let node = nodes[j];

                  let obj = {
                    text: node.innerText || node.textContent
                  };

                  line_obj["array"].push(obj);
                }
              }
            }
          }
        });
    },
    modern: function(data) {
      axios
        .get(this.url_modern, {
          responseType: "document"
        })
        .then(response => {
          let xml = response.data;

          const div = xml.getElementsByTagName("body")[0];

          const lines = div.querySelectorAll("*[*|id]");

          let lines_modern = {};
          this.lines_modern = lines_modern;

          for (let i = 0; i < lines.length; i++) {
            let line = lines[i];

            let line_id = line.attributes[0].value;

            let nodes = line.childNodes;

            let line_obj = {
              array: [],
              selected: false
            };

            lines_modern[line_id] = line_obj;

            for (let j = 0; j < nodes.length; j++) {
              let node = nodes[j];

              let obj = {
                text: node.innerText || node.textContent
              };

              line_obj["array"].push(obj);
            }
          }
        });
    },
    mouseover: function(data) {
      if (
        data.target.attributes.length > 0 &&
        data.target.attributes[0].name == "id"
      ) {
        let lines = this.lines_org;
        let target_id = data.target.attributes[0].value;
        for (let line_id in lines) {
          let selected = false;
          if (line_id == target_id) {
            selected = true;
          }
          lines[line_id].selected = selected;
        }

        let modern_ids = this.org_modern_map[target_id];

        if (!modern_ids) {
          modern_ids = [];
        }

        let lines_modern = this.lines_modern;
        for (let line_id in lines_modern) {
          let selected = false;
          if (modern_ids.indexOf(line_id) != -1) {
            selected = true;
          }
          lines_modern[line_id].selected = selected;
        }

        this.id = target_id; //おまじない
      }
    },

    mouseover_modern: function(data) {
      let lines = this.lines_modern;
      let target_id = data.target.attributes[0].value;

      for (let line_id in lines) {
        let selected = false;
        if (line_id == target_id) {
          selected = true;
        }
        lines[line_id].selected = selected;
      }

      let org_ids = this.modern_org_map[target_id];

      if (!org_ids) {
        org_ids = [];
      }

      let lines_org = this.lines_org;
      for (let line_id in lines_org) {
        let selected = false;
        if (org_ids.indexOf(line_id) != -1) {
          selected = true;
        }
        lines_org[line_id].selected = selected;
      }

      this.id_modern = target_id; //おまじない
    }
  }
};
</script>

<style>
.scroll {
  height: 100%;
  overflow-y: auto;
}
</style>
