<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import Header from '../components/Header.svelte';
	import InlineProfileForm from '../components/InlineProfileForm.svelte';
	import SearchableProfileList from '../components/SearchableProfileList.svelte';
	import { getProfiles, deleteProfile, type Profile } from '$lib/api';

	let profiles = $state<Profile[]>([]);
	let isLoading = $state(true);
	let error = $state<string | null>(null);
	let showCreateForm = $state(false);

	async function loadProfiles() {
		try {
			isLoading = true;
			const data = await getProfiles();
			profiles = data;
			error = null;
		} catch (err) {
			error = err instanceof Error ? err.message : 'Failed to load profiles';
		} finally {
			isLoading = false;
		}
	}

	onMount(() => {
		loadProfiles();
	});

	function handleProfileCreated(profile: { id: string; name: string }) {
		showCreateForm = false;
		goto(`/profile/${profile.id}`);
	}

	async function handleDeleteProfile(id: string) {
		if (!confirm('Are you sure you want to delete this profile?')) return;

		try {
			await deleteProfile(id);
			profiles = profiles.filter((p) => p.id !== id);
		} catch (err) {
			error = err instanceof Error ? err.message : 'Failed to delete profile';
		}
	}
</script>

<div class="min-h-screen tui-bg">
	<Header />
	<main class="mx-auto main-content px-4 py-4">
		<div class="mx-auto" style="max-width: 800px;">
			<div class="page-header">
				<h1 class="text-2xl font-bold tui-text">Profiles</h1>
				{#if !showCreateForm}
					<button
						onclick={() => { showCreateForm = true; }}
						class="tui-btn"
					>
						+ New Profile
					</button>
				{/if}
			</div>

			{#if error}
				<div class="error-banner tui-frame" style="border-color: var(--tui-error); color: var(--tui-error);">
					{error}
				</div>
			{/if}

			<!-- Inline Create Form -->
			{#if showCreateForm}
				<div class="form-wrapper">
					<InlineProfileForm
						onSuccess={handleProfileCreated}
						onCancel={() => { showCreateForm = false; }}
					/>
				</div>
			{/if}

			<!-- Searchable Profile List -->
			{#if !showCreateForm}
				<SearchableProfileList
					{profiles}
					onDelete={handleDeleteProfile}
					{isLoading}
				/>
			{/if}
		</div>
	</main>
</div>

<style>
	.page-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 1rem;
	}

	.error-banner {
		margin-bottom: 1rem;
		padding: 0.75rem;
	}

	.form-wrapper {
		margin-bottom: 1rem;
	}
</style>
