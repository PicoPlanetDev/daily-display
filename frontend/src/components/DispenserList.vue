<template>
    <div>
        <h3><i class="bi bi-gear"></i> Dispensers</h3>
        <hr>
        <div>
            <button type="button" class="btn btn-outline-secondary" @click="getDispensers">
                <i class="bi bi-arrow-clockwise"></i> Refresh list
            </button>
        </div>
        <div>
            <div class="mt-3" v-if="dispensers.length == 0">
                No dispensers found. Click the button above to create one, or try refreshing the list.
                <hr>
            </div>
            <div class="table-responsive">
                <table class="table table-dark" v-if="dispensers.length > 0">
                    <thead>
                        <tr>
                            <th scope="col">Index</th>
                            <th scope="col">Servo Min</th>
                            <th scope="col">Servo Max</th>
                            <th scope="col">Default Angle</th>
                            <th scope="col">Chute Angle</th>
                            <th scope="col">Smooth Enabled</th>
                            <th scope="col">Smooth Duration</th>
                            <th scope="col">Smooth Step Time</th>
                            <th scope="col">Sensor Pin</th>
                            <th scope="col">Sensor Enabled</th>
                            <th><!-- Left blank for buttons --></th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(dispenser, index) in dispensers" :key="index">
                            <td>{{ dispenser.index }}</td>
                            <td>{{ dispenser.servo_min }}</td>
                            <td>{{ dispenser.servo_max }}</td>
                            <td>{{ dispenser.angle_default }}</td>
                            <td>{{ dispenser.angle_chute }}</td>
                            <td>{{ dispenser.smooth_enabled }}</td>
                            <td>{{ dispenser.smooth_duration }}</td>
                            <td>{{ dispenser.step_time }}</td>
                            <td>{{ dispenser.sensor_pin }}</td>
                            <td>{{ dispenser.sensor_enabled }}</td>
                            <td>
                                <div class="btn-group" role="group">
                                    <button type="button" class="btn btn-outline-warning btn-sm"
                                        @click="setupFormEditDispenser(dispenser)" data-bs-toggle="modal"
                                        data-bs-target="#editDispenserModal">
                                        <i class="bi bi-pencil"></i>
                                    </button>
                                </div>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <!-- Edit dispenser modal -->
    <div class="modal fade" id="editDispenserModal" tabindex="-1" aria-labelledby="editDispenserModalLabel"
        aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5" id="editDispenserModalLabel">Edit Dispenser {{ editDispenserForm.index }}
                    </h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <!-- Options -->
                    <p>You probably shouldn't change these unless you know what you're doing.</p>
                    <!-- Servo timings -->
                    <div class="input-group mb-3">
                        <span class="input-group-text">Servo min</span>
                        <input type="number" class="form-control" placeholder="100" aria-label="Servo min"
                            v-model="editDispenserForm.servo_min" step="1">
                        <span class="input-group-text">Servo max</span>
                        <input type="number" class="form-control" placeholder="500" aria-label="Servo max"
                            v-model="editDispenserForm.servo_max" step="1">
                    </div>
                    <!-- Servo angles -->
                    <div class="input-group mb-3">
                        <span class="input-group-text">Default angle</span>
                        <input type="number" class="form-control" placeholder="90" aria-label="Default angle"
                            v-model="editDispenserForm.angle_default" step="1">
                        <span class="input-group-text">Chute angle</span>
                        <input type="number" class="form-control" placeholder="0" aria-label="Chute angle"
                            v-model="editDispenserForm.angle_chute" step="1">
                    </div>
                    <!-- Smoothing -->
                    <div class="form-check form-switch mb-1">
                        <input class="form-check-input" type="checkbox" role="switch" id="smoothingEnabledCheck"
                            v-model="editDispenserForm.smooth_enabled">
                        <label class="form-check-label" for="smoothingEnabledCheck">Smooth servo rotation</label>
                    </div>
                    <div class="input-group mb-3">
                        <span class="input-group-text">Duration (s)</span>
                        <input type="number" class="form-control" placeholder="1" aria-label="Smooth duration"
                            v-model="editDispenserForm.smooth_duration" step="0.1">
                        <span class="input-group-text">Step time (s)</span>
                        <input type="number" class="form-control" placeholder="0.01" aria-label="Smooth step time"
                            v-model="editDispenserForm.step_time" step="0.01">
                    </div>
                    <div class="form-check form-switch mb-1">
                        <input class="form-check-input" type="checkbox" role="switch" id="sensorEnabledCheck"
                            v-model="editDispenserForm.sensor_enabled">
                        <label class="form-check-label" for="sensorEnabledCheck">IR reflective sensor</label>
                    </div>
                    <div class="input-group mb-3">
                        <span class="input-group-text">Sensor pin</span>
                        <input type="number" class="form-control" placeholder="1" aria-label="Sensor pin"
                            v-model="editDispenserForm.sensor_pin" step="1">
                        <div id="pinHelp" class="form-text">The board's pins are numbered left to right, from top to bottom,
                            if you orient the board with the GPIO header (double row of pins) on the left, and the USB,
                            HDMI, and Ethernet ports facing toward you.</div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-outline-danger me-2" data-bs-dismiss="modal">Cancel</button>
                        <button type="button" class="btn btn-primary" data-bs-dismiss="modal" @click="editDispenser()">Save
                            dispenser</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    name: 'DispenserList',
    data() {
        return {
            dispensers: [],
            editDispenserForm: {
                id: '',
                index: 0,
                servo_min: 0,
                servo_max: 0,
                angle_default: 0,
                angle_chute: 0,
                smooth_duration: 0,
                step_time: 0,
                smooth_enabled: 0,
                sensor_pin: 0,
                sensor_enabled: 0,
            },
        };
    },
    methods: {
        getDispensers() {
            const path = '/dispensers';

            // Count the number of times we've tried to get the Dispensers
            // If we've tried too many times, stop trying
            // Looking back, this is a pretty bad way to do this
            // An infinite loop would occur if it kept failing
            var fails = 0;
            axios.get(path)
                .then(response => {
                    this.dispensers = response.data.dispensers;
                })
                .catch(error => {
                    console.log(error);
                    fails++;
                    if (fails < 5) {
                        this.getDispensers();
                    }
                });
        },
        setupFormEditDispenser(dispenser) {
            this.editDispenserForm.id = dispenser.id;
            this.editDispenserForm.index = dispenser.index;
            this.editDispenserForm.servo_min = dispenser.servo_min;
            this.editDispenserForm.servo_max = dispenser.servo_max;
            this.editDispenserForm.angle_default = dispenser.angle_default;
            this.editDispenserForm.angle_chute = dispenser.angle_chute;
            this.editDispenserForm.smooth_duration = dispenser.smooth_duration;
            this.editDispenserForm.step_time = dispenser.step_time;
            this.editDispenserForm.smooth_enabled = dispenser.smooth_enabled == 1;
            this.editDispenserForm.sensor_pin = dispenser.sensor_pin;
            this.editDispenserForm.sensor_enabled = dispenser.sensor_enabled == 1;
        },
        editDispenser() {
            const path = '/dispensers';
            axios.put(path, {
                id: this.editDispenserForm.id,
                index: this.editDispenserForm.index,
                servo_min: this.editDispenserForm.servo_min,
                servo_max: this.editDispenserForm.servo_max,
                angle_default: this.editDispenserForm.angle_default,
                angle_chute: this.editDispenserForm.angle_chute,
                smooth_duration: this.editDispenserForm.smooth_duration,
                step_time: this.editDispenserForm.step_time,
                smooth_enabled: this.editDispenserForm.smooth_enabled ? 1 : 0,
                sensor_pin: this.editDispenserForm.sensor_pin,
                sensor_enabled: this.editDispenserForm.sensor_enabled ? 1 : 0,
            })
                .then(response => {
                    //console.log(response);
                    this.getDispensers();
                })
                .catch(error => {
                    console.log(error);
                });
        },
    },
    created() {
        this.getDispensers();
    }
}
</script>