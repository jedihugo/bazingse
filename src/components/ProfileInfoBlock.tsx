'use client';

import { useState, useEffect, useRef } from 'react';
import { type Profile, type ProfileUpdate, updateProfile } from '@/lib/api';

interface ProfileInfoBlockProps {
  profile: Profile;
  onProfileUpdate: (profile: Profile) => void;
  onBack?: () => void;
}

export default function ProfileInfoBlock({
  profile,
  onProfileUpdate,
  onBack,
}: ProfileInfoBlockProps) {
  const [editingField, setEditingField] = useState<string | null>(null);
  const [editValue, setEditValue] = useState('');
  const [isSaving, setIsSaving] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (editingField && inputRef.current) {
      inputRef.current.focus();
      inputRef.current.select();
    }
  }, [editingField]);

  const handleEdit = (field: string, value: string) => {
    setEditingField(field);
    setEditValue(value);
  };

  const handleSave = async () => {
    if (!editingField || isSaving) return;

    const trimmedValue = editValue.trim();

    // Build update payload
    const updateData: ProfileUpdate = {};
    if (editingField === 'name' && trimmedValue !== profile.name) {
      if (!trimmedValue) {
        setEditingField(null);
        return; // Don't save empty name
      }
      updateData.name = trimmedValue;
    } else if (editingField === 'place_of_birth' && trimmedValue !== (profile.place_of_birth || '')) {
      updateData.place_of_birth = trimmedValue || undefined;
    } else if (editingField === 'phone' && trimmedValue !== (profile.phone || '')) {
      updateData.phone = trimmedValue || undefined;
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

  const formatBirthInfo = () => {
    const parts = [profile.birth_date];
    if (profile.birth_time) {
      parts.push(profile.birth_time);
    }
    return parts.join(' ');
  };

  return (
    <div className="tui-bg-panel border-b tui-border-color px-4 py-4 mb-4">
      {/* Back button + Name row */}
      <div className="flex items-center gap-3 mb-2">
        {onBack && (
          <button
            onClick={onBack}
            className="tui-text-muted p-1 -ml-1"
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

      {/* Birth info row (not editable for safety) */}
      <div className="flex flex-wrap items-center gap-x-3 gap-y-1 text-sm tui-text-dim mb-2">
        <span>{formatBirthInfo()}</span>
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
