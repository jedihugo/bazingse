<script lang="ts">
	import InlineSelector from './InlineSelector.svelte';

	interface Props {
		value: 'male' | 'female';
		onChange: (value: string) => void;
		disabled?: boolean;
		class?: string;
		autoFocus?: boolean;
		onComplete?: () => void;
	}

	let {
		value,
		onChange,
		disabled,
		class: className,
		autoFocus,
		onComplete
	}: Props = $props();

	const genderOptions = [
		{ value: 'male', label: 'M', shortcut: 'm' },
		{ value: 'female', label: 'F', shortcut: 'f' }
	];
</script>

<InlineSelector
	options={genderOptions}
	{value}
	{onChange}
	{disabled}
	class={className}
	name="gender"
	{autoFocus}
	{onComplete}
/>
