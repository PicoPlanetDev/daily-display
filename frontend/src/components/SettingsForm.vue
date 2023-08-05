<template>
    <Alert v-if="showAlert" :message="alertMessage" :style="alertStyle" />
    <div class="col-sm-6">
        <div class="mb-3">
            <label for="notificationUrl" class="form-label">Notification Webhook</label>
            <input type="url" class="form-control" id="notificationUrl" aria-describedby="notificationUrl"
                v-model="notificationUrl">
            <div id="emailHelp" class="form-text">Daily Display will make a POST request to this URL (designed for <a
                    target="_blank" href="https://ntfy.sh">ntfy.sh</a>)</div>
        </div>
        <div class="form-check form-switch mb-3">
            <input class="form-check-input" type="checkbox" role="switch" id="notificationsCheck"
                v-model="notificationSwitch">
            <label class="form-check-label" for="notificationsCheck">Send notifications</label>
        </div>
        <div class="mb-3">
            <button type="submit" class="btn btn-outline-secondary" @click="testNotification()">Test notifications</button>
        </div>
        <div class="mb-3">
            <RouterLink to="/" class="btn btn-danger me-3">Exit</RouterLink>
            <button type="submit" class="btn btn-primary" @click="saveSettings()">Save</button>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import Alert from './Alert.vue';
import { RouterLink } from 'vue-router';
export default {
    name: 'SettingsForm',
    data() {
        return {
            notificationUrl: '',
            notificationSwitch: false,
            // alert
            alertMessage: '',
            alertStyle: '',
            showAlert: false,
        };
    },
    methods: {
        resetForm() {
            const path = 'http://localhost:5000/api/settings';
            axios.get(path)
                .then(response => {
                    // response.data.settings.whatever
                    // fill in the form with the data
                    this.notificationUrl = response.data.settings.notification_url;
                    this.notificationSwitch = response.data.settings.notifications_enabled;
                })
                .catch(error => {
                    console.log(error);
                });
        },
        saveSettings() {
            const path = 'http://localhost:5000/api/settings';
            axios.post(path, {
                notification_url: this.notificationUrl,
                notifications_enabled: this.notificationSwitch
            })
                .then(response => {
                    console.log(response);
                    if (response.data.status == "success") {
                        this.alertMessage = "Settings saved successfully";
                        this.alertStyle = "alert-success";
                        this.showAlert = true;
                    }
                    else {
                        this.alertMessage = "Error saving settings";
                        this.alertStyle = "alert-danger";
                        this.showAlert = true;
                    }
                })
                .catch(error => {
                    console.log(error);
                });
        },
        testNotification() {
            const path = 'http://localhost:5000/api/test_notification';
            axios.get(path)
                .then(response => {
                    console.log(response);
                    if (response.data.status == "success") {
                        this.alertMessage = "Test notification sent successfully";
                        this.alertStyle = "alert-success";
                        this.showAlert = true;
                    }
                    else {
                        this.alertMessage = "Error sending test notification";
                        this.alertStyle = "alert-danger";
                        this.showAlert = true;
                    }
                })
                .catch(error => {
                    console.log(error);
                });
        }
    },
    created() {
        this.resetForm();
    },
    components: { Alert, RouterLink }
}
</script>