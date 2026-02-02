'use client';

import { isValidJiaziPair, type StoredFormData } from '@/lib/api';
import { TypeaheadSelect } from './chat-form';

interface TalismanInputPanelProps {
  formData: StoredFormData;
  updateFormData: (updates: Partial<StoredFormData>) => void;
}

// Heavenly Stems for typeahead (10 stems)
const HEAVENLY_STEMS_OPTIONS = [
  { value: 'Jia', label: '甲 Jia', searchTerms: ['wood', 'yang'] },
  { value: 'Yi', label: '乙 Yi', searchTerms: ['wood', 'yin'] },
  { value: 'Bing', label: '丙 Bing', searchTerms: ['fire', 'yang'] },
  { value: 'Ding', label: '丁 Ding', searchTerms: ['fire', 'yin'] },
  { value: 'Wu', label: '戊 Wu', searchTerms: ['earth', 'yang'] },
  { value: 'Ji', label: '己 Ji', searchTerms: ['earth', 'yin'] },
  { value: 'Geng', label: '庚 Geng', searchTerms: ['metal', 'yang'] },
  { value: 'Xin', label: '辛 Xin', searchTerms: ['metal', 'yin'] },
  { value: 'Ren', label: '壬 Ren', searchTerms: ['water', 'yang'] },
  { value: 'Gui', label: '癸 Gui', searchTerms: ['water', 'yin'] },
];

// Earthly Branches for typeahead (12 branches)
const EARTHLY_BRANCHES_OPTIONS = [
  { value: 'Zi', label: '子 Zi', searchTerms: ['rat', 'water'] },
  { value: 'Chou', label: '丑 Chou', searchTerms: ['ox', 'earth'] },
  { value: 'Yin', label: '寅 Yin', searchTerms: ['tiger', 'wood'] },
  { value: 'Mao', label: '卯 Mao', searchTerms: ['rabbit', 'wood'] },
  { value: 'Chen', label: '辰 Chen', searchTerms: ['dragon', 'earth'] },
  { value: 'Si', label: '巳 Si', searchTerms: ['snake', 'fire'] },
  { value: 'Wu', label: '午 Wu', searchTerms: ['horse', 'fire'] },
  { value: 'Wei', label: '未 Wei', searchTerms: ['goat', 'sheep', 'earth'] },
  { value: 'Shen', label: '申 Shen', searchTerms: ['monkey', 'metal'] },
  { value: 'You', label: '酉 You', searchTerms: ['rooster', 'metal'] },
  { value: 'Xu', label: '戌 Xu', searchTerms: ['dog', 'earth'] },
  { value: 'Hai', label: '亥 Hai', searchTerms: ['pig', 'water'] },
];

// Compact pillar selector component using TypeaheadSelect
function PillarSelector({
  label,
  hsValue,
  ebValue,
  onHsChange,
  onEbChange,
  isValid,
}: {
  label: string;
  hsValue: string | null;
  ebValue: string | null;
  onHsChange: (value: string | null) => void;
  onEbChange: (value: string | null) => void;
  isValid: boolean;
}) {
  return (
    <div className="flex items-center gap-1">
      <span className={`tui-text-dim text-[10px] ${!isValid ? 'tui-text-fire' : ''}`}>
        {label}:
      </span>
      <div className="talisman-typeahead">
        <TypeaheadSelect
          options={HEAVENLY_STEMS_OPTIONS}
          value={hsValue}
          onChange={onHsChange}
          placeholder="HS"
          hasError={!isValid}
          allowClear={true}
          className="talisman-select-hs"
        />
      </div>
      <div className="talisman-typeahead">
        <TypeaheadSelect
          options={EARTHLY_BRANCHES_OPTIONS}
          value={ebValue}
          onChange={onEbChange}
          placeholder="EB"
          hasError={!isValid}
          allowClear={true}
          className="talisman-select-eb"
        />
      </div>
    </div>
  );
}

export default function TalismanInputPanel({
  formData,
  updateFormData,
}: TalismanInputPanelProps) {
  const hasInvalidTalismanPairs =
    !isValidJiaziPair(formData.talismanYearHS, formData.talismanYearEB) ||
    !isValidJiaziPair(formData.talismanMonthHS, formData.talismanMonthEB) ||
    !isValidJiaziPair(formData.talismanDayHS, formData.talismanDayEB) ||
    !isValidJiaziPair(formData.talismanHourHS, formData.talismanHourEB);

  return (
    <div className="px-2 py-1">
      {/* TUI-style inline form row */}
      <div className="flex flex-wrap items-center gap-x-3 gap-y-1 text-xs">
        {/* Talisman Toggle */}
        <label className="cursor-pointer flex items-center gap-1">
          <input
            type="checkbox"
            checked={formData.showTalismans}
            onChange={(e) => updateFormData({ showTalismans: e.target.checked })}
            className="sr-only"
          />
          <span className={formData.showTalismans ? 'tui-text-teal' : 'tui-text-muted'}>
            [{formData.showTalismans ? '×' : ' '}]
          </span>
          <span className="tui-text-teal">Talisman</span>
          {formData.showTalismans && hasInvalidTalismanPairs && (
            <span className="tui-text-fire text-[10px]">Invalid</span>
          )}
        </label>

        {/* Talisman Pillar Selectors */}
        {formData.showTalismans && (
          <>
            <PillarSelector
              label="Y"
              hsValue={formData.talismanYearHS}
              ebValue={formData.talismanYearEB}
              onHsChange={(v) => updateFormData({ talismanYearHS: v })}
              onEbChange={(v) => updateFormData({ talismanYearEB: v })}
              isValid={isValidJiaziPair(formData.talismanYearHS, formData.talismanYearEB)}
            />
            <PillarSelector
              label="M"
              hsValue={formData.talismanMonthHS}
              ebValue={formData.talismanMonthEB}
              onHsChange={(v) => updateFormData({ talismanMonthHS: v })}
              onEbChange={(v) => updateFormData({ talismanMonthEB: v })}
              isValid={isValidJiaziPair(formData.talismanMonthHS, formData.talismanMonthEB)}
            />
            <PillarSelector
              label="D"
              hsValue={formData.talismanDayHS}
              ebValue={formData.talismanDayEB}
              onHsChange={(v) => updateFormData({ talismanDayHS: v })}
              onEbChange={(v) => updateFormData({ talismanDayEB: v })}
              isValid={isValidJiaziPair(formData.talismanDayHS, formData.talismanDayEB)}
            />
            <PillarSelector
              label="H"
              hsValue={formData.talismanHourHS}
              ebValue={formData.talismanHourEB}
              onHsChange={(v) => updateFormData({ talismanHourHS: v })}
              onEbChange={(v) => updateFormData({ talismanHourEB: v })}
              isValid={isValidJiaziPair(formData.talismanHourHS, formData.talismanHourEB)}
            />
          </>
        )}
      </div>
    </div>
  );
}
