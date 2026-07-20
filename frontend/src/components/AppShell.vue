<script setup>
defineProps({
  apiBaseUrl: {
    type: String,
    required: true,
  },
});
</script>

<template>
  <main class="min-h-screen px-6 py-10">
    <div class="mx-auto flex max-w-5xl flex-col gap-8">
      <section class="rounded-3xl border border-white/10 bg-white/5 p-8 shadow-2xl shadow-black/20 backdrop-blur">
        <p class="text-sm uppercase tracking-[0.3em] text-ember-400">HeppySitoUsato</p>
        <h1 class="mt-4 text-4xl font-semibold text-white">Frontend Vue inizializzato</h1>
        <p class="mt-4 max-w-2xl text-base leading-7 text-stone-300">
          La base Vite, Pinia, TanStack Query e Tailwind è pronta. I componenti di ricerca
          verranno introdotti negli step successivi della roadmap.
        </p>
      </section>

      <section class="grid gap-4 md:grid-cols-2">
        <article class="rounded-3xl border border-white/10 bg-stone-900/80 p-6">
          <h2 class="text-lg font-medium text-white">Stack attivo</h2>
          <ul class="mt-4 space-y-2 text-sm text-stone-300">
            <li>Vue 3 con Composition API</li>
            <li>Vite come build tool</li>
            <li>Pinia per stato client</li>
            <li>TanStack Query per server state</li>
            <li>Tailwind CSS per styling</li>
          </ul>
        </article>

        <article class="rounded-3xl border border-white/10 bg-stone-900/80 p-6">
          <h2 class="text-lg font-medium text-white">Configurazione API</h2>
          <p class="mt-4 text-sm text-stone-300">
            Base URL corrente:
            <code class="rounded bg-white/10 px-2 py-1 text-ember-400">{{ apiBaseUrl }}</code>
          </p>
        </article>
      </section>
    </div>
  </main>
</template>
