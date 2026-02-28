<script lang="ts">
	import { onMount } from 'svelte';

	interface SelectorOption {
		value: string;
		label: string;
		shortcut?: string;
	}

	interface Props {
		options: SelectorOption[];
		value: string;
		onChange: (value: string) => void;
		disabled?: boolean;
		class?: string;
		name?: string;
		autoFocus?: boolean;
		onComplete?: () => void;
	}

	let {
		options,
		value,
		onChange,
		disabled = false,
		class: className = '',
		name = 'inline-selector',
		autoFocus = false,
		onComplete
	}: Props = $props();

	let containerEl: HTMLDivElement;

	let currentIndex = $derived(options.findIndex((opt) => opt.value === value));

	onMount(() => {
		if (autoFocus && containerEl) {
			containerEl.focus();
		}
	});

	function handleKeyDown(e: KeyboardEvent) {
		if (disabled) return;

		// Arrow navigation
		if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
			e.preventDefault();
			const prevIndex = currentIndex > 0 ? currentIndex - 1 : options.length - 1;
			onChange(options[prevIndex].value);
		} else if (e.key === 'ArrowRight' || e.key === 'ArrowDown') {
			e.preventDefault();
			const nextIndex = currentIndex < options.length - 1 ? currentIndex + 1 : 0;
			onChange(options[nextIndex].value);
		}

		// Space/Enter to confirm current selection and move to next field
		else if (e.key === ' ' || e.key === 'Enter') {
			e.preventDefault();
			onComplete?.();
		}

		// Shortcut keys (case-insensitive)
		else {
			const key = e.key.toLowerCase();
			const matchingOption = options.find((opt) => opt.shortcut?.toLowerCase() === key);
			if (matchingOption) {
				e.preventDefault();
				onChange(matchingOption.value);
				// Auto-advance after shortcut selection
				setTimeout(() => onComplete?.(), 50);
			}
		}
	}

	function handleOptionClick(optValue: string) {
		if (disabled) return;
		onChange(optValue);
		// Focus container after click for continued keyboard navigation
		containerEl?.focus();
	}
</script>

<div
	bind:this={containerEl}
	class="inline-selector {className}"
	role="radiogroup"
	aria-label={name}
	tabindex={disabled ? -1 : 0}
	onkeydown={handleKeyDown}
>
	{#each options as option (option.value)}
		{@const isSelected = option.value === value}
		<!-- svelte-ignore a11y_click_events_have_key_events -->
		<!-- svelte-ignore a11y_no_noninteractive_element_interactions -->
		<label
			class="inline-selector-option {isSelected ? 'inline-selector-option-selected' : ''}"
			onclick={() => handleOptionClick(option.value)}
		>
			<input
				type="radio"
				{name}
				value={option.value}
				checked={isSelected}
				oninput={() => onChange(option.value)}
				{disabled}
				class="sr-only"
				aria-checked={isSelected}
			/>
			<span class={isSelected ? 'tui-text' : 'tui-text-muted'}>
				({isSelected ? '\u25CF' : '\u25CB'})
				{option.label}
				{#if option.shortcut}
					<span class="inline-selector-shortcut">
						[{option.shortcut.toUpperCase()}]
					</span>
				{/if}
			</span>
		</label>
	{/each}
</div>
