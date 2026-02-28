<script lang="ts">
	import { onMount } from 'svelte';

	interface Props {
		year: number | string;
		month: number | string;
		day: number | string;
		onYearChange: (value: number | string) => void;
		onMonthChange: (value: number | string) => void;
		onDayChange: (value: number | string) => void;
		onComplete?: () => void;
		disabled?: boolean;
		hasError?: boolean;
		yearPlaceholder?: string;
		monthPlaceholder?: string;
		dayPlaceholder?: string;
		class?: string;
		autoFocusYear?: boolean;
	}

	let {
		year,
		month,
		day,
		onYearChange,
		onMonthChange,
		onDayChange,
		onComplete,
		disabled = false,
		hasError = false,
		yearPlaceholder = 'YYYY',
		monthPlaceholder = 'MM',
		dayPlaceholder = 'DD',
		class: className = '',
		autoFocusYear = false
	}: Props = $props();

	let yearEl: HTMLInputElement;
	let monthEl: HTMLInputElement;
	let dayEl: HTMLInputElement;

	onMount(() => {
		if (autoFocusYear && yearEl) {
			yearEl.focus();
		}
	});

	function isValidYear(value: string): boolean {
		const num = parseInt(value, 10);
		return !isNaN(num) && num >= 1900 && num <= 2100;
	}

	function handleYearInput(e: Event) {
		const value = (e.target as HTMLInputElement).value;
		// Only allow digits, max 4 characters
		if (!/^\d*$/.test(value) || value.length > 4) return;

		onYearChange(value);

		// Auto-advance: 4 digits AND valid year -> move to month
		if (value.length === 4 && isValidYear(value)) {
			setTimeout(() => monthEl?.focus(), 0);
		}
	}

	function handleMonthInput(e: Event) {
		const value = (e.target as HTMLInputElement).value;
		// Only allow digits, max 2 characters
		if (!/^\d*$/.test(value) || value.length > 2) return;

		const num = parseInt(value, 10);
		// Clamp to valid month range
		if (num > 12) return;

		onMonthChange(value);

		// Auto-advance: 2 digits OR single digit > 1 (can only be 2-9) -> move to day
		if (value.length === 2 || (value.length === 1 && num > 1)) {
			setTimeout(() => dayEl?.focus(), 0);
		}
	}

	function handleDayInput(e: Event) {
		const value = (e.target as HTMLInputElement).value;
		// Only allow digits, max 2 characters
		if (!/^\d*$/.test(value) || value.length > 2) return;

		const num = parseInt(value, 10);
		// Clamp to valid day range
		if (num > 31) return;

		onDayChange(value);

		// Auto-complete: 2 digits -> trigger onComplete
		if (value.length === 2) {
			onComplete?.();
		}
	}

	function handleYearKeyDown(e: KeyboardEvent) {
		// No previous field from year
	}

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

	let errorStyle = $derived(hasError ? 'border-color: var(--tui-error)' : '');
</script>

<div class="guided-date-input {className}" role="group" aria-label="Date input">
	<!-- Year -->
	<input
		bind:this={yearEl}
		type="text"
		inputmode="numeric"
		pattern="[0-9]*"
		value={year}
		oninput={handleYearInput}
		onkeydown={handleYearKeyDown}
		placeholder={yearPlaceholder}
		{disabled}
		class="guided-input-segment guided-input-year tui-input"
		style={errorStyle}
		aria-label="Year"
		autocomplete="off"
	/>
	<span class="guided-input-separator">/</span>

	<!-- Month -->
	<input
		bind:this={monthEl}
		type="text"
		inputmode="numeric"
		pattern="[0-9]*"
		value={month}
		oninput={handleMonthInput}
		onkeydown={handleMonthKeyDown}
		placeholder={monthPlaceholder}
		{disabled}
		class="guided-input-segment guided-input-month tui-input"
		style={errorStyle}
		aria-label="Month"
		autocomplete="off"
	/>
	<span class="guided-input-separator">/</span>

	<!-- Day -->
	<input
		bind:this={dayEl}
		type="text"
		inputmode="numeric"
		pattern="[0-9]*"
		value={day}
		oninput={handleDayInput}
		onkeydown={handleDayKeyDown}
		placeholder={dayPlaceholder}
		{disabled}
		class="guided-input-segment guided-input-day tui-input"
		style={errorStyle}
		aria-label="Day"
		autocomplete="off"
	/>
</div>
