'use client';

import { useState, useEffect, useCallback, useRef } from 'react';
import { getDongGongCalendar, type DongGongDay, type DongGongCalendarResponse } from '@/lib/api';

const WEEKDAYS = ['SU', 'MO', 'TU', 'WE', 'TH', 'FR', 'SA'];
const MONTH_NAMES = [
  'January', 'February', 'March', 'April', 'May', 'June',
  'July', 'August', 'September', 'October', 'November', 'December',
];

function ratingColor(value: number): string {
  if (value >= 4) return 'var(--tui-wood)';
  if (value === 3) return 'var(--tui-earth)';
  return 'var(--tui-fire)';
}

function ratingBg(value: number): string {
  if (value >= 4) return 'color-mix(in srgb, var(--tui-wood) 15%, var(--tui-bg))';
  if (value === 3) return 'color-mix(in srgb, var(--tui-earth) 15%, var(--tui-bg))';
  return 'color-mix(in srgb, var(--tui-fire) 15%, var(--tui-bg))';
}

export default function DongGongCalendar() {
  const today = new Date();
  const [year, setYear] = useState(today.getFullYear());
  const [month, setMonth] = useState(today.getMonth() + 1);
  const [data, setData] = useState<DongGongCalendarResponse | null>(null);
  const [selectedDay, setSelectedDay] = useState<number | null>(null);
  const [focusedDay, setFocusedDay] = useState<number | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const gridRef = useRef<HTMLDivElement>(null);

  const isToday = useCallback(
    (day: number) => year === today.getFullYear() && month === today.getMonth() + 1 && day === today.getDate(),
    [year, month, today],
  );

  const loadCalendar = useCallback(async () => {
    try {
      setIsLoading(true);
      setError(null);
      const result = await getDongGongCalendar(year, month);
      setData(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load calendar');
    } finally {
      setIsLoading(false);
    }
  }, [year, month]);

  useEffect(() => {
    loadCalendar();
    setSelectedDay(null);
    setFocusedDay(null);
  }, [loadCalendar]);

  const goToPrevMonth = () => {
    if (month === 1) { setYear(y => y - 1); setMonth(12); }
    else setMonth(m => m - 1);
  };

  const goToNextMonth = () => {
    if (month === 12) { setYear(y => y + 1); setMonth(1); }
    else setMonth(m => m + 1);
  };

  const goToToday = () => {
    setYear(today.getFullYear());
    setMonth(today.getMonth() + 1);
    setSelectedDay(today.getDate());
    setFocusedDay(today.getDate());
  };

  // Keyboard navigation
  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      // Ignore if typing in an input
      if ((e.target as HTMLElement)?.tagName === 'INPUT') return;

      if (e.key === '[' || e.key === 'h') { goToPrevMonth(); return; }
      if (e.key === ']' || e.key === 'l') { goToNextMonth(); return; }
      if (e.key === 't') { goToToday(); return; }

      if (!data) return;
      const maxDay = data.days_in_month;

      if (e.key === 'Escape') { setSelectedDay(null); return; }

      if (e.key === 'Enter' && focusedDay) {
        setSelectedDay(prev => prev === focusedDay ? null : focusedDay);
        return;
      }

      // Arrow key navigation
      if (['ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown'].includes(e.key)) {
        e.preventDefault();
        setFocusedDay(prev => {
          const current = prev || 1;
          let next = current;
          if (e.key === 'ArrowLeft') next = current - 1;
          if (e.key === 'ArrowRight') next = current + 1;
          if (e.key === 'ArrowUp') next = current - 7;
          if (e.key === 'ArrowDown') next = current + 7;
          if (next < 1) next = 1;
          if (next > maxDay) next = maxDay;
          return next;
        });
      }
    };
    window.addEventListener('keydown', handler);
    return () => window.removeEventListener('keydown', handler);
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [data, focusedDay]);

  const selectedDayData = data?.days.find(d => d.day === selectedDay) || null;

  // Build grid: padding cells + day cells
  const emptyCells = data ? data.first_day_weekday : 0;

  return (
    <div className="tui-frame" style={{ border: '1px solid var(--tui-border)' }}>
      {/* Title bar */}
      <div
        className="px-3 py-2 text-center font-bold text-sm"
        style={{ borderBottom: '1px solid var(--tui-border)', background: 'var(--tui-bg-alt)' }}
      >
        董公日曆
      </div>

      {/* Month navigation */}
      <div
        className="flex items-center justify-between px-3 py-2"
        style={{ borderBottom: '1px solid var(--tui-border)' }}
      >
        <button onClick={goToPrevMonth} className="tui-btn px-2 py-0.5 text-sm" title="Previous month">
          &lt;
        </button>
        <div className="text-center">
          <span className="font-bold tui-text">{MONTH_NAMES[month - 1]} {year}</span>
          {data && data.chinese_months_spanned.length > 0 && (
            <div className="text-xs tui-text-muted mt-0.5">
              {data.chinese_months_spanned.map((cm, i) => (
                <span key={cm.month}>
                  {i > 0 && ' / '}
                  {cm.chinese} ({cm.branch})
                </span>
              ))}
            </div>
          )}
        </div>
        <button onClick={goToNextMonth} className="tui-btn px-2 py-0.5 text-sm" title="Next month">
          &gt;
        </button>
      </div>

      {/* Today button */}
      <div className="flex justify-center py-1.5" style={{ borderBottom: '1px solid var(--tui-border)' }}>
        <button onClick={goToToday} className="tui-btn text-xs px-3 py-0.5">
          Today
        </button>
      </div>

      {/* Loading / Error */}
      {isLoading && (
        <div className="py-8 text-center tui-text-muted text-sm">Loading...</div>
      )}
      {error && (
        <div className="py-4 text-center text-sm" style={{ color: 'var(--tui-fire)' }}>{error}</div>
      )}

      {/* Calendar grid */}
      {data && !isLoading && (
        <div ref={gridRef}>
          {/* Weekday headers */}
          <div
            className="grid text-center text-xs font-bold py-1"
            style={{
              gridTemplateColumns: 'repeat(7, 1fr)',
              borderBottom: '1px solid var(--tui-border)',
              background: 'var(--tui-bg-alt)',
            }}
          >
            {WEEKDAYS.map(wd => (
              <div key={wd} className="tui-text-muted">{wd}</div>
            ))}
          </div>

          {/* Day cells */}
          <div
            className="grid"
            style={{ gridTemplateColumns: 'repeat(7, 1fr)' }}
          >
            {/* Empty cells for offset */}
            {Array.from({ length: emptyCells }).map((_, i) => (
              <div key={`empty-${i}`} style={{ borderBottom: '1px solid var(--tui-border-dim, var(--tui-border))' }} />
            ))}

            {/* Day cells */}
            {data.days.map((dayData) => {
              const isTodayCell = isToday(dayData.day);
              const isSelected = selectedDay === dayData.day;
              const isFocused = focusedDay === dayData.day;

              return (
                <button
                  key={dayData.day}
                  onClick={() => setSelectedDay(prev => prev === dayData.day ? null : dayData.day)}
                  onFocus={() => setFocusedDay(dayData.day)}
                  className="relative text-center py-1.5 px-0.5"
                  style={{
                    borderBottom: '1px solid var(--tui-border-dim, var(--tui-border))',
                    borderRight: (emptyCells + dayData.day) % 7 !== 0 ? '1px solid var(--tui-border-dim, var(--tui-border))' : undefined,
                    background: isSelected
                      ? (dayData.rating ? ratingBg(dayData.rating.value) : 'var(--tui-bg-alt)')
                      : 'transparent',
                    outline: isFocused ? '2px solid var(--tui-water)' : isTodayCell ? '2px solid var(--tui-water)' : 'none',
                    outlineOffset: '-2px',
                    cursor: 'pointer',
                    minHeight: '52px',
                  }}
                >
                  {/* Day number */}
                  <div
                    className="text-sm font-bold"
                    style={{ color: dayData.weekday === 0 ? 'var(--tui-fire)' : 'var(--tui-fg)' }}
                  >
                    {dayData.day}
                  </div>

                  {/* Rating symbol */}
                  {dayData.rating && (
                    <div
                      className="text-xs font-bold mt-0.5"
                      style={{ color: ratingColor(dayData.rating.value) }}
                    >
                      {dayData.rating.symbol}
                    </div>
                  )}

                  {/* Day stem-branch (abbreviated) */}
                  <div className="text-[9px] tui-text-muted mt-0.5 leading-none">
                    {dayData.day_stem_chinese}{dayData.day_branch_chinese}
                  </div>
                </button>
              );
            })}
          </div>
        </div>
      )}

      {/* Selected day detail panel */}
      {selectedDayData && (
        <DayDetail day={selectedDayData} onClose={() => setSelectedDay(null)} />
      )}

      {/* Keyboard hints */}
      <div
        className="text-center text-[10px] tui-text-muted py-1.5 px-2"
        style={{ borderTop: '1px solid var(--tui-border)' }}
      >
        [h/&#91;] Prev &nbsp; [l/&#93;] Next &nbsp; [t] Today &nbsp; [Enter] Select &nbsp; [Esc] Close
      </div>
    </div>
  );
}

function DayDetail({ day, onClose }: { day: DongGongDay; onClose: () => void }) {
  return (
    <div
      className="px-3 py-3"
      style={{ borderTop: '2px solid var(--tui-border-bright, var(--tui-border))' }}
    >
      {/* Header: date + pillar */}
      <div className="flex items-center justify-between mb-2">
        <div className="font-bold tui-text text-sm">
          {day.day} &middot; {day.day_stem_chinese}{day.day_branch_chinese} {day.pillar}
        </div>
        <button onClick={onClose} className="tui-btn text-xs px-1.5 py-0.5">
          &times;
        </button>
      </div>

      {/* Officer + Rating */}
      <div className="flex items-center gap-3 mb-2 text-sm">
        {day.officer && (
          <span className="tui-text-muted">
            {day.officer.chinese} {day.officer.english}
          </span>
        )}
        {day.rating && (
          <span
            className="font-bold px-1.5 py-0.5 text-xs"
            style={{
              color: ratingColor(day.rating.value),
              background: ratingBg(day.rating.value),
            }}
          >
            {day.rating.symbol} {day.rating.chinese}
          </span>
        )}
      </div>

      {/* Chinese month */}
      {day.chinese_month_name && (
        <div className="text-xs tui-text-muted mb-2">
          {day.chinese_month_name}
        </div>
      )}

      {/* Good for */}
      {day.good_for.length > 0 && (
        <div className="mb-1.5">
          <span className="text-xs font-bold" style={{ color: 'var(--tui-wood)' }}>Good for: </span>
          <span className="text-xs tui-text">
            {day.good_for.map(a => a.replace(/_/g, ' ')).join(', ')}
          </span>
        </div>
      )}

      {/* Bad for */}
      {day.bad_for.length > 0 && (
        <div className="mb-1.5">
          <span className="text-xs font-bold" style={{ color: 'var(--tui-fire)' }}>Avoid: </span>
          <span className="text-xs tui-text">
            {day.bad_for.map(a => a.replace(/_/g, ' ')).join(', ')}
          </span>
        </div>
      )}

      {/* Description */}
      {day.description_chinese && (
        <div className="text-xs tui-text-muted mt-2 leading-relaxed" style={{ borderTop: '1px solid var(--tui-border)', paddingTop: '0.5rem' }}>
          {day.description_chinese}
        </div>
      )}
      {day.description_english && (
        <div className="text-xs tui-text-muted mt-1 leading-relaxed">
          {day.description_english}
        </div>
      )}
    </div>
  );
}
