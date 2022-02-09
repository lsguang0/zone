<template>
    <h2>Child</h2>
    <h3>{{msg}}</h3>
    <button @click="updateMsg">改变</button>
</template>

<script lang="ts">
import { defineComponent, ref, onBeforeMount, onMounted, onUpdated, onBeforeUpdate, onBeforeUnmount, onUnmounted } from 'vue';
export default defineComponent({
    name: 'Child',
    setup() {
        const msg=ref('----');
        const updateMsg = () => {
            msg.value += '-'
        };
        onBeforeMount(() => {
            console.log('onBeforeMount')

        })
        onMounted(() => {
            console.log('onMounted')

        })
        onUpdated(() => {
            console.log('onUpdated')
        })
        onBeforeUpdate(() => {
            console.log('onBeforeUpdate')
        })
        onBeforeUnmount(() => {
            console.log('onBeforeUnmount')
        })
        onUnmounted(() => {
            console.log('onUnmounted')
        })
        return {
            msg,
            updateMsg
        }
    }
})
</script>
