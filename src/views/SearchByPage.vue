<template>
    <v-container>
    
        <v-simple-table>
            <thead>
                <tr>
                    <th class="text-left">源氏物語大成のページ数</th>
                    <th class="text-left"></th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="obj in result">
                    <td>{{obj.label.value}}</td>
                    <td>
                        <router-link to="/searchByPage">View</router-link>
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
            result: []
        }
    },
    created: function() {

        let query = " PREFIX dcterms: <http://purl.org/dc/terms/> \n";
        query += " PREFIX dcndl: <http://ndl.go.jp/dcndl/terms/> \n";
        query += " SELECT DISTINCT ?label ?page ?count(?manifest) as ?c WHERE { \n";
        query += "  ?page rdfs:label ?label .  \n";
        query += "  ?canvas dcterms:subject ?page .  \n";
        query += "  ?canvas dcterms:isPartOf ?manifest  .  \n";
        query += "  ?manifest dcterms:isPartOf ?collection  .  \n";
        query += " } group by ?manifest order by ?label \n";

        console.log(query)

        axios.get("https://dydra.com/ut-digital-archives/genji/sparql?query=" + encodeURIComponent(query) + "&output=json")
            .then(response => {

                let result = response.data.results.bindings
                this.result = result

                console.log(result)

            }).catch(error => { console.log(error); });

    }
};
</script>
