'use client';

import { useState } from 'react';

interface AddTimelineModalProps {
  onAdd: (date: { year: number; month?: number; day?: number }) => void;
  onClose: () => void;
  existingDates: { year: number; month?: number; day?: number }[];
}

export default function AddTimelineModal({ onAdd, onClose, existingDates }: AddTimelineModalProps) {
  const currentYear = new Date().getFullYear();
  const [year, setYear] = useState<number>(currentYear);
  const [month, setMonth] = useState<number | ''>('');
  const [day, setDay] = useState<number | ''>('');
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    // Check for duplicate
    const isDuplicate = existingDates.some(d =>
      d.year === year &&
      (d.month || undefined) === (month || undefined) &&
      (d.day || undefined) === (day || undefined)
    );

    if (isDuplicate) {
      setError('This date already exists in the timeline');
      return;
    }

    onAdd({
      year,
      month: month || undefined,
      day: day || undefined,
    });
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="tui-frame tui-bg-panel p-6 w-full max-w-sm mx-4">
        <h2 className="text-xl font-bold mb-4 tui-text">Add Timeline Entry</h2>
        <form onSubmit={handleSubmit}>
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
            />
          </div>
          <div className="mb-4">
            <label className="block text-sm font-medium tui-text-dim mb-1">
              Month <span className="tui-text-muted">(optional)</span>
            </label>
            <select
              value={month}
              onChange={(e) => setMonth(e.target.value ? parseInt(e.target.value) : '')}
              className="tui-input w-full"
            >
              <option value="">-- Select Month --</option>
              {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12].map(m => (
                <option key={m} value={m}>
                  {new Date(2000, m - 1, 1).toLocaleString('default', { month: 'long' })}
                </option>
              ))}
            </select>
          </div>
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
              disabled={!month}
              className="tui-input w-full disabled:opacity-50"
            />
          </div>

          {error && (
            <div className="mb-4 p-2 tui-frame text-sm" style={{ borderColor: 'var(--tui-error)', color: 'var(--tui-error)' }}>
              {error}
            </div>
          )}

          <div className="flex gap-3">
            <button
              type="button"
              onClick={onClose}
              className="tui-btn flex-1"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="tui-btn flex-1"
              style={{ background: 'var(--tui-water)', color: 'var(--tui-bg)' }}
            >
              Add
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
