import { getContext, setContext } from 'svelte';

const CHAT_FORM_KEY = 'chat-form';

interface FieldRegistration {
	id: string;
	el: HTMLElement | null;
	order: number;
}

export function createChatFormContext() {
	let focusedFieldId = $state<string | null>(null);
	let isSubmitting = $state(false);
	const fields = new Map<string, FieldRegistration>();

	function getSortedFields() {
		return Array.from(fields.values()).sort((a, b) => a.order - b.order);
	}

	const ctx = {
		get focusedFieldId() {
			return focusedFieldId;
		},
		set focusedFieldId(v: string | null) {
			focusedFieldId = v;
		},
		get isSubmitting() {
			return isSubmitting;
		},
		set isSubmitting(v: boolean) {
			isSubmitting = v;
		},
		registerField(id: string, el: HTMLElement | null, order: number) {
			fields.set(id, { id, el, order });
		},
		unregisterField(id: string) {
			fields.delete(id);
		},
		focusNext() {
			const sorted = getSortedFields();
			if (sorted.length === 0) return;
			const idx = sorted.findIndex((f) => f.id === focusedFieldId);
			const next = sorted[(idx + 1) % sorted.length];
			if (next?.el) {
				next.el.focus();
				focusedFieldId = next.id;
			}
		},
		focusPrev() {
			const sorted = getSortedFields();
			if (sorted.length === 0) return;
			const idx = sorted.findIndex((f) => f.id === focusedFieldId);
			const prev = sorted[idx > 0 ? idx - 1 : sorted.length - 1];
			if (prev?.el) {
				prev.el.focus();
				focusedFieldId = prev.id;
			}
		},
		focusField(id: string) {
			const field = fields.get(id);
			if (field?.el) {
				field.el.focus();
				focusedFieldId = id;
			}
		}
	};

	setContext(CHAT_FORM_KEY, ctx);
	return ctx;
}

export type ChatFormContext = ReturnType<typeof createChatFormContext>;

export function getChatFormContext(): ChatFormContext {
	return getContext(CHAT_FORM_KEY);
}
