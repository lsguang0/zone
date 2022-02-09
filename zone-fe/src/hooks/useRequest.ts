import { ref } from 'vue';
import axios from 'axios';

export default function <T>(url: string) {
    const loading = ref(true)
    const data = ref< T | null >(null)
    const errorMsg = ref('')
    axios.get(url).then(res => {
        loading.value = false;
        data.value = res.data;

    }).catch(error => {
        loading.value = false;
        errorMsg.value = error.message;
    })
    return {
        loading,
        data,
        errorMsg
    }
}