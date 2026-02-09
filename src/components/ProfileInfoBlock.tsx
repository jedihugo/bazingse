'use client';

import { useState, useEffect, useRef } from 'react';
import { type Profile, type ProfileUpdate, updateProfile } from '@/lib/api';
import GuidedDateInput from './chat-form/GuidedDateInput';
import GuidedTimeInput from './chat-form/GuidedTimeInput';

interface ProfileInfoBlockProps {
  profile: Profile;
  onProfileUpdate: (profile: Profile) => void;
  onBack?: () => void;
  onBirthDataChange?: () => void;
}

export default function ProfileInfoBlock({
  profile,
  onProfileUpdate,
  onBack,
  onBirthDataChange,
}: ProfileInfoBlockProps) {
  const [editingField, setEditingField] = useState<string | null>(null);
  const [editValue, setEditValue] = useState('');
  const [isSaving, setIsSaving] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  // Structured date/time editing state
  const [dateYear, setDateYear] = useState<string | number>('');
  const [dateMonth, setDateMonth] = useState<string | number>('');
  const [dateDay, setDateDay] = useState<string | number>('');
  const [timeHour, setTimeHour] = useState('');
  const [timeMinute, setTimeMinute] = useState('');
  const [timeUnknown, setTimeUnknown] = useState(false);

  useEffect(() => {
    if (editingField && editingField !== 'birth_date' && editingField !== 'birth_time' && inputRef.current) {
      inputRef.current.focus();
      inputRef.current.select();
    }
  }, [editingField]);

  const handleEdit = (field: string, value: string) => {
    if (field === 'birth_date') {
      const parts = profile.birth_date.split('-');
      setDateYear(parts[0] || '');
      setDateMonth(parts[1] ? String(parseInt(parts[1])) : '');
      setDateDay(parts[2] ? String(parseInt(parts[2])) : '');
    } else if (field === 'birth_time') {
      if (profile.birth_time) {
        const parts = profile.birth_time.split(':');
        setTimeHour(parts[0] || '');
        setTimeMinute(parts[1] || '');
        setTimeUnknown(false);
      } else {
        setTimeHour('');
        setTimeMinute('');
        setTimeUnknown(true);
      }
    } else {
      setEditValue(value);
    }
    setEditingField(field);
  };

  const handleSave = async () => {
    if (!editingField || isSaving) return;

    // Build update payload
    const updateData: ProfileUpdate = {};
    let isBirthDataChange = false;

    if (editingField === 'birth_date') {
      const y = String(dateYear).padStart(4, '0');
      const m = String(dateMonth).padStart(2, '0');
      const d = String(dateDay).padStart(2, '0');
      const newDate = `${y}-${m}-${d}`;
      // Basic validation
      const yNum = parseInt(y); const mNum = parseInt(m); const dNum = parseInt(d);
      if (yNum < 1900 || yNum > 2100 || mNum < 1 || mNum > 12 || dNum < 1 || dNum > 31) {
        setEditingField(null);
        return;
      }
      if (newDate !== profile.birth_date) {
        updateData.birth_date = newDate;
        isBirthDataChange = true;
      }
    } else if (editingField === 'birth_time') {
      if (timeUnknown) {
        // Clear birth time
        if (profile.birth_time) {
          updateData.birth_time = '';
          isBirthDataChange = true;
        }
      } else {
        const h = timeHour.padStart(2, '0');
        const min = timeMinute.padStart(2, '0');
        const hNum = parseInt(h); const minNum = parseInt(min);
        if (isNaN(hNum) || hNum < 0 || hNum > 23 || isNaN(minNum) || minNum < 0 || minNum > 59) {
          setEditingField(null);
          return;
        }
        const newTime = `${h}:${min}`;
        if (newTime !== (profile.birth_time || '')) {
          updateData.birth_time = newTime;
          isBirthDataChange = true;
        }
      }
    } else {
      const trimmedValue = editValue.trim();
      if (editingField === 'name' && trimmedValue !== profile.name) {
        if (!trimmedValue) {
          setEditingField(null);
          return;
        }
        updateData.name = trimmedValue;
      } else if (editingField === 'place_of_birth' && trimmedValue !== (profile.place_of_birth || '')) {
        updateData.place_of_birth = trimmedValue || undefined;
      } else if (editingField === 'phone' && trimmedValue !== (profile.phone || '')) {
        updateData.phone = trimmedValue || undefined;
      }
    }

    // Only save if there are changes
    if (Object.keys(updateData).length === 0) {
      setEditingField(null);
      return;
    }

    try {
      setIsSaving(true);
      const updated = await updateProfile(profile.id, updateData);
      onProfileUpdate(updated);
      if (isBirthDataChange) {
        onBirthDataChange?.();
      }
    } catch (err) {
      console.error('Failed to save:', err);
    } finally {
      setIsSaving(false);
      setEditingField(null);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSave();
    } else if (e.key === 'Escape') {
      setEditingField(null);
    }
  };

  return (
    <div className="tui-bg-panel border-b tui-border-color px-4 py-4 mb-4">
      {/* Back button + Name row */}
      <div className="flex items-center gap-3 mb-2">
        {onBack && (
          <button
            onClick={onBack}
            className="tui-back-btn"
            title="Back to profiles"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
          </button>
        )}

        {/* Editable Name */}
        {editingField === 'name' ? (
          <input
            ref={inputRef}
            type="text"
            value={editValue}
            onChange={(e) => setEditValue(e.target.value)}
            onBlur={handleSave}
            onKeyDown={handleKeyDown}
            className="text-2xl font-bold tui-text bg-transparent border-b-2 outline-none w-full"
            style={{ borderColor: 'var(--tui-water)' }}
            maxLength={100}
          />
        ) : (
          <h1
            onClick={() => handleEdit('name', profile.name)}
            className="text-2xl font-bold tui-text cursor-pointer px-1 -mx-1"
            title="Click to edit"
          >
            {profile.name}
          </h1>
        )}
      </div>

      {/* Birth info row */}
      <div className="flex flex-wrap items-center gap-x-3 gap-y-1 text-sm tui-text-dim mb-2">
        {editingField === 'birth_date' ? (
          <div className="flex items-center gap-2" onKeyDown={(e) => {
            if (e.key === 'Escape') setEditingField(null);
            if (e.key === 'Enter') handleSave();
          }}>
            <GuidedDateInput
              year={dateYear}
              month={dateMonth}
              day={dateDay}
              onYearChange={setDateYear}
              onMonthChange={setDateMonth}
              onDayChange={setDateDay}
              autoFocusYear
            />
            <button onClick={handleSave} className="text-xs tui-btn px-2 py-0.5" style={{ color: 'var(--tui-water)' }}>OK</button>
            <button onClick={() => setEditingField(null)} className="text-xs tui-text-muted px-1">Esc</button>
          </div>
        ) : (
          <span
            onClick={() => handleEdit('birth_date', '')}
            className="cursor-pointer px-1 -mx-1"
            title="Click to edit birth date"
          >
            {profile.birth_date}
          </span>
        )}
        {editingField === 'birth_time' ? (
          <div className="flex items-center gap-2" onKeyDown={(e) => {
            if (e.key === 'Escape') setEditingField(null);
            if (e.key === 'Enter') handleSave();
          }}>
            <GuidedTimeInput
              hour={timeHour}
              minute={timeMinute}
              onHourChange={setTimeHour}
              onMinuteChange={setTimeMinute}
              showUnknownToggle
              isUnknown={timeUnknown}
              onUnknownChange={setTimeUnknown}
              autoFocus
            />
            <button onClick={handleSave} className="text-xs tui-btn px-2 py-0.5" style={{ color: 'var(--tui-water)' }}>OK</button>
            <button onClick={() => setEditingField(null)} className="text-xs tui-text-muted px-1">Esc</button>
          </div>
        ) : (
          <span
            onClick={() => handleEdit('birth_time', '')}
            className={`cursor-pointer px-1 -mx-1 ${profile.birth_time ? '' : 'tui-text-muted italic'}`}
            title="Click to edit birth time"
          >
            {profile.birth_time || 'Add time...'}
          </span>
        )}
        <span className="tui-text-muted">|</span>
        <span style={{ color: profile.gender === 'female' ? 'var(--tui-accent-pink)' : 'var(--tui-water)' }}>
          {profile.gender === 'female' ? '\u2640 Female' : '\u2642 Male'}
        </span>
      </div>

      {/* Place of birth (editable) */}
      <div className="flex items-center text-sm">
        <span className="tui-text-muted mr-2">Place of birth:</span>
        {editingField === 'place_of_birth' ? (
          <input
            ref={inputRef}
            type="text"
            value={editValue}
            onChange={(e) => setEditValue(e.target.value)}
            onBlur={handleSave}
            onKeyDown={handleKeyDown}
            placeholder="Enter place of birth..."
            className="tui-text-dim bg-transparent border-b outline-none flex-1"
            style={{ borderColor: 'var(--tui-water)' }}
            maxLength={200}
          />
        ) : (
          <span
            onClick={() => handleEdit('place_of_birth', profile.place_of_birth || '')}
            className={`cursor-pointer px-1 -mx-1 ${
              profile.place_of_birth ? 'tui-text-dim' : 'tui-text-muted italic'
            }`}
            title="Click to edit"
          >
            {profile.place_of_birth || 'Click to add...'}
          </span>
        )}
      </div>

      {/* Phone (editable) */}
      <div className="flex items-center text-sm mt-1">
        <span className="tui-text-muted mr-2">Phone:</span>
        {editingField === 'phone' ? (
          <input
            ref={inputRef}
            type="tel"
            value={editValue}
            onChange={(e) => setEditValue(e.target.value)}
            onBlur={handleSave}
            onKeyDown={handleKeyDown}
            placeholder="Enter phone number..."
            className="tui-text-dim bg-transparent border-b outline-none flex-1"
            style={{ borderColor: 'var(--tui-water)' }}
            maxLength={20}
          />
        ) : (
          <span
            onClick={() => handleEdit('phone', profile.phone || '')}
            className={`cursor-pointer px-1 -mx-1 ${
              profile.phone ? 'tui-text-dim' : 'tui-text-muted italic'
            }`}
            title="Click to edit"
          >
            {profile.phone || 'Click to add...'}
          </span>
        )}
      </div>

      {/* Saving indicator */}
      {isSaving && (
        <div className="absolute top-2 right-2 text-xs tui-text-muted">
          Saving...
        </div>
      )}
    </div>
  );
}
