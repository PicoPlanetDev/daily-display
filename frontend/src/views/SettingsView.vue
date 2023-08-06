<script setup>
import PillList from '../components/PillList.vue';
import RoundList from '../components/RoundList.vue';
import SettingsForm from '../components/SettingsForm.vue';
</script>

<template>
  <div class="container">
    <h1>Settings</h1>
    <SettingsForm />
    <PillList />
    <RoundList />
  </div>
</template>