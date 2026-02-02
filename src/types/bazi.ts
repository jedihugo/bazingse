// Qi score structure for each stem
export interface QiValue {
  [stemName: string]: number
}

// Base and post-interaction state for nodes
export interface NodeState {
  id: string
  qi: QiValue
}

// Node structure for heavenly stems and earthly branches
export interface BaziNode {
  base: NodeState
  interaction_ids: string[]
  post: NodeState
  transformed: boolean
  alive: boolean
  interacted: boolean
}

// Birth information
export interface BirthInfo {
  date: string
  time: string
  gender: string
}

// Element score structure
export interface ElementScores {
  [element: string]: number
}

// Daymaster analysis
export interface DaymasterAnalysis {
  daymaster: string
  daymaster_strength: number
  daymaster_percentage: number
  support_percentage: number
  drain_percentage: number
  chart_type: string
  element_relationships: {
    support: string[]
    drain: string[]
    neutral: string[]
  }
  favorable_elements: string[]
  unfavorable_elements: string[]
  useful_god: string
  explanation: string
}

// Interaction detail
export interface InteractionDetail {
  type: string
  pattern: string
  nodes: string[]
  effect?: string
  stage?: string
}

// Interactions structure
export interface Interactions {
  [category: string]: InteractionDetail[] | any
}

// Mapping structures
export interface HeavenlyStemMapping {
  id: string
  pinyin: string
  chinese: string
  english: string
  hex_color: string
}

export interface EarthlyBranchMapping {
  id: string
  chinese: string
  animal: string
  hex_color: string
}

export interface Mappings {
  heavenly_stems: { [key: string]: HeavenlyStemMapping }
  earthly_branches: { [key: string]: EarthlyBranchMapping }
  ten_gods: { [key: string]: { [key: string]: string } }
}

// Luck pillar timing information
export interface LuckPillarTiming {
  start_datetime: string
  end_datetime: string
  start_age: number
  end_age: number
  start_year: number
  start_month: number
  start_day: number
  start_hour: number
  end_year: number
  end_month: number
  end_day: number
  end_hour: number
  duration_days: number
  duration_years: number
}

// Luck pillar from API response
export interface LuckPillarData {
  index: number
  pillar: string
  hs_element: string
  eb_animal: string
  ten_god_hs: string
  ten_god_hidden: { [key: string]: string }
  timing: LuckPillarTiming
  is_current: boolean
}

// Luck pillar response from /generate_10lp_chart
export interface LuckPillarResponse {
  luck_pillars: LuckPillarData[]
  current_luck_pillar: LuckPillarData | null
  luck_calculation_details: any
}

// Main natal chart response structure
export interface NatalChartResponse {
  birth_info: BirthInfo
  hs_y: BaziNode  // Year heavenly stem
  eb_y: BaziNode  // Year earthly branch
  hs_m: BaziNode  // Month heavenly stem
  eb_m: BaziNode  // Month earthly branch
  hs_d: BaziNode  // Day heavenly stem
  eb_d: BaziNode  // Day earthly branch
  hs_h?: BaziNode  // Hour heavenly stem (optional if hour unknown)
  eb_h?: BaziNode  // Hour earthly branch (optional if hour unknown)
  base_element_score: ElementScores
  natal_element_score: ElementScores
  post_element_score: ElementScores
  interactions: Interactions
  daymaster_analysis: DaymasterAnalysis
  mappings: Mappings
  // Optional luck pillar data (for integrated display)
  current_luck_pillar?: LuckPillarData
  // Unit Story tracker (video game style qi tracking)
  unit_tracker?: UnitTrackerResponse
}

// Legacy structures for backward compatibility
export interface TenGodHidden {
  [key: string]: string
}

export interface Pillar {
  pillar: string
  hs_element: string
  eb_animal: string
  ten_god_hs: string
  ten_god_hidden: TenGodHidden
}

export interface DailyPillar extends Pillar {
  day: number
}

export interface MonthlyPillar extends Pillar {
  month: number
  chinese_year?: string
  note?: string
  daily_pillars?: DailyPillar[]
}

export interface AnnualPillar extends Pillar {
  year: number
  monthly_pillars?: MonthlyPillar[]
}

export interface LuckPillar extends Pillar {
  year: string
  age: string
  index?: number
  annual_pillars?: AnnualPillar[]
}

export interface NatalChart {
  year_pillar: Pillar
  month_pillar: Pillar
  day_pillar: Pillar
  hour_pillar: Pillar
}

export interface BaZiData {
  natal_chart: NatalChart
  luck_pillars: LuckPillar[]
  selected_luck_pillar: LuckPillar
}

export type ElementType = 'Fire' | 'Earth' | 'Metal' | 'Water' | 'Wood'

// ============= PRIMARY QI & HIDDEN STEM TYPES =============
// BaZi Terminology:
// - Primary Qi (本氣): Index 0 - the main/dominant energy of an Earthly Branch - NOT hidden
// - Hidden Stems (藏干): Index 1+ - secondary/tertiary energies that ARE actually hidden within

// Primary Qi (本氣) - main energy at index 0
export interface PrimaryQi {
  stem: string           // Stem ID (e.g., "Jia", "Bing")
  score: number          // Qi score value
  weight: number         // Percentage for display width (proportional to total qi)
  god?: string           // Ten God abbreviation
  color?: string         // Hex color for display
}

// Hidden Stem (藏干) - secondary/tertiary at index 1+
export interface HiddenStem {
  stem: string           // Stem ID (e.g., "Bing", "Wu")
  score: number          // Qi score value
  weight: number         // Percentage for display width (proportional to total qi)
  god?: string           // Ten God abbreviation
  color?: string         // Hex color for display
}

// Combined qi display structure for a branch
export interface BranchQiDisplay {
  primaryQi: PrimaryQi | null      // Index 0 - main energy
  hiddenStems: HiddenStem[]        // Index 1+ - hidden energies
  totalQi: number                   // Sum of all qi for percentage calculations
}

// ============= UNIT TRACKER TYPES =============
// Tracks qi units as "video game characters" throughout BaZi calculation

// Single interaction event for a qi unit
export interface UnitEvent {
  phase: string
  phase_step: number
  event_type: 'controlled' | 'controlling' | 'produced' | 'producing'
  partner_stem: string
  partner_node: string
  partner_ten_god: string
  partner_ten_god_english: string
  qi_before: number
  qi_change: number
  qi_after: number
  description: string
  // Distance penalty fields
  distance: number
  distance_multiplier: number
  math_formula: string
}

// Complete journey of one qi unit (stem) in a specific node
export interface UnitStory {
  stem: string
  stem_chinese: string
  element: string
  polarity: string
  ten_god: string
  ten_god_id: string
  ten_god_english: string
  home_node: string
  initial_qi: number
  final_qi: number
  total_gained: number
  total_lost: number
  events: UnitEvent[]
  narrative: string
}

// Timeline event (can be registration, interaction, adjustment, seasonal, combination, or conflict)
export interface TimelineEvent {
  type: 'registration' | 'interaction' | 'adjustment' | 'seasonal' | 'combination' | 'conflict'
  step?: number
  node?: string
  stem?: string
  stem_chinese?: string
  ten_god?: string
  ten_god_english?: string
  qi?: number
  qi_before?: number
  qi_change?: number
  qi_after?: number
  description?: string
  interaction_type?: string
  // Distance penalty fields
  distance?: number
  distance_multiplier?: number
  math_formula?: string
  // Seasonal adjustment fields
  element?: string
  seasonal_state?: string
  multiplier?: number
  month_branch?: string
  // Combination fields
  combination_type?: string
  pattern?: string
  nodes?: string[]
  stems?: string[]
  boost_amount?: number
  is_transformed?: boolean
  // Conflict fields
  conflict_type?: string
  severity?: string
  aggressor?: {
    node: string
    stem: string
    stem_chinese: string
    ten_god: string
    ten_god_english: string
    damage: number
  }
  victim?: {
    node: string
    stem: string
    stem_chinese: string
    ten_god: string
    ten_god_english: string
    damage: number
  }
  source?: {
    node: string
    stem?: string
    stem_chinese?: string
    ten_god?: string
    ten_god_english?: string
    element?: string  // For cross-pillar interactions
    qi_before: number
    qi_change: number
    qi_after: number
  }
  target?: {
    node: string
    stem?: string
    stem_chinese?: string
    ten_god?: string
    ten_god_english?: string
    element?: string  // For cross-pillar interactions
    qi_before: number
    qi_change: number
    qi_after: number
  }
}

// Timeline phase containing events
export interface TimelinePhase {
  phase: string
  phase_label: string
  events: TimelineEvent[]
  event_count: number
  running_total: number
}

// Main unit tracker response
export interface UnitTrackerResponse {
  day_master: string
  day_master_chinese: string
  timeline: TimelinePhase[]
  unit_stories: { [nodeId: string]: UnitStory[] }
  summary: {
    total_units: number
    total_phases: number
    total_interactions: number
    final_total_qi: number
  }
}