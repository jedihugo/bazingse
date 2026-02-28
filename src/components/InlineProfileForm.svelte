<script lang="ts">
	import { ChatForm, ChatFormField, GuidedDateInput, GuidedTimeInput, GenderSelector } from './chat-form';
	import { createProfile, type ProfileCreate } from '$lib/api';

	interface Props {
		onSuccess?: (profile: { id: string; name: string }) => void;
		onCancel?: () => void;
		class?: string;
	}

	let {
		onSuccess,
		onCancel,
		class: className = ''
	}: Props = $props();

	// Form state
	let name = $state('');
	let year = $state<number | string>('');
	let month = $state<number | string>('');
	let day = $state<number | string>('');
	let hour = $state('');
	let minute = $state('');
	let unknownTime = $state(false);
	let gender = $state<'male' | 'female'>('male');
	let phone = $state('');

	// UI state
	let error = $state<string | null>(null);

	// Refs for focus management
	let nameEl = $state<HTMLInputElement>(undefined!);

	// Validation
	function isValidDate(): boolean {
		const y = typeof year === 'string' ? parseInt(year, 10) : year;
		const m = typeof month === 'string' ? parseInt(month, 10) : month;
		const d = typeof day === 'string' ? parseInt(day, 10) : day;

		if (isNaN(y) || isNaN(m) || isNaN(d)) return false;
		if (y < 1900 || y > 2100) return false;
		if (m < 1 || m > 12) return false;
		if (d < 1 || d > 31) return false;

		const date = new Date(y, m - 1, d);
		return date.getFullYear() === y && date.getMonth() === m - 1 && date.getDate() === d;
	}

	let isValid = $derived(name.trim().length > 0 && isValidDate());

	let showDateError = $derived(year !== '' && month !== '' && day !== '' && !isValidDate());

	// Format date for API
	function formatDate(): string {
		const y = typeof year === 'string' ? year.padStart(4, '0') : String(year).padStart(4, '0');
		const m = typeof month === 'string' ? month.padStart(2, '0') : String(month).padStart(2, '0');
		const d = typeof day === 'string' ? day.padStart(2, '0') : String(day).padStart(2, '0');
		return `${y}-${m}-${d}`;
	}

	// Format time for API
	function formatTime(): string | undefined {
		if (unknownTime) return undefined;
		if (!hour && !minute) return undefined;
		const h = hour.padStart(2, '0');
		const min = minute.padStart(2, '0');
		return `${h}:${min}`;
	}

	// Handle form submission
	async function handleSubmit() {
		if (!isValid) {
			error = 'Please fill in all required fields';
			return;
		}

		error = null;

		try {
			const data: ProfileCreate = {
				name: name.trim(),
				birth_date: formatDate(),
				birth_time: formatTime(),
				gender,
				phone: phone.trim() || undefined,
			};

			const profile = await createProfile(data);
			onSuccess?.({ id: profile.id, name: profile.name });
		} catch (err) {
			error = err instanceof Error ? err.message : 'Failed to create profile';
		}
	}

	// Field transitions
	function handleNameKeyDown(e: KeyboardEvent) {
		if (e.key === 'Enter' || e.key === 'Tab') {
			if (e.key === 'Enter') e.preventDefault();
		}
	}

	function handleDateComplete() {
		// GuidedTimeInput manages its own focus internally
		// Nothing to do here — the user can Tab to the next field
	}

	function handleTimeComplete() {
		// Form is complete — user can press Enter to submit
	}
</script>

<ChatForm
	title="New Profile"
	onSubmit={handleSubmit}
	{onCancel}
	submitLabel="Create"
	cancelLabel="Cancel"
	{isValid}
	{error}
	class={className}
>
	<!-- Name -->
	<ChatFormField id="name" label="Name" order={1} required>
		<input
			bind:this={nameEl}
			type="text"
			value={name}
			oninput={(e) => { name = (e.target as HTMLInputElement).value; }}
			onkeydown={handleNameKeyDown}
			placeholder="Enter full name"
			class="tui-input"
			autocomplete="off"
		/>
	</ChatFormField>

	<!-- Birth Date -->
	<ChatFormField
		id="birth-date"
		label="Birth Date"
		order={2}
		required
		error={showDateError ? 'Invalid date' : undefined}
	>
		<GuidedDateInput
			{year}
			{month}
			{day}
			onYearChange={(v) => { year = v; }}
			onMonthChange={(v) => { month = v; }}
			onDayChange={(v) => { day = v; }}
			onComplete={handleDateComplete}
		/>
	</ChatFormField>

	<!-- Birth Time -->
	<ChatFormField id="birth-time" label="Birth Time" order={3}>
		<GuidedTimeInput
			{hour}
			{minute}
			onHourChange={(v) => { hour = v; }}
			onMinuteChange={(v) => { minute = v; }}
			onComplete={handleTimeComplete}
			showUnknownToggle={true}
			isUnknown={unknownTime}
			onUnknownChange={(v) => { unknownTime = v; }}
			autoFocus={false}
		/>
	</ChatFormField>

	<!-- Gender -->
	<ChatFormField id="gender" label="Gender" order={4} required>
		<GenderSelector
			value={gender}
			onChange={(v) => { gender = v as 'male' | 'female'; }}
		/>
	</ChatFormField>

	<!-- WhatsApp / Phone -->
	<ChatFormField id="phone" label="WhatsApp" order={5} hint="e.g. 628123456789">
		<input
			type="tel"
			value={phone}
			oninput={(e) => { phone = (e.target as HTMLInputElement).value; }}
			placeholder="e.g. 628123456789"
			class="tui-input"
			autocomplete="tel"
		/>
	</ChatFormField>
</ChatForm>
