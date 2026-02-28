<script lang="ts">
	import { createChatFormContext } from './context.svelte';

	interface Props {
		title: string;
		onSubmit: () => void | Promise<void>;
		onCancel?: () => void;
		submitLabel?: string;
		cancelLabel?: string;
		isValid?: boolean;
		error?: string | null;
		class?: string;
		children: import('svelte').Snippet;
	}

	let {
		title,
		onSubmit,
		onCancel,
		submitLabel = 'Submit',
		cancelLabel = 'Cancel',
		isValid = true,
		error = null,
		class: className = '',
		children
	}: Props = $props();

	const ctx = createChatFormContext();

	async function handleSubmit(e: SubmitEvent) {
		e.preventDefault();
		if (!isValid || ctx.isSubmitting) return;

		ctx.isSubmitting = true;
		try {
			await onSubmit();
		} finally {
			ctx.isSubmitting = false;
		}
	}

	function handleKeyDown(e: KeyboardEvent) {
		// Enter to submit (only if not in a textarea)
		if (e.key === 'Enter' && !e.shiftKey) {
			const target = e.target as HTMLElement;
			if (target.tagName !== 'TEXTAREA') {
				e.preventDefault();
				if (isValid && !ctx.isSubmitting) {
					handleSubmit(new SubmitEvent('submit'));
				}
			}
		}

		// Escape to cancel
		if (e.key === 'Escape' && onCancel) {
			e.preventDefault();
			onCancel();
		}
	}
</script>

<!-- svelte-ignore a11y_no_noninteractive_element_interactions -->
<form
	onsubmit={handleSubmit}
	onkeydown={handleKeyDown}
	class="chat-form tui-frame {className}"
>
	<!-- Title Bar -->
	<div class="chat-form-title tui-frame-title">
		{title}
	</div>

	<!-- Form Body -->
	<div class="chat-form-body">
		{@render children()}

		<!-- Error Display -->
		{#if error}
			<div class="chat-form-error" role="alert">
				{error}
			</div>
		{/if}
	</div>

	<!-- Footer with Shortcuts -->
	<div class="chat-form-footer">
		<div class="chat-form-shortcuts">
			<span class="chat-form-shortcut">
				<kbd>Tab</kbd> Next
			</span>
			{#if onCancel}
				<span class="chat-form-shortcut">
					<kbd>Esc</kbd> {cancelLabel}
				</span>
			{/if}
			<span class="chat-form-shortcut">
				<kbd>Enter</kbd> {submitLabel}
			</span>
		</div>

		<!-- Action Buttons -->
		<div class="chat-form-actions">
			{#if onCancel}
				<button
					type="button"
					onclick={onCancel}
					class="tui-btn"
					disabled={ctx.isSubmitting}
				>
					{cancelLabel}
				</button>
			{/if}
			<button
				type="submit"
				class="tui-btn chat-form-submit"
				disabled={!isValid || ctx.isSubmitting}
			>
				{ctx.isSubmitting ? 'Saving...' : submitLabel}
			</button>
		</div>
	</div>
</form>
