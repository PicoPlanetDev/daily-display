<template>
    <div class="datetime">
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
            const path = 'http://localhost:5000/api/datetime';
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