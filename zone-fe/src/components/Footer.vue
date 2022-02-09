<template>
    <div class="footer">
       <div  v-for="item in contactMode" :key="item.id" class="contact-mode" @click="entryLink(item.link)">
           <i :class="'iconfont ' + item.name"></i>
       </div>
       
    </div>
</template>
<script lang="ts" setup>
import { reactive } from 'vue';
const contactMode = [
    {
        name: 'icon-github',
        id: 'github',
        link: 'https://github.com/lsguang0'
    },
    {
        name: 'icon-QQ',
        id: 'QQ',
        link: '/#/qq'
    },
    {
        name: 'icon-juejin',
        id: 'juejin',
        link: 'https://juejin.cn/user/2823201593235752/posts'
    }
]
const entryLink = (params: string) => {
    window.open(params)
}
</script>
<style lang="scss">
.footer {
    width: 100%;
    height: 60px;
    display: flex;
    justify-content: center;
    align-items: top;

    .contact-mode {
        height: 40px;
        width: 40px;
        border-radius: 50%;
        margin-right: 20px;
        background-color: #ccc;
        text-align: center;
        cursor: pointer;
        i {
            font-size: 20px;
            line-height: 40px;
            color: #000;
        }
    }
}
</style>