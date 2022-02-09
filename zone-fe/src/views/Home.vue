<template>
    <div class="home">
        <Header />
        <ShowInfo />
        <Footer />
        <el-backtop />
    </div>
</template> 
<script lang="ts" setup >
import { provide,ref,reactive  } from 'vue';
import Header from './../components/Header.vue';
import ShowInfo from '../components/ShowInfo.vue';
import Footer from '../components/Footer.vue';

</script>
<style lang="scss">
.home {
    width: 100%;
    background-size: 100% 100%;
    background-position: center center;
}
</style>