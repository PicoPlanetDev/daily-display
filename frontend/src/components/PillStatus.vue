<template>
    <div class="row">
        <div class="col" v-for="pill in pills">
            <div class="alert alert-primary">
                {{ pill.name }}
                <br>
                Dispensed: {{ pill.dispensed }}
                <br>
                Taken: {{ pill.taken }}
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    name: 'PillStatus',
    data() {
        return {
            pills: [],
        }
    },
    methods: {
        getPills() {
            axios.get('/pills')
                .then(response => {
                    this.pills = response.data.pills;
                })
                .catch(error => {
                    console.log(error);
                });
        }
    },
    mounted() {
        this.getPills();
        this.interval = setInterval(() => {
            this.getPills();
        }, 5000);
    },
    unmounted() {
        clearInterval(this.interval);
    }
}
</script>