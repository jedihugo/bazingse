<script lang="ts">
  import { page } from '$app/stores';
  import Header from '../../../components/Header.svelte';
  import ProfilePage from '../../../components/ProfilePage.svelte';

  let id = $derived($page.params.id);
</script>

{#if !id}
  <div class="min-h-screen tui-bg">
    <Header />
    <main class="mx-auto main-content p-4">
      <p class="text-center tui-text-muted">Loading...</p>
    </main>
  </div>
{:else}
  <div class="min-h-screen tui-bg">
    <Header />
    <main class="mx-auto main-content">
      <div class="mx-auto" style="max-width: 900px;">
        <ProfilePage profileId={id} />
      </div>
    </main>
  </div>
{/if}
