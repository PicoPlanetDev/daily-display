<template>
    <div class="row" v-for="event in events">
        <div class="col">{{ event.all_day ? 'All day' : event.time_string }}</div>
        <div class="col">{{ event.title }}</div>
        <div class="col">{{ event.type }}</div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    name: 'TodayEvents',
    data() {
        return {
            events: [],
        }
    },
    methods: {
        getEvents() {
            const path = 'http://localhost:5000/api/events';
            axios.get(path)
                .then(response => {
                    //this.events = response.data.events;
                    // events is a json with uid keys
                    // convert to array
                    let eventsArray = [];
                    for (const [key, value] of Object.entries(response.data.events)) {
                        eventsArray.push(value);
                    }
                    // sort by datetime
                    // eventsArray.sort((a, b) => {
                    //     return a.datetime.localeCompare(b.datetime);
                    // });
                    // sort by timestamp
                    eventsArray.sort((a, b) => {
                        return a.timestamp - b.timestamp;
                    });
                    console.log(eventsArray);
                    this.events = eventsArray;
                })
                .catch(error => {
                    console.log(error);
                });
        }
    },
    created() {
        this.getEvents();
    }
}
</script>