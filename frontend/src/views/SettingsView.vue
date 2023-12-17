<script setup>
import DangerZone from '../components/DangerZone.vue';
import DispenserList from '../components/DispenserList.vue';
import PillList from '../components/PillList.vue';
import RoundList from '../components/RoundList.vue';
import SettingsForm from '../components/SettingsForm.vue';
</script>

<template>
  <div class="container">
    <div class="fs-1"><i class="bi bi-gear-wide-connected"></i> Settings</div>
    <div class="lead">Changing some of these settings will require Daily Display to restart.</div>
    <hr>
    <SettingsForm />
    <div class="fs-2"><i class="bi bi-capsule-pill"></i> Pill Dispenser</div>
    <div class="lead">These settings apply immediately</div>
    <hr>
    <!-- Database editors -->
    <PillList />
    <RoundList />
    <DispenserList />
    <!-- Danger zone -->
    <!-- <div class="border rounded border-danger-subtle bg-danger-subtle"> -->
    <div class="fs-2 text-danger-emphasis"><i class="bi bi-exclamation-triangle-fill"></i> Danger Zone</div>
    <hr>
    <DangerZone />
    <!-- </div> -->
  </div>
</template>