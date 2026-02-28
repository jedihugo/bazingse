<script lang="ts">
	import { onMount } from 'svelte';

	interface TypeaheadOption {
		value: string;
		label: string;
		searchTerms?: string[];
	}

	interface Props {
		options: TypeaheadOption[];
		value: string | null;
		onChange: (value: string | null) => void;
		placeholder?: string;
		disabled?: boolean;
		hasError?: boolean;
		class?: string;
		allowClear?: boolean;
		onComplete?: () => void;
		autoFocus?: boolean;
	}

	let {
		options,
		value,
		onChange,
		placeholder = 'Type to search...',
		disabled = false,
		hasError = false,
		class: className = '',
		allowClear = true,
		onComplete,
		autoFocus = false
	}: Props = $props();

	let isOpen = $state(false);
	let searchTerm = $state('');
	let highlightedIndex = $state(0);

	let inputEl: HTMLInputElement;
	let listEl = $state<HTMLUListElement>(undefined!);
	let containerEl: HTMLDivElement;

	// Get selected option label for display
	let selectedOption = $derived(options.find((opt) => opt.value === value));
	let displayValue = $derived(isOpen ? searchTerm : (selectedOption?.label || ''));

	// Filter options based on search term
	let filteredOptions = $derived.by(() => {
		if (!searchTerm) return options;
		const search = searchTerm.toLowerCase();
		return options.filter((opt) => {
			const matchesLabel = opt.label.toLowerCase().includes(search);
			const matchesValue = String(opt.value).toLowerCase().includes(search);
			const matchesTerms = opt.searchTerms?.some((term) =>
				term.toLowerCase().includes(search)
			);
			return matchesLabel || matchesValue || matchesTerms;
		});
	});

	// Reset highlighted index when filtered options change
	$effect(() => {
		filteredOptions.length; // track dependency
		highlightedIndex = 0;
	});

	// Scroll highlighted option into view
	$effect(() => {
		if (isOpen && listEl) {
			const highlightedEl = listEl.children[highlightedIndex] as HTMLElement;
			if (highlightedEl) {
				highlightedEl.scrollIntoView({ block: 'nearest' });
			}
		}
	});

	onMount(() => {
		if (autoFocus && inputEl) {
			inputEl.focus();
		}

		// Close dropdown when clicking outside
		function handleClickOutside(e: MouseEvent) {
			if (containerEl && !containerEl.contains(e.target as Node)) {
				isOpen = false;
				searchTerm = '';
			}
		}

		document.addEventListener('mousedown', handleClickOutside);
		return () => document.removeEventListener('mousedown', handleClickOutside);
	});

	function handleInputChange(e: Event) {
		searchTerm = (e.target as HTMLInputElement).value;
		isOpen = true;
		highlightedIndex = 0;
	}

	function handleInputFocus() {
		isOpen = true;
		searchTerm = '';
	}

	function selectOption(opt: TypeaheadOption) {
		onChange(opt.value);
		isOpen = false;
		searchTerm = '';
		onComplete?.();
	}

	function clearSelection() {
		onChange(null);
		searchTerm = '';
		inputEl?.focus();
	}

	function handleKeyDown(e: KeyboardEvent) {
		if (disabled) return;

		switch (e.key) {
			case 'ArrowDown':
				e.preventDefault();
				if (!isOpen) {
					isOpen = true;
				} else {
					highlightedIndex =
						highlightedIndex < filteredOptions.length - 1 ? highlightedIndex + 1 : 0;
				}
				break;

			case 'ArrowUp':
				e.preventDefault();
				if (isOpen) {
					highlightedIndex =
						highlightedIndex > 0 ? highlightedIndex - 1 : filteredOptions.length - 1;
				}
				break;

			case 'Enter':
				e.preventDefault();
				if (isOpen && filteredOptions[highlightedIndex]) {
					selectOption(filteredOptions[highlightedIndex]);
				} else if (!isOpen) {
					isOpen = true;
				}
				break;

			case 'Escape':
				e.preventDefault();
				if (isOpen) {
					isOpen = false;
					searchTerm = '';
				}
				break;

			case 'Backspace':
				if (searchTerm === '' && value && allowClear) {
					clearSelection();
				}
				break;

			case 'Tab':
				// Allow natural tab behavior but close dropdown
				if (isOpen) {
					isOpen = false;
					searchTerm = '';
				}
				break;
		}
	}

	let errorStyle = $derived(hasError ? 'border-color: var(--tui-error)' : '');
</script>

<div
	bind:this={containerEl}
	class="typeahead-container {isOpen ? 'typeahead-open' : ''} {className}"
>
	<div class="typeahead-input-wrapper">
		<input
			bind:this={inputEl}
			type="text"
			value={displayValue}
			oninput={handleInputChange}
			onfocus={handleInputFocus}
			onkeydown={handleKeyDown}
			placeholder={value ? '' : placeholder}
			{disabled}
			class="typeahead-input tui-input"
			style={errorStyle}
			role="combobox"
			aria-expanded={isOpen}
			aria-haspopup="listbox"
			aria-controls="typeahead-listbox"
			autocomplete="off"
		/>

		<!-- Clear button -->
		{#if allowClear && value && !disabled}
			<button
				type="button"
				onclick={clearSelection}
				class="typeahead-clear tui-btn"
				aria-label="Clear selection"
			>
				&times;
			</button>
		{/if}

		<!-- Dropdown indicator -->
		<span class="typeahead-arrow" aria-hidden="true">
			{isOpen ? '\u25B2' : '\u25BC'}
		</span>
	</div>

	<!-- Dropdown list -->
	{#if isOpen}
		<ul
			bind:this={listEl}
			id="typeahead-listbox"
			class="typeahead-dropdown"
			role="listbox"
		>
			{#if filteredOptions.length === 0}
				<li class="typeahead-no-results tui-text-muted">
					No matches found
				</li>
			{:else}
				{#each filteredOptions as opt, index (opt.value)}
					<!-- svelte-ignore a11y_click_events_have_key_events -->
					<li
						onclick={() => selectOption(opt)}
						onmouseenter={() => (highlightedIndex = index)}
						class="typeahead-option {index === highlightedIndex
							? 'typeahead-option-highlighted'
							: ''} {opt.value === value ? 'typeahead-option-selected' : ''}"
						role="option"
						aria-selected={opt.value === value}
					>
						{#if opt.value === value}
							<span class="typeahead-check">{'\u25CF'}</span>
						{/if}
						{opt.label}
					</li>
				{/each}
			{/if}
		</ul>
	{/if}
</div>
