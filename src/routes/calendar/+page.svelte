<script lang="ts">
  import Header from '../../components/Header.svelte';
  import DongGongCalendar from '../../components/DongGongCalendar.svelte';
</script>

<div class="min-h-screen tui-bg">
  <Header />
  <main class="mx-auto main-content px-4 py-4">
    <div class="mx-auto" style="max-width: 800px;">
      <DongGongCalendar />
    </div>
  </main>
</div>
