<script setup>
import BottomBar from '../components/BottomBar.vue';
import DateTime from '../components/DateTime.vue';
import TodayEvents from '../components/TodayEvents.vue';
</script>

<template>
  <main class="container">
    <div class="row">
      <div class="col text-center">
        <DateTime />
      </div>
    </div>
    <div class="row">
      <div class="col">
        <TodayEvents />
      </div>
    </div>
  </main>
  <!-- Full width footer with space for buttons, sticks to bottom -->
  <BottomBar />
</template>