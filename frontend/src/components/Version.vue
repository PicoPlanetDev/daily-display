<template>
    Daily Display version {{ version }}
</template>

<script>
import axios from 'axios';

export default {
    name: 'BottomBar',
    data() {
        return {
            version: 'Loading...'
        };
    },
    methods: {
        getVersion() {
            const path = '/version';
            axios.get(path)
                .then(response => {
                    this.version = response.data.version;
                })
                .catch(error => {
                    console.log(error);
                });
        }
    },
    created() {
        this.getVersion();
    }
}
</script>