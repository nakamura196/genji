<template>
    <v-container>
    
        <a :href="comp_url" target="_blank">Compare</a>
    
        <v-simple-table class="mt-5">
            <thead>
                <tr>
                    <th class="text-left">源氏物語大成 p.{{$route.query.page}}</th>
                    <th class="text-left"></th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="obj in result">
                    <td>{{obj.clabel}}</td>
                    <td>
                        <a :href="'http://da.dl.itc.u-tokyo.ac.jp/mirador/?manifest='+obj.manifest.value+'&canvas='+obj.canvas_id.value" target="_blank">View</a>
                    </td>
                </tr>
            </tbody>
        </v-simple-table>
    
    </v-container>
</template>

<script>
import axios from 'axios';

export default {
    data() {
        return {
            result: [],
            comp_url: ""
        }
    },
    created: function() {

        let query = " PREFIX dcterms: <http://purl.org/dc/terms/> \n";
        query += " PREFIX dcndl: <http://ndl.go.jp/dcndl/terms/> \n";
        query += " SELECT DISTINCT ?manifest ?canvas_id ?clabel WHERE { \n";
        query += "  ?taisei_page rdfs:label \"" + this.$route.query.page + "\"^^xsd:int . \n";
        query += "  ?canvas_id dcterms:subject ?taisei_page . \n";
        query += "  ?canvas_id dcterms:isPartOf ?manifest .  \n";
        query += "  ?manifest dcterms:isPartOf ?collection .  \n";
        query += "  ?collection rdfs:label ?clabel .  \n";
        query += " } \n";

        axios.get("https://dydra.com/ut-digital-archives/genji/sparql?query=" + encodeURIComponent(query) + "&output=json")
            .then(response => {

                let result = response.data.results.bindings
                this.result = result

                let manifests = ""
                let canvases = ""

                for (let i = 0; i < result.length; i++) {
                    let obj = result[i]
                    manifests += obj.manifest.value + ";"
                    canvases += obj.canvas_id.value + ";"
                }

                this.comp_url = "https://nakamura196.github.io/genji/mirador2/compare?manifest=" + manifests.slice(0, -1) + "&canvas=" + canvases.slice(0, -1)

            }).catch(error => { console.log(error); });

    }
};
</script>
