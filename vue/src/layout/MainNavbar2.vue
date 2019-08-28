<template>
    <navbar type="info" :transparent="transparent" :color-on-scroll="colorOnScroll" menu-classes="ml-auto">
        <template>
                      <router-link class="navbar-brand" to="/">
                        源氏物語・研究活用プロジェクト
                      </router-link>
</template>

<template slot="navbar-menu">
    <drop-down tag="li" title=" 校異源氏物語" icon="now-ui-icons education_paper" class="nav-item">
        <router-link to="/searchByPage" class="dropdown-item"> <i class="now-ui-icons design_image"></i> 頁数でさがす</router-link>
        <router-link to="/text" class="dropdown-item"><i class="now-ui-icons design_bullet-list-67"></i> テキストからさがす</router-link>
        <router-link to="/main" class="dropdown-item"> <i class="now-ui-icons business_bulb-63"></i> プロトタイプ</router-link>
    </drop-down>
    <drop-down tag="li" title=" 新編日本古典文学全集" icon="now-ui-icons education_paper" class="nav-item">
        <router-link to="/searchByPage4saga" class="dropdown-item"> <i class="now-ui-icons design_image"></i> 頁数でさがす</router-link>
        <router-link to="/text4saga" class="dropdown-item"><i class="now-ui-icons design_bullet-list-67"></i> テキストからさがす</router-link>
        <router-link to="/viewer" class="dropdown-item"> <i class="now-ui-icons business_bulb-63"></i> プロトタイプ</router-link>
    </drop-down>
    <li class="nav-item">
        <router-link to="/searchByWork" class="nav-link"><i class="now-ui-icons education_agenda-bookmark"></i> 帖名でさがす</router-link>
    </li>
    <li class="nav-item">
        <a href="https://www.kanzaki.com/works/2016/pub/image-annotator?u=https%3A%2F%2Fnakamura196.github.io%2Fgenji%2Fugm%2Fgenji.json" class="nav-link"><i class="now-ui-icons media-1_album"></i> IIIFコレクションをみる</a>
    </li>
</template>
  </navbar>
</template>

<script>
import { DropDown, NavbarToggleButton, Navbar, NavLink } from '@/components';
import { Popover } from 'element-ui';
export default {
    name: 'main-navbar',
    props: {
        transparent: Boolean,
        colorOnScroll: Number
    },
    components: {
        DropDown,
        Navbar,
        NavbarToggleButton,
        NavLink,
        [Popover.name]: Popover
    }
};
</script>

<style scoped>

</style>
