<template>
    <q-table hide-header flat class="w-full" @row-click="onRowClick">
        <template v-slot:body-cell-value="props">
            <q-td :props="props">
                {{ props.row.value }}
            </q-td>
        </template>
    </q-table>
</template>

<script>
export default {
    methods: {
        onRowClick(evt, row) {
            this.$emit('row_clicked', row);
        }
    }
}
</script>