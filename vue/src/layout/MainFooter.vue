<template>
    <footer class="footer" :class="{ [`footer-${type}`]: type }" :data-background-color="backgroundColor">
        <div class="container">
            <div class="copyright">
                TEI-C東アジア/日本語分科会
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
