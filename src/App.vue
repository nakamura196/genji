<template>
  <v-app>
    <myheader></myheader>
    <v-content class="my-5">
      <router-view class="my-5"/>
    </v-content>
    <myfooter></myfooter>
  </v-app>
</template>

<script>
import myheader from './components/myheader'
import myfooter from './components/myfooter'

export default {
  name: 'App',
  components: {
    myheader,
    myfooter
  },
  data: () => ({
    //
  }),
};
</script>
