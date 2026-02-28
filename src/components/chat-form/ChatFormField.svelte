<script lang="ts">
	import { onMount } from 'svelte';
	import { getChatFormContext } from './context.svelte';

	interface Props {
		id: string;
		label: string;
		order: number;
		required?: boolean;
		hint?: string;
		error?: string;
		class?: string;
		children: import('svelte').Snippet;
	}

	let {
		id,
		label,
		order,
		required = false,
		hint,
		error,
		class: className = '',
		children
	}: Props = $props();

	const ctx = getChatFormContext();
	let fieldEl: HTMLDivElement;

	let isFocused = $derived(ctx.focusedFieldId === id);

	onMount(() => {
		ctx.registerField(id, fieldEl, order);
		return () => ctx.unregisterField(id);
	});

	function handleFocus() {
		ctx.focusedFieldId = id;
	}

	function handleBlur() {
		// Small delay to allow focus to move to another field
		setTimeout(() => {
			if (ctx.focusedFieldId === id) {
				ctx.focusedFieldId = null;
			}
		}, 100);
	}
</script>

<div
	bind:this={fieldEl}
	class="chat-field {isFocused ? 'chat-field-focused' : ''} {error ? 'chat-field-error' : ''} {className}"
	role="group"
	aria-labelledby="{id}-label"
	onfocusin={handleFocus}
	onfocusout={handleBlur}
	tabindex="-1"
>
	<!-- Label with cursor indicator -->
	<div class="chat-field-label-row">
		<span id="{id}-label" class="chat-field-label">
			{label}:
			{#if required}
				<span class="chat-field-required">*</span>
			{/if}
		</span>
		<span class="chat-field-cursor {isFocused ? 'chat-field-cursor-active' : ''}">
			{isFocused ? '>' : ' '}
		</span>
	</div>

	<!-- Input area -->
	<div class="chat-field-input">
		{@render children()}
	</div>

	<!-- Hint or Error -->
	{#if hint || error}
		<div class="chat-field-hint {error ? 'chat-field-hint-error' : ''}">
			{error || hint}
		</div>
	{/if}
</div>
