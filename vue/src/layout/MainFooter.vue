<template>
    <footer class="footer" :class="{ [`footer-${type}`]: type }" :data-background-color="backgroundColor">
        <div class="container">
            <nav>
                <ul>
                    <li>
                        <a href="https://iiif.dl.itc.u-tokyo.ac.jp/repo/s/genji/page/home">
                  東京大学総合図書館所蔵『源氏物語』
                </a>
                    </li>
                    <li>
                        <a href="https://guides.lib.kyushu-u.ac.jp/c.php?g=774839&p=5560033">
                  源氏物語 古活字版 - 貴重資料（九大コレクション）
                </a>
                    </li>
                </ul>
            </nav>
            <div class="copyright">
                裏源氏研究チーム
            </div>
        </div>
    </footer>
</template>

<script>
export default {
    props: {
        backgroundColor: String,
        type: String
    },
    data() {
        return {
            year: new Date().getFullYear()
        };
    }
};
</script>

<style>

</style>
