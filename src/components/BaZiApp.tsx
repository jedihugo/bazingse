'use client';

import { useState, useEffect, useCallback, useMemo } from 'react';
import { analyzeBazi, loadFromStorage, saveToStorage, isValidDate, type AnalyzeBaziParams, type StoredFormData } from '@/lib/api';
import NatalInputPanel from './NatalInputPanel';
import ComparisonInputPanel from './ComparisonInputPanel';
import TalismanInputPanel from './TalismanInputPanel';
import BaZiChart from './BaZiChart';
import ElementAnalysis from './ElementAnalysis';
import NarrativeDisplay from './NarrativeDisplay';
import PillarStoryDisplay from './PillarStoryDisplay';

// Quick test presets
interface TestPreset {
  date: string;
  time: string;
  gender: 'male' | 'female';
  note?: string;
  unknownHour?: boolean;
}

const TEST_PRESETS: TestPreset[] = [
  { date: '1969-07-04', time: '18:20', gender: 'female' },
  { date: '1992-07-06', time: '09:30', gender: 'female' },
  { date: '1995-04-19', time: '17:30', gender: 'male' },
  { date: '1985-06-23', time: '13:30', gender: 'male' },
  { date: '1988-02-02', time: '13:30', gender: 'male' },
  { date: '1986-11-29', time: '13:30', gender: 'male' },
  { date: '1995-08-14', time: '11:30', gender: 'female' },
  { date: '1995-07-18', time: '16:30', gender: 'female' },
  { date: '1992-09-18', time: '09:30', gender: 'female' },
  { date: '2002-04-17', time: '08:20', gender: 'female' },
  { date: '2019-09-18', time: '05:00', gender: 'female' },
  { date: '2021-08-09', time: '21:00', gender: 'female' },
  { date: '1985-03-20', time: '23:00', gender: 'female' },
  { date: '1995-02-10', time: '10:10', gender: 'female' },
  { date: '1946-08-12', time: '07:00', gender: 'male', note: 'Suharsa' },
  { date: '1962-11-03', time: '11:45', gender: 'male', note: 'Malaysian - Mata Ikan' },
  { date: '1954-02-09', time: '09:30', gender: 'female' },
  { date: '1949-12-19', time: '08:00', gender: 'male' },
  { date: '1955-10-18', time: '20:00', gender: 'female' },
  { date: '1992-12-25', time: '', gender: 'female', unknownHour: true },
  { date: '1945-03-26', time: '18:00', gender: 'male', note: 'batubara, hutan, punya tanah, pulau' },
  { date: '1969-04-07', time: '18:30', gender: 'female', note: 'Wu Chen wealth storage' },
];

// Default form state
const DEFAULT_FORM: StoredFormData = {
  birthDate: '1992-07-06',
  birthTime: '09:30',
  gender: 'female',
  unknownHour: false,
  yearInput: 1992,
  monthInput: 7,
  dayInput: 6,
  analysisYear: null,
  analysisMonth: null,
  analysisDay: null,
  analysisTime: '',
  showAnalysisPeriod: false,
  includeAnnualLuck: true,
  includeMonthlyLuck: false,
  includeDailyLuck: false,
  includeHourlyLuck: false,
  showTalismans: false,
  talismanYearHS: null,
  talismanYearEB: null,
  talismanMonthHS: null,
  talismanMonthEB: null,
  talismanDayHS: null,
  talismanDayEB: null,
  talismanHourHS: null,
  talismanHourEB: null,
  showLocation: false,
  locationType: null,
};

export default function BaZiApp() {
  // Form state
  const [formData, setFormData] = useState<StoredFormData>(DEFAULT_FORM);
  const [isClient, setIsClient] = useState(false);
  const [showPresets, setShowPresets] = useState(false);

  // Chart data from API
  const [chartData, setChartData] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Initialize from localStorage on client
  useEffect(() => {
    setIsClient(true);
    const saved = loadFromStorage();
    if (saved) {
      setFormData(saved);
    }
  }, []);

  // Derived values
  const isValidBirthDate = useMemo(() => {
    return isValidDate(formData.yearInput, formData.monthInput, formData.dayInput);
  }, [formData.yearInput, formData.monthInput, formData.dayInput]);

  // Update form data and save to storage
  const updateFormData = useCallback((updates: Partial<StoredFormData>) => {
    setFormData(prev => {
      const newData = { ...prev, ...updates };

      // Sync birthDate from individual inputs
      if (updates.yearInput !== undefined || updates.monthInput !== undefined || updates.dayInput !== undefined) {
        const year = updates.yearInput ?? prev.yearInput;
        const month = String(updates.monthInput ?? prev.monthInput).padStart(2, '0');
        const day = String(updates.dayInput ?? prev.dayInput).padStart(2, '0');
        newData.birthDate = `${year}-${month}-${day}`;
      }

      saveToStorage(newData);
      return newData;
    });
  }, []);

  // Generate chart
  const generateChart = useCallback(async () => {
    if (!isValidBirthDate) return;

    setError(null);
    setIsLoading(true);

    try {
      const params: AnalyzeBaziParams = {
        birthDate: formData.birthDate,
        birthTime: formData.birthTime,
        gender: formData.gender,
        unknownHour: formData.unknownHour,
      };

      // Add analysis parameters if time travel mode is enabled
      if (formData.showAnalysisPeriod && formData.analysisYear) {
        params.analysisYear = formData.analysisYear;
        params.includeAnnualLuck = formData.includeAnnualLuck;
        params.analysisMonth = formData.analysisMonth;
        params.includeMonthlyLuck = formData.includeMonthlyLuck;
        params.analysisDay = formData.analysisDay;
        params.includeDailyLuck = formData.includeDailyLuck;
        params.analysisTime = formData.analysisTime;
        params.includeHourlyLuck = formData.includeHourlyLuck;
      }

      // Add talisman parameters
      if (formData.showTalismans) {
        params.showTalismans = true;
        params.talismanYearHS = formData.talismanYearHS;
        params.talismanYearEB = formData.talismanYearEB;
        params.talismanMonthHS = formData.talismanMonthHS;
        params.talismanMonthEB = formData.talismanMonthEB;
        params.talismanDayHS = formData.talismanDayHS;
        params.talismanDayEB = formData.talismanDayEB;
        params.talismanHourHS = formData.talismanHourHS;
        params.talismanHourEB = formData.talismanHourEB;
      }

      // Add location parameters
      if (formData.showLocation && formData.locationType) {
        params.showLocation = true;
        params.locationType = formData.locationType;
      }

      const data = await analyzeBazi(params);
      setChartData(data);
    } catch (err) {
      console.error('Error generating chart:', err);
      setError(err instanceof Error ? err.message : 'Failed to generate chart');
    } finally {
      setIsLoading(false);
    }
  }, [formData, isValidBirthDate]);

  // Load preset
  const loadPreset = useCallback((preset: TestPreset) => {
    const [year, month, day] = preset.date.split('-').map(Number);

    updateFormData({
      birthDate: preset.date,
      birthTime: preset.unknownHour ? '' : preset.time,
      gender: preset.gender,
      yearInput: year,
      monthInput: month,
      dayInput: day,
      unknownHour: preset.unknownHour || false,
      showAnalysisPeriod: false,
      analysisYear: null,
      analysisMonth: null,
      analysisDay: null,
      analysisTime: '',
    });
    setShowPresets(false);
  }, [updateFormData]);

  // Generate chart on form change
  useEffect(() => {
    if (isClient && isValidBirthDate) {
      generateChart();
    }
  }, [isClient, formData.birthDate, formData.birthTime, formData.gender, formData.unknownHour,
      formData.showAnalysisPeriod, formData.analysisYear, formData.includeAnnualLuck,
      formData.analysisMonth, formData.includeMonthlyLuck, formData.analysisDay,
      formData.includeDailyLuck, formData.analysisTime, formData.includeHourlyLuck,
      formData.showTalismans, formData.talismanYearHS, formData.talismanYearEB,
      formData.talismanMonthHS, formData.talismanMonthEB, formData.talismanDayHS,
      formData.talismanDayEB, formData.talismanHourHS, formData.talismanHourEB,
      formData.showLocation, formData.locationType, isValidBirthDate, generateChart]);

  // Check if comparison/luck row should be shown
  const hasLuckData = chartData?.analysis_info?.has_luck_pillar ||
    chartData?.analysis_info?.year ||
    chartData?.analysis_info?.has_monthly ||
    chartData?.analysis_info?.has_daily ||
    chartData?.analysis_info?.has_hourly ||
    (chartData?.hs_o1 || chartData?.eb_o1) ||
    (chartData?.hs_b1 || chartData?.eb_b1);

  // Check if talisman row should be shown
  const hasTalismanData = chartData?.hs_ty || chartData?.eb_ty ||
    chartData?.hs_tm || chartData?.eb_tm ||
    chartData?.hs_td || chartData?.eb_td ||
    chartData?.hs_th || chartData?.eb_th;

  return (
    <div className="w-full max-w-2xl mx-auto p-2">
      {/* Main TUI Frame */}
      <div className="tui-frame">
        {/* Title Bar */}
        <div className="tui-frame-title flex items-center justify-between">
          <span>BAZINGSE 八字</span>
          <div className="flex items-center gap-2">
            {isLoading && <span className="tui-text-muted">...</span>}
            <button
              onClick={() => setShowPresets(!showPresets)}
              className="tui-btn"
            >
              {showPresets ? '[-]' : '[+]'}
            </button>
          </div>
        </div>

        {/* Quick Test Presets (collapsible) */}
        {showPresets && (
          <div className="border-b tui-border-color p-2">
            <div className="flex flex-wrap gap-1">
              {TEST_PRESETS.map((preset, idx) => (
                <button
                  key={idx}
                  onClick={() => loadPreset(preset)}
                  className="tui-btn"
                >
                  {preset.date.substring(2)} {preset.unknownHour ? '?' : preset.time.substring(0,5)} {preset.gender === 'female' ? 'F' : 'M'}
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Error Display */}
        {error && (
          <div className="border-b tui-border-color px-2 py-1 tui-text-fire">
            Error: {error}
          </div>
        )}

        {/* NATAL CHART */}
        <div className="border-b tui-border-color">
          <div className="tui-bg-alt px-2 py-1 tui-text-dim border-b tui-border-color">
            NATAL 命盤
          </div>
          <NatalInputPanel
            formData={formData}
            updateFormData={updateFormData}
            isValidBirthDate={isValidBirthDate}
          />
          {chartData && (
            <div className="px-1 pb-1">
              <BaZiChart
                chartData={chartData}
                showNatal={true}
                showLuck={false}
                showTalisman={false}
                showLocation={true}
              />
            </div>
          )}
        </div>

        {/* TIME TRAVEL */}
        <div className="border-b tui-border-color">
          <div className="tui-bg-alt px-2 py-1 tui-text-dim border-b tui-border-color">
            TIME TRAVEL 運
          </div>
          <ComparisonInputPanel
            formData={formData}
            updateFormData={updateFormData}
            chartData={chartData}
          />
          {chartData && hasLuckData && (
            <div className="px-1 pb-1">
              <BaZiChart
                chartData={chartData}
                showNatal={false}
                showLuck={true}
                showTalisman={false}
                showLocation={false}
              />
            </div>
          )}
        </div>

        {/* TALISMAN */}
        <div>
          <div className="tui-bg-alt px-2 py-1 tui-text-dim border-b tui-border-color">
            TALISMAN 符
          </div>
          <TalismanInputPanel
            formData={formData}
            updateFormData={updateFormData}
          />
          {chartData && hasTalismanData && (
            <div className="px-1 pb-1">
              <BaZiChart
                chartData={chartData}
                showNatal={false}
                showLuck={false}
                showTalisman={true}
                showLocation={false}
              />
            </div>
          )}
        </div>
      </div>

      {/* Element Analysis */}
      {chartData && (
        <ElementAnalysis chartData={chartData} />
      )}

      {/* Pillar Story (Node-by-Node) */}
      {chartData && chartData.pillar_stories && (
        <PillarStoryDisplay chartData={chartData} />
      )}

      {/* Interaction-Based Narratives */}
      {chartData && chartData.narrative_analysis && (
        <details className="tui-frame mt-2">
          <summary className="tui-frame-title cursor-pointer">
            [+] INTERACTION ANALYSIS
          </summary>
          <NarrativeDisplay chartData={chartData} />
        </details>
      )}
    </div>
  );
}
