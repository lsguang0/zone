import axios from 'axios';
export async function index() {
    const res = await axios.get('/api/')
    return res;
}
export async function login({username, password}: {username: string, password: string}) {
    const res = await axios.post('/api/login', {
        username,
        password
    })
    return res;
}
export async function register({username, password}: {username: string, password: string}) {
    const res = await axios.post('/api/register', {
        username,
        password
    })
    return res;
}

