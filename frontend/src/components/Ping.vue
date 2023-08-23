<template>
    <div class="ping">
        <h1>Ping</h1>
        <p>{{ message }}</p>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    name: 'Ping',
    data() {
        return {
            message: 'Loading...'
        }
    },
    methods: {
        getMessage() {
            const path = '/ping';
            axios.get(path)
                .then(response => {
                    this.message = response.data;
                })
                .catch(error => {
                    console.log(error);
                });
        }
    },
    created() {
        this.getMessage();
    }
}
</script>