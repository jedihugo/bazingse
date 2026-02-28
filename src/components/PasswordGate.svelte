<script lang="ts">
  import { onMount } from 'svelte';
  import type { Snippet } from 'svelte';

  const CORRECT_PASSWORD = 'lombok29';
  const AUTH_KEY = 'bazingse_auth';

  interface Props {
    children: Snippet;
  }

  let { children }: Props = $props();

  let isAuthenticated: boolean | null = $state(null);
  let password = $state('');
  let error = $state(false);
  let shake = $state(false);

  onMount(() => {
    const auth = sessionStorage.getItem(AUTH_KEY);
    isAuthenticated = auth === 'true';
  });

  function handleSubmit(e: SubmitEvent) {
    e.preventDefault();
    if (password === CORRECT_PASSWORD) {
      sessionStorage.setItem(AUTH_KEY, 'true');
      isAuthenticated = true;
    } else {
      error = true;
      shake = true;
      password = '';
      setTimeout(() => {
        shake = false;
      }, 500);
    }
  }

  function handleInput(e: Event) {
    const target = e.target as HTMLInputElement;
    password = target.value;
    error = false;
  }
</script>

{#if isAuthenticated === null}
  <div class="min-h-screen tui-bg flex items-center justify-center">
    <div class="tui-text-muted">Loading...</div>
  </div>
{:else if isAuthenticated}
  {@render children()}
{:else}
  <div class="min-h-screen tui-bg flex items-center justify-center gate-container">
    <div class="tui-frame gate-frame" class:animate-shake={shake}>
      <div class="text-center gate-header">
        <h1 class="text-xl font-bold tui-text gate-title">BaZingSe</h1>
        <p class="tui-text-muted text-sm">Enter password</p>
      </div>
      <form onsubmit={handleSubmit}>
        <div class="gate-field">
          <div class="flex items-center gap-2">
            <span class="tui-text-water">&gt;</span>
            <input
              type="password"
              value={password}
              oninput={handleInput}
              class="gate-input"
              placeholder="Password"
              autofocus
              autocomplete="off"
            />
          </div>
          {#if error}
            <p class="gate-error">Incorrect password</p>
          {/if}
        </div>
        <button type="submit" class="w-full tui-btn gate-submit">Enter</button>
      </form>
      <div class="gate-hint">
        <span class="tui-text-dim text-xs">[Enter] Submit</span>
      </div>
    </div>
  </div>
{/if}

<style>
  .gate-container {
    padding: 1rem;
  }

  .gate-frame {
    padding: 1.5rem;
    width: 100%;
    max-width: 24rem;
  }

  .gate-header {
    margin-bottom: 1.5rem;
  }

  .gate-title {
    margin-bottom: 0.5rem;
  }

  .gate-field {
    margin-bottom: 1rem;
  }

  .gate-input {
    flex: 1;
    background: transparent;
    color: var(--tui-fg);
    outline: none;
    border: none;
    border-bottom: 1px solid var(--tui-border);
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.875rem;
    padding: 0.25rem 0;
    transition: border-color 0.15s ease;
  }

  .gate-input:focus {
    border-bottom-color: var(--tui-water);
  }

  .gate-input::placeholder {
    color: var(--tui-fg-muted);
  }

  .gate-error {
    margin-top: 0.5rem;
    font-size: 0.875rem;
    color: var(--tui-fire);
  }

  .gate-submit {
    padding-top: 0.5rem;
    padding-bottom: 0.5rem;
  }

  .gate-hint {
    margin-top: 1rem;
    text-align: center;
  }

  .animate-shake {
    animation: shake 0.5s ease-in-out;
  }

  @keyframes shake {
    0%, 100% { transform: translateX(0); }
    10%, 30%, 50%, 70%, 90% { transform: translateX(-4px); }
    20%, 40%, 60%, 80% { transform: translateX(4px); }
  }
</style>
