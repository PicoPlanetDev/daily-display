<template>
    <!-- Button for shutdown -->
    <button type="button" class="btn btn-danger me-2" data-bs-toggle="modal" data-bs-target="#shutdownModal"
        @click="resetConfirmationVariables()">
        <i class="bi bi-power"></i> Shutdown
    </button>
    <!-- Button for reboot -->
    <button type="button" class="btn btn-warning me-2" data-bs-toggle="modal" data-bs-target="#rebootModal"
        @click="resetConfirmationVariables()">
        <i class=" bi bi-arrow-counterclockwise"></i> Reboot
    </button>
    <!-- Button for auto update -->
    <button type="button" class="btn btn-primary me-2" data-bs-toggle="modal" data-bs-target="#updateModal"
        @click="resetConfirmationVariables()">
        <i class="bi bi-cloud-download"></i> Update
    </button>

    <!-- Modal to verify shutdown request -->
    <div class="modal fade" id="shutdownModal" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1"
        aria-labelledby="staticBackdropLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5 text-danger-emphasis" id="staticBackdropLabel"><i class="bi bi-power"></i>
                        Really Shutdown?</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    If you shutdown the machine, you may not be able to turn it back on without physical access.
                    <!-- Checkbox that says I understand -->
                    <div class="form-check">
                        <input class="form-check-input" type="checkbox" id="flexCheckDefault" v-model="commandAllowed">
                        <label class="form-check-label" for="flexCheckDefault">
                            I understand
                        </label>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                    <button type="button" class="btn btn-danger" :disabled="!commandAllowed" @click="shutdown('poweroff')"
                        data-bs-dismiss="modal">Shutdown</button>
                </div>
            </div>
        </div>
    </div>

    <!-- Modal to verify reboot request -->
    <div class="modal fade" id="rebootModal" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1"
        aria-labelledby="staticBackdropLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5 text-warning-emphasis" id="staticBackdropLabel"><i
                            class="bi bi-arrow-counterclockwise"></i>
                        Really Reboot?</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    Rebooting the machine will cause it to restart. Ensure that you can gain physical access to the machine
                    if it does not restart properly.
                    <!-- Checkbox that says I understand -->
                    <div class="form-check">
                        <input class="form-check-input" type="checkbox" id="flexCheckDefault" v-model="commandAllowed">
                        <label class="form-check-label" for="flexCheckDefault">
                            I understand
                        </label>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                    <button type="button" class="btn btn-warning" :disabled="!commandAllowed" @click="shutdown('reboot')"
                        data-bs-dismiss="modal">Reboot</button>
                </div>
            </div>
        </div>
    </div>

    <!-- Modal to verify update request -->
    <div class="modal fade" id="updateModal" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1"
        aria-labelledby="staticBackdropLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5 text-primary-emphasis" id="staticBackdropLabel"><i
                            class="bi bi-cloud-download"></i>
                        Really Update?</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    If you update Daily Display, it may not work properly. Ensure that you can gain physical access to the
                    machine if it exhibits unexpected behavior.
                    <!-- Checkbox that says I understand -->
                    <div class="form-check">
                        <input class="form-check-input" type="checkbox" id="flexCheckDefault" v-model="commandAllowed">
                        <label class="form-check-label" for="flexCheckDefault">
                            I understand
                        </label>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                    <button type="button" class="btn btn-primary" :disabled="!commandAllowed" @click="update()"
                        data-bs-dismiss="modal">Update</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    name: 'DangerZone',
    data() {
        return {
            commandAllowed: false,
        }
    },
    methods: {
        shutdown(type) {
            axios.post('/shutdown', { type: type })
                .then(response => {
                    console.log(response);
                })
                .catch(error => {
                    console.log(error);
                });
        },
        update() {
            axios.post('/update')
                .then(response => {
                    console.log(response);
                })
                .catch(error => {
                    console.log(error);
                });
        },
        resetConfirmationVariables() {
            this.commandAllowed = false;
        },
    },
}
</script>