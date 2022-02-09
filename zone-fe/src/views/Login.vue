<template>
    <div class="login-form">
        <el-form
            v-show="isLogin"
            class="form-content"
            label-position="right"
            label-width="100px"
            :model="loginFormLabelAlign"
            style="max-width: 460px"
        >
            <el-form-item label="username">
            <el-input v-model="loginFormLabelAlign.username"></el-input>
            </el-form-item>
            <el-form-item label="password">
            <el-input type="password" v-model="loginFormLabelAlign.password"></el-input>
            </el-form-item>
        </el-form>
        <el-form
            v-show="!isLogin"
            class="form-content"
            label-position="right"
            label-width="100px"
            :model="registerFormLabelAlign"
            style="max-width: 460px"
        >
            <el-form-item label="username">
            <el-input v-model="registerFormLabelAlign.username"></el-input>
            </el-form-item>
            <el-form-item label="password">
            <el-input type="password" v-model="registerFormLabelAlign.password"></el-input>
            </el-form-item>
            <el-form-item label="repass">
            <el-input type="password" v-model="registerFormLabelAlign.rePassword"></el-input>
            </el-form-item>
        </el-form>
        <el-button v-if="isLogin" class="login-button" @click="userLogin">登陆</el-button>
        <el-button v-else class="login-button" @click="userRegister">注册</el-button>
        <el-button class="change-type" @click="changeFormType"> 切换{{isLogin ? '注册' : '登陆'}}页面</el-button>
    </div>

</template>
<script lang="ts" setup>
import { onMounted, reactive, ref} from 'vue';
import {ElMessage} from 'element-plus';
import router from './../router';
import {login, register} from '@/request/index';
import mouse from '@/hooks/useMousePointer';

// 表单状态
const isLogin = ref(true)
const changeFormType = () => {
    isLogin.value = !isLogin.value
} 
// 登陆表单
const loginFormLabelAlign = reactive({
  username: '',
  password: '',
})
const registerFormLabelAlign = reactive({
  username: '',
  password: '',
  rePassword: '',
})

// 
const entryRouter = (params: string, event?: MouseEvent) => {
    router.push(`/${params}`)
}
// 登陆验证
const userLogin = () => {
    login({
        username: loginFormLabelAlign.username,
        password: loginFormLabelAlign.password
    }).then(res => {
        const {data} = res;
        if (data.status === 200) {
            entryRouter('');
        }
        else {
            message(data.msg);
        }
    })
}
// 注册验证
const userRegister = () => {
    const {rePassword, password, username} = registerFormLabelAlign;
    if (!(rePassword && password && username)) {
        ElMessage.warning('注册信息不完整')
        return;
    }
    if (password !== rePassword) {
        ElMessage.warning('两次输入密码不一致')
    }
    else {
        register({
            username,
            password
        }).then(res => {
            const {data} = res;
            if (data.status === 200) {
                ElMessage.info('注册成功')
                registerFormLabelAlign.rePassword = ''
                registerFormLabelAlign.password = ''
                registerFormLabelAlign.username = ''
                isLogin.value = true;
            }
            else {
                ElMessage.info(data.msg)
            }
        })
    }

}
const message = (msg: string) => {
    ElMessage.warning(msg)
}
onMounted(() => {
    mouse()
})
</script>
<style lang="scss">
.login-form {
    width: 500px;
    height: 500px;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background: linear-gradient(#e66465, #9198e5);
    border-radius: 20px;

    .form-content {
        margin-top: 150px;
    }
    
    .login-button {
        margin: 0 50%;
        transform: translate( -50%, 0);
    }
    .change-type {
        height: 20px;
        // width: 50px;
        font-size: 10px;
        position: absolute;
        bottom: 20px;
        right: 0;
    }
}
</style>