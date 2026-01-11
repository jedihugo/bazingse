import type { 
  BaZiData, 
  LuckPillar, 
  AnnualPillar, 
  MonthlyPillar, 
  DailyPillar,
  NatalChartResponse,
  NatalChart,
  Pillar,
  LuckPillarData,
  LuckPillarResponse
} from '~/types/bazi'

export const useBaziData = () => {
  // Reactive state
  const baziData = ref<BaZiData | null>(null)
  const natalChartData = ref<NatalChartResponse | null>(null)
  const currentLuckPillar = ref<LuckPillarData | null>(null)  // Current 10-year luck pillar
  const selectedLuckPillar = ref<LuckPillar | null>(null)
  const selectedAnnualLuck = ref<AnnualPillar | null>(null)
  const selectedMonthlyLuck = ref<MonthlyPillar | null>(null)
  const selectedDailyLuck = ref<DailyPillar | null>(null)
  const isLoading = ref(false)
  const error = ref<string>('')

  // API base URLs
  const DIRECT_API_URL = 'http://localhost:8008'
  const PROXY_API_URL = '/api/bazi' // Nuxt server proxy route

  // Helper function to extract Ten Gods from the new API format
  const extractTenGodsFromNode = (nodeData: any, mappings: any, dayMaster: string): { [key: string]: string } => {
    const tenGods: { [key: string]: string } = {}
    
    if (!nodeData?.post?.qi || !mappings?.ten_gods) return tenGods
    
    // Get ten gods for each stem in the qi
    Object.keys(nodeData.post.qi).forEach(stemName => {
      if (mappings.ten_gods[dayMaster] && mappings.ten_gods[dayMaster][stemName]) {
        // Get the abbreviated ten god value
        const fullTenGod = mappings.ten_gods[dayMaster][stemName]
        tenGods[stemName] = getTenGodAbbreviation(fullTenGod)
      }
    })
    
    return tenGods
  }

  // Helper function to convert ten god names to abbreviations
  // Uses API-provided abbreviation when available, falls back to pattern matching
  const getTenGodAbbreviation = (tenGod: string | { abbreviation?: string, id?: string }): string => {
    // If tenGod is already an object with abbreviation, use it
    if (typeof tenGod === 'object' && tenGod !== null) {
      return tenGod.abbreviation || tenGod.id || 'Unknown'
    }
    // If it's a short string (already an abbreviation), return as-is
    if (typeof tenGod === 'string' && tenGod.length <= 3) {
      return tenGod
    }
    // Fallback pattern matching for legacy string format
    // NOTE: These should ideally come from API mappings.ten_gods
    const abbreviations: { [key: string]: string } = {
      'Friend': 'F',
      'Rob Wealth': 'RW',
      'Eating God': 'EG',
      'Hurting Officer': 'HO',
      'Direct Wealth': 'DW',
      'Indirect Wealth': 'IW',
      'Direct Officer': 'DO',
      '7 Killings': '7K',
      'Seven Killings': '7K',
      'Direct Resource': 'DR',
      'Indirect Resource': 'IR',
      'Day Master': 'DM'
    }
    return abbreviations[tenGod as string] || (tenGod as string)
  }

  // Helper function to transform new API response to legacy format
  const transformToLegacyFormat = (apiResponse: NatalChartResponse): BaZiData => {
    if (!apiResponse) {
      throw new Error('No API response to transform')
    }

    // Get the day master stem ID (not the English name)
    const dayMaster = apiResponse.hs_d?.base?.id || apiResponse.hs_d?.post?.id || 'Yi'
    const mappings = apiResponse.mappings
    
    // Debug logging (can be commented out in production)
    // console.log('Day Master for transformation:', dayMaster)
    // console.log('Available mappings:', {
    //   hasStemsMapping: !!mappings?.heavenly_stems,
    //   hasBranchesMapping: !!mappings?.earthly_branches,
    //   hasTenGodsMapping: !!mappings?.ten_gods,
    //   tenGodsForDayMaster: mappings?.ten_gods?.[dayMaster] ? Object.keys(mappings.ten_gods[dayMaster]).length : 0
    // })

    // Helper to create a pillar from nodes
    const createPillarFromNodes = (hsNode: any, ebNode: any, pillarName?: string): Pillar => {
      const hsId = hsNode?.base?.id || hsNode?.post?.id || ''
      const ebId = ebNode?.base?.id || ebNode?.post?.id || ''
      
      // For transformed earthly branches, use the base ID for pillar name
      // but we'll note the transformation separately
      const hsIdFinal = hsId
      const ebIdFinal = ebNode?.transformed ? (ebNode?.base?.id || ebId) : ebId
      
      // Debug logging (can be commented out in production)
      // console.log(`Creating pillar ${pillarName || 'unknown'}:`, {
      //   hsId: hsIdFinal,
      //   ebId: ebIdFinal,
      //   hsTransformed: hsNode?.transformed,
      //   ebTransformed: ebNode?.transformed
      // })
      
      // Get element and animal from mappings
      const hsElement = mappings?.heavenly_stems?.[hsIdFinal]?.english || 'Unknown'
      const ebAnimal = mappings?.earthly_branches?.[ebIdFinal]?.animal || 'Unknown'
      
      // Get ten god for heavenly stem
      const tenGodHs = mappings?.ten_gods?.[dayMaster]?.[hsIdFinal] 
        ? getTenGodAbbreviation(mappings.ten_gods[dayMaster][hsIdFinal])
        : 'Unknown'
      
      // Get ten gods for hidden stems
      const tenGodsHidden = extractTenGodsFromNode(ebNode, mappings, dayMaster)
      
      return {
        pillar: `${hsIdFinal} ${ebIdFinal}`,
        hs_element: hsElement,
        eb_animal: ebAnimal,
        ten_god_hs: tenGodHs,
        ten_god_hidden: tenGodsHidden
      }
    }

    // Create natal chart from nodes
    const natalChart: NatalChart = {
      year_pillar: createPillarFromNodes(apiResponse.hs_y, apiResponse.eb_y, 'year'),
      month_pillar: createPillarFromNodes(apiResponse.hs_m, apiResponse.eb_m, 'month'),
      day_pillar: createPillarFromNodes(apiResponse.hs_d, apiResponse.eb_d, 'day'),
      hour_pillar: (apiResponse.hs_h && apiResponse.eb_h)
        ? createPillarFromNodes(apiResponse.hs_h, apiResponse.eb_h, 'hour')
        : {
            pillar: 'Unknown Unknown',
            hs_element: 'Unknown',
            eb_animal: 'Unknown',
            ten_god_hs: 'Unknown',
            ten_god_hidden: {}
          }
    }

    // Luck pillars should come from the API via fetchLuckPillar()
    // Return empty array here - actual luck pillars are fetched separately
    // and stored in currentLuckPillar
    return {
      natal_chart: natalChart,
      luck_pillars: [], // Populated from API via fetchLuckPillar
      selected_luck_pillar: null as any
    }
  }

  // Function to fetch 10-year luck pillar data
  const fetchLuckPillar = async (birthDate: string, birthTime: string, gender: string): Promise<LuckPillarData | null> => {
    try {
      const encodedTime = encodeURIComponent(birthTime || 'unknown')
      const url = `${DIRECT_API_URL}/generate_10lp_chart?birth_date=${birthDate}&birth_time=${encodedTime}&gender=${gender}`
      
      const response = await fetch(url, {
        method: 'GET',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
        },
        mode: 'cors'
      })
      
      if (!response.ok) {
        throw new Error(`Luck pillar API returned ${response.status}`)
      }
      
      const data: LuckPillarResponse = await response.json()
      return data.current_luck_pillar
    } catch (err: any) {
      console.error('Failed to fetch luck pillar:', err)
      // Don't throw - just return null so natal chart can still display
      return null
    }
  }

  // Function to generate chart from API (with fallback to proxy)
  const generateChart = async (birthDate: string, birthTime: string, gender: string, luckPillarIndex: number = 0) => {
    isLoading.value = true
    error.value = ''
    
    // Try direct API first, then fallback to proxy
    const tryDirectAPI = async () => {
      const encodedTime = encodeURIComponent(birthTime || 'unknown')
      const url = `${DIRECT_API_URL}/generate_natal_chart?birth_date=${birthDate}&birth_time=${encodedTime}&gender=${gender}`
      
      console.log('Trying direct API call to:', url)
      
      const response = await fetch(url, {
        method: 'GET',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
        },
        mode: 'cors'
      })
      
      if (!response.ok) {
        throw new Error(`API returned ${response.status}: ${response.statusText}`)
      }
      
      return await response.json()
    }
    
    const tryProxyAPI = async () => {
      const url = `${PROXY_API_URL}?birth_date=${birthDate}&birth_time=${encodeURIComponent(birthTime || 'unknown')}&gender=${gender}`
      
      console.log('Trying proxy API call to:', url)
      
      return await $fetch(url, {
        method: 'GET'
      })
    }
    
    try {
      // Fetch natal chart and luck pillar in parallel
      const [natalData, luckData] = await Promise.all([
        (async () => {
          try {
            return await tryDirectAPI()
          } catch (directError: any) {
            console.log('Direct API failed, trying proxy:', directError.message)
            return await tryProxyAPI()
          }
        })(),
        fetchLuckPillar(birthDate, birthTime, gender)
      ])
      
      // Store the raw natal chart response
      natalChartData.value = natalData
      
      // Store current luck pillar
      currentLuckPillar.value = luckData
      
      // Transform to legacy format for UI compatibility
      const transformedData = transformToLegacyFormat(natalData)
      baziData.value = transformedData
      selectedLuckPillar.value = transformedData.selected_luck_pillar
      
      console.log('BaZi chart and luck pillar generated successfully')
      console.log('Current luck pillar:', luckData)
    } catch (err: any) {
      console.error('API calls failed:', err)
      
      // More specific error messages for backend integration
      if (err.name === 'TypeError' && err.message.includes('Failed to fetch')) {
        error.value = 'Cannot connect to BaZingSe API server. Please ensure:\n1. Python FastAPI server is running: python run_bazingse.py\n2. Server is accessible on http://localhost:8008\n3. No firewall is blocking the connection'
      } else if (err.message.includes('CORS')) {
        error.value = 'CORS error: The BaZingSe API server needs CORS configuration. The request is using the Nuxt proxy as fallback.'
      } else if (err.message.includes('422')) {
        error.value = 'Invalid input format. Please check the birth date, time format, and gender values match the expected API format.'
      } else if (err.message.includes('500')) {
        error.value = 'BaZi calculation error on server. This may be due to invalid Chinese calendar conversion or missing sxtwl library.'
      } else {
        error.value = err?.data?.statusMessage || err?.message || 'Failed to generate BaZi chart. Please check the console for details.'
      }
    } finally {
      isLoading.value = false
    }
  }

  // Function to update data from API
  const updateBaziData = (newData: BaZiData) => {
    baziData.value = newData
    selectedLuckPillar.value = newData.selected_luck_pillar
  }

  // Function to select a different luck pillar and fetch its annual pillars from API
  const selectLuckPillar = async (pillar: LuckPillar, birthDate?: string, birthTime?: string, gender?: string) => {
    console.log('selectLuckPillar called with:', pillar)
    
    // Check if clicking the same pillar - if so, deselect it
    if (selectedLuckPillar.value && selectedLuckPillar.value.pillar === pillar.pillar) {
      selectedLuckPillar.value = null
      if (baziData.value) {
        baziData.value.selected_luck_pillar = null as any
      }
      selectedAnnualLuck.value = null
      console.log('selectedLuckPillar deselected')
      return
    }
    
    // For now, just select the pillar locally
    // In the future, this could fetch additional data from the API
    selectedLuckPillar.value = pillar
    if (baziData.value) {
      baziData.value.selected_luck_pillar = pillar
    }
    
    // Reset annual luck selection when changing luck pillar
    selectedAnnualLuck.value = null
    
    console.log('selectedLuckPillar updated to:', selectedLuckPillar.value)
  }

  // Function to select annual luck
  const selectAnnualLuck = (annualPillar: AnnualPillar) => {
    // Check if clicking the same annual pillar - if so, deselect it
    if (selectedAnnualLuck.value && selectedAnnualLuck.value.year === annualPillar.year) {
      selectedAnnualLuck.value = null
      selectedMonthlyLuck.value = null
      console.log('selectedAnnualLuck deselected')
      return
    }
    
    selectedAnnualLuck.value = annualPillar
    selectedMonthlyLuck.value = null // Reset monthly selection when annual changes
    console.log('selectedAnnualLuck updated to:', selectedAnnualLuck.value)
  }

  // Function to select monthly luck
  const selectMonthlyLuck = (monthlyPillar: MonthlyPillar) => {
    // Check if clicking the same monthly pillar - if so, deselect it
    if (selectedMonthlyLuck.value && selectedMonthlyLuck.value.month === monthlyPillar.month) {
      selectedMonthlyLuck.value = null
      selectedDailyLuck.value = null
      console.log('selectedMonthlyLuck deselected')
      return
    }
    
    selectedMonthlyLuck.value = monthlyPillar
    selectedDailyLuck.value = null // Reset daily selection when monthly changes
    console.log('selectedMonthlyLuck updated to:', selectedMonthlyLuck.value)
  }

  // Function to select daily luck
  const selectDailyLuck = (dailyPillar: DailyPillar) => {
    // Check if clicking the same daily pillar - if so, deselect it
    if (selectedDailyLuck.value && selectedDailyLuck.value.day === dailyPillar.day) {
      selectedDailyLuck.value = null
      console.log('selectedDailyLuck deselected')
      return
    }
    
    selectedDailyLuck.value = dailyPillar
    console.log('selectedDailyLuck updated to:', selectedDailyLuck.value)
  }

  // Get annual luck pillars from API response
  const getAnnualLuckPillars = computed(() => {
    if (!selectedLuckPillar.value?.annual_pillars) return []
    
    // Return the annual pillars from the API response
    // The API returns full pillar data with ten gods, so we just pass it through
    return selectedLuckPillar.value.annual_pillars
  })

  // Get monthly luck pillars from selected annual pillar
  const getMonthlyLuckPillars = computed(() => {
    if (!selectedAnnualLuck.value?.monthly_pillars) return []
    return selectedAnnualLuck.value.monthly_pillars
  })

  // Get daily luck pillars from selected monthly pillar
  const getDailyLuckPillars = computed(() => {
    if (!selectedMonthlyLuck.value?.daily_pillars) return []
    return selectedMonthlyLuck.value.daily_pillars
  })

  return {
    baziData: readonly(baziData),
    natalChartData: readonly(natalChartData),
    currentLuckPillar: readonly(currentLuckPillar),  // Current 10-year luck pillar
    selectedLuckPillar: readonly(selectedLuckPillar),
    selectedAnnualLuck: readonly(selectedAnnualLuck),
    selectedMonthlyLuck: readonly(selectedMonthlyLuck),
    selectedDailyLuck: readonly(selectedDailyLuck),
    isLoading: readonly(isLoading),
    error: readonly(error),
    getAnnualLuckPillars,
    getMonthlyLuckPillars,
    getDailyLuckPillars,
    generateChart,
    updateBaziData,
    selectLuckPillar,
    selectAnnualLuck,
    selectMonthlyLuck,
    selectDailyLuck
  }
}