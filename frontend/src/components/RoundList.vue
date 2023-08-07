<template>
    <div class="row">
        <div class="col-sm-10">
            <h3><i class="bi bi-clock"></i> Rounds</h3>
            <hr>
            <div>
                <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#addRoundModal">
                    <i class="bi bi-plus"></i> Add Round
                </button>
            </div>
            <div>
                <div class="mt-3" v-if="rounds.length == 0">
                    No rounds found. Click the button above to create one!
                    <hr>
                </div>
                <table class="table table-hover" v-if="rounds.length > 0">
                    <thead>
                        <tr>
                            <th scope="col">Name</th>
                            <th scope="col">Time</th>
                            <th><!-- Left blank for buttons --></th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(round, index) in rounds" :key="index">
                            <td>{{ round.name }}</td>
                            <td>{{ round.time }}</td>
                            <td>
                                <div class="btn-group" role="group">
                                    <button type="button" class="btn btn-outline-warning btn-sm"
                                        @click="setupFormEditRound(round)" data-bs-toggle="modal"
                                        data-bs-target="#editRoundModal">
                                        <i class="bi bi-pencil"></i>
                                    </button>
                                    <button type="button" class="btn btn-outline-danger btn-sm"
                                        @click="setupFormDeleteRound(round)" data-bs-toggle="modal"
                                        data-bs-target="#deleteRoundModal">
                                        <i class="bi bi-trash"></i>
                                    </button>
                                </div>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <!-- Add round modal -->
    <div class="modal fade" id="addRoundModal" tabindex="-1" aria-labelledby="addRoundModalLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5" id="addRoundModalLabel">Add Round</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"
                        @click="clearForm"></button>
                </div>
                <div class="modal-body">
                    <div class="mb-3">
                        <label for="addRoundFormName" class="form-label">Name</label>
                        <input type="text" class="form-control" id="addRoundFormName" placeholder="Morning"
                            v-model="addRoundForm.name">
                    </div>
                    <div class="mb-3">
                        <label for="addRoundFormTime" class="form-label">Time</label>
                        <input type="text" class="form-control" id="addRoundFormRound" placeholder="08:00"
                            aria-describedby="roundHelp" v-model="addRoundForm.time">
                        <div id="roundHelp" class="form-text">24 hour time in hh:mm format</div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-outline-danger me-2" data-bs-dismiss="modal"
                            @click="clearForm()">Cancel</button>
                        <button type="button" class="btn btn-primary" data-bs-dismiss="modal" @click="addRound()">Save
                            round</button>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Pretty bad code duplication here -->
    <!-- Edit round modal -->
    <div class="modal fade" id="editRoundModal" tabindex="-1" aria-labelledby="editRoundModalLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5" id="editRoundModalLabel">Edit Round</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <div class="mb-3">
                        <label for="editRoundFormName" class="form-label">Name</label>
                        <input type="text" class="form-control" id="editRoundFormName" placeholder="Morning"
                            v-model="editRoundForm.name">
                    </div>
                    <div class="mb-3">
                        <label for="editRoundFormRound" class="form-label">Time</label>
                        <input type="text" class="form-control" id="editRoundFormRound" placeholder="08:00"
                            aria-describedby="roundHelp" v-model="editRoundForm.time">
                        <div id="roundHelp" class="form-text">24 hour time in hh:mm format</div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-outline-danger me-2" data-bs-dismiss="modal">Cancel</button>
                        <button type="button" class="btn btn-primary" data-bs-dismiss="modal" @click="editRound()">Save
                            round</button>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Delete round modal -->
    <div class="modal fade" id="deleteRoundModal" tabindex="-1" aria-labelledby="deleteRoundModalLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5" id="deleteRoundModalLabel">Confirm deletion</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <p>Are you sure that you would like to delete the round {{ deleteRoundDialog.name }}?</p>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-outline-secondary" data-bs-dismiss="modal">Close</button>
                    <button type="button" class="btn btn-danger" @click="deleteRound()" data-bs-dismiss="modal">Delete
                        round</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    name: 'RoundList',
    data() {
        return {
            rounds: [],
            addRoundForm: {
                name: '',
                time: '',
            },
            editRoundForm: {
                id: '',
                name: '',
                time: '',
            },
            deleteRoundDialog: {
                id: '',
                name: '',
            }
        };
    },
    methods: {
        getRounds() {
            const path = '/rounds';
            axios.get(path)
                .then(response => {
                    this.rounds = response.data.rounds;
                })
                .catch(error => {
                    console.log(error);
                });
        },
        clearForm() {
            this.addRoundForm.name = '';
            this.addRoundForm.round = '';
        },
        setupFormEditRound(round) {
            this.editRoundForm.id = round.id;
            this.editRoundForm.name = round.name;
            this.editRoundForm.time = round.time;
        },
        setupFormDeleteRound(round) {
            this.deleteRoundDialog.id = round.id;
            this.deleteRoundDialog.name = round.name;
        },
        deleteRound() {
            const path = '/rounds';
            console.log(this.deleteRoundDialog.id);
            axios.delete(path, {
                data: {
                    id: this.deleteRoundDialog.id,
                    name: this.deleteRoundDialog.name
                }
            })
                .then(response => {
                    console.log(response);
                    this.getRounds();
                })
                .catch(error => {
                    console.log(error);
                });
        },
        editRound() {
            const path = '/rounds';
            axios.put(path, {
                id: this.editRoundForm.id,
                name: this.editRoundForm.name,
                time: this.editRoundForm.time,
            })
                .then(response => {
                    console.log(response);
                    this.getRounds();
                })
                .catch(error => {
                    console.log(error);
                });
        },
        addRound() {
            const path = '/rounds';
            axios.post(path, {
                name: this.addRoundForm.name,
                time: this.addRoundForm.time,
            })
                .then(response => {
                    console.log(response);
                    this.clearForm();
                    this.getRounds();
                })
                .catch(error => {
                    console.log(error);
                });
        }
    },
    created() {
        this.getRounds();
    }
}
</script>