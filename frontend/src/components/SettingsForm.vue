<template>
    <Alert v-if="showAlert" :message="alertMessage" :style="alertStyle" />
    <div class="col">
        <!-- Calendar -->
        <div class="fs-4"><i class="bi bi-calendar-date"></i> Calendar</div>
        <hr>
        <div class="mb-3 col-lg-6">
            <label for="calendarUrl" class="form-label">Calendar URL</label>
            <input type="url" class="form-control" id="calendarUrl" aria-describedby="calendarUrlHelp"
                v-model="calendarUrl">
            <div id="calendarUrlHelp" class="form-text">The url should end in an <span class="font-monospace">.ics</span>
                file,
                such as <span class="font-monospace">basic.ics</span></div>
        </div>
        <div class="mb-3 col-lg-6">
            <label for="timezone" class="form-label">Timezone</label>
            <div class="row">
                <div class="col">
                    <input type="text" class="form-control" id="timezone" aria-describedby="timezoneHelp"
                        v-model="timezone">
                    <div id="timezoneHelp" class="form-text">A timezone string, such as <span
                            class="font-monospace">America/New_York</span></div>
                </div>
                <div class="col">
                    <button type="button" class="btn btn-primary" @click="this.timezone = this.getTimeZone()"
                        :hidden="detectTimezoneDisabled"><i class="bi bi-stars"></i> Detect
                        timezone</button>
                </div>
            </div>
        </div>
        <!-- Notifications -->
        <div class="fs-4"><i class="bi bi-bell"></i> Notifications</div>
        <hr>
        <div class="form-check form-switch mb-3">
            <input class="form-check-input" type="checkbox" role="switch" id="notificationsCheck"
                v-model="notificationSwitch">
            <label class="form-check-label" for="notificationsCheck">Notifications enabled</label>
        </div>
        <div class="mb-3 col-lg-6">
            <label for="notificationUrl" class="form-label">Notification Webhook</label>
            <input type="url" class="form-control" id="notificationUrl" aria-describedby="notificationUrl"
                v-model="notificationUrl" :disabled="notificationSwitch ? false : true">
            <div id="notificationUrlHelp" class="form-text">Daily Display will make a POST request to this URL (designed for
                <a target="_blank" href="https://ntfy.sh">ntfy.sh</a>)
            </div>
        </div>
        <div class="mb-3">
            <button type="button" class="btn btn-outline-secondary" @click="testNotification()"
                :disabled="notificationSwitch ? false : true">Test notifications</button>
        </div>
        <!-- Printer -->
        <div class="fs-4"><i class="bi bi-printer"></i> Printer</div>
        <hr>
        <div class="form-check form-switch mb-3">
            <input class="form-check-input" type="checkbox" role="switch" id="printerCheck" v-model="printerEnabled">
            <label class="form-check-label" for="printerCheck">Printer enabled</label>
        </div>
        <div class="mb-3 col-lg-6">
            <label for="printerPort" class="form-label">Printer Port</label>
            <input type="text" class="form-control" id="printerPort" aria-describedby="printerPortDescription"
                v-model="printerPort" :disabled="printerEnabled ? false : true">
            <div id="printerPortDescription" class="form-text">The serial port that the printer is connected to, such as
                <span class="font-monospace">/dev/ttyUSB0</span>
            </div>
        </div>
        <div class="mb-3 col-lg-6">
            <label for="receiptRounds" class="form-label">Reciept Rounds</label>
            <input type="text" class="form-control" id="receiptRounds" aria-describedby="receiptRoundsDescription"
                v-model="receiptRounds" :disabled="printerEnabled ? false : true">
            <div id="receiptRoundsDescription" class="form-text">The rounds (from below) that the reciept should be printed
                during, such as
                <span class="font-monospace">Morning,Lunch</span>
            </div>
        </div>
        <!-- Dispenser -->
        <div class="fs-4"><i class="bi bi-capsule"></i> Pill dispensing</div>
        <hr>
        <div class="form-check form-switch mb-3">
            <input class="form-check-input" type="checkbox" role="switch" id="dispenserCheck" v-model="dispenserEnabled">
            <label class="form-check-label" for="dispenserCheck">Dispenser enabled</label>
        </div>
        <div class="mb-3 col-lg-6">
            <label for="manualDispense" class="form-label">Manual dispense</label>
            <input type="text" class="form-control" id="manualDispense" aria-describedby="manualDispenseDescription"
                v-model="manualDispense">
            <div id="manualDispenseDescription" class="form-text">The number of minutes before the round time that the pill
                can be manually dispensed, such as
                <span class="font-monospace">60</span>
            </div>
        </div>
        <!-- Exit and save buttons -->
        <hr>
        <div class="mb-3">
            <RouterLink to="/" class="btn btn-outline-danger me-3"><i class="bi bi-x-lg"></i> Cancel</RouterLink>
            <button type="reset" class="btn btn-outline-danger me-3" @click="resetForm()"><i class="bi bi-trash"></i>
                Discard</button>
            <button type="submit" class="btn btn-primary me-3" @click="saveSettings(exit = false)"><i
                    class="bi bi-save"></i>
                Save</button>
            <button type="submit" class="btn btn-primary me-3" @click="saveSettings(exit = true)"><i
                    class="bi bi-door-open"></i>
                Save
                and exit</button>
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
            calendarUrl: '',
            printerEnabled: true,
            printerPort: '',
            printerBaudrate: '',
            // alert
            alertMessage: '',
            alertStyle: '',
            showAlert: false,
            dispenserEnabled: true,
            receiptRounds: '',
            manualDispense: '',
            timezone: '',
        };
    },
    methods: {
        resetForm() {
            const path = '/settings';
            axios.get(path)
                .then(response => {
                    // response.data.settings.whatever
                    // fill in the form with the data
                    this.notificationUrl = response.data.settings.notification_url;
                    this.notificationSwitch = response.data.settings.notifications_enabled;
                    this.calendarUrl = response.data.settings.calendar_url;
                    this.printerEnabled = response.data.settings.printer_enabled;
                    this.printerPort = response.data.settings.printer_port;
                    this.printerBaudrate = response.data.settings.printer_baudrate;
                    this.dispenserEnabled = response.data.settings.dispenser_enabled;
                    this.receiptRounds = response.data.settings.receipt_rounds;
                    this.manualDispense = response.data.settings.manual_dispense;
                    this.timezone = response.data.settings.timezone;

                    this.scrollToTop();
                })
                .catch(error => {
                    console.log(error);
                });
        },
        saveSettings(exit = false) {
            const path = '/settings';
            axios.post(path, {
                notification_url: this.notificationUrl,
                notifications_enabled: this.notificationSwitch,
                calendar_url: this.calendarUrl,
                printer_enabled: this.printerEnabled,
                printer_port: this.printerPort,
                printer_baudrate: this.printerBaudrate,
                dispenser_enabled: this.dispenserEnabled,
                receipt_rounds: this.receiptRounds,
                manual_dispense: this.manualDispense,
                timezone: this.timezone,
            })
                .then(response => {
                    console.log(response);
                    if (response.data.status == "success") {
                        this.alertMessage = "Settings saved successfully";
                        this.alertStyle = "alert-success";
                        this.showAlert = true;
                        this.scrollToTop();

                        if (exit) {
                            this.$router.push('/');
                        }
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
            const path = '/test_notification';
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
        },
        scrollToTop() {
            document.body.scrollTop = 0;
            document.documentElement.scrollTop = 0;
        },
        getTimeZone() {
            return Intl.DateTimeFormat().resolvedOptions().timeZone;
        },
    },
    computed: {
        detectTimezoneDisabled() {
            return this.timezone === this.getTimeZone();
        }
    },
    created() {
        this.resetForm();
    },
    components: { Alert, RouterLink }
}
</script>