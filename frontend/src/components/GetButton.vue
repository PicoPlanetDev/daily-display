<template>
    <button class="btn btn-outline-secondary btn-sm" @click="getPath()">{{ label }}</button>
</template>

<script>
import axios from 'axios';
export default {
    name: 'GetButton',
    props: {
        path: String,
        label: String,
    },
    methods: {
        getPath() {
            const path = this.path;
            axios.get(path)
                .then(response => {
                    console.log(response);
                })
                .catch(error => {
                    console.log(error);
                });
        }
    }
}
</script>