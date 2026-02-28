<script lang="ts">
	import { onMount } from 'svelte';
	import type { LifeEventCreate, LifeEvent } from '$lib/api.types';
	import { createLifeEvent } from '$lib/api';

	interface Props {
		profileId: string;
		onSuccess?: (event: LifeEvent) => void;
		onCancel?: () => void;
		existingDates?: { year: number; month?: number | null; day?: number | null }[];
		class?: string;
	}

	let {
		profileId,
		onSuccess,
		onCancel,
		existingDates = [],
		class: className = ''
	}: Props = $props();

	const currentYear = new Date().getFullYear();

	// Form state
	let year: number | string = $state(currentYear.toString());
	let month: number | string = $state('');
	let day: number | string = $state('');
	let location = $state('');
	let isAbroad = $state(false);
	let notes = $state('');

	// UI state
	let error: string | null = $state(null);
	let isSubmitting = $state(false);

	// Element refs
	let yearEl: HTMLInputElement | undefined = $state(undefined);
	let monthEl: HTMLInputElement | undefined = $state(undefined);
	let dayEl: HTMLInputElement | undefined = $state(undefined);
	let locationEl: HTMLInputElement | undefined = $state(undefined);

	// Auto-focus year on mount
	onMount(() => {
		yearEl?.focus();
	});

	// Derived validation
	let yearNum = $derived(typeof year === 'string' ? parseInt(year, 10) : year);
	let monthNum = $derived(typeof month === 'string' && month !== '' ? parseInt(month, 10) : null);
	let dayNum = $derived(typeof day === 'string' && day !== '' ? parseInt(day, 10) : null);

	let isValidYear = $derived(!isNaN(yearNum) && yearNum >= 1900 && yearNum <= 2100);
	let isValid = $derived(isValidYear);

	// Check for duplicate
	let isDuplicate = $derived(
		existingDates.some(
			(d) =>
				d.year === yearNum &&
				(d.month || null) === monthNum &&
				(d.day || null) === dayNum
		)
	);

	// Handle form submission
	async function handleSubmit() {
		error = null;

		if (!isValidYear) {
			error = 'Please enter a valid year (1900-2100)';
			return;
		}

		if (isDuplicate) {
			error = 'An event with this date already exists';
			return;
		}

		if (dayNum && !monthNum) {
			error = 'Please specify the month if you know the day';
			return;
		}

		isSubmitting = true;

		try {
			const eventData: LifeEventCreate = {
				year: yearNum,
				month: monthNum,
				day: dayNum,
				location: location.trim() || null,
				notes: notes.trim() || null,
				is_abroad: location.trim() ? isAbroad : false
			};

			const newEvent = await createLifeEvent(profileId, eventData);
			onSuccess?.(newEvent);
		} catch (err) {
			error = err instanceof Error ? err.message : 'Failed to create event';
		} finally {
			isSubmitting = false;
		}
	}

	// Handle year input
	function handleYearInput(e: Event) {
		const value = (e.target as HTMLInputElement).value;
		if (!/^\d*$/.test(value) || value.length > 4) return;
		year = value;

		if (value.length === 4) {
			const num = parseInt(value, 10);
			if (num >= 1900 && num <= 2100) {
				setTimeout(() => monthEl?.focus(), 0);
			}
		}
	}

	// Handle month input
	function handleMonthInput(e: Event) {
		const value = (e.target as HTMLInputElement).value;
		if (!/^\d*$/.test(value) || value.length > 2) return;

		const num = parseInt(value, 10);
		if (num > 12) return;

		month = value;

		// Auto-advance: 2 digits OR single digit > 1
		if (value.length === 2 || (value.length === 1 && num > 1)) {
			setTimeout(() => dayEl?.focus(), 0);
		}
	}

	// Handle day input
	function handleDayInput(e: Event) {
		const value = (e.target as HTMLInputElement).value;
		if (!/^\d*$/.test(value) || value.length > 2) return;

		const num = parseInt(value, 10);
		if (num > 31) return;

		day = value;

		// Auto-advance: 2 digits
		if (value.length === 2) {
			setTimeout(() => locationEl?.focus(), 0);
		}
	}

	// Handle backspace for navigation between fields
	function handleMonthKeyDown(e: KeyboardEvent) {
		if (e.key === 'Backspace' && monthEl?.value === '') {
			e.preventDefault();
			yearEl?.focus();
		}
	}

	function handleDayKeyDown(e: KeyboardEvent) {
		if (e.key === 'Backspace' && dayEl?.value === '') {
			e.preventDefault();
			monthEl?.focus();
		}
	}

	// Handle location input
	function handleLocationInput(e: Event) {
		location = (e.target as HTMLInputElement).value;
	}

	// Handle notes input
	function handleNotesInput(e: Event) {
		notes = (e.target as HTMLTextAreaElement).value;
	}

	// Keyboard handling for the form wrapper
	function handleKeyDown(e: KeyboardEvent) {
		// Enter to submit (only if not in a textarea)
		if (e.key === 'Enter' && !e.shiftKey) {
			const target = e.target as HTMLElement;
			if (target.tagName !== 'TEXTAREA') {
				e.preventDefault();
				if (isValid && !isDuplicate && !isSubmitting) {
					handleSubmit();
				}
			}
		}

		// Escape to cancel
		if (e.key === 'Escape' && onCancel) {
			e.preventDefault();
			onCancel();
		}
	}

	let yearErrorStyle = $derived(
		!isValidYear && year !== '' ? 'border-color: var(--tui-error)' : ''
	);
</script>

<!-- svelte-ignore a11y_no_static_element_interactions -->
<div class="tui-frame {className}" onkeydown={handleKeyDown}>
	<div class="tui-frame-title">Add Life Event</div>
	<table class="tui-table-form">
		<tbody>
			<tr>
				<td>Date*</td>
				<td>
					<div class="guided-date-input">
						<input
							bind:this={yearEl}
							type="text"
							inputmode="numeric"
							pattern="[0-9]*"
							value={year}
							oninput={handleYearInput}
							placeholder="YYYY"
							disabled={isSubmitting}
							class="guided-input-segment guided-input-year tui-input"
							style={yearErrorStyle}
							aria-label="Year"
							autocomplete="off"
						/>
						<span class="guided-input-separator">/</span>
						<input
							bind:this={monthEl}
							type="text"
							inputmode="numeric"
							pattern="[0-9]*"
							value={month}
							oninput={handleMonthInput}
							onkeydown={handleMonthKeyDown}
							placeholder="MM"
							disabled={isSubmitting}
							class="guided-input-segment guided-input-month tui-input"
							aria-label="Month (optional)"
							autocomplete="off"
						/>
						<span class="guided-input-separator">/</span>
						<input
							bind:this={dayEl}
							type="text"
							inputmode="numeric"
							pattern="[0-9]*"
							value={day}
							oninput={handleDayInput}
							onkeydown={handleDayKeyDown}
							placeholder="DD"
							disabled={isSubmitting || !monthNum}
							class="guided-input-segment guided-input-day tui-input"
							style={!monthNum ? 'opacity: 0.5' : ''}
							aria-label="Day (optional)"
							autocomplete="off"
						/>
					</div>
					<div class="date-hint">
						Year required; month and day optional
					</div>
				</td>
			</tr>
			<tr>
				<td>Location</td>
				<td>
					<input
						bind:this={locationEl}
						type="text"
						value={location}
						oninput={handleLocationInput}
						placeholder="Where did it happen?"
						maxlength={200}
						disabled={isSubmitting}
						autocomplete="off"
					/>
					{#if location.trim()}
						<div class="abroad-toggle-row">
							<button
								type="button"
								onclick={() => { isAbroad = !isAbroad; }}
								disabled={isSubmitting}
								class="abroad-toggle"
								style="
									color: {isAbroad ? 'var(--tui-water)' : 'var(--tui-fg-muted)'};
									background: {isAbroad ? 'color-mix(in srgb, var(--tui-water) 15%, var(--tui-bg))' : 'transparent'};
									border-color: {isAbroad ? 'var(--tui-water)' : 'var(--tui-border)'}
								"
								title="Was this event abroad (outside birth country)?"
							>
								<span class="abroad-checkbox">{isAbroad ? '[x]' : '[_]'}</span>
								<span>Abroad</span>
							</button>
						</div>
					{/if}
				</td>
			</tr>
			<tr>
				<td>Notes</td>
				<td>
					<textarea
						value={notes}
						oninput={handleNotesInput}
						placeholder="What happened?"
						class="notes-textarea"
						rows={2}
						maxlength={10000}
						disabled={isSubmitting}
					></textarea>
				</td>
			</tr>
		</tbody>
	</table>

	{#if isDuplicate}
		<div class="tui-form-error" role="alert">An event with this date already exists</div>
	{/if}

	{#if error}
		<div class="tui-form-error" role="alert">{error}</div>
	{/if}

	<div class="tui-form-actions">
		{#if onCancel}
			<button type="button" onclick={onCancel} class="tui-btn" disabled={isSubmitting}>
				Cancel
			</button>
		{/if}
		<button
			type="button"
			onclick={handleSubmit}
			class="tui-btn"
			disabled={!isValid || isDuplicate || isSubmitting}
		>
			{isSubmitting ? '...' : 'Add'}
		</button>
	</div>
</div>

<style>
	.date-hint {
		font-size: 0.625rem;
		color: var(--tui-fg-muted);
		margin-top: 0.125rem;
	}

	.abroad-toggle-row {
		margin-top: 0.25rem;
	}

	.abroad-toggle {
		display: inline-flex;
		align-items: center;
		gap: 0.25rem;
		padding: 0.125rem 0.375rem;
		font-size: 0.75rem;
		border: 1px solid;
		cursor: pointer;
		transition: color 0.15s, background 0.15s, border-color 0.15s;
	}

	.abroad-checkbox {
		font-family: monospace;
	}

	.notes-textarea {
		resize: none;
		width: 100%;
	}
</style>
