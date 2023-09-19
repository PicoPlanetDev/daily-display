<template>
    <div class="rounded fs-5 text-center" :class="warningBackground">{{ warningMessage }}</div>
</template>

<script>
import axios from 'axios';

export default {
    name: 'PillWarning',
    data() {
        return {
            warningBackground: "bg-primary",
            warningMessage: "Loading...",
        }
    },
    methods: {
        getWarningData() {
            const path = '/pill_warning';
            axios.get(path)
                .then(response => {
                    if (response.data.status == "error") {
                        this.warningBackground = "bg-danger";
                        this.warningMessage = "Error: " + response.data.message;
                        return;
                    }
                    if (response.data.warning == "wait") {
                        this.warningBackground = "bg-secondary-subtle";
                        this.warningMessage = "Wait for " + response.data.pill_round + " pills in " + response.data.time_until;
                    } else if (response.data.warning == "take") {
                        this.warningBackground = "bg-warning";
                        this.warningMessage = "Take " + response.data.pill_round + " pills";
                    } else if (response.data.warning == "none") {
                        this.warningBackground = "bg-success-subtle";
                        this.warningMessage = "Pills taken!";
                    }
                })
                .catch(error => {
                    console.log(error);
                });
        }
    },
    created() {
        this.getWarningData();
    }
}
</script>