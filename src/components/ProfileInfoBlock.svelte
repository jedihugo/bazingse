<script lang="ts">
	import { tick } from 'svelte';
	import type { Profile, ProfileUpdate } from '$lib/api.types';
	import { updateProfile } from '$lib/api';
	import GuidedDateInput from './chat-form/GuidedDateInput.svelte';
	import GuidedTimeInput from './chat-form/GuidedTimeInput.svelte';

	interface Props {
		profile: Profile;
		onUpdate?: (profile: Profile) => void;
		onBack?: () => void;
		onBirthDataChange?: () => void;
	}

	let {
		profile,
		onUpdate,
		onBack,
		onBirthDataChange
	}: Props = $props();

	// Editing state
	let editingField: string | null = $state(null);
	let editValue = $state('');
	let isSaving = $state(false);

	// Structured date editing state
	let dateYear: string | number = $state('');
	let dateMonth: string | number = $state('');
	let dateDay: string | number = $state('');

	// Structured time editing state
	let timeHour = $state('');
	let timeMinute = $state('');
	let timeUnknown = $state(false);

	// Refs for text inputs
	let inputEl: HTMLInputElement | undefined = $state(undefined);

	// Auto-focus text input when editing a text field
	$effect(() => {
		if (
			editingField &&
			editingField !== 'birth_date' &&
			editingField !== 'birth_time' &&
			inputEl
		) {
			inputEl.focus();
			inputEl.select();
		}
	});

	function handleEdit(field: string, value: string) {
		if (field === 'birth_date') {
			const parts = profile.birth_date.split('-');
			dateYear = parts[0] || '';
			dateMonth = parts[1] ? String(parseInt(parts[1])) : '';
			dateDay = parts[2] ? String(parseInt(parts[2])) : '';
		} else if (field === 'birth_time') {
			if (profile.birth_time) {
				const parts = profile.birth_time.split(':');
				timeHour = parts[0] || '';
				timeMinute = parts[1] || '';
				timeUnknown = false;
			} else {
				timeHour = '';
				timeMinute = '';
				timeUnknown = true;
			}
		} else {
			editValue = value;
		}
		editingField = field;
	}

	async function handleSave() {
		if (!editingField || isSaving) return;

		const updateData: ProfileUpdate = {};
		let isBirthDataChange = false;

		if (editingField === 'birth_date') {
			const y = String(dateYear).padStart(4, '0');
			const m = String(dateMonth).padStart(2, '0');
			const d = String(dateDay).padStart(2, '0');
			const newDate = `${y}-${m}-${d}`;

			const yNum = parseInt(y);
			const mNum = parseInt(m);
			const dNum = parseInt(d);
			if (yNum < 1900 || yNum > 2100 || mNum < 1 || mNum > 12 || dNum < 1 || dNum > 31) {
				editingField = null;
				return;
			}
			if (newDate !== profile.birth_date) {
				updateData.birth_date = newDate;
				isBirthDataChange = true;
			}
		} else if (editingField === 'birth_time') {
			if (timeUnknown) {
				if (profile.birth_time) {
					updateData.birth_time = '';
					isBirthDataChange = true;
				}
			} else {
				const h = timeHour.padStart(2, '0');
				const min = timeMinute.padStart(2, '0');
				const hNum = parseInt(h);
				const minNum = parseInt(min);
				if (isNaN(hNum) || hNum < 0 || hNum > 23 || isNaN(minNum) || minNum < 0 || minNum > 59) {
					editingField = null;
					return;
				}
				const newTime = `${h}:${min}`;
				if (newTime !== (profile.birth_time || '')) {
					updateData.birth_time = newTime;
					isBirthDataChange = true;
				}
			}
		} else {
			const trimmedValue = editValue.trim();
			if (editingField === 'name' && trimmedValue !== profile.name) {
				if (!trimmedValue) {
					editingField = null;
					return;
				}
				updateData.name = trimmedValue;
			} else if (editingField === 'place_of_birth' && trimmedValue !== (profile.place_of_birth || '')) {
				updateData.place_of_birth = trimmedValue || undefined;
			} else if (editingField === 'phone' && trimmedValue !== (profile.phone || '')) {
				updateData.phone = trimmedValue || undefined;
			}
		}

		// Only save if there are changes
		if (Object.keys(updateData).length === 0) {
			editingField = null;
			return;
		}

		try {
			isSaving = true;
			const updated = await updateProfile(profile.id, updateData);
			onUpdate?.(updated);
			if (isBirthDataChange) {
				onBirthDataChange?.();
			}
		} catch (err) {
			console.error('Failed to save:', err);
		} finally {
			isSaving = false;
			editingField = null;
		}
	}

	function handleKeyDown(e: KeyboardEvent) {
		if (e.key === 'Enter') {
			handleSave();
		} else if (e.key === 'Escape') {
			editingField = null;
		}
	}

	function handleDateKeyDown(e: KeyboardEvent) {
		if (e.key === 'Escape') editingField = null;
		if (e.key === 'Enter') handleSave();
	}

	function handleInputChange(e: Event) {
		editValue = (e.target as HTMLInputElement).value;
	}
</script>

<div class="profile-info-block tui-bg-panel border-b tui-border-color">
	<!-- Back button + Name row -->
	<div class="name-row">
		{#if onBack}
			<button onclick={onBack} class="tui-back-btn" title="Click to edit">
				<svg xmlns="http://www.w3.org/2000/svg" class="back-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
				</svg>
			</button>
		{/if}

		<!-- Editable Name -->
		{#if editingField === 'name'}
			<input
				bind:this={inputEl}
				type="text"
				value={editValue}
				oninput={handleInputChange}
				onblur={handleSave}
				onkeydown={handleKeyDown}
				class="name-edit-input tui-text"
				style="border-color: var(--tui-water)"
				maxlength={100}
			/>
		{:else}
			<!-- svelte-ignore a11y_click_events_have_key_events -->
			<!-- svelte-ignore a11y_no_noninteractive_element_interactions -->
			<h1
				onclick={() => handleEdit('name', profile.name)}
				class="name-display tui-text"
				title="Click to edit"
			>
				{profile.name}
			</h1>
		{/if}
	</div>

	<!-- Birth info row -->
	<div class="birth-info-row tui-text-dim">
		{#if editingField === 'birth_date'}
			<!-- svelte-ignore a11y_no_static_element_interactions -->
			<div class="inline-edit-row" onkeydown={handleDateKeyDown}>
				<GuidedDateInput
					year={dateYear}
					month={dateMonth}
					day={dateDay}
					onYearChange={(v) => { dateYear = v; }}
					onMonthChange={(v) => { dateMonth = v; }}
					onDayChange={(v) => { dateDay = v; }}
					autoFocusYear
				/>
				<button onclick={handleSave} class="inline-ok-btn tui-btn" style="color: var(--tui-water)">OK</button>
				<button onclick={() => { editingField = null; }} class="inline-esc-btn tui-text-muted">Esc</button>
			</div>
		{:else}
			<!-- svelte-ignore a11y_click_events_have_key_events -->
			<!-- svelte-ignore a11y_no_static_element_interactions -->
			<span
				onclick={() => handleEdit('birth_date', '')}
				class="editable-span"
				title="Click to edit"
			>
				{profile.birth_date}
			</span>
		{/if}

		{#if editingField === 'birth_time'}
			<!-- svelte-ignore a11y_no_static_element_interactions -->
			<div class="inline-edit-row" onkeydown={handleDateKeyDown}>
				<GuidedTimeInput
					hour={timeHour}
					minute={timeMinute}
					onHourChange={(v) => { timeHour = v; }}
					onMinuteChange={(v) => { timeMinute = v; }}
					showUnknownToggle
					isUnknown={timeUnknown}
					onUnknownChange={(v) => { timeUnknown = v; }}
					autoFocus
				/>
				<button onclick={handleSave} class="inline-ok-btn tui-btn" style="color: var(--tui-water)">OK</button>
				<button onclick={() => { editingField = null; }} class="inline-esc-btn tui-text-muted">Esc</button>
			</div>
		{:else}
			<!-- svelte-ignore a11y_click_events_have_key_events -->
			<!-- svelte-ignore a11y_no_static_element_interactions -->
			<span
				onclick={() => handleEdit('birth_time', '')}
				class="editable-span {profile.birth_time ? '' : 'tui-text-muted placeholder'}"
				title="Click to edit"
			>
				{profile.birth_time || 'Add time'}
			</span>
		{/if}

		<span class="tui-text-muted">|</span>
		<span
			class="gender-label"
			style="color: {profile.gender === 'female' ? 'var(--tui-accent-pink)' : 'var(--tui-water)'}"
		>
			{profile.gender === 'female' ? '\u2640 Female' : '\u2642 Male'}
		</span>
	</div>

	<!-- Place of birth (editable) -->
	<div class="info-field">
		<span class="info-label tui-text-muted">Place of birth:</span>
		{#if editingField === 'place_of_birth'}
			<input
				bind:this={inputEl}
				type="text"
				value={editValue}
				oninput={handleInputChange}
				onblur={handleSave}
				onkeydown={handleKeyDown}
				placeholder="Click to add"
				class="info-edit-input tui-text-dim"
				style="border-color: var(--tui-water)"
				maxlength={200}
			/>
		{:else}
			<!-- svelte-ignore a11y_click_events_have_key_events -->
			<!-- svelte-ignore a11y_no_static_element_interactions -->
			<span
				onclick={() => handleEdit('place_of_birth', profile.place_of_birth || '')}
				class="editable-span {profile.place_of_birth ? 'tui-text-dim' : 'tui-text-muted placeholder'}"
				title="Click to edit"
			>
				{profile.place_of_birth || 'Click to add'}
			</span>
		{/if}
	</div>

	<!-- Phone (editable) -->
	<div class="info-field info-field-phone">
		<span class="info-label tui-text-muted">Phone:</span>
		{#if editingField === 'phone'}
			<input
				bind:this={inputEl}
				type="tel"
				value={editValue}
				oninput={handleInputChange}
				onblur={handleSave}
				onkeydown={handleKeyDown}
				placeholder="Click to add"
				class="info-edit-input tui-text-dim"
				style="border-color: var(--tui-water)"
				maxlength={20}
			/>
		{:else}
			<!-- svelte-ignore a11y_click_events_have_key_events -->
			<!-- svelte-ignore a11y_no_static_element_interactions -->
			<span
				onclick={() => handleEdit('phone', profile.phone || '')}
				class="editable-span {profile.phone ? 'tui-text-dim' : 'tui-text-muted placeholder'}"
				title="Click to edit"
			>
				{profile.phone || 'Click to add'}
			</span>
		{/if}
	</div>

	<!-- Saving indicator -->
	{#if isSaving}
		<div class="saving-indicator tui-text-muted">Saving...</div>
	{/if}
</div>

<style>
	.profile-info-block {
		position: relative;
		padding: 1rem;
		margin-bottom: 1rem;
	}

	.name-row {
		display: flex;
		align-items: center;
		gap: 0.75rem;
		margin-bottom: 0.5rem;
	}

	.back-icon {
		width: 1.25rem;
		height: 1.25rem;
	}

	.name-edit-input {
		font-size: 1.5rem;
		font-weight: bold;
		background: transparent;
		border: none;
		border-bottom: 2px solid;
		outline: none;
		width: 100%;
	}

	.name-display {
		font-size: 1.5rem;
		font-weight: bold;
		cursor: pointer;
		padding: 0 0.25rem;
		margin: 0 -0.25rem;
	}

	.birth-info-row {
		display: flex;
		flex-wrap: wrap;
		align-items: center;
		gap: 0.75rem 0.75rem;
		font-size: 0.875rem;
		margin-bottom: 0.5rem;
	}

	.inline-edit-row {
		display: flex;
		align-items: center;
		gap: 0.5rem;
	}

	.inline-ok-btn {
		font-size: 0.75rem;
		padding: 0.125rem 0.5rem;
	}

	.inline-esc-btn {
		font-size: 0.75rem;
		padding: 0 0.25rem;
		background: none;
		border: none;
		cursor: pointer;
	}

	.editable-span {
		cursor: pointer;
		padding: 0 0.25rem;
		margin: 0 -0.25rem;
	}

	.placeholder {
		font-style: italic;
	}

	.info-field {
		display: flex;
		align-items: center;
		font-size: 0.875rem;
	}

	.info-field-phone {
		margin-top: 0.25rem;
	}

	.info-label {
		margin-right: 0.5rem;
	}

	.info-edit-input {
		background: transparent;
		border: none;
		border-bottom: 1px solid;
		outline: none;
		flex: 1;
	}

	.saving-indicator {
		position: absolute;
		top: 0.5rem;
		right: 0.5rem;
		font-size: 0.75rem;
	}
</style>
