'use client';

import { useState } from 'react';
import TimelineEntry from './TimelineEntry';
import AddTimelineModal from './AddTimelineModal';

interface TimelineDate {
  year: number;
  month?: number;
  day?: number;
}

interface TimelineItem {
  date: TimelineDate;
  chartData: any;
  isLoading: boolean;
  error: string | null;
}

interface TimelineViewProps {
  natalChartData: any;
  items: TimelineItem[];
  onAddEntry: (date: TimelineDate) => void;
  onRemoveEntry: (index: number) => void;
}

// Sort entries by date (ascending)
function sortByDate(a: TimelineDate, b: TimelineDate): number {
  if (a.year !== b.year) return a.year - b.year;
  if ((a.month || 0) !== (b.month || 0)) return (a.month || 0) - (b.month || 0);
  return (a.day || 0) - (b.day || 0);
}

export default function TimelineView({
  natalChartData,
  items,
  onAddEntry,
  onRemoveEntry,
}: TimelineViewProps) {
  const [showAddModal, setShowAddModal] = useState(false);

  const existingDates = items.map(item => item.date);

  const handleAdd = (date: TimelineDate) => {
    onAddEntry(date);
    setShowAddModal(false);
  };

  // Sort items by date
  const sortedItems = [...items].sort((a, b) => sortByDate(a.date, b.date));

  return (
    <div className="space-y-4">
      {/* Natal Entry (always first) */}
      <TimelineEntry
        date={{ year: 0 }}
        chartData={natalChartData}
        isNatal={true}
      />

      {/* Timeline Entries */}
      {sortedItems.map((item, idx) => {
        // Find original index for deletion
        const originalIndex = items.findIndex(i =>
          i.date.year === item.date.year &&
          i.date.month === item.date.month &&
          i.date.day === item.date.day
        );

        return (
          <TimelineEntry
            key={`${item.date.year}-${item.date.month || 0}-${item.date.day || 0}`}
            date={item.date}
            chartData={item.chartData}
            isLoading={item.isLoading}
            error={item.error}
            onDelete={() => onRemoveEntry(originalIndex)}
          />
        );
      })}

      {/* Add Entry Button */}
      <button
        onClick={() => setShowAddModal(true)}
        className="w-full py-3 border-2 border-dashed tui-border-color tui-text-muted transition-colors flex items-center justify-center gap-2"
      >
        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
          <path fillRule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clipRule="evenodd" />
        </svg>
        Add Period
      </button>

      {/* Add Modal */}
      {showAddModal && (
        <AddTimelineModal
          onAdd={handleAdd}
          onClose={() => setShowAddModal(false)}
          existingDates={existingDates}
        />
      )}
    </div>
  );
}
