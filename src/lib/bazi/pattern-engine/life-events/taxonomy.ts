
// =============================================================================
// LIFE EVENT TAXONOMY
// =============================================================================
// Comprehensive classification of life events for BaZi correlation analysis.
// Every event type is mapped to affected TCM organs, elements, and pillars.
// Ported from api/library/pattern_engine/life_events/taxonomy.py
// =============================================================================

// =============================================================================
// DOMAIN DEFINITIONS
// =============================================================================

export enum LifeDomain {
  HEALTH = "health",
  WEALTH = "wealth",
  CAREER = "career",
  RELATIONSHIP = "relationship",
  EDUCATION = "education",
  FAMILY = "family",
  LEGAL = "legal",
  TRAVEL = "travel",
}

export enum Sentiment {
  POSITIVE = "positive",
  NEGATIVE = "negative",
  NEUTRAL = "neutral",
  CONDITIONAL = "conditional",
}

export enum Severity {
  MINOR = "minor",
  MODERATE = "moderate",
  MAJOR = "major",
  CRITICAL = "critical",
}

// =============================================================================
// TCM ORGAN MAPPING
// =============================================================================

export interface TCMOrganSystem {
  readonly element: string;
  readonly zang_organ: string;
  readonly fu_organ: string;
  readonly chinese_zang: string;
  readonly chinese_fu: string;
  readonly body_parts: ReadonlySet<string>;
  readonly emotion: string;
  readonly season: string;
  readonly color: string;
}

export const TCM_ORGANS: Record<string, TCMOrganSystem> = {
  Wood: {
    element: "Wood",
    zang_organ: "Liver",
    fu_organ: "Gallbladder",
    chinese_zang: "肝",
    chinese_fu: "膽",
    body_parts: new Set(["eyes", "tendons", "nails", "sinews"]),
    emotion: "anger",
    season: "Spring",
    color: "green",
  },
  Fire: {
    element: "Fire",
    zang_organ: "Heart",
    fu_organ: "Small Intestine",
    chinese_zang: "心",
    chinese_fu: "小腸",
    body_parts: new Set(["tongue", "blood_vessels", "complexion", "sweat"]),
    emotion: "joy/anxiety",
    season: "Summer",
    color: "red",
  },
  Earth: {
    element: "Earth",
    zang_organ: "Spleen",
    fu_organ: "Stomach",
    chinese_zang: "脾",
    chinese_fu: "胃",
    body_parts: new Set(["muscles", "mouth", "lips", "flesh"]),
    emotion: "worry",
    season: "Late Summer",
    color: "yellow",
  },
  Metal: {
    element: "Metal",
    zang_organ: "Lungs",
    fu_organ: "Large Intestine",
    chinese_zang: "肺",
    chinese_fu: "大腸",
    body_parts: new Set(["skin", "nose", "body_hair", "pores"]),
    emotion: "grief",
    season: "Autumn",
    color: "white",
  },
  Water: {
    element: "Water",
    zang_organ: "Kidneys",
    fu_organ: "Bladder",
    chinese_zang: "腎",
    chinese_fu: "膀胱",
    body_parts: new Set(["bones", "ears", "head_hair", "marrow", "brain"]),
    emotion: "fear",
    season: "Winter",
    color: "black",
  },
};


// =============================================================================
// EVENT TYPE DEFINITIONS
// =============================================================================

export interface EventType {
  readonly id: string;
  readonly domain: LifeDomain;
  readonly name: string;
  readonly chinese_name: string;
  readonly default_sentiment: Sentiment;
  readonly severity_range: ReadonlySet<Severity>;
  readonly primary_elements: ReadonlySet<string>;
  readonly secondary_elements: ReadonlySet<string>;
  readonly pillar_weights: Record<string, number>;
  readonly tcm_organs: ReadonlySet<string>;
  readonly common_patterns: ReadonlySet<string>;
  readonly description: string;
}


// =============================================================================
// HEALTH EVENTS
// =============================================================================

export const HEALTH_EVENTS: Record<string, EventType> = {
  illness_major: {
    id: "illness_major",
    domain: LifeDomain.HEALTH,
    name: "Major Illness",
    chinese_name: "大病",
    default_sentiment: Sentiment.NEGATIVE,
    severity_range: new Set([Severity.MAJOR, Severity.CRITICAL]),
    primary_elements: new Set(["Fire", "Water"]),
    secondary_elements: new Set(),
    tcm_organs: new Set(["Heart", "Kidneys", "Liver"]),
    pillar_weights: { day: 1.5, month: 1.2, year: 1.0, hour: 0.8 },
    common_patterns: new Set([
      "PUNISHMENT~Yin-Si-Shen~shi_xing",
      "CLASH~Zi-Wu~opposite",
      "STEM_CONFLICT~Bing-Ren~",
    ]),
    description: "Severe illness requiring medical intervention",
  },
  illness_minor: {
    id: "illness_minor",
    domain: LifeDomain.HEALTH,
    name: "Minor Illness",
    chinese_name: "小病",
    default_sentiment: Sentiment.NEGATIVE,
    severity_range: new Set([Severity.MINOR, Severity.MODERATE]),
    primary_elements: new Set(["Metal", "Earth"]),
    secondary_elements: new Set(),
    tcm_organs: new Set(["Lungs", "Spleen"]),
    pillar_weights: { day: 1.3, month: 1.1, year: 0.9, hour: 0.9 },
    common_patterns: new Set(),
    description: "Minor health issues, easily recoverable",
  },
  injury_accident: {
    id: "injury_accident",
    domain: LifeDomain.HEALTH,
    name: "Injury/Accident",
    chinese_name: "意外傷害",
    default_sentiment: Sentiment.NEGATIVE,
    severity_range: new Set([Severity.MINOR, Severity.MODERATE, Severity.MAJOR]),
    primary_elements: new Set(["Metal", "Wood"]),
    secondary_elements: new Set(),
    tcm_organs: new Set(["Liver", "Gallbladder"]),
    pillar_weights: { day: 1.4, year: 1.1, month: 1.0, hour: 1.0 },
    common_patterns: new Set([
      "CLASH~Yin-Shen~opposite",
      "PUNISHMENT~Yin-Si-Shen~shi_xing",
      "STEM_CONFLICT~Jia-Geng~",
    ]),
    description: "Physical injury from accident or trauma",
  },
  surgery: {
    id: "surgery",
    domain: LifeDomain.HEALTH,
    name: "Surgery",
    chinese_name: "手術",
    default_sentiment: Sentiment.CONDITIONAL,
    severity_range: new Set([Severity.MODERATE, Severity.MAJOR, Severity.CRITICAL]),
    primary_elements: new Set(["Metal"]),
    secondary_elements: new Set(),
    tcm_organs: new Set(["Lungs", "Large Intestine"]),
    pillar_weights: { day: 1.5, month: 1.2, year: 0.9, hour: 0.9 },
    common_patterns: new Set([
      "STEM_CONFLICT~Jia-Geng~",
      "STEM_CONFLICT~Bing-Geng~",
    ]),
    description: "Surgical procedure (can be positive if successful)",
  },
  recovery: {
    id: "recovery",
    domain: LifeDomain.HEALTH,
    name: "Recovery",
    chinese_name: "康復",
    default_sentiment: Sentiment.POSITIVE,
    severity_range: new Set([Severity.MINOR, Severity.MODERATE, Severity.MAJOR]),
    primary_elements: new Set(["Wood", "Water"]),
    secondary_elements: new Set(),
    tcm_organs: new Set(["Kidneys", "Liver"]),
    pillar_weights: { day: 1.3, month: 1.1, year: 1.0, hour: 1.0 },
    common_patterns: new Set([
      "SIX_HARMONIES~Yin-Hai~Wood",
      "STEM_COMBINATION~Ding-Ren~Wood",
    ]),
    description: "Recovery from illness or injury",
  },
  mental_health: {
    id: "mental_health",
    domain: LifeDomain.HEALTH,
    name: "Mental Health Event",
    chinese_name: "心理健康",
    default_sentiment: Sentiment.NEGATIVE,
    severity_range: new Set([Severity.MODERATE, Severity.MAJOR, Severity.CRITICAL]),
    primary_elements: new Set(["Fire", "Water"]),
    secondary_elements: new Set(),
    tcm_organs: new Set(["Heart", "Kidneys"]),
    pillar_weights: { day: 1.6, hour: 1.2, month: 1.0, year: 0.8 },
    common_patterns: new Set([
      "CLASH~Zi-Wu~opposite",
      "STEM_CONFLICT~Bing-Ren~",
      "PUNISHMENT~Chen-Chen~zi_xing",
    ]),
    description: "Anxiety, depression, or other mental health challenges",
  },
  diagnosis: {
    id: "diagnosis",
    domain: LifeDomain.HEALTH,
    name: "Medical Diagnosis",
    chinese_name: "診斷",
    default_sentiment: Sentiment.NEUTRAL,
    severity_range: new Set([Severity.MINOR, Severity.MODERATE, Severity.MAJOR]),
    primary_elements: new Set(["Metal", "Water"]),
    secondary_elements: new Set(),
    tcm_organs: new Set(["Lungs", "Kidneys"]),
    pillar_weights: { day: 1.3, month: 1.2, year: 1.0, hour: 0.9 },
    common_patterns: new Set(),
    description: "Receiving a medical diagnosis (neutral - depends on outcome)",
  },
  seizure_neurological: {
    id: "seizure_neurological",
    domain: LifeDomain.HEALTH,
    name: "Seizure/Neurological Event",
    chinese_name: "癲癇/神經",
    default_sentiment: Sentiment.NEGATIVE,
    severity_range: new Set([Severity.MODERATE, Severity.MAJOR, Severity.CRITICAL]),
    primary_elements: new Set(["Fire", "Water", "Wood"]),
    secondary_elements: new Set(),
    tcm_organs: new Set(["Heart", "Liver", "Kidneys"]),
    pillar_weights: { day: 1.5, hour: 1.3, month: 1.1, year: 0.9 },
    common_patterns: new Set([
      "PUNISHMENT~Yin-Si-Shen~shi_xing",
      "CLASH~Zi-Wu~opposite",
      "STEM_CONFLICT~Bing-Ren~",
    ]),
    description: "Epileptic seizure or other neurological event - Fire/Water imbalance affecting Heart/Brain",
  },
};


// =============================================================================
// WEALTH EVENTS
// =============================================================================

export const WEALTH_EVENTS: Record<string, EventType> = {
  income_increase: {
    id: "income_increase",
    domain: LifeDomain.WEALTH,
    name: "Income Increase",
    chinese_name: "收入增加",
    default_sentiment: Sentiment.POSITIVE,
    severity_range: new Set([Severity.MINOR, Severity.MODERATE, Severity.MAJOR]),
    primary_elements: new Set(["Metal", "Earth"]),
    secondary_elements: new Set(),
    tcm_organs: new Set(),
    pillar_weights: { month: 1.4, day: 1.2, year: 1.0, hour: 0.8 },
    common_patterns: new Set([
      "SIX_HARMONIES~Chen-You~Metal",
      "STEM_COMBINATION~Yi-Geng~Metal",
    ]),
    description: "Salary raise, bonus, or income growth",
  },
  income_decrease: {
    id: "income_decrease",
    domain: LifeDomain.WEALTH,
    name: "Income Decrease",
    chinese_name: "收入減少",
    default_sentiment: Sentiment.NEGATIVE,
    severity_range: new Set([Severity.MINOR, Severity.MODERATE, Severity.MAJOR]),
    primary_elements: new Set(["Metal", "Fire"]),
    secondary_elements: new Set(),
    tcm_organs: new Set(),
    pillar_weights: { month: 1.4, day: 1.2, year: 1.0, hour: 0.8 },
    common_patterns: new Set([
      "STEM_CONFLICT~Bing-Geng~",
      "CLASH~Mao-You~opposite",
    ]),
    description: "Salary cut or income loss",
  },
  investment_gain: {
    id: "investment_gain",
    domain: LifeDomain.WEALTH,
    name: "Investment Gain",
    chinese_name: "投資獲利",
    default_sentiment: Sentiment.POSITIVE,
    severity_range: new Set([Severity.MINOR, Severity.MODERATE, Severity.MAJOR]),
    primary_elements: new Set(["Metal", "Water"]),
    secondary_elements: new Set(),
    tcm_organs: new Set(),
    pillar_weights: { month: 1.3, year: 1.2, day: 1.1, hour: 0.9 },
    common_patterns: new Set(),
    description: "Profit from investments",
  },
  investment_loss: {
    id: "investment_loss",
    domain: LifeDomain.WEALTH,
    name: "Investment Loss",
    chinese_name: "投資虧損",
    default_sentiment: Sentiment.NEGATIVE,
    severity_range: new Set([Severity.MINOR, Severity.MODERATE, Severity.MAJOR, Severity.CRITICAL]),
    primary_elements: new Set(["Metal", "Fire"]),
    secondary_elements: new Set(),
    tcm_organs: new Set(),
    pillar_weights: { month: 1.3, year: 1.2, day: 1.1, hour: 0.9 },
    common_patterns: new Set([
      "STEM_CONFLICT~Bing-Geng~",
      "DESTRUCTION~Wei-Xu~",
    ]),
    description: "Loss from investments",
  },
  property_purchase: {
    id: "property_purchase",
    domain: LifeDomain.WEALTH,
    name: "Property Purchase",
    chinese_name: "購置房產",
    default_sentiment: Sentiment.POSITIVE,
    severity_range: new Set([Severity.MODERATE, Severity.MAJOR]),
    primary_elements: new Set(["Earth"]),
    secondary_elements: new Set(),
    tcm_organs: new Set(),
    pillar_weights: { year: 1.4, month: 1.2, day: 1.0, hour: 0.8 },
    common_patterns: new Set([
      "SIX_HARMONIES~Zi-Chou~Earth",
      "STEM_COMBINATION~Jia-Ji~Earth",
    ]),
    description: "Buying real estate or property",
  },
  property_sale: {
    id: "property_sale",
    domain: LifeDomain.WEALTH,
    name: "Property Sale",
    chinese_name: "出售房產",
    default_sentiment: Sentiment.CONDITIONAL,
    severity_range: new Set([Severity.MODERATE, Severity.MAJOR]),
    primary_elements: new Set(["Earth", "Metal"]),
    secondary_elements: new Set(),
    tcm_organs: new Set(),
    pillar_weights: { year: 1.3, month: 1.2, day: 1.0, hour: 0.8 },
    common_patterns: new Set(),
    description: "Selling real estate or property",
  },
  windfall: {
    id: "windfall",
    domain: LifeDomain.WEALTH,
    name: "Windfall",
    chinese_name: "橫財",
    default_sentiment: Sentiment.POSITIVE,
    severity_range: new Set([Severity.MODERATE, Severity.MAJOR]),
    primary_elements: new Set(["Water", "Metal"]),
    secondary_elements: new Set(),
    tcm_organs: new Set(),
    pillar_weights: { hour: 1.3, day: 1.2, month: 1.0, year: 0.9 },
    common_patterns: new Set(),
    description: "Unexpected financial gain (lottery, inheritance, etc.)",
  },
  bankruptcy: {
    id: "bankruptcy",
    domain: LifeDomain.WEALTH,
    name: "Bankruptcy",
    chinese_name: "破產",
    default_sentiment: Sentiment.NEGATIVE,
    severity_range: new Set([Severity.CRITICAL]),
    primary_elements: new Set(["Metal", "Fire"]),
    secondary_elements: new Set(),
    tcm_organs: new Set(),
    pillar_weights: { month: 1.5, year: 1.3, day: 1.2, hour: 0.8 },
    common_patterns: new Set([
      "STEM_CONFLICT~Bing-Geng~",
      "CLASH~Chen-Xu~same",
    ]),
    description: "Financial ruin or bankruptcy",
  },
};


// =============================================================================
// CAREER EVENTS
// =============================================================================

export const CAREER_EVENTS: Record<string, EventType> = {
  job_new: {
    id: "job_new",
    domain: LifeDomain.CAREER,
    name: "New Job",
    chinese_name: "新工作",
    default_sentiment: Sentiment.POSITIVE,
    severity_range: new Set([Severity.MODERATE, Severity.MAJOR]),
    primary_elements: new Set(["Wood", "Fire"]),
    secondary_elements: new Set(),
    tcm_organs: new Set(),
    pillar_weights: { month: 1.5, day: 1.2, year: 1.0, hour: 0.8 },
    common_patterns: new Set([
      "THREE_MEETINGS~Yin-Mao-Chen~Wood",
      "STEM_COMBINATION~Ding-Ren~Wood",
    ]),
    description: "Starting a new job or position",
  },
  job_loss: {
    id: "job_loss",
    domain: LifeDomain.CAREER,
    name: "Job Loss",
    chinese_name: "失業",
    default_sentiment: Sentiment.NEGATIVE,
    severity_range: new Set([Severity.MODERATE, Severity.MAJOR]),
    primary_elements: new Set(["Metal", "Earth"]),
    secondary_elements: new Set(),
    tcm_organs: new Set(),
    pillar_weights: { month: 1.5, day: 1.2, year: 1.0, hour: 0.8 },
    common_patterns: new Set([
      "CLASH~Yin-Shen~opposite",
      "PUNISHMENT~Yin-Si-Shen~shi_xing",
    ]),
    description: "Losing employment",
  },
  promotion: {
    id: "promotion",
    domain: LifeDomain.CAREER,
    name: "Promotion",
    chinese_name: "升職",
    default_sentiment: Sentiment.POSITIVE,
    severity_range: new Set([Severity.MODERATE, Severity.MAJOR]),
    primary_elements: new Set(["Fire", "Wood"]),
    secondary_elements: new Set(),
    tcm_organs: new Set(),
    pillar_weights: { month: 1.5, day: 1.2, year: 1.1, hour: 0.9 },
    common_patterns: new Set([
      "THREE_MEETINGS~Si-Wu-Wei~Fire",
      "STEM_COMBINATION~Wu-Gui~Fire",
    ]),
    description: "Career advancement or promotion",
  },
  demotion: {
    id: "demotion",
    domain: LifeDomain.CAREER,
    name: "Demotion",
    chinese_name: "降職",
    default_sentiment: Sentiment.NEGATIVE,
    severity_range: new Set([Severity.MODERATE, Severity.MAJOR]),
    primary_elements: new Set(["Fire", "Water"]),
    secondary_elements: new Set(),
    tcm_organs: new Set(),
    pillar_weights: { month: 1.5, day: 1.2, year: 1.0, hour: 0.8 },
    common_patterns: new Set([
      "STEM_CONFLICT~Bing-Ren~",
      "HARM~Chou-Wu~",
    ]),
    description: "Reduction in position or status",
  },
  business_start: {
    id: "business_start",
    domain: LifeDomain.CAREER,
    name: "Start Business",
    chinese_name: "創業",
    default_sentiment: Sentiment.POSITIVE,
    severity_range: new Set([Severity.MAJOR]),
    primary_elements: new Set(["Wood", "Fire"]),
    secondary_elements: new Set(),
    tcm_organs: new Set(),
    pillar_weights: { day: 1.4, month: 1.3, year: 1.1, hour: 1.0 },
    common_patterns: new Set(),
    description: "Starting a new business venture",
  },
  business_close: {
    id: "business_close",
    domain: LifeDomain.CAREER,
    name: "Close Business",
    chinese_name: "結束經營",
    default_sentiment: Sentiment.NEGATIVE,
    severity_range: new Set([Severity.MAJOR]),
    primary_elements: new Set(["Metal", "Fire"]),
    secondary_elements: new Set(),
    tcm_organs: new Set(),
    pillar_weights: { day: 1.4, month: 1.3, year: 1.1, hour: 1.0 },
    common_patterns: new Set(),
    description: "Closing or failing a business",
  },
  recognition: {
    id: "recognition",
    domain: LifeDomain.CAREER,
    name: "Recognition/Award",
    chinese_name: "表彰",
    default_sentiment: Sentiment.POSITIVE,
    severity_range: new Set([Severity.MINOR, Severity.MODERATE, Severity.MAJOR]),
    primary_elements: new Set(["Fire"]),
    secondary_elements: new Set(),
    tcm_organs: new Set(),
    pillar_weights: { month: 1.4, day: 1.2, year: 1.1, hour: 0.9 },
    common_patterns: new Set([
      "THREE_MEETINGS~Si-Wu-Wei~Fire",
      "THREE_COMBINATIONS~Yin-Wu-Xu~Fire",
    ]),
    description: "Public recognition, award, or honor",
  },
};


// =============================================================================
// RELATIONSHIP EVENTS
// =============================================================================

export const RELATIONSHIP_EVENTS: Record<string, EventType> = {
  marriage: {
    id: "marriage",
    domain: LifeDomain.RELATIONSHIP,
    name: "Marriage",
    chinese_name: "結婚",
    default_sentiment: Sentiment.POSITIVE,
    severity_range: new Set([Severity.MAJOR]),
    primary_elements: new Set(["Fire", "Earth"]),
    secondary_elements: new Set(),
    tcm_organs: new Set(),
    pillar_weights: { day: 1.6, month: 1.2, year: 1.0, hour: 0.9 },
    common_patterns: new Set([
      "SIX_HARMONIES~Wu-Wei~Fire",
      "STEM_COMBINATION~Jia-Ji~Earth",
      "SIX_HARMONIES~Mao-Xu~Fire",
    ]),
    description: "Getting married",
  },
  divorce: {
    id: "divorce",
    domain: LifeDomain.RELATIONSHIP,
    name: "Divorce",
    chinese_name: "離婚",
    default_sentiment: Sentiment.NEGATIVE,
    severity_range: new Set([Severity.MAJOR]),
    primary_elements: new Set(["Fire", "Water"]),
    secondary_elements: new Set(),
    tcm_organs: new Set(),
    pillar_weights: { day: 1.6, month: 1.2, year: 1.0, hour: 0.8 },
    common_patterns: new Set([
      "CLASH~Zi-Wu~opposite",
      "PUNISHMENT~Zi-Mao~en_xing",
      "PUNISHMENT~Chou-Wei-Xu~wu_li_xing",
    ]),
    description: "Marriage ending in divorce",
  },
  engagement: {
    id: "engagement",
    domain: LifeDomain.RELATIONSHIP,
    name: "Engagement",
    chinese_name: "訂婚",
    default_sentiment: Sentiment.POSITIVE,
    severity_range: new Set([Severity.MODERATE]),
    primary_elements: new Set(["Fire", "Wood"]),
    secondary_elements: new Set(),
    tcm_organs: new Set(),
    pillar_weights: { day: 1.5, month: 1.2, year: 1.0, hour: 0.9 },
    common_patterns: new Set(),
    description: "Getting engaged to be married",
  },
  breakup: {
    id: "breakup",
    domain: LifeDomain.RELATIONSHIP,
    name: "Breakup",
    chinese_name: "分手",
    default_sentiment: Sentiment.NEGATIVE,
    severity_range: new Set([Severity.MODERATE, Severity.MAJOR]),
    primary_elements: new Set(["Metal", "Wood"]),
    secondary_elements: new Set(),
    tcm_organs: new Set(),
    pillar_weights: { day: 1.5, month: 1.1, year: 0.9, hour: 0.9 },
    common_patterns: new Set([
      "CLASH~Mao-You~opposite",
      "HARM~Zi-Wei~",
    ]),
    description: "End of a romantic relationship",
  },
  new_relationship: {
    id: "new_relationship",
    domain: LifeDomain.RELATIONSHIP,
    name: "New Relationship",
    chinese_name: "新戀情",
    default_sentiment: Sentiment.POSITIVE,
    severity_range: new Set([Severity.MINOR, Severity.MODERATE]),
    primary_elements: new Set(["Fire", "Wood"]),
    secondary_elements: new Set(),
    tcm_organs: new Set(),
    pillar_weights: { day: 1.4, hour: 1.2, month: 1.0, year: 0.9 },
    common_patterns: new Set(),
    description: "Starting a new romantic relationship",
  },
  conflict_partner: {
    id: "conflict_partner",
    domain: LifeDomain.RELATIONSHIP,
    name: "Partner Conflict",
    chinese_name: "伴侶衝突",
    default_sentiment: Sentiment.NEGATIVE,
    severity_range: new Set([Severity.MINOR, Severity.MODERATE, Severity.MAJOR]),
    primary_elements: new Set(["Fire", "Metal"]),
    secondary_elements: new Set(),
    tcm_organs: new Set(),
    pillar_weights: { day: 1.5, month: 1.1, year: 0.9, hour: 1.0 },
    common_patterns: new Set([
      "PUNISHMENT~Chou-Wei-Xu~wu_li_xing",
      "HARM~You-Xu~",
    ]),
    description: "Significant conflict with partner/spouse",
  },
};


// =============================================================================
// EDUCATION EVENTS
// =============================================================================

export const EDUCATION_EVENTS: Record<string, EventType> = {
  enrollment: {
    id: "enrollment",
    domain: LifeDomain.EDUCATION,
    name: "School Enrollment",
    chinese_name: "入學",
    default_sentiment: Sentiment.POSITIVE,
    severity_range: new Set([Severity.MODERATE]),
    primary_elements: new Set(["Wood", "Water"]),
    secondary_elements: new Set(),
    tcm_organs: new Set(),
    pillar_weights: { year: 1.3, month: 1.2, day: 1.0, hour: 0.9 },
    common_patterns: new Set([
      "THREE_MEETINGS~Hai-Zi-Chou~Water",
      "SIX_HARMONIES~Yin-Hai~Wood",
    ]),
    description: "Starting school or university",
  },
  graduation: {
    id: "graduation",
    domain: LifeDomain.EDUCATION,
    name: "Graduation",
    chinese_name: "畢業",
    default_sentiment: Sentiment.POSITIVE,
    severity_range: new Set([Severity.MODERATE, Severity.MAJOR]),
    primary_elements: new Set(["Fire", "Metal"]),
    secondary_elements: new Set(),
    tcm_organs: new Set(),
    pillar_weights: { year: 1.2, month: 1.3, day: 1.1, hour: 0.9 },
    common_patterns: new Set(),
    description: "Completing education and graduating",
  },
  exam_pass: {
    id: "exam_pass",
    domain: LifeDomain.EDUCATION,
    name: "Pass Exam",
    chinese_name: "考試通過",
    default_sentiment: Sentiment.POSITIVE,
    severity_range: new Set([Severity.MINOR, Severity.MODERATE, Severity.MAJOR]),
    primary_elements: new Set(["Fire", "Water"]),
    secondary_elements: new Set(),
    tcm_organs: new Set(),
    pillar_weights: { month: 1.3, day: 1.2, year: 1.0, hour: 1.0 },
    common_patterns: new Set(),
    description: "Passing an important examination",
  },
  exam_fail: {
    id: "exam_fail",
    domain: LifeDomain.EDUCATION,
    name: "Fail Exam",
    chinese_name: "考試失敗",
    default_sentiment: Sentiment.NEGATIVE,
    severity_range: new Set([Severity.MINOR, Severity.MODERATE]),
    primary_elements: new Set(["Water", "Earth"]),
    secondary_elements: new Set(),
    tcm_organs: new Set(),
    pillar_weights: { month: 1.3, day: 1.2, year: 1.0, hour: 1.0 },
    common_patterns: new Set([
      "STEM_CONFLICT~Wu-Ren~",
    ]),
    description: "Failing an important examination",
  },
};


// =============================================================================
// FAMILY EVENTS
// =============================================================================

export const FAMILY_EVENTS: Record<string, EventType> = {
  birth_child: {
    id: "birth_child",
    domain: LifeDomain.FAMILY,
    name: "Child Birth",
    chinese_name: "生子",
    default_sentiment: Sentiment.POSITIVE,
    severity_range: new Set([Severity.MAJOR]),
    primary_elements: new Set(["Wood", "Fire"]),
    secondary_elements: new Set(),
    tcm_organs: new Set(),
    pillar_weights: { hour: 1.5, day: 1.3, month: 1.1, year: 0.9 },
    common_patterns: new Set([
      "STEM_COMBINATION~Ding-Ren~Wood",
      "THREE_COMBINATIONS~Hai-Mao-Wei~Wood",
    ]),
    description: "Birth of a child",
  },
  death_family: {
    id: "death_family",
    domain: LifeDomain.FAMILY,
    name: "Family Death",
    chinese_name: "喪親",
    default_sentiment: Sentiment.NEGATIVE,
    severity_range: new Set([Severity.MAJOR, Severity.CRITICAL]),
    primary_elements: new Set(["Metal", "Water"]),
    secondary_elements: new Set(),
    tcm_organs: new Set(),
    pillar_weights: { year: 1.4, month: 1.2, day: 1.1, hour: 1.0 },
    common_patterns: new Set([
      "CLASH~Mao-You~opposite",
      "PUNISHMENT~Yin-Si-Shen~shi_xing",
    ]),
    description: "Death of a family member",
  },
  parent_illness: {
    id: "parent_illness",
    domain: LifeDomain.FAMILY,
    name: "Parent Illness",
    chinese_name: "父母生病",
    default_sentiment: Sentiment.NEGATIVE,
    severity_range: new Set([Severity.MODERATE, Severity.MAJOR]),
    primary_elements: new Set(["Metal", "Earth"]),
    secondary_elements: new Set(),
    tcm_organs: new Set(),
    pillar_weights: { year: 1.4, month: 1.3, day: 1.0, hour: 0.8 },
    common_patterns: new Set(),
    description: "Parent becoming seriously ill",
  },
  family_conflict: {
    id: "family_conflict",
    domain: LifeDomain.FAMILY,
    name: "Family Conflict",
    chinese_name: "家庭衝突",
    default_sentiment: Sentiment.NEGATIVE,
    severity_range: new Set([Severity.MINOR, Severity.MODERATE, Severity.MAJOR]),
    primary_elements: new Set(["Fire", "Metal"]),
    secondary_elements: new Set(),
    tcm_organs: new Set(),
    pillar_weights: { year: 1.3, month: 1.2, day: 1.1, hour: 1.0 },
    common_patterns: new Set([
      "PUNISHMENT~Chou-Wei-Xu~wu_li_xing",
      "HARM~Zi-Wei~",
    ]),
    description: "Significant family disagreement or conflict",
  },
};


// =============================================================================
// LEGAL EVENTS
// =============================================================================

export const LEGAL_EVENTS: Record<string, EventType> = {
  lawsuit_filed: {
    id: "lawsuit_filed",
    domain: LifeDomain.LEGAL,
    name: "Lawsuit Filed",
    chinese_name: "訴訟",
    default_sentiment: Sentiment.NEGATIVE,
    severity_range: new Set([Severity.MODERATE, Severity.MAJOR]),
    primary_elements: new Set(["Metal", "Fire"]),
    secondary_elements: new Set(),
    tcm_organs: new Set(),
    pillar_weights: { month: 1.4, year: 1.2, day: 1.1, hour: 0.9 },
    common_patterns: new Set([
      "PUNISHMENT~Yin-Si-Shen~shi_xing",
      "CLASH~Mao-You~opposite",
    ]),
    description: "Being involved in legal proceedings",
  },
  lawsuit_won: {
    id: "lawsuit_won",
    domain: LifeDomain.LEGAL,
    name: "Lawsuit Won",
    chinese_name: "勝訴",
    default_sentiment: Sentiment.POSITIVE,
    severity_range: new Set([Severity.MODERATE, Severity.MAJOR]),
    primary_elements: new Set(["Metal", "Earth"]),
    secondary_elements: new Set(),
    tcm_organs: new Set(),
    pillar_weights: { month: 1.4, year: 1.2, day: 1.1, hour: 0.9 },
    common_patterns: new Set(),
    description: "Winning a legal case",
  },
  lawsuit_lost: {
    id: "lawsuit_lost",
    domain: LifeDomain.LEGAL,
    name: "Lawsuit Lost",
    chinese_name: "敗訴",
    default_sentiment: Sentiment.NEGATIVE,
    severity_range: new Set([Severity.MODERATE, Severity.MAJOR]),
    primary_elements: new Set(["Metal", "Fire"]),
    secondary_elements: new Set(),
    tcm_organs: new Set(),
    pillar_weights: { month: 1.4, year: 1.2, day: 1.1, hour: 0.9 },
    common_patterns: new Set(),
    description: "Losing a legal case",
  },
  contract_signed: {
    id: "contract_signed",
    domain: LifeDomain.LEGAL,
    name: "Contract Signed",
    chinese_name: "簽約",
    default_sentiment: Sentiment.CONDITIONAL,
    severity_range: new Set([Severity.MINOR, Severity.MODERATE, Severity.MAJOR]),
    primary_elements: new Set(["Metal", "Earth"]),
    secondary_elements: new Set(),
    tcm_organs: new Set(),
    pillar_weights: { month: 1.3, day: 1.2, year: 1.0, hour: 0.9 },
    common_patterns: new Set([
      "SIX_HARMONIES~Chen-You~Metal",
      "STEM_COMBINATION~Yi-Geng~Metal",
    ]),
    description: "Signing an important contract",
  },
};


// =============================================================================
// TRAVEL EVENTS
// =============================================================================

export const TRAVEL_EVENTS: Record<string, EventType> = {
  relocation_major: {
    id: "relocation_major",
    domain: LifeDomain.TRAVEL,
    name: "Major Relocation",
    chinese_name: "搬遷",
    default_sentiment: Sentiment.CONDITIONAL,
    severity_range: new Set([Severity.MAJOR]),
    primary_elements: new Set(["Water", "Wood"]),
    secondary_elements: new Set(),
    tcm_organs: new Set(),
    pillar_weights: { year: 1.3, month: 1.2, day: 1.1, hour: 0.9 },
    common_patterns: new Set([
      "CLASH~Yin-Shen~opposite",
      "CLASH~Si-Hai~opposite",
    ]),
    description: "Moving to a new city or country",
  },
  immigration: {
    id: "immigration",
    domain: LifeDomain.TRAVEL,
    name: "Immigration",
    chinese_name: "移民",
    default_sentiment: Sentiment.CONDITIONAL,
    severity_range: new Set([Severity.MAJOR]),
    primary_elements: new Set(["Water", "Metal"]),
    secondary_elements: new Set(),
    tcm_organs: new Set(),
    pillar_weights: { year: 1.4, month: 1.2, day: 1.0, hour: 0.8 },
    common_patterns: new Set([
      "CLASH~Si-Hai~opposite",
      "THREE_COMBINATIONS~Shen-Zi-Chen~Water",
    ]),
    description: "Immigration to another country",
  },
};


// =============================================================================
// COMBINED EVENT REGISTRY
// =============================================================================

export const ALL_EVENT_TYPES: Record<string, EventType> = {
  ...HEALTH_EVENTS,
  ...WEALTH_EVENTS,
  ...CAREER_EVENTS,
  ...RELATIONSHIP_EVENTS,
  ...EDUCATION_EVENTS,
  ...FAMILY_EVENTS,
  ...LEGAL_EVENTS,
  ...TRAVEL_EVENTS,
};

export function getEventsByDomain(domain: LifeDomain): Record<string, EventType> {
  const result: Record<string, EventType> = {};
  for (const [k, v] of Object.entries(ALL_EVENT_TYPES)) {
    if (v.domain === domain) {
      result[k] = v;
    }
  }
  return result;
}

export function getEventsByElement(element: string): Record<string, EventType> {
  const result: Record<string, EventType> = {};
  for (const [k, v] of Object.entries(ALL_EVENT_TYPES)) {
    if (v.primary_elements.has(element) || v.secondary_elements.has(element)) {
      result[k] = v;
    }
  }
  return result;
}

export function getEventStatistics(): Record<string, any> {
  const byDomain: Record<string, number> = {};
  for (const event of Object.values(ALL_EVENT_TYPES)) {
    const dom = event.domain;
    byDomain[dom] = (byDomain[dom] ?? 0) + 1;
  }

  const bySentiment: Record<string, number> = {};
  for (const event of Object.values(ALL_EVENT_TYPES)) {
    const sent = event.default_sentiment;
    bySentiment[sent] = (bySentiment[sent] ?? 0) + 1;
  }

  return {
    total_event_types: Object.keys(ALL_EVENT_TYPES).length,
    by_domain: byDomain,
    by_sentiment: bySentiment,
    with_pattern_correlations: Object.values(ALL_EVENT_TYPES).filter(
      (e) => e.common_patterns.size > 0
    ).length,
  };
}
