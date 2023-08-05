<template>
    <div class="rounded"></div>
</template>

<script>
import axios from 'axios';

export default {
    name: 'PillWarning',
    props: {
        warningBackground: "bg-primary",
        warningMessage: "Loading",
    },
    methods: {
        getWarningData() {
            const path = 'http://localhost:5000/api/pill_warning';
            axios.get(path)
                .then(response => {
                    if (response.data.warning == "wait") {
                        this.warningBackground = "bg-secondary";
                        this.warningMessage = "Wait for " + response.data.pill_round + " pills";
                    } else if (response.data.warning == "take") {
                        this.warningBackground = "bg-danger";
                        this.warningMessage = "Take " + response.data.pill_round + " pills";
                    } else if (response.data.warning == "none") {
                        this.warningBackground = "bg-success";
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