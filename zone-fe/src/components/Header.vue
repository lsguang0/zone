<template>
    <div class="header">
        <div class="new-world" @click="entryNewWorld">IN</div>
        <el-affix target=".header" :offset="0">
            <div class="affix-nav">
                <div class="chicken-soup">
                talk is cheap，show me the code
            </div>
            <el-menu
                :default-active="activeIndex"
                class="el-menu"
                mode="horizontal"
                background-color="#545c6400"
                text-color="#fff"
                active-text-color="#fff"
                @select="handleSelect"
            >
                <el-menu-item index="1">HOME</el-menu-item>
                <el-sub-menu popper-class="nav-menu" index="2">
                    <template #title>FE</template>
                    <el-menu-item index="2-1">CSS</el-menu-item>
                    <el-menu-item index="2-2">Maptalks</el-menu-item>
                    <el-menu-item index="2-3">ThreeJs</el-menu-item>
                    <el-menu-item index="2-4">React</el-menu-item>
                    <el-menu-item index="2-5">Vue</el-menu-item>
                </el-sub-menu>
                <el-sub-menu popper-class="nav-menu" index="3" >
                    <template #title>RD</template>
                    <el-menu-item index="3-1">Python</el-menu-item>
                    <el-menu-item index="3-2">NodeJs</el-menu-item>
                    <el-menu-item index="3-3">Mysql</el-menu-item>
                    <el-menu-item index="3-4">MongoDB</el-menu-item>
                    <el-menu-item index="3-5">Sql</el-menu-item>
                </el-sub-menu>
                 <el-menu-item index="4">LeetCode</el-menu-item>
            </el-menu>  
            <div class="avatar">  
                <el-popover
                    placement="bottom"
                    trigger="hover"
                    width="70px"
                >
                    <template #reference>
                        <el-avatar :size="30" :src="url">
                        </el-avatar>
                    </template>
                    <div class="button" @click="modifyPassword">重置密码</div>
                    <div class="button">退出登录</div>
                </el-popover>
            </div>
            </div>
        </el-affix>
    </div>
</template>
<script lang="ts" setup>
import { ref } from 'vue';
import router from './../router'
const url = ref('https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg');
const modifyPassword = () => {
    
}
const activeIndex = ref('1')
const handleSelect = (key: string, keyPath: string[]) => {
  console.log(key, keyPath)
}

const entryNewWorld = () => {
    router.push('/test')
}
</script>
<style lang="scss" scoped>
.header {
    width: 100%;
    height:400px;
    color: #fff;
    background: url('../assets/image/bg-default.jpg') no-repeat center center;
    background-size: cover;
    background-color: #ccc;
    margin-bottom: 10px;
    position: relative;

    .new-world {
        width: 100px;
        height: 30px;
        text-align: center;
        line-height: 30px;
        font-weight: bold;
        border-radius: 15px;
        border: 2px solid #ddd;
        position: absolute;
        bottom: 30px;
        left: 50%;
        transform: translate(-50%, 0);
        cursor: pointer;
    }
    .new-world:hover {
        background-color: aqua;
        border-color:#fff;
        color: #000;
        animation: move 1s linear;
    }
}
.affix-nav {
    width: 100%;
    height: 60px;
    box-sizing: border-box;
    padding: 0 10px;
    display: flex;
    align-items: center;
    justify-content: space-between;
        .el-menu {
            width: 420px;
            margin: 0  50px 0 auto;
            border-bottom: none;
            ::v-deep .el-sub-menu .el-sub-menu__title {
                border: none;
            }

        }
}
@keyframes move {
    0% {
        background-color: #fff;
    }
    100% {
        background-color: aqua;
    }
}
</style>