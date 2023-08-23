<template>
    <div class="alert fade show" :class="style" role="alert">
        {{ message }}
    </div>
</template>

<script>
export default {
    name: 'Alert',
    props: {
        message: String,
        style: "alert-primary",
    },
}
</script>