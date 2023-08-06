<template>
    <div class="row">
        <div class="col-sm-10">
            <h2>Pills</h2>
            <hr>
            <div>
                <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#addPillModal">
                    <i class="bi bi-plus"></i> Add Pill
                </button>
            </div>
            <div>
                <div class="mt-3" v-if="pills.length == 0">No pills found. Click the button above to create one!</div>
                <table class="table table-hover" v-if="pills.length > 0">
                    <thead>
                        <tr>
                            <th scope="col">Name</th>
                            <th scope="col">Round</th>
                            <th scope="col">Number</th>
                            <th scope="col">Dispenser</th>
                            <th></th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(pill, index) in pills" :key="index">
                            <td>{{ pill.name }}</td>
                            <td>{{ pill.round }}</td>
                            <td>{{ pill.number }}</td>
                            <td>{{ pill.dispenser }}</td>
                            <td>
                                <div class="btn-group" role="group">
                                    <button type="button" class="btn btn-outline-warning btn-sm"
                                        @click="setupFormEditPill(pill)" data-bs-toggle="modal"
                                        data-bs-target="#editPillModal">
                                        <i class="bi bi-pencil"></i>
                                    </button>
                                    <button type="button" class="btn btn-outline-danger btn-sm"
                                        @click="setupFormDeletePill(pill)" data-bs-toggle="modal"
                                        data-bs-target="#deletePillModal">
                                        <i class="bi bi-trash"></i>
                                    </button>
                                </div>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <hr>
        </div>
    </div>

    <!-- Add pill modal -->
    <div class="modal fade" id="addPillModal" tabindex="-1" aria-labelledby="addPillModalLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5" id="addPillModalLabel">Add pill</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"
                        @click="clearForm"></button>
                </div>
                <div class="modal-body">
                    <div class="mb-3">
                        <label for="addPillFormName" class="form-label">Name</label>
                        <input type="text" class="form-control" id="addPillFormName" placeholder="Paracetamol"
                            v-model="addPillForm.name">
                    </div>
                    <div class="mb-3">
                        <label for="addPillFormRound" class="form-label">Round</label>
                        <input type="text" class="form-control" id="addPillFormRound" placeholder="Morning"
                            aria-describedby="roundHelp" v-model="addPillForm.round">
                        <div id="roundHelp" class="form-text">Ensure that this exactly matches a round name that you have
                            set</div>
                    </div>
                    <div class="mb-3">
                        <label for="addPillFormNumber" class="form-label">Number</label>
                        <input type="number" class="form-control" id="addPillFormNumber" placeholder="1"
                            aria-describedby="numberHelp" v-model="addPillForm.number">
                        <div id="numberHelp" class="form-text">The number of pills to dispense for a full dose</div>
                    </div>
                    <div class="mb-3">
                        <label for="addPillFormDispenser" class="form-label">Dispenser</label>
                        <input type="number" class="form-control" id="addPillFormDispenser" placeholder="0"
                            aria-describedby="dispenserHelp" v-model="addPillForm.dispenser">
                        <div id="dispenserHelp" class="form-text">The dispenser index that this pill is loaded in</div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-outline-danger me-2" data-bs-dismiss="modal"
                            @click="clearForm()">Cancel</button>
                        <button type="button" class="btn btn-primary" data-bs-dismiss="modal" @click="addPill()">Save
                            pill</button>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Pretty bad code duplication here -->
    <!-- Edit pill modal -->
    <div class="modal fade" id="editPillModal" tabindex="-1" aria-labelledby="editPillModalLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5" id="editPillModalLabel">Edit pill</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <div class="mb-3">
                        <label for="editPillFormName" class="form-label">Name</label>
                        <input type="text" class="form-control" id="editPillFormName" placeholder="Paracetamol"
                            v-model="editPillForm.name">
                    </div>
                    <div class="mb-3">
                        <label for="editPillFormRound" class="form-label">Round</label>
                        <input type="text" class="form-control" id="editPillFormRound" placeholder="Morning"
                            aria-describedby="roundHelp" v-model="editPillForm.round">
                        <div id="roundHelp" class="form-text">Ensure that this exactly matches a round name that you have
                            set</div>
                    </div>
                    <div class="mb-3">
                        <label for="editPillFormNumber" class="form-label">Number</label>
                        <input type="number" class="form-control" id="editPillFormNumber" placeholder="1"
                            aria-describedby="numberHelp" v-model="editPillForm.number">
                        <div id="numberHelp" class="form-text">The number of pills to dispense for a full dose</div>
                    </div>
                    <div class="mb-3">
                        <label for="editPillFormDispenser" class="form-label">Dispenser</label>
                        <input type="number" class="form-control" id="editPillFormDispenser" placeholder="1"
                            aria-describedby="dispenserHelp" v-model="editPillForm.dispenser">
                        <div id="dispenserHelp" class="form-text">The dispenser index that this pill is loaded in</div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-outline-danger me-2" data-bs-dismiss="modal">Cancel</button>
                        <button type="button" class="btn btn-primary" data-bs-dismiss="modal" @click="editPill()">Save
                            pill</button>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Delete pill modal -->
    <div class="modal fade" id="deletePillModal" tabindex="-1" aria-labelledby="deletePillModalLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5" id="deletePillModalLabel">Confirm deletion</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <p>Are you sure that you would like to delete the pill {{ deletePillDialog.name }}?</p>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-outline-secondary" data-bs-dismiss="modal">Close</button>
                    <button type="button" class="btn btn-danger" @click="deletePill()" data-bs-dismiss="modal">Delete
                        pill</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    name: 'PillList',
    data() {
        return {
            pills: [],
            addPillForm: {
                name: '',
                round: '',
                number: '',
                dispenser: '',
            },
            editPillForm: {
                id: '',
                name: '',
                round: '',
                number: '',
                dispenser: '',
            },
            deletePillDialog: {
                id: '',
                name: '',
            }
        };
    },
    methods: {
        getPills() {
            const path = '/pills';
            axios.get(path)
                .then(response => {
                    this.pills = response.data.pills;
                })
                .catch(error => {
                    console.log(error);
                });
        },
        clearForm() {
            this.addPillForm.name = '';
            this.addPillForm.round = '';
            this.addPillForm.number = '';
            this.addPillForm.dispenser = '';
        },
        setupFormEditPill(pill) {
            this.editPillForm.id = pill.id;
            this.editPillForm.name = pill.name;
            this.editPillForm.round = pill.round;
            this.editPillForm.number = pill.number;
            this.editPillForm.dispenser = pill.dispenser;
        },
        setupFormDeletePill(pill) {
            this.deletePillDialog.id = pill.id;
            this.deletePillDialog.name = pill.name;
        },
        deletePill() {
            const path = '/pills';
            console.log(this.deletePillDialog.id);
            axios.delete(path, {
                data: {
                    id: this.deletePillDialog.id,
                    name: this.deletePillDialog.name
                }
            })
                .then(response => {
                    console.log(response);
                    this.getPills();
                })
                .catch(error => {
                    console.log(error);
                });
        },
        editPill() {
            const path = '/pills';
            axios.put(path, {
                id: this.editPillForm.id,
                name: this.editPillForm.name,
                round: this.editPillForm.round,
                number: this.editPillForm.number,
                dispenser: this.editPillForm.dispenser,
            })
                .then(response => {
                    console.log(response);
                    this.getPills();
                })
                .catch(error => {
                    console.log(error);
                });
        },
        addPill() {
            const path = '/pills';
            axios.post(path, {
                name: this.addPillForm.name,
                round: this.addPillForm.round,
                number: this.addPillForm.number,
                dispenser: this.addPillForm.dispenser,
            })
                .then(response => {
                    console.log(response);
                    this.clearForm();
                    this.getPills();
                })
                .catch(error => {
                    console.log(error);
                });
        }
    },
    created() {
        this.getPills();
    }
}
</script>