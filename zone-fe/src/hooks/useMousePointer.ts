import { ref, onMounted, onUnmounted } from 'vue';

export default function() {
    const x = ref(0);
    const y = ref(0);
    const clickEventHandle = (event: any) => {
        x.value = event.pageX;
        y.value = event.pageY
    }
    onMounted(() => {
        window.addEventListener('click', clickEventHandle);
    })
    onUnmounted(() => {
        window.removeEventListener('click', clickEventHandle);
    })
    return {
        x,
        y,
    }
}