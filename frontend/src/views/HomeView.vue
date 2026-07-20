<script setup>
import AppShell from "../components/AppShell.vue";
import { useAppShell } from "../composables/useAppShell";

const { apiBaseUrl } = useAppShell();
</script>

<template>
  <AppShell :api-base-url="apiBaseUrl" />
</template>
