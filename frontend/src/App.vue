<script setup>
import DateTime from './components/DateTime.vue';
import TodayEvents from './components/TodayEvents.vue';
</script>

<template>
  <main class="container-fluid">
    <div class="row">
      <div class="col">
        <DateTime />
      </div>
    </div>
    <div class="row">
      <div class="col">
        <TodayEvents />
      </div>
    </div>

  </main>
</template>

<style scoped></style>
