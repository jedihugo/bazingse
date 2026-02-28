<script lang="ts">
  import '../app.css';
  import PasswordGate from '../components/PasswordGate.svelte';
</script>

<svelte:head>
  <title>BaZingSe - Chinese BaZi Astrology</title>
  <meta name="description" content="Chinese BaZi Four Pillars astrology calculator" />
</svelte:head>

<PasswordGate>
  {#snippet children()}
    <slot />
  {/snippet}
</PasswordGate>
