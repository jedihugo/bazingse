import type { ElementType } from '~/types/bazi'

// Yang stems (used for polarity detection)
const yangStems = ['Jia', 'Bing', 'Wu', 'Geng', 'Ren']

// Yang branches (used for polarity detection)
const yangBranches = ['Zi', 'Yin', 'Chen', 'Wu', 'Shen', 'Xu']

// NOTE: Element colors should come from API mappings.elements
// These are kept for legacy compatibility but should be phased out.
// Use API: mappings.elements[element].hex_color instead

// Helper to get element hex color from API mappings
export function getElementHexColorFromMappings(element: ElementType, mappings: any, polarity?: 'Yang' | 'Yin'): string {
  const elementData = mappings?.elements?.[element]
  if (!elementData) return '#6b7280' // gray fallback

  if (polarity === 'Yang' && elementData.hex_color_yang) {
    return elementData.hex_color_yang
  }
  if (polarity === 'Yin' && elementData.hex_color_yin) {
    return elementData.hex_color_yin
  }
  return elementData.hex_color || '#6b7280'
}

// Legacy Tailwind class mappings - DEPRECATED, use API hex colors instead
// Kept for backward compatibility during migration
export const elementColorsYang: Record<ElementType, string> = {
  Fire: 'text-red-600',
  Earth: 'text-yellow-700',
  Metal: 'text-gray-600',
  Water: 'text-blue-700',
  Wood: 'text-green-700'
}

export const elementColorsYin: Record<ElementType, string> = {
  Fire: 'text-red-400',
  Earth: 'text-yellow-600',
  Metal: 'text-gray-400',
  Water: 'text-blue-500',
  Wood: 'text-green-500'
}

// Legacy color mapping (for backward compatibility)
export const elementColors: Record<ElementType, string> = elementColorsYang

// Ten Gods abbreviation to full name mapping
export const tenGodNames: Record<string, { en: string, zh: string }> = {
  'RW': { en: 'Rival/Wealth', zh: '比劫' },
  'DR': { en: 'Direct Resource', zh: '正印' },
  'HO': { en: 'Hurting Officer', zh: '傷官' },
  'EG': { en: 'Eating God', zh: '食神' },
  'DO': { en: 'Direct Officer', zh: '正官' },
  '7K': { en: '7 Killings', zh: '七殺' },
  'IW': { en: 'Indirect Wealth', zh: '偏財' },
  'IR': { en: 'Indirect Resource', zh: '偏印' },
  'F': { en: 'Friend', zh: '比肩' },
  'DW': { en: 'Direct Wealth', zh: '正財' },
  'Day Master': { en: 'Day Master', zh: '日主' },
  'DM': { en: 'Day Master', zh: '日主' }
}

// Chinese stem/branch mappings
export const stemMappings: Record<string, string> = {
  'Jia': '甲', 'Yi': '乙', 'Bing': '丙', 'Ding': '丁', 'Wu': '戊',
  'Ji': '己', 'Geng': '庚', 'Xin': '辛', 'Ren': '壬', 'Gui': '癸'
}

export const branchMappings: Record<string, string> = {
  'Zi': '子', 'Chou': '丑', 'Yin': '寅', 'Mao': '卯', 'Chen': '辰', 'Si': '巳',
  'Wu': '午', 'Wei': '未', 'Shen': '申', 'You': '酉', 'Xu': '戌', 'Hai': '亥'
}

// Earthly branch element associations
export const branchElements: Record<string, ElementType> = {
  'Zi': 'Water',    // 子 Rat
  'Chou': 'Earth',  // 丑 Ox
  'Yin': 'Wood',    // 寅 Tiger
  'Mao': 'Wood',    // 卯 Rabbit
  'Chen': 'Earth',  // 辰 Dragon
  'Si': 'Fire',     // 巳 Snake
  'Wu': 'Fire',     // 午 Horse
  'Wei': 'Earth',   // 未 Goat
  'Shen': 'Metal',  // 申 Monkey
  'You': 'Metal',   // 酉 Rooster
  'Xu': 'Earth',    // 戌 Dog
  'Hai': 'Water'    // 亥 Pig
}

// Parse pillar string (e.g., "Bing Yin" -> { stem: "丙", branch: "寅" })
export function parsePillar(pillarString: string): { stem: string, branch: string } {
  const [stemEn, branchEn] = pillarString.split(' ')
  return {
    stem: stemMappings[stemEn] || stemEn,
    branch: branchMappings[branchEn] || branchEn
  }
}

// Get element hex color by stem - uses API mappings
export function getElementHexByStem(stemEnglish: string, mappings: any): string {
  const stemData = mappings?.heavenly_stems?.[stemEnglish]
  return stemData?.hex_color || '#6b7280'
}

// Get element hex color by branch - uses API mappings
export function getElementHexByBranch(branchEnglish: string, mappings: any): string {
  const branchData = mappings?.earthly_branches?.[branchEnglish]
  return branchData?.hex_color || '#6b7280'
}

// Get element color class based on stem (Yang/Yin) - DEPRECATED, use getElementHexByStem
export function getElementColorByStem(element: ElementType, stemEnglish: string): string {
  const isYang = yangStems.includes(stemEnglish)
  const colors = isYang ? elementColorsYang : elementColorsYin
  return colors[element] || 'text-gray-600'
}

// Get element color class based on branch (Yang/Yin) - DEPRECATED, use getElementHexByBranch
export function getElementColorByBranch(branchEnglish: string): string {
  const element = branchElements[branchEnglish]
  if (!element) return 'text-gray-600'

  const isYang = yangBranches.includes(branchEnglish)
  const colors = isYang ? elementColorsYang : elementColorsYin
  return colors[element] || 'text-gray-600'
}

// Legacy function for backward compatibility - DEPRECATED, use API mappings
export function getElementColor(element: ElementType): string {
  return elementColors[element] || 'text-gray-600'
}

// Get ten god display names
export function getTenGodName(abbreviation: string, lang: 'en' | 'zh' = 'zh'): string {
  return tenGodNames[abbreviation]?.[lang] || abbreviation
}

// Get element from Chinese stem character
export function getElementFromChineseStem(stem: string): ElementType | null {
  const stemElementMap: Record<string, ElementType> = {
    '甲': 'Wood', '乙': 'Wood',
    '丙': 'Fire', '丁': 'Fire',
    '戊': 'Earth', '己': 'Earth',
    '庚': 'Metal', '辛': 'Metal',
    '壬': 'Water', '癸': 'Water'
  }
  return stemElementMap[stem] || null
}

// Get element from Chinese branch character
export function getElementFromChineseBranch(branch: string): ElementType | null {
  const branchElementMap: Record<string, ElementType> = {
    '寅': 'Wood', '卯': 'Wood',
    '巳': 'Fire', '午': 'Fire',
    '辰': 'Earth', '戌': 'Earth', '丑': 'Earth', '未': 'Earth',
    '申': 'Metal', '酉': 'Metal',
    '子': 'Water', '亥': 'Water'
  }
  return branchElementMap[branch] || null
}

// Get element color for Chinese stem character
export function getElementColorFromChineseStem(stem: string): string {
  const element = getElementFromChineseStem(stem)
  if (!element) return 'text-gray-600'
  
  const yangStems = ['甲', '丙', '戊', '庚', '壬']
  const isYang = yangStems.includes(stem)
  const colors = isYang ? elementColorsYang : elementColorsYin
  return colors[element] || 'text-gray-600'
}

// Get element color for Chinese branch character
export function getElementColorFromChineseBranch(branch: string): string {
  const element = getElementFromChineseBranch(branch)
  if (!element) return 'text-gray-600'
  
  const yangBranches = ['子', '寅', '辰', '午', '申', '戌']
  const isYang = yangBranches.includes(branch)
  const colors = isYang ? elementColorsYang : elementColorsYin
  return colors[element] || 'text-gray-600'
}