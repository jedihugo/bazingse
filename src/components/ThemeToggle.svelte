<script lang="ts">
  import { onMount } from 'svelte';

  type Theme = 'system' | 'light' | 'dark';

  let theme: Theme = $state('system');
  let mounted = $state(false);

  onMount(() => {
    mounted = true;
    const saved = localStorage.getItem('theme') as Theme | null;
    if (saved && ['system', 'light', 'dark'].includes(saved)) {
      theme = saved;
      applyTheme(saved);
    }
  });

  function applyTheme(newTheme: Theme) {
    if (newTheme === 'system') {
      document.documentElement.removeAttribute('data-theme');
    } else {
      document.documentElement.setAttribute('data-theme', newTheme);
    }
  }

  function cycleTheme() {
    const nextTheme: Theme = theme === 'system' ? 'dark' : theme === 'dark' ? 'light' : 'system';
    theme = nextTheme;
    localStorage.setItem('theme', nextTheme);
    applyTheme(nextTheme);
  }

  const icon = $derived(theme === 'system' ? 'A' : theme === 'dark' ? 'D' : 'L');
  const label = $derived(theme === 'system' ? 'Auto' : theme === 'dark' ? 'Dark' : 'Light');
</script>

{#if !mounted}
  <button class="tui-btn opacity-0" aria-hidden="true">[A]</button>
{:else}
  <button
    onclick={cycleTheme}
    class="tui-btn"
    title="Theme: {label} (click to cycle)"
    aria-label="Current theme: {label}. Click to change."
  >
    [{icon}]
  </button>
{/if}

<style>
  .opacity-0 {
    opacity: 0;
  }
</style>
