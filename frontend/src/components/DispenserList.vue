<template>
    <div>
        <h3><i class="bi bi-gear"></i> Dispensers</h3>
        <hr>
        <div>
            <!-- <button type="button" class="btn btn-primary me-3" data-bs-toggle="modal" data-bs-target="#addDispenserModal">
                <i class="bi bi-plus"></i> Add Dispenser
            </button> -->
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
                            <td>
                                <div class="btn-group" role="group">
                                    <button type="button" class="btn btn-outline-warning btn-sm"
                                        @click="setupFormEditDispenser(dispenser)" data-bs-toggle="modal"
                                        data-bs-target="#editDispenserModal">
                                        <i class="bi bi-pencil"></i>
                                    </button>
                                    <!-- <button type="button" class="btn btn-outline-danger btn-sm"
                                        @click="setupFormDeleteDispenser(dispenser)" data-bs-toggle="modal"
                                        data-bs-target="#deleteDispenserModal">
                                        <i class="bi bi-trash"></i>
                                    </button> -->
                                </div>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <!-- Add dispenser modal -->
    <div class="modal fade" id="addDispenserModal" tabindex="-1" aria-labelledby="addDispenserModalLabel"
        aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5" id="addDispenserModalLabel">Add Dispenser</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"
                        @click="clearForm"></button>
                </div>
                <div class="modal-body">
                    <!-- Options -->
                    You probably shouldn't change these unless you know what you're doing.
                    <!-- Index -->
                    <div class="mb-3">
                        <label for="addDispenserFormIndex" class="form-label">Index</label>
                        <input type="text" class="form-control" id="addDispenserFormIndex" placeholder="0"
                            v-model="addDispenserForm.index">
                    </div>
                    <!-- Servo timings -->
                    <div class="input-group mb-3">
                        <span class="input-group-text">Servo min</span>
                        <input type="text" class="form-control" placeholder="100" aria-label="Servo min"
                            v-model="addDispenserForm.servo_min">
                        <span class="input-group-text">Servo max</span>
                        <input type="text" class="form-control" placeholder="500" aria-label="Servo max"
                            v-model="addDispenserForm.servo_max">
                    </div>
                    <!-- Servo angles -->
                    <div class="input-group mb-3">
                        <span class="input-group-text">Default angle</span>
                        <input type="text" class="form-control" placeholder="90" aria-label="Default angle"
                            v-model="addDispenserForm.angle_default">
                        <span class="input-group-text">Chute angle</span>
                        <input type="text" class="form-control" placeholder="0" aria-label="Chute angle"
                            v-model="addDispenserForm.angle_chute">
                    </div>
                    <!-- Smoothing -->
                    <div class="form-check form-switch mb-1">
                        <input class="form-check-input" type="checkbox" role="switch" id="smoothingEnabledCheck"
                            v-model="addDispenserForm.smooth_enabled">
                        <label class="form-check-label" for="smoothingEnabledCheck">Smooth servo rotation</label>
                    </div>
                    <div class="input-group mb-3">
                        <span class="input-group-text">Smooth duration (s)</span>
                        <input type="text" class="form-control" placeholder="1" aria-label="Smooth duration"
                            v-model="addDispenserForm.smooth_duration">
                        <span class="input-group-text">Smooth step time (s)</span>
                        <input type="text" class="form-control" placeholder="10" aria-label="Smooth step time"
                            v-model="addDispenserForm.step_time">
                    </div>
                    <!-- Footer -->
                    <div class="modal-footer">
                        <button type="button" class="btn btn-outline-danger me-2" data-bs-dismiss="modal"
                            @click="clearForm()">Cancel</button>
                        <button type="button" class="btn btn-primary" data-bs-dismiss="modal" @click="addDispenser()">Save
                            dispenser</button>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Pretty bad code duplication here -->
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
                        <span class="input-group-text">Smooth duration (s)</span>
                        <input type="number" class="form-control" placeholder="1" aria-label="Smooth duration"
                            v-model="editDispenserForm.smooth_duration" step="0.1">
                        <span class="input-group-text">Smooth step time (s)</span>
                        <input type="number" class="form-control" placeholder="0.01" aria-label="Smooth step time"
                            v-model="editDispenserForm.step_time" step="0.01">
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

    <!-- Delete dispenser modal -->
    <div class="modal fade" id="deleteDispenserModal" tabindex="-1" aria-labelledby="deleteDispenserModalLabel"
        aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5" id="deleteDispenserModalLabel">Confirm deletion</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <p>Are you sure that you would like to delete the dispenser index {{ deleteDispenserForm.index }}?</p>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-outline-secondary" data-bs-dismiss="modal">Close</button>
                    <button type="button" class="btn btn-danger" @click="deleteDispenser()" data-bs-dismiss="modal">Delete
                        Dispenser</button>
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
            addDispenserForm: {
                index: 0,
                servo_min: 0,
                servo_max: 0,
                angle_default: 0,
                angle_chute: 0,
                smooth_duration: 0,
                step_time: 0,
                smooth_enabled: 0,
            },
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
            },
            deleteDispenserForm: {
                id: '',
                index: '',
            }
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
        clearForm() {
            this.addDispenserForm.index = '';
            this.addDispenserForm.servo_min = '';
            this.addDispenserForm.servo_max = '';
            this.addDispenserForm.angle_default = '';
            this.addDispenserForm.angle_chute = '';
            this.addDispenserForm.smooth_duration = '';
            this.addDispenserForm.step_time = '';
            this.addDispenserForm.smooth_enabled = '';
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
        },
        setupFormDeleteDispenser(dispenser) {
            this.deleteDispenserForm.id = dispenser.id;
            this.deleteDispenserForm.index = dispenser.index;
        },
        deleteDispenser() {
            const path = '/dispensers';
            axios.delete(path, {
                data: {
                    id: this.deleteDispenserForm.id,
                    index: this.deleteDispenserForm.index
                }
            })
                .then(response => {
                    console.log(response);
                    this.getDispensers();
                })
                .catch(error => {
                    console.log(error);
                });
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
            })
                .then(response => {
                    //console.log(response);
                    this.getDispensers();
                })
                .catch(error => {
                    console.log(error);
                });
        },
        addDispenser() {
            const path = '/dispensers';
            axios.post(path, {
                index: this.editDispenserForm.index,
                servo_min: this.editDispenserForm.servo_min,
                servo_max: this.editDispenserForm.servo_max,
                angle_default: this.editDispenserForm.angle_default,
                angle_chute: this.editDispenserForm.angle_chute,
                smooth_duration: this.editDispenserForm.smooth_duration,
                step_time: this.editDispenserForm.step_time,
                smooth_enabled: this.editDispenserForm.smooth_enabled,
            })
                .then(response => {
                    //console.log(response);
                    this.clearForm();
                    this.getDispensers();
                })
                .catch(error => {
                    console.log(error);
                });
        }
    },
    created() {
        this.getDispensers();
    }
}
</script>