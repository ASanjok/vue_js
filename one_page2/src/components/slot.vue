<template>
    <b-col class="ml-1 mb-1 mt-1 border border-secondary">
        <template v-if="$slots.default">
            <slot></slot> 
        </template>
        <template v-else>
            <p>Нет контента для отображения.</p> 
        </template>
    </b-col>

</template>
