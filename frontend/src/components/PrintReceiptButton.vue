<template>
    <button class="btn btn-outline-secondary btn-sm" @click="printReceipt()">Print Receipt</button>
</template>

<script>
import axios from 'axios';
export default {
    name: 'PrintReceiptButton',
    methods: {
        printReceipt() {
            const path = '/print_receipt';
            axios.get(path)
                .then(response => {
                    console.log(response);
                })
                .catch(error => {
                    console.log(error);
                });
        }
    }
}
</script>