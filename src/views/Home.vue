<template>
    <v-container>
    
        <v-simple-table>
            <thead>
                <tr>
                    <th class="text-left">メニュー</th>
                    <th class="text-left"></th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>源氏物語大成のページ番号から探す。</td>
                    <td><router-link to="/searchByPage">View</router-link></td>
                </tr>
                 <tr>
                    <td>作品名から探す。</td>
                    <td><router-link to="/searchByWork">View</router-link></td>
                </tr>
                <tr>
                    <td>本文テキストから探す。</td>
                    <td>Under development</td>
                </tr>
            </tbody>
        </v-simple-table>
    
    </v-container>
</template>

<script>
export default {
    components: {},
};
</script>
