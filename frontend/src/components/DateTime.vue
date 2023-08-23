<template>
    <div class="mb-5 border rounded bg-secondary-subtle">
        <h1>{{ time }}</h1>
        <h2>{{ date }}</h2>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    name: 'DateTime',
    data() {
        return {
            time: 'Loading...',
            date: 'Loading...'
        }
    },
    methods: {
        getDateTime() {
            const path = '/datetime';
            axios.get(path)
                .then(response => {
                    this.time = response.data.time;
                    this.date = response.data.date
                })
                .catch(error => {
                    console.log(error);
                });
        }
    },
    created() {
        this.getDateTime();
    }
}
</script>