<template>
    <q-table hide-header flat class="w-full" @row-click="(e, row) => { $emit('row_clicked', row) }">
        <template v-slot:body-cell-value="props">
            <q-td :props="props">
                {{ props.row.display }}
            </q-td>
        </template>
        <template v-slot:no-data="">
            No matching commands
        </template>
    </q-table>
</template>