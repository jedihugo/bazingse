'use client';

import { useMemo, useState } from 'react';
import { useTranslations } from 'next-intl';
import PillarCard from './PillarCard';

interface BaZiChartProps {
  chartData: any;
  showNatal?: boolean;
  show10YrLuck?: boolean;  // Show 10-yr luck with natal pillars
  showLuck?: boolean;       // Show comparison date luck (Annual, Monthly, Daily, Hourly)
  showTalisman?: boolean;
  showLocation?: boolean;
}

// Branch to element mapping
const BRANCH_TO_ELEMENT: Record<string, string> = {
  'Zi': 'Water', 'Chou': 'Earth', 'Yin': 'Wood', 'Mao': 'Wood',
  'Chen': 'Earth', 'Si': 'Fire', 'Wu': 'Fire', 'Wei': 'Earth',
  'Shen': 'Metal', 'You': 'Metal', 'Xu': 'Earth', 'Hai': 'Water'
};

// Stem to element mapping (with yin/yang polarity)
const STEM_TO_ELEMENT: Record<string, { element: string; polarity: 'yang' | 'yin' }> = {
  'Jia': { element: 'Wood', polarity: 'yang' },
  'Yi': { element: 'Wood', polarity: 'yin' },
  'Bing': { element: 'Fire', polarity: 'yang' },
  'Ding': { element: 'Fire', polarity: 'yin' },
  'Wu': { element: 'Earth', polarity: 'yang' },
  'Ji': { element: 'Earth', polarity: 'yin' },
  'Geng': { element: 'Metal', polarity: 'yang' },
  'Xin': { element: 'Metal', polarity: 'yin' },
  'Ren': { element: 'Water', polarity: 'yang' },
  'Gui': { element: 'Water', polarity: 'yin' },
};

// Element to Chinese character
const ELEMENT_CHAR: Record<string, string> = {
  'Wood': '木', 'Fire': '火', 'Earth': '土', 'Metal': '金', 'Water': '水'
};


export default function BaZiChart({
  chartData,
  showNatal = true,
  show10YrLuck = false,
  showLuck = true,
  showTalisman = true,
  showLocation = true
}: BaZiChartProps) {
  const t = useTranslations('forms');
  const mappings = chartData?.mappings || {};
  const dayMasterStem = chartData?.hs_d?.id || 'Yi';
  const [hoveredInteractionId, setHoveredInteractionId] = useState<string | null>(null);

  // Build pillar data from node
  const buildPillar = (hsKey: string, ebKey: string, label: string, isDayMaster = false) => {
    const hsNode = chartData?.[hsKey];
    const ebNode = chartData?.[ebKey];

    if (!hsNode && !ebNode) return null;

    const stemId = hsNode?.id;
    const branchId = ebNode?.id;

    // Get stem data from API mappings
    const stemMapping = mappings.heavenly_stems?.[stemId] || {};
    const stemInfo = STEM_TO_ELEMENT[stemId];
    const stemElement = stemInfo?.element || 'Unknown';

    const stem = {
      chinese: stemMapping.chinese || stemId || '?',
      element: stemElement,
      color: stemMapping.hex_color  // Just use API hex_color directly
    };

    // Check if branch is pure element transformation
    const isPureElement = ['Fire', 'Water', 'Metal', 'Wood', 'Earth'].includes(branchId);

    let branch;
    if (isPureElement) {
      // Pure element transformation - use element hex_color from API
      branch = {
        chinese: ELEMENT_CHAR[branchId] || branchId,
        animal: branchId,
        element: branchId,
        color: mappings.elements?.[branchId]?.hex_color  // Just use API hex_color directly
      };
    } else {
      // Normal branch - use branch hex_color from API
      const branchMapping = mappings.earthly_branches?.[branchId] || {};
      const branchElement = BRANCH_TO_ELEMENT[branchId] || 'Unknown';
      branch = {
        chinese: branchMapping.chinese || branchId || '?',
        animal: branchMapping.animal || '?',
        element: branchElement,
        color: branchMapping.hex_color  // Just use API hex_color directly
      };
    }

    // Get hidden stems (qi) data
    const postQi = ebNode?.post_interaction_qi && Object.keys(ebNode.post_interaction_qi).length > 0
      ? ebNode.post_interaction_qi : null;
    const baseQi = ebNode?.base_qi && Object.keys(ebNode.base_qi).length > 0
      ? ebNode.base_qi : null;
    const hiddenQi = postQi || baseQi || {};

    // Map hidden stems to Ten Gods
    const hiddenStems: Record<string, string> = {};
    if (hiddenQi && mappings.ten_gods) {
      for (const stemName of Object.keys(hiddenQi)) {
        const tenGodData = mappings.ten_gods?.[dayMasterStem]?.[stemName];
        hiddenStems[stemName] = tenGodData?.abbreviation || tenGodData?.id || '';
      }
    }

    // Get Ten God for stem
    let tenGod = null;
    if (isDayMaster) {
      tenGod = 'DM';
    } else if (stemId && mappings.ten_gods) {
      const tenGodData = mappings.ten_gods?.[dayMasterStem]?.[stemId];
      tenGod = tenGodData?.abbreviation || tenGodData?.id || null;
    }

    // Get badges
    const stemBadges = hsNode?.badges || [];
    const branchBadges = ebNode?.badges || [];

    return {
      label,
      stem,
      stemName: stemId,
      branch,
      branchName: branchId,
      stemKey: hsKey,
      branchKey: ebKey,
      hiddenStems,
      hiddenQi,
      tenGod,
      isDayMaster,
      isUnknown: !hsNode && !ebNode,
      qiPhase: hsNode?.qi_phase || ebNode?.qi_phase || null,
      stemTransformations: stemBadges.filter((b: any) => b.type === 'transformation'),
      branchTransformations: branchBadges.filter((b: any) => b.type === 'transformation'),
      stemCombinations: stemBadges.filter((b: any) => b.type === 'combination'),
      branchCombinations: branchBadges.filter((b: any) => b.type === 'combination'),
      stemNegatives: stemBadges.filter((b: any) =>
        ['clash', 'harm', 'punishment', 'destruction', 'stem_conflict'].includes(b.type)),
      branchNegatives: branchBadges.filter((b: any) =>
        ['clash', 'harm', 'punishment', 'destruction', 'stem_conflict'].includes(b.type)),
      branchWealthStorage: branchBadges.filter((b: any) => b.type === 'wealth_storage'),
    };
  };

  // Build natal pillars
  const natalPillars = useMemo(() => {
    const hour = buildPillar('hs_h', 'eb_h', t('natal.pillar_labels.hour')) || {
      label: t('natal.pillar_labels.hour'),
      stem: { chinese: '?', element: 'Unknown', color: '' },
      stemName: '?',
      branch: { chinese: '?', animal: '?', element: 'Unknown', color: '' },
      branchName: '?',
      hiddenStems: {},
      hiddenQi: {},
      tenGod: null,
      isDayMaster: false,
      isUnknown: true,
      stemTransformations: [],
      branchTransformations: [],
      stemCombinations: [],
      branchCombinations: [],
      stemNegatives: [],
      branchNegatives: [],
      branchWealthStorage: [],
    };
    const day = buildPillar('hs_d', 'eb_d', t('natal.pillar_labels.day'), true);
    const month = buildPillar('hs_m', 'eb_m', t('natal.pillar_labels.month'));
    const year = buildPillar('hs_y', 'eb_y', t('natal.pillar_labels.year'));

    return [hour, day, month, year].filter(Boolean) as any[];
  }, [chartData, t]);

  // Empty placeholder pillar for alignment
  const createEmptyPillar = (label: string) => ({
    label,
    stem: { chinese: '', element: 'Unknown', color: '' },
    stemName: '',
    branch: { chinese: '', animal: '', element: 'Unknown', color: '' },
    branchName: '',
    hiddenStems: {},
    hiddenQi: {},
    tenGod: null,
    isDayMaster: false,
    isUnknown: true,
    isEmpty: true,
    stemTransformations: [],
    branchTransformations: [],
    stemCombinations: [],
    branchCombinations: [],
    stemNegatives: [],
    branchNegatives: [],
    branchWealthStorage: [],
  });

  // Build aligned comparison row: Hourly | Daily | Monthly | Annual | 10-Yr Luck
  // Order matches natal: Hour | Day | Month | Year | (extra column)
  const alignedLuckPillars = useMemo(() => {
    // Hourly luck (aligns with Hour)
    let hourlyPillar = createEmptyPillar(t('comparison.pillar_labels.hourly'));
    if (chartData?.analysis_info?.has_hourly && chartData?.hs_hl && chartData?.eb_hl) {
      const pillar = buildPillar('hs_hl', 'eb_hl', t('comparison.pillar_labels.hourly')) as any;
      if (pillar) {
        pillar.isHourlyLuck = true;
        hourlyPillar = pillar;
      }
    }

    // Daily luck (aligns with Day)
    let dailyPillar = createEmptyPillar(t('comparison.pillar_labels.daily'));
    if (chartData?.analysis_info?.has_daily && chartData?.hs_dl && chartData?.eb_dl) {
      const pillar = buildPillar('hs_dl', 'eb_dl', t('comparison.pillar_labels.daily')) as any;
      if (pillar) {
        pillar.isDailyLuck = true;
        dailyPillar = pillar;
      }
    }

    // Monthly luck (aligns with Month)
    let monthlyPillar = createEmptyPillar(t('comparison.pillar_labels.monthly'));
    if (chartData?.analysis_info?.has_monthly && chartData?.hs_ml && chartData?.eb_ml) {
      const pillar = buildPillar('hs_ml', 'eb_ml', t('comparison.pillar_labels.monthly')) as any;
      if (pillar) {
        pillar.isMonthlyLuck = true;
        monthlyPillar = pillar;
      }
    }

    // Annual luck (aligns with Year)
    let annualPillar = createEmptyPillar(t('comparison.pillar_labels.annual'));
    if (chartData?.analysis_info?.year && chartData?.hs_yl && chartData?.eb_yl) {
      const pillar = buildPillar('hs_yl', 'eb_yl', t('comparison.pillar_labels.annual')) as any;
      if (pillar) {
        pillar.isAnnualLuck = true;
        pillar.year = chartData.analysis_info.year;
        annualPillar = pillar;
      }
    }

    // 10-Yr luck (rightmost column)
    let tenYrPillar = createEmptyPillar(t('comparison.pillar_labels.ten_year'));
    if (chartData?.analysis_info?.has_luck_pillar && chartData?.hs_10yl && chartData?.eb_10yl) {
      const pillar = buildPillar('hs_10yl', 'eb_10yl', t('comparison.pillar_labels.ten_year')) as any;
      if (pillar) {
        pillar.isLuckPillar = true;
        pillar.is10YrLuck = true;
        const misc = chartData.hs_10yl?.misc || chartData.eb_10yl?.misc;
        if (misc) {
          pillar.timing = {
            start_year: parseInt(misc.start_date?.split('-')[0] || '0'),
            end_year: parseInt(misc.end_date?.split('-')[0] || '0'),
            start_age: misc.start_age || 0,
            end_age: misc.end_age || 10,
          };
        }
        tenYrPillar = pillar;
      }
    }

    return [hourlyPillar, dailyPillar, monthlyPillar, annualPillar, tenYrPillar];
  }, [chartData, t]);

  // Build comparison date luck pillars (legacy - keep for backward compatibility)
  const luckPillars = useMemo(() => {
    const pillars: any[] = [];

    // Annual luck pillar
    if (chartData?.analysis_info?.year && chartData?.hs_yl && chartData?.eb_yl) {
      const pillar = buildPillar('hs_yl', 'eb_yl', 'Annual 年運') as any;
      if (pillar) {
        pillar.isAnnualLuck = true;
        pillar.year = chartData.analysis_info.year;
        pillars.push(pillar);
      }
    }

    // Monthly luck pillar
    if (chartData?.analysis_info?.has_monthly && chartData?.hs_ml && chartData?.eb_ml) {
      const pillar = buildPillar('hs_ml', 'eb_ml', 'Monthly 月運') as any;
      if (pillar) {
        pillar.isMonthlyLuck = true;
        pillars.push(pillar);
      }
    }

    // Daily luck pillar
    if (chartData?.analysis_info?.has_daily && chartData?.hs_dl && chartData?.eb_dl) {
      const pillar = buildPillar('hs_dl', 'eb_dl', 'Daily 日運') as any;
      if (pillar) {
        pillar.isDailyLuck = true;
        pillars.push(pillar);
      }
    }

    // Hourly luck pillar
    if (chartData?.analysis_info?.has_hourly && chartData?.hs_hl && chartData?.eb_hl) {
      const pillar = buildPillar('hs_hl', 'eb_hl', 'Hourly 時運') as any;
      if (pillar) {
        pillar.isHourlyLuck = true;
        pillars.push(pillar);
      }
    }

    return pillars;
  }, [chartData]);

  // Build talisman pillars
  const talismanPillars = useMemo(() => {
    const pillars: any[] = [];

    // Talisman Year
    if (chartData?.hs_ty || chartData?.eb_ty) {
      const pillar = buildPillar('hs_ty', 'eb_ty', t('talisman.pillar_labels.year')) as any;
      if (pillar) {
        pillar.isTalisman = true;
        pillar.isTalismanYear = true;
        pillars.push(pillar);
      }
    }

    // Talisman Month
    if (chartData?.hs_tm || chartData?.eb_tm) {
      const pillar = buildPillar('hs_tm', 'eb_tm', t('talisman.pillar_labels.month')) as any;
      if (pillar) {
        pillar.isTalisman = true;
        pillar.isTalismanMonth = true;
        pillars.push(pillar);
      }
    }

    // Talisman Day
    if (chartData?.hs_td || chartData?.eb_td) {
      const pillar = buildPillar('hs_td', 'eb_td', t('talisman.pillar_labels.day')) as any;
      if (pillar) {
        pillar.isTalisman = true;
        pillar.isTalismanDay = true;
        pillars.push(pillar);
      }
    }

    // Talisman Hour
    if (chartData?.hs_th || chartData?.eb_th) {
      const pillar = buildPillar('hs_th', 'eb_th', t('talisman.pillar_labels.hour')) as any;
      if (pillar) {
        pillar.isTalisman = true;
        pillar.isTalismanHour = true;
        pillars.push(pillar);
      }
    }

    return pillars;
  }, [chartData, t]);

  // Build location pillars (overseas or birthplace)
  const locationPillars = useMemo(() => {
    const pillars: any[] = [];

    // Overseas pillars (o1, o2) - blue border
    if (chartData?.hs_o1 || chartData?.eb_o1) {
      const pillar = buildPillar('hs_o1', 'eb_o1', t('location.pillar_labels.overseas_1')) as any;
      if (pillar) {
        pillar.isLocation = true;
        pillar.isOverseas = true;
        pillars.push(pillar);
      }
    }
    if (chartData?.hs_o2 || chartData?.eb_o2) {
      const pillar = buildPillar('hs_o2', 'eb_o2', t('location.pillar_labels.overseas_2')) as any;
      if (pillar) {
        pillar.isLocation = true;
        pillar.isOverseas = true;
        pillars.push(pillar);
      }
    }

    // Birthplace pillars (b1-b4) - amber border
    if (chartData?.hs_b1 || chartData?.eb_b1) {
      const pillar = buildPillar('hs_b1', 'eb_b1', t('location.pillar_labels.birthplace_1')) as any;
      if (pillar) {
        pillar.isLocation = true;
        pillar.isBirthplace = true;
        pillars.push(pillar);
      }
    }
    if (chartData?.hs_b2 || chartData?.eb_b2) {
      const pillar = buildPillar('hs_b2', 'eb_b2', t('location.pillar_labels.birthplace_2')) as any;
      if (pillar) {
        pillar.isLocation = true;
        pillar.isBirthplace = true;
        pillars.push(pillar);
      }
    }
    if (chartData?.hs_b3 || chartData?.eb_b3) {
      const pillar = buildPillar('hs_b3', 'eb_b3', t('location.pillar_labels.birthplace_3')) as any;
      if (pillar) {
        pillar.isLocation = true;
        pillar.isBirthplace = true;
        pillars.push(pillar);
      }
    }
    if (chartData?.hs_b4 || chartData?.eb_b4) {
      const pillar = buildPillar('hs_b4', 'eb_b4', t('location.pillar_labels.birthplace_4')) as any;
      if (pillar) {
        pillar.isLocation = true;
        pillar.isBirthplace = true;
        pillars.push(pillar);
      }
    }

    return pillars;
  }, [chartData, t]);

  // Filter pillars based on props
  const displayNatalPillars = showNatal ? natalPillars : [];

  // Use aligned luck pillars when showing comparison row (includes 10-yr luck at the end)
  const displayAlignedLuckPillars = (showLuck || show10YrLuck) ? alignedLuckPillars : [];

  const displayTalismanPillars = showTalisman ? talismanPillars : [];
  const displayLocationPillars = showLocation ? locationPillars : [];

  // Calculate cumulative indices for proper ordering
  const natalOffset = 0;
  const luckOffset = displayNatalPillars.length;
  const talismanOffset = luckOffset + displayAlignedLuckPillars.length;
  const locationOffset = talismanOffset + displayTalismanPillars.length;

  // Check if any pillars to display
  const hasPillars = displayNatalPillars.length > 0 || displayAlignedLuckPillars.length > 0 ||
    displayTalismanPillars.length > 0 || displayLocationPillars.length > 0;

  if (!hasPillars) return null;

  return (
    <div className="relative">
      <div className="relative w-full">
        {/* Heavenly Stems Row */}
        <div className="flex gap-0 items-center flex-wrap">
          {/* Natal Pillar Stems */}
          {displayNatalPillars.map((pillar, index) => (
            <PillarCard
              key={`stem-${index}`}
              pillar={pillar}
              type="stem"
              index={natalOffset + index}
              mappings={mappings}
              hoveredInteractionId={hoveredInteractionId}
              onHoverInteraction={setHoveredInteractionId}
            />
          ))}

          {/* Aligned Luck Pillar Stems: Hourly | Daily | Monthly | Annual | 10-Yr */}
          {displayAlignedLuckPillars.map((pillar, index) => (
            <PillarCard
              key={`luck-stem-${index}`}
              pillar={pillar}
              type="stem"
              index={luckOffset + index}
              mappings={mappings}
              isLuck
              isEmpty={pillar.isEmpty}
              hoveredInteractionId={hoveredInteractionId}
              onHoverInteraction={setHoveredInteractionId}
            />
          ))}

          {/* Divider before location pillars */}
          {displayAlignedLuckPillars.length > 0 && displayLocationPillars.length > 0 && (
            <div className={`luck-divider self-stretch bg-gradient-to-b from-transparent to-transparent opacity-70 ${
              displayLocationPillars[0]?.isOverseas ? 'via-blue-500' : 'via-amber-500'
            }`}></div>
          )}

          {/* Location Pillar Stems */}
          {displayLocationPillars.map((pillar, index) => (
            <PillarCard
              key={`location-stem-${index}`}
              pillar={pillar}
              type="stem"
              index={locationOffset + index}
              mappings={mappings}
              isLocation
              isOverseas={pillar.isOverseas}
              isBirthplace={pillar.isBirthplace}
              hoveredInteractionId={hoveredInteractionId}
              onHoverInteraction={setHoveredInteractionId}
            />
          ))}

          {/* Talisman Pillar Stems */}
          {displayTalismanPillars.map((pillar, index) => (
            <PillarCard
              key={`talisman-stem-${index}`}
              pillar={pillar}
              type="stem"
              index={talismanOffset + index}
              mappings={mappings}
              isTalisman
              hoveredInteractionId={hoveredInteractionId}
              onHoverInteraction={setHoveredInteractionId}
            />
          ))}
        </div>

        {/* Earthly Branches Row */}
        <div className="flex gap-0 overflow-visible items-stretch">
          {/* Natal Pillar Branches */}
          {displayNatalPillars.map((pillar, index) => (
            <PillarCard
              key={`branch-${index}`}
              pillar={pillar}
              type="branch"
              index={natalOffset + index}
              mappings={mappings}
              hoveredInteractionId={hoveredInteractionId}
              onHoverInteraction={setHoveredInteractionId}
            />
          ))}

          {/* Aligned Luck Pillar Branches: Hourly | Daily | Monthly | Annual | 10-Yr */}
          {displayAlignedLuckPillars.map((pillar, index) => (
            <PillarCard
              key={`luck-branch-${index}`}
              pillar={pillar}
              type="branch"
              index={luckOffset + index}
              mappings={mappings}
              isLuck
              isEmpty={pillar.isEmpty}
              hoveredInteractionId={hoveredInteractionId}
              onHoverInteraction={setHoveredInteractionId}
            />
          ))}

          {/* Divider before location pillars */}
          {displayAlignedLuckPillars.length > 0 && displayLocationPillars.length > 0 && (
            <div className={`luck-divider self-stretch bg-gradient-to-b from-transparent to-transparent opacity-70 ${
              displayLocationPillars[0]?.isOverseas ? 'via-blue-500' : 'via-amber-500'
            }`}></div>
          )}

          {/* Location Pillar Branches */}
          {displayLocationPillars.map((pillar, index) => (
            <PillarCard
              key={`location-branch-${index}`}
              pillar={pillar}
              type="branch"
              index={locationOffset + index}
              mappings={mappings}
              isLocation
              isOverseas={pillar.isOverseas}
              isBirthplace={pillar.isBirthplace}
              hoveredInteractionId={hoveredInteractionId}
              onHoverInteraction={setHoveredInteractionId}
            />
          ))}

          {/* Talisman Pillar Branches */}
          {displayTalismanPillars.map((pillar, index) => (
            <PillarCard
              key={`talisman-branch-${index}`}
              pillar={pillar}
              type="branch"
              index={talismanOffset + index}
              mappings={mappings}
              isTalisman
              hoveredInteractionId={hoveredInteractionId}
              onHoverInteraction={setHoveredInteractionId}
            />
          ))}
        </div>
      </div>
    </div>
  );
}
