import { customRef } from 'vue';
export default function<T>(value: T, delay = 200) {
    let timeOutId: number;
    return customRef((track, trigger) => {
        return {
            get() {
                track();
                return value
            },
            set(newValue: T) {
                clearTimeout(timeOutId)
                timeOutId = setTimeout(() => {
                    value = newValue;
                    trigger()
                }, delay);
            }
        }
    })
}