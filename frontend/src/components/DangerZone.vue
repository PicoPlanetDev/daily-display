<template>
    <!-- Button for shutdown -->
    <button type="button" class="btn btn-danger me-2" @click="shutdown('poweroff')">
        <i class="bi bi-power"></i> Shutdown
    </button>
    <!-- Button for reboot -->
    <button type="button" class="btn btn-warning me-2" @click="shutdown('reboot')">
        <i class=" bi bi-arrow-counterclockwise"></i> Reboot
    </button>
    <!-- Button for auto update -->
    <button type="button" class="btn btn-secondary me-2" @click="update()">
        <i class="bi bi-cloud-download"></i> Update
    </button>
</template>

<script>
import axios from 'axios';

export default {
    name: 'DangerZone',
    methods: {
        shutdown(type) {
            axios.post('/shutdown', { type: type })
                .then(response => {
                    console.log(response);
                })
                .catch(error => {
                    console.log(error);
                });
        },
        update() {
            axios.post('/update')
                .then(response => {
                    console.log(response);
                })
                .catch(error => {
                    console.log(error);
                });
        }
    },
}
</script>