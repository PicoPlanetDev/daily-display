<script setup>
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

                </div>
                <div class="col">
                    <RouterLink to="/settings" class="btn btn-outline-secondary btn-sm float-end">Settings</RouterLink>
                </div>
            </div>
        </div>
    </footer>
</template>