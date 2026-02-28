<script lang="ts">
	import { goto } from '$app/navigation';
	import type { Profile } from '$lib/api';

	interface Props {
		profiles: Profile[];
		onDelete?: (id: string) => void;
		isLoading?: boolean;
	}

	let {
		profiles,
		onDelete,
		isLoading = false
	}: Props = $props();

	const ITEMS_PER_PAGE = 50;

	let searchQuery = $state('');
	let selectedIndex = $state(0);
	let visibleCount = $state(ITEMS_PER_PAGE);

	let searchEl = $state<HTMLInputElement>(undefined!);
	let listEl = $state<HTMLDivElement>(undefined!);

	// Filter profiles based on search query
	let filteredProfiles = $derived.by(() => {
		if (!searchQuery.trim()) return profiles;

		const query = searchQuery.toLowerCase();
		return profiles.filter((profile) => {
			const name = profile.name?.toLowerCase() || '';
			const date = profile.birth_date || '';
			const place = profile.place_of_birth?.toLowerCase() || '';
			return name.includes(query) || date.includes(query) || place.includes(query);
		});
	});

	// Visible profiles (lazy loaded)
	let visibleProfiles = $derived(filteredProfiles.slice(0, visibleCount));

	// Reset selection when search changes
	$effect(() => {
		// Read searchQuery to track it
		searchQuery;
		selectedIndex = 0;
		visibleCount = ITEMS_PER_PAGE;
	});

	// Scroll selected item into view
	$effect(() => {
		if (selectedIndex >= 0 && listEl) {
			const items = listEl.querySelectorAll('[data-profile-item]');
			const selected = items[selectedIndex] as HTMLElement | undefined;
			selected?.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
		}
	});

	function loadMore() {
		visibleCount = Math.min(visibleCount + ITEMS_PER_PAGE, filteredProfiles.length);
	}

	function handleScroll() {
		if (!listEl) return;
		const { scrollTop, scrollHeight, clientHeight } = listEl;
		if (scrollHeight - scrollTop - clientHeight < 100) {
			if (visibleCount < filteredProfiles.length) {
				visibleCount = Math.min(visibleCount + ITEMS_PER_PAGE, filteredProfiles.length);
			}
		}
	}

	// Keyboard navigation
	function handleKeyDown(e: KeyboardEvent) {
		const maxIndex = visibleProfiles.length - 1;

		switch (e.key) {
			case 'ArrowDown':
				e.preventDefault();
				selectedIndex = Math.min(selectedIndex + 1, maxIndex);
				// Load more if near end
				if (selectedIndex >= visibleCount - 5 && visibleCount < filteredProfiles.length) {
					visibleCount = Math.min(visibleCount + ITEMS_PER_PAGE, filteredProfiles.length);
				}
				break;
			case 'ArrowUp':
				e.preventDefault();
				selectedIndex = Math.max(selectedIndex - 1, 0);
				break;
			case 'Enter':
				e.preventDefault();
				if (visibleProfiles[selectedIndex]) {
					goto(`/profile/${visibleProfiles[selectedIndex].id}`);
				}
				break;
			case 'Escape':
				e.preventDefault();
				if (searchQuery) {
					searchQuery = '';
				} else {
					searchEl?.blur();
				}
				break;
		}
	}

	function handleProfileClick(profile: Profile) {
		goto(`/profile/${profile.id}`);
	}

	function handleDeleteClick(e: MouseEvent, id: string) {
		e.stopPropagation();
		onDelete?.(id);
	}
</script>

{#if isLoading}
	<div class="text-center py-12 tui-text-muted">Loading profiles...</div>
{:else}
	<div class="profile-list-container">
		<!-- Search Input -->
		<div class="tui-frame search-frame">
			<div class="search-row">
				<span class="tui-text search-prompt" style="color: var(--tui-water)">&gt;</span>
				<input
					bind:this={searchEl}
					type="text"
					bind:value={searchQuery}
					onkeydown={handleKeyDown}
					placeholder="Type to search..."
					class="search-input tui-text"
					style="caret-color: var(--tui-water)"
					autocomplete="off"
					spellcheck="false"
				/>
				<span class="text-xs tui-text-muted">
					{filteredProfiles.length.toLocaleString()} profiles
				</span>
			</div>
			<div class="search-hints tui-text-dim">
				<span>[&#8593;&#8595;] Navigate</span>
				<span>[Enter] Open</span>
				<span>[Esc] Clear</span>
			</div>
		</div>

		<!-- Profile List -->
		<div
			bind:this={listEl}
			class="profile-list-scroll"
			onscroll={handleScroll}
		>
			{#if visibleProfiles.length === 0}
				<div class="text-center py-8 tui-text-muted">
					{#if searchQuery}
						No match for "{searchQuery}"
					{:else}
						No profiles yet. Create one to get started.
					{/if}
				</div>
			{:else}
				<div class="profile-items">
					{#each visibleProfiles as profile, index (profile.id)}
							<div
							data-profile-item
							class="profile-item"
							class:profile-item-selected={index === selectedIndex}
							onclick={() => handleProfileClick(profile)}
							onkeydown={(e) => { if (e.key === 'Enter') handleProfileClick(profile); }}
							onmouseenter={() => { selectedIndex = index; }}
							role="button"
							tabindex="-1"
						>
							<div class="profile-item-row">
								<div class="profile-item-left">
									<span
										class="profile-cursor"
										style="color: {index === selectedIndex ? 'var(--tui-water)' : 'transparent'}"
									>
										&gt;
									</span>
									<div>
										<div class="font-semibold tui-text">{profile.name}</div>
										<div class="text-sm tui-text-dim">
											{profile.birth_date}
											{#if profile.birth_time}
												{' '}{profile.birth_time}
											{/if}
											{' - '}
											<span style="color: {profile.gender === 'female' ? 'var(--tui-accent-pink)' : 'var(--tui-water)'}">
												{profile.gender === 'female' ? '\u2640' : '\u2642'}
											</span>
											{#if profile.place_of_birth}
												<span class="tui-text-muted" style="margin-left: 0.5rem">
													{profile.place_of_birth.length > 30
														? profile.place_of_birth.substring(0, 30) + '...'
														: profile.place_of_birth}
												</span>
											{/if}
										</div>
									</div>
								</div>
								{#if onDelete}
									<button
										onclick={(e) => handleDeleteClick(e, profile.id)}
										class="delete-btn tui-text-muted"
										title="Delete profile"
									>
										<svg xmlns="http://www.w3.org/2000/svg" class="delete-icon" viewBox="0 0 20 20" fill="currentColor">
											<path fill-rule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd" />
										</svg>
									</button>
								{/if}
							</div>
						</div>
					{/each}

					<!-- Load more button -->
					{#if visibleCount < filteredProfiles.length}
						<button
							onclick={loadMore}
							class="load-more-btn tui-text-muted tui-frame"
						>
							Showing {visibleCount.toLocaleString()} of {filteredProfiles.length.toLocaleString()}
							<span class="font-bold" style="margin-left: 0.5rem">Load more</span>
						</button>
					{/if}
				</div>
			{/if}
		</div>
	</div>
{/if}

<style>
	.profile-list-container {
		display: flex;
		flex-direction: column;
		height: calc(100vh - 200px);
	}

	.search-frame {
		padding: 0.75rem;
		margin-bottom: 1rem;
	}

	.search-row {
		display: flex;
		align-items: center;
		gap: 0.5rem;
	}

	.search-prompt {
		flex-shrink: 0;
	}

	.search-input {
		flex: 1;
		background: transparent;
		border: none;
		outline: none;
		font-family: inherit;
		font-size: inherit;
		color: inherit;
	}

	.search-hints {
		margin-top: 0.5rem;
		font-size: 0.75rem;
		display: flex;
		gap: 1rem;
	}

	.profile-list-scroll {
		flex: 1;
		overflow-y: auto;
		scrollbar-width: thin;
	}

	.profile-items {
		display: flex;
		flex-direction: column;
		gap: 0.25rem;
	}

	.profile-item {
		padding: 0.75rem;
		cursor: pointer;
		transition: background-color 0.1s ease;
		border: 1px solid transparent;
	}

	.profile-item-selected {
		border-color: var(--tui-water);
		background-color: var(--tui-bg-alt);
	}

	.profile-item-row {
		display: flex;
		justify-content: space-between;
		align-items: flex-start;
	}

	.profile-item-left {
		display: flex;
		align-items: flex-start;
		gap: 0.5rem;
	}

	.profile-cursor {
		font-family: 'JetBrains Mono', monospace;
		width: 1rem;
		flex-shrink: 0;
	}

	.delete-btn {
		padding: 0.25rem;
		opacity: 0;
		transition: opacity 0.15s ease;
		background: none;
		border: none;
		cursor: pointer;
		color: inherit;
	}

	.profile-item:hover .delete-btn {
		opacity: 1;
	}

	.delete-icon {
		width: 1rem;
		height: 1rem;
	}

	.load-more-btn {
		width: 100%;
		text-align: center;
		padding: 1rem;
		font-size: 0.875rem;
		cursor: pointer;
		margin-top: 0.5rem;
		background: none;
		border-color: var(--tui-border);
	}

	.load-more-btn:hover {
		background-color: var(--tui-bg-alt);
	}
</style>
