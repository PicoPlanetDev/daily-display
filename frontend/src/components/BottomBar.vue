<script setup>
import PillWarning from './PillWarning.vue';
import GetButton from './GetButton.vue';
import Version from './Version.vue';
import { RouterLink } from 'vue-router';
</script>

<template>
    <footer class="footer fixed-bottom py-1 bg-dark">
        <div class="container-fluid">
            <div class="row">
                <div class="col">
                    <Version />
                </div>
                <div class="col">
                    <PillWarning />
                </div>
                <div class="col">
                    <GetButton path="/print_receipt" label="Print reciept" />
                    <GetButton path="/feed_printer" label="Feed printer" />
                    <GetButton path="/print_qr" label="Print QR" />
                    <RouterLink to="/settings" class="btn btn-outline-secondary btn-sm float-end">Settings</RouterLink>
                </div>
            </div>
        </div>
    </footer>
</template>