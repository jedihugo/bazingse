<script lang="ts">
  import ThemeToggle from './ThemeToggle.svelte';
</script>

<header class="tui-bg-panel header-border">
  <div class="header-container">
    <a href="/" class="logo-link">
      <img src="/bazingse-logo.png" alt="BaZingSe Logo" class="logo-img" />
      <h1 class="text-xl font-bold tui-text">BaZingSe</h1>
    </a>
    <div class="flex items-center gap-2">
      <a href="/calendar" class="tui-btn text-xs nav-link">Calendar</a>
      <ThemeToggle />
    </div>
  </div>
</header>

<style>
  .header-border {
    border-bottom: 1px solid var(--tui-border);
  }

  .header-container {
    max-width: 80rem;
    margin-left: auto;
    margin-right: auto;
    padding: 0.25rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  @media (min-width: 640px) {
    .header-container {
      padding: 0.5rem;
    }
  }

  @media (min-width: 768px) {
    .header-container {
      padding: 0.75rem;
    }
  }

  .logo-link {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    text-decoration: none;
    color: inherit;
  }

  .logo-img {
    width: 3rem;
    height: 3rem;
    object-fit: contain;
  }

  .nav-link {
    padding: 0.25rem 0.5rem;
    text-decoration: none;
  }
</style>
