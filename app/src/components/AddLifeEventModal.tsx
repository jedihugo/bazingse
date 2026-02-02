'use client';

import { useState } from 'react';
import { type LifeEventCreate, type LifeEvent, createLifeEvent } from '@/lib/api';

interface AddLifeEventModalProps {
  profileId: string;
  onAdd: (event: LifeEvent) => void;
  onClose: () => void;
  existingDates: { year: number; month?: number | null; day?: number | null }[];
}

export default function AddLifeEventModal({
  profileId,
  onAdd,
  onClose,
  existingDates,
}: AddLifeEventModalProps) {
  const currentYear = new Date().getFullYear();
  const [year, setYear] = useState<number>(currentYear);
  const [month, setMonth] = useState<number | ''>('');
  const [day, setDay] = useState<number | ''>('');
  const [location, setLocation] = useState('');
  const [notes, setNotes] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    // Check for duplicate
    const isDuplicate = existingDates.some(d =>
      d.year === year &&
      (d.month || undefined) === (month || undefined) &&
      (d.day || undefined) === (day || undefined)
    );

    if (isDuplicate) {
      setError('This date already exists in your life events');
      return;
    }

    // Validate day requires month
    if (day && !month) {
      setError('Please select a month when specifying a day');
      return;
    }

    try {
      setIsSubmitting(true);

      const eventData: LifeEventCreate = {
        year,
        month: month || null,
        day: day || null,
        location: location.trim() || null,
        notes: notes.trim() || null,
      };

      const newEvent = await createLifeEvent(profileId, eventData);
      onAdd(newEvent);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create life event');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="tui-frame tui-bg-panel p-6 w-full max-w-sm mx-4 max-h-[90vh] overflow-y-auto">
        <h2 className="text-xl font-bold mb-4 tui-text">Add Life Event</h2>
        <form onSubmit={handleSubmit}>
          {/* Year */}
          <div className="mb-4">
            <label className="block text-sm font-medium tui-text-dim mb-1">
              Year <span style={{ color: 'var(--tui-error)' }}>*</span>
            </label>
            <input
              type="number"
              value={year}
              onChange={(e) => setYear(parseInt(e.target.value) || currentYear)}
              min="1900"
              max="2100"
              className="tui-input w-full"
              required
              disabled={isSubmitting}
            />
          </div>

          {/* Month */}
          <div className="mb-4">
            <label className="block text-sm font-medium tui-text-dim mb-1">
              Month <span className="tui-text-muted">(optional)</span>
            </label>
            <select
              value={month}
              onChange={(e) => {
                setMonth(e.target.value ? parseInt(e.target.value) : '');
                if (!e.target.value) setDay(''); // Clear day if month cleared
              }}
              className="tui-input w-full"
              disabled={isSubmitting}
            >
              <option value="">-- Select Month --</option>
              {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12].map(m => (
                <option key={m} value={m}>
                  {new Date(2000, m - 1, 1).toLocaleString('default', { month: 'long' })}
                </option>
              ))}
            </select>
          </div>

          {/* Day */}
          <div className="mb-4">
            <label className="block text-sm font-medium tui-text-dim mb-1">
              Day <span className="tui-text-muted">(optional, requires month)</span>
            </label>
            <input
              type="number"
              value={day}
              onChange={(e) => setDay(e.target.value ? parseInt(e.target.value) : '')}
              min="1"
              max="31"
              disabled={!month || isSubmitting}
              className="tui-input w-full disabled:opacity-50"
            />
          </div>

          {/* Location */}
          <div className="mb-4">
            <label className="block text-sm font-medium tui-text-dim mb-1">
              Location <span className="tui-text-muted">(optional)</span>
            </label>
            <input
              type="text"
              value={location}
              onChange={(e) => setLocation(e.target.value)}
              placeholder="Where did this happen?"
              className="tui-input w-full"
              maxLength={200}
              disabled={isSubmitting}
            />
          </div>

          {/* Notes */}
          <div className="mb-4">
            <label className="block text-sm font-medium tui-text-dim mb-1">
              Notes <span className="tui-text-muted">(optional)</span>
            </label>
            <textarea
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
              placeholder="What happened during this period?"
              className="tui-input w-full resize-none"
              rows={3}
              maxLength={10000}
              disabled={isSubmitting}
            />
          </div>

          {/* Error */}
          {error && (
            <div className="mb-4 p-2 tui-frame text-sm" style={{ borderColor: 'var(--tui-error)', color: 'var(--tui-error)' }}>
              {error}
            </div>
          )}

          {/* Buttons */}
          <div className="flex gap-3">
            <button
              type="button"
              onClick={onClose}
              className="tui-btn flex-1"
              disabled={isSubmitting}
            >
              Cancel
            </button>
            <button
              type="submit"
              className="tui-btn flex-1 disabled:opacity-50 disabled:cursor-not-allowed"
              style={{ background: 'var(--tui-water)', color: 'var(--tui-bg)' }}
              disabled={isSubmitting}
            >
              {isSubmitting ? 'Adding...' : 'Add'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
