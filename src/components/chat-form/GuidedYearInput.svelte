<script lang="ts">
	import { onMount } from 'svelte';

	interface Props {
		year: number | string;
		onYearChange: (value: number | string) => void;
		onComplete?: () => void;
		disabled?: boolean;
		hasError?: boolean;
		placeholder?: string;
		class?: string;
		autoFocus?: boolean;
	}

	let {
		year,
		onYearChange,
		onComplete,
		disabled = false,
		hasError = false,
		placeholder = 'YYYY',
		class: className = '',
		autoFocus = false
	}: Props = $props();

	let yearEl: HTMLInputElement;

	onMount(() => {
		if (autoFocus && yearEl) {
			yearEl.focus();
		}
	});

	function handleInput(e: Event) {
		const value = (e.target as HTMLInputElement).value;
		if (!/^\d*$/.test(value) || value.length > 4) return;

		onYearChange(value);

		if (value.length === 4) {
			const num = parseInt(value, 10);
			if (num >= 1900 && num <= 2100) {
				onComplete?.();
			}
		}
	}

	let errorStyle = $derived(hasError ? 'border-color: var(--tui-error)' : '');
</script>

<input
	bind:this={yearEl}
	type="text"
	inputmode="numeric"
	pattern="[0-9]*"
	value={year}
	oninput={handleInput}
	{placeholder}
	{disabled}
	class="guided-input-segment guided-input-year tui-input {className}"
	style={errorStyle}
	aria-label="Year"
	autocomplete="off"
/>
