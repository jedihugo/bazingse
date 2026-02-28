<script lang="ts">
	import { onMount } from 'svelte';

	interface Props {
		hour: string;
		minute: string;
		onHourChange: (value: string) => void;
		onMinuteChange: (value: string) => void;
		onComplete?: () => void;
		disabled?: boolean;
		hasError?: boolean;
		showUnknownToggle?: boolean;
		isUnknown?: boolean;
		onUnknownChange?: (unknown: boolean) => void;
		class?: string;
		autoFocus?: boolean;
	}

	let {
		hour,
		minute,
		onHourChange,
		onMinuteChange,
		onComplete,
		disabled = false,
		hasError = false,
		showUnknownToggle = false,
		isUnknown = false,
		onUnknownChange,
		class: className = '',
		autoFocus = false
	}: Props = $props();

	let hourEl = $state<HTMLInputElement>(undefined!);
	let minuteEl = $state<HTMLInputElement>(undefined!);

	onMount(() => {
		if (autoFocus && hourEl && !isUnknown) {
			hourEl.focus();
		}
	});

	function handleHourInput(e: Event) {
		const value = (e.target as HTMLInputElement).value;
		// Only allow digits, max 2 characters
		if (!/^\d*$/.test(value) || value.length > 2) return;

		const num = parseInt(value, 10);
		if (num > 23) return;

		onHourChange(value);

		// Auto-advance: 2 digits OR single digit > 2 (3-9)
		if (value.length === 2 || (value.length === 1 && num > 2)) {
			setTimeout(() => minuteEl?.focus(), 0);
		}
	}

	function handleMinuteInput(e: Event) {
		const value = (e.target as HTMLInputElement).value;
		// Only allow digits, max 2 characters
		if (!/^\d*$/.test(value) || value.length > 2) return;

		const num = parseInt(value, 10);
		if (num > 59) return;

		onMinuteChange(value);

		// Auto-complete: 2 digits -> trigger onComplete
		if (value.length === 2) {
			onComplete?.();
		}
	}

	function handleHourKeyDown(_e: KeyboardEvent) {
		// No previous field from hour
	}

	function handleMinuteKeyDown(e: KeyboardEvent) {
		if (e.key === 'Backspace' && minuteEl?.value === '') {
			e.preventDefault();
			hourEl?.focus();
		}
	}

	function handleUnknownToggle() {
		const newUnknown = !isUnknown;
		onUnknownChange?.(newUnknown);

		if (newUnknown) {
			// Clear time values when marking as unknown
			onHourChange('');
			onMinuteChange('');
		} else {
			// Set default time when unmarking as unknown
			onHourChange('12');
			onMinuteChange('00');
			setTimeout(() => hourEl?.focus(), 0);
		}
	}

	let errorStyle = $derived(hasError ? 'border-color: var(--tui-error)' : '');
</script>

{#if isUnknown}
	<div class="guided-time-input {className}" role="group" aria-label="Time input">
		<span class="guided-time-unknown tui-input tui-text-muted">??:??</span>
		{#if showUnknownToggle}
			<button
				type="button"
				onclick={handleUnknownToggle}
				class="guided-time-toggle tui-btn tui-border-bright"
				title="I know the birth time"
				aria-pressed={isUnknown}
			>
				?
			</button>
		{/if}
	</div>
{:else}
	<div class="guided-time-input {className}" role="group" aria-label="Time input">
		<!-- Hour -->
		<input
			bind:this={hourEl}
			type="text"
			inputmode="numeric"
			pattern="[0-9]*"
			value={hour}
			oninput={handleHourInput}
			onkeydown={handleHourKeyDown}
			placeholder="HH"
			{disabled}
			class="guided-input-segment guided-input-hour tui-input"
			style={errorStyle}
			aria-label="Hour"
			autocomplete="off"
		/>
		<span class="guided-input-separator">:</span>

		<!-- Minute -->
		<input
			bind:this={minuteEl}
			type="text"
			inputmode="numeric"
			pattern="[0-9]*"
			value={minute}
			oninput={handleMinuteInput}
			onkeydown={handleMinuteKeyDown}
			placeholder="MM"
			{disabled}
			class="guided-input-segment guided-input-minute tui-input"
			style={errorStyle}
			aria-label="Minute"
			autocomplete="off"
		/>

		<!-- Unknown toggle button -->
		{#if showUnknownToggle}
			<button
				type="button"
				onclick={handleUnknownToggle}
				class="guided-time-toggle tui-btn"
				title="I don't know the birth time"
				aria-pressed={isUnknown}
			>
				?
			</button>
		{/if}
	</div>
{/if}
