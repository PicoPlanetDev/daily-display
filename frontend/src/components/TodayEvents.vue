<template>
    <div class="row text-center">
        <h3>Calendar</h3>
    </div>
    <div class="row mx-0 mb-3 p-3 border rounded bg-secondary-subtle" v-for="event in events">
        <div class="row text-center mb-2" v-if="event.up_next">
            <div class="col"><span class="badge bg-success fs-5">Up next {{ event.time_until }}</span></div>
        </div>
        <div class="row">
            <div class="col-sm-2 fs-5" :class="event.all_day ? 'badge bg-primary' : ''">
                {{ event.all_day ? 'All day' : event.time_string }}
            </div>
            <div class="col fs-5">
                {{ event.title }}
            </div>
            <div class="col-sm-2 badge fs-5" v-if="event.type != null" :class="getEventTypeBgClass(event)">
                {{ event.type }}
            </div>
        </div>
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
            const path = '/events';
            axios.get(path)
                .then(response => {
                    // events is a json with uid keys
                    // convert to array
                    let eventsArray = [];
                    for (const [key, value] of Object.entries(response.data.events)) {
                        eventsArray.push(value);
                    }

                    // sort by timestamp
                    eventsArray.sort((a, b) => {
                        return a.timestamp - b.timestamp;
                    });
                    this.events = eventsArray;
                })
                .catch(error => {
                    console.log(error);
                });
        },
        getEventTypeBgClass(event) {
            return {
                'bg-secondary': event.type == 'Task',
                'bg-success': event.type == 'Event',
                'bg-warning': event.type == 'Appointment',
            }
        }
    },
    created() {
        this.getEvents();
    },
    mounted() {
        this.interval = setInterval(() => {
            this.getEvents();
        }, 30000);
    },
    beforeUnmount() {
        clearInterval(this.interval);
    }
}
</script>