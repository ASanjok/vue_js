<template>
    <b-col class="ml-1 mb-1 mt-1 border border-secondary">
        <template v-if="$slots.default">
            <slot></slot> <!-- Показываем контент из слота -->
        </template>
        <template v-else>
            <p>Нет контента для отображения.</p> <!-- Показываем альтернативное сообщение -->
        </template>
    </b-col>

</template>
