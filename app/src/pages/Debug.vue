<template>
 <div class="min-h-screen bg-gray-50">
  
  <!-- Header - TUI style: minimal chrome -->
  <header class="bg-white border-b border-gray-200">
   <div class="max-w-7xl mx-auto px-1 py-1 sm:px-2 sm:py-2 md:px-3 flex items-center gap-2">
    <img 
     src="/bazingse-logo.png" 
     alt="BaZingSe Logo" 
     class="w-12 h-12 object-contain"
    />
    <div>
     <h1 class="text-xl font-bold text-gray-800">
      BaZingSe
     </h1>
    </div>
   </div>
  </header>

  <!-- Main Content - Mobile-first: base = compact, larger screens = more spacious -->
  <main class="mx-auto main-content">
   <!-- Main Container -->
   <div class="mx-auto" style="max-width: 800px;">
    <!-- BaZi Chart Section -->
    <div class="w-full">
     
     <!-- Quick Test Presets - TUI style: tight -->
     <div class="bg-gradient-to-r from-blue-50 to-purple-50 border border-blue-200 rounded p-1 sm:p-2 md:p-3 mb-2">
      <div class="flex items-center gap-2 mb-2">
       <span class="text-xs font-semibold text-gray-700">⚡ Quick Test:</span>
      </div>
      <div class="flex flex-wrap gap-2">
       <button
        v-for="(preset, idx) in testPresets"
        :key="idx"
        @click="loadPreset(preset)"
        class="px-3 py-1.5 text-xs font-medium rounded-md border transition-all hover:scale-105"
        :class="preset.gender === 'female' 
         ? 'bg-pink-50 border-pink-300 text-pink-700 hover:bg-pink-100' 
         : 'bg-blue-50 border-blue-300 text-blue-700 hover:bg-blue-100'"
       >
        <span class="font-mono">{{ preset.date }}</span>
        <span class="mx-1">{{ preset.time }}</span>
        <span v-if="preset.note" class="mr-1 font-bold">({{ preset.note }})</span>
        <span>{{ preset.gender === 'female' ? '♀' : '♂' }}</span>
       </button>
      </div>
     </div>
     
     <!-- BaZi Chart with Integrated Input - TUI style: content focus -->
     <div class="bg-white shadow-sm p-1 sm:p-2 md:p-3">
    <!-- Chart Grid with Input Fields -->
    <div class="w-full">
     <!-- Controls Row: Gender + Time Travel aligned with columns -->
     <div class="flex gap-1 mb-2">
      <!-- Spacer for Hour column -->
      <div class="w-28 flex-shrink-0"></div>
      
      <!-- Gender in Day column position -->
      <div class="w-28 flex-shrink-0">
       <div class="flex justify-center gap-3">
        <label class="cursor-pointer flex items-center gap-0.5">
         <input
          type="radio"
          v-model="gender"
          value="male"
          class="w-3 h-3 text-blue-600 focus:ring-blue-500"
          @change="triggerChartUpdate"
         />
         <span class="text-sm">♂</span>
        </label>
        <label class="cursor-pointer flex items-center gap-0.5">
         <input
          type="radio"
          v-model="gender"
          value="female"
          class="w-3 h-3 text-pink-600 focus:ring-pink-500"
          @change="triggerChartUpdate"
         />
         <span class="text-sm">♀</span>
        </label>
       </div>
      </div>
      
      <!-- Spacers for Month and Year columns -->
      <div class="w-28 flex-shrink-0"></div>
      <div class="w-28 flex-shrink-0"></div>
     </div>
     
     <!-- Column Headers: Each input aligned with pillar below (9 columns max) -->
     <div class="flex gap-1 mb-2 flex-wrap items-center">
      
      <!-- Column 1: Hour (Natal) -->
      <div class="w-28 flex-shrink-0">
       <label v-once class="block text-[10px] font-semibold text-gray-700 mb-1 text-center">時 Hour</label>
       <div class="relative">
        <input
         v-if="!unknownHour"
         v-model="birthTime"
         type="time"
         class="w-full pl-1 pr-5 py-1.5 text-xs border border-gray-300 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 text-center hour-input-no-icon"
         @change="triggerChartUpdate"
        />
        <input
         v-else
         value="?"
         disabled
         class="w-full px-1 py-1.5 text-xs border border-gray-300 bg-gray-100 text-center text-gray-500"
        />
        <button
         @click="unknownHour = !unknownHour; handleUnknownHourChange()"
         :class="[
          'unknown-hour-btn border transition-colors',
          unknownHour
           ? 'bg-blue-500 text-white border-blue-500'
           : 'bg-white text-gray-600 border-gray-300'
         ]"
         title="Toggle unknown hour"
        >
         ?
        </button>
       </div>
      </div>
      
      <!-- Column 2: Day (Natal) -->
      <div class="w-28 flex-shrink-0">
       <label v-once class="block text-[10px] font-semibold text-gray-700 mb-1 text-center">日 Day</label>
       <input
        v-model="dayInput"
        type="number"
        min="1"
        max="31"
        placeholder="DD"
        :class="[
         'w-full px-1 py-1.5 text-xs border focus:outline-none focus:ring-1 text-center',
         isValidBirthDate
          ? 'border-gray-300 focus:border-blue-500 focus:ring-blue-500'
          : 'border-red-400 bg-red-50 focus:border-red-500 focus:ring-red-500'
        ]"
        @change="triggerChartUpdate"
       />
      </div>
      
      <!-- Column 3: Month (Natal) -->
      <div class="w-28 flex-shrink-0">
       <label v-once class="block text-[10px] font-semibold text-gray-700 mb-1 text-center">月 Month</label>
       <input
        v-model="monthInput"
        type="number"
        min="1"
        max="12"
        placeholder="MM"
        :class="[
         'w-full px-1 py-1.5 text-xs border focus:outline-none focus:ring-1 text-center',
         isValidBirthDate
          ? 'border-gray-300 focus:border-blue-500 focus:ring-blue-500'
          : 'border-red-400 bg-red-50 focus:border-red-500 focus:ring-red-500'
        ]"
        @change="triggerChartUpdate"
       />
      </div>
      
      <!-- Column 4: Year (Natal) -->
      <div class="w-28 flex-shrink-0">
       <label v-once class="block text-[10px] font-semibold text-gray-700 mb-1 text-center">年 Year</label>
       <input
        v-model="yearInput"
        type="number"
        min="1900"
        max="2100"
        placeholder="YYYY"
        :class="[
         'w-full px-1 py-1.5 text-xs border focus:outline-none focus:ring-1 text-center',
         isValidBirthDate
          ? 'border-gray-300 focus:border-blue-500 focus:ring-blue-500'
          : 'border-red-400 bg-red-50 focus:border-red-500 focus:ring-red-500'
        ]"
        @change="triggerChartUpdate"
       />
      </div>

      <!-- Divider before Location -->
      <div class="flex-shrink-0 flex flex-col justify-end mx-3">
       <div class="w-0.5 h-12 bg-gradient-to-b from-transparent via-emerald-600 to-transparent opacity-80"></div>
      </div>

      <!-- Column 5: Location Toggle (地) -->
      <div class="flex-shrink-0 flex flex-col justify-end">
       <label class="block text-[10px] font-semibold text-gray-700 mb-1 text-center">地 Location</label>
       <div class="flex items-center gap-1 px-2 py-1.5 border border-gray-300 rounded bg-gray-50 h-[34px]" style="min-width: 110px;">
        <label class="cursor-pointer flex items-center gap-0.5">
         <input
          type="checkbox"
          v-model="showLocation"
          class="w-3 h-3 focus:ring-blue-500"
          style="accent-color: #2563EB;"
          @change="triggerChartUpdate"
         />
        </label>
        <div class="flex gap-1" :class="{ 'opacity-40': !showLocation }">
         <label class="cursor-pointer flex items-center gap-0.5" :class="{ 'pointer-events-none': !showLocation }">
          <input
           type="radio"
           v-model="locationType"
           value="overseas"
           class="w-2.5 h-2.5"
           style="accent-color: #2563EB;"
           :disabled="!showLocation"
           @change="triggerChartUpdate"
          />
          <span class="text-[10px] text-blue-700">海外</span>
         </label>
         <label class="cursor-pointer flex items-center gap-0.5" :class="{ 'pointer-events-none': !showLocation }">
          <input
           type="radio"
           v-model="locationType"
           value="birthplace"
           class="w-2.5 h-2.5"
           style="accent-color: #D97706;"
           :disabled="!showLocation"
           @change="triggerChartUpdate"
          />
          <span class="text-[10px] text-amber-700">鄉土</span>
         </label>
        </div>
       </div>
      </div>

      <!-- Left Partition Divider (before 10Y Luck) -->
      <div v-if="chartData?.analysis_info?.has_luck_pillar" 
         class="relative flex-shrink-0 mx-3 self-stretch" 
         style="width: 2px; min-height: 60px;">
       <div class="absolute inset-0 bg-gradient-to-b from-transparent via-purple-500 to-transparent opacity-70"></div>
      </div>
      
     </div>

     <!-- Loading Indicator DISABLED - causes flicker -->
     <div v-if="false" class="fixed inset-0 bg-white/50 backdrop-blur-sm flex items-center justify-center z-40">
      <div class="bg-white px-4 py-3 rounded-lg shadow-lg border border-gray-200">
       <div class="flex items-center gap-2">
        <svg class="animate-spin h-5 w-5 text-blue-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
         <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
         <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        <span class="text-sm text-gray-700 font-medium">Calculating...</span>
       </div>
      </div>
     </div>

     <!-- BaZi Chart Display - ALWAYS VISIBLE -->
     <div class="relative">
      <!-- NATAL CHART (Row 1) - No horizontal scroll on mobile -->
      <div class="relative w-full">

       <!-- Heavenly Stems Row (Natal Only) -->
       <div class="flex gap-1 items-center flex-wrap">
        <template v-for="(pillar, index) in natalPillarsOrdered" :key="`natal-stem-${index}`">
         <!-- Pillar Content -->
        <div class="relative w-28 flex-shrink-0">
         <div
          :id="`stem-${index}`"
          class="aspect-square p-3 transition-all duration-300 relative flex flex-col items-center justify-center cursor-pointer"
          :class="[
           hoveredNode === `stem-${index}` ? 'shadow-lg scale-105' : 'border border-gray-300',
           getNodeHighlightClass(`stem-${index}`),
           highlightedNodes.includes(`stem-${index}`) ? 'z-50' : '',
           index === 1 ? 'border-2 border-blue-500' : '',
           pillar.isUnknown ? 'bg-gray-100 border-dashed opacity-60' : ''
          ]"
          :style="pillar.isUnknown ? {} : (pillar.stem ? getNodeBgColor(pillar.stem.element, pillar.stem.color) : {})"
         >
          <!-- Negative Badges (top-left corner, stacked vertically) -->
          <div v-if="pillar.stemNegatives && pillar.stemNegatives.length > 0" 
             class="absolute top-1 left-1 gap-0.5 z-20"
             :class="pillar.stemNegatives.length >= 3 ? 'grid grid-cols-2 items-start' : 'flex flex-col items-start'">
           <div v-for="(neg, idx) in pillar.stemNegatives" 
              :key="`stem-neg-${index}-${idx}`"
              class="flex items-center justify-center font-bold transition-transform cursor-help"
              :class="[
               getNegativeBadgeSizeClass(neg.strength),
               isBadgeHighlighted(neg) ? 'scale-125 shadow-lg' : 'hover:scale-110'
              ]"
              :style="getNegativeBadgeStyle(neg)"
              :title="getNegativeBadgeTooltip(neg)"
              @mouseenter="handleBadgeHover(neg)"
              @mouseleave="clearHighlight()">
            <span class="leading-none">{{ getNegativeBadgeSymbol(neg) }}</span>
           </div>
          </div>
          
          <!-- Transformation Badges (top-right corner, stacked vertically) -->
          <div v-if="pillar.stemTransformations && pillar.stemTransformations.length > 0" 
             class="absolute top-1 right-1 gap-0.5"
             :class="pillar.stemTransformations.length >= 3 ? 'grid grid-cols-2 items-start' : 'flex flex-col items-end'">
           <div v-for="(trans, idx) in pillar.stemTransformations" 
              :key="`stem-trans-${index}-${idx}`"
              class="flex items-center justify-center font-bold rounded-full shadow-md transition-transform cursor-help"
              :class="[
               getTransformationSizeClass(trans.strength),
               isBadgeHighlighted(trans) ? 'scale-125 shadow-lg' : 'hover:scale-110'
              ]"
              :style="getTransformationBadgeStyles(trans)"
              :title="getTransformationTooltip(trans)"
              @mouseenter="handleBadgeHover(trans)"
              @mouseleave="clearHighlight()">
            <span class="leading-none">{{ getTransformBadgeDisplay(trans.badge) }}</span>
           </div>
          </div>
          
          <!-- Pinyin name at top (hidden on mobile for compact view) -->
          <div v-if="!pillar.isUnknown && pillar.stemName" class="text-xs text-gray-700 mb-1 hidden-mobile sm:block">{{ pillar.stemName }}</div>
          <!-- Chinese character (always show original from base) -->
          <div v-if="pillar.stem" class="text-2xl font-bold text-black">
           {{ pillar.stem.chinese }}
          </div>
          <div v-else class="text-xl text-gray-400">-</div>
          <!-- Element type (hidden on mobile) -->
          <div v-if="!pillar.isUnknown && pillar.stem" class="text-xs text-gray-700 hidden-mobile sm:block">
           <template v-if="showTransformed && pillar.stem.transformedElement">
            {{ pillar.stem.transformedElement.replace('Yang ', '').replace('Yin ', '') }}
           </template>
           <template v-else>
            {{ pillar.stem.element.replace('Yang ', '').replace('Yin ', '') }} {{ pillar.stem.element.includes('Yang') ? '+' : '-' }}
           </template>
          </div>
          <!-- Day Master label (always visible) -->
          <div v-if="!pillar.isUnknown && index === 1" class="text-xs mt-1 text-gray-900 font-bold">
           <span class="sm:hidden">DM</span><span class="hidden-mobile sm:inline">Day master</span>
          </div>
          <!-- Ten God (hidden on mobile) -->
          <div v-if="!pillar.isUnknown && index !== 1" class="text-xs mt-1 text-gray-900 hidden-mobile sm:block">
           {{ pillar.tenGod || '' }}
          </div>
          
          <!-- Combination Badges (bottom-right corner) -->
          <div v-if="pillar.stemCombinations && pillar.stemCombinations.length > 0" 
             class="absolute bottom-1 right-1 gap-0.5 flex items-start content-start"
             :class="pillar.stemCombinations.length >= 3 ? 'flex-wrap-reverse flex-row justify-end' : 'flex-row items-end'"
             :style="pillar.stemCombinations.length >= 3 ? 'max-width: 40px;' : ''">
           <div v-for="(comb, idx) in pillar.stemCombinations" 
              :key="`stem-comb-${index}-${idx}`"
              class="flex items-center justify-center font-bold rounded-full transition-transform cursor-help"
              :class="[
               getCombinationBadgeSizeClass(comb.strength),
               isBadgeHighlighted(comb) ? 'scale-125 shadow-lg' : 'hover:scale-110'
              ]"
              :style="getCombinationBadgeStyle(comb)"
              :title="getCombinationTooltip(comb)"
              @mouseenter="handleBadgeHover(comb)"
              @mouseleave="clearHighlight()">
            <span class="leading-none">{{ getTransformBadgeDisplay(comb.badge) }}</span>
           </div>
          </div>
          
          
          
          <!-- Horizontal WuXing Flow to Next Stem (only in post/transformed view) -->
          <div v-if="viewMode !== 'base' && !pillar.isUnknown && pillar.stem && natalPillarsOrdered[index + 1]?.stem && index < natalPillarsOrdered.length - 1 && !natalPillarsOrdered[index + 1].isUnknown && getWuXingRelation(pillar.stem.element, natalPillarsOrdered[index + 1].stem.element)"
             class="absolute -right-3 top-1/2 -translate-y-1/2 text-lg font-bold z-30"
             :class="getWuXingRelationClass(pillar.stem.element, natalPillarsOrdered[index + 1].stem.element)"
             :title="`${pillar.stem.element} to ${natalPillarsOrdered[index + 1].stem.element}`">
           {{ getWuXingRelation(pillar.stem.element, natalPillarsOrdered[index + 1].stem.element) }}
          </div>
         </div>
        </div>
        </template>
       </div>
       
       <!-- Vertical WuXing Flow Indicators - Always present to maintain consistent spacing -->
       <div class="flex gap-1 -mt-1.5 -mb-1.5 relative z-40 items-center">
        <template v-for="(pillar, index) in natalPillarsOrdered" :key="`natal-flow-${index}`">
        <div class="flex justify-center items-center h-5 w-28 flex-shrink-0">
         <div v-if="viewMode !== 'base' && !pillar.isUnknown && pillar.stem && pillar.branch && getVerticalWuXingRelation(pillar.stem.element, pillar.branch.element)"
            class="text-lg font-bold"
            :class="getVerticalWuXingClass(pillar.stem.element, pillar.branch.element)"
            :title="`${pillar.stem.element} to ${pillar.branch.element}`">
          {{ getVerticalWuXingRelation(pillar.stem.element, pillar.branch.element) }}
         </div>
        </div>
        </template>
       </div>
       
       <!-- Earthly Branches Row (Natal Only) -->
       <div class="flex gap-1 overflow-visible items-stretch">
        <template v-for="(pillar, index) in natalPillarsOrdered" :key="`natal-branch-${index}`">
         <!-- Pillar Content -->
        <div class="relative w-28 flex-shrink-0">
         <div
          :id="`branch-${index}`"
          class="pb-0 pt-2 px-3 transition-all duration-300 relative flex flex-col items-center justify-start cursor-pointer"
          :class="[
           hoveredNode === `branch-${index}` ? 'shadow-lg scale-105' : 'border border-gray-300',
           getNodeHighlightClass(`branch-${index}`),
           highlightedNodes.includes(`branch-${index}`) ? 'z-50' : '',
           index === 1 ? 'border-2 border-blue-500' : '',
           pillar.isUnknown ? 'bg-gray-100 border-dashed opacity-60' : ''
          ]"
          :style="pillar.isUnknown ? { aspectRatio: '1/1.2' } : {
           ...(pillar.branch ? getNodeBgColor(pillar.branch.element, pillar.branch.color) : {}),
           aspectRatio: '1/1.2'
          }"
         >
          <!-- Negative Badges (top-left corner, stacked vertically) -->
          <div v-if="pillar.branchNegatives && pillar.branchNegatives.length > 0" 
             class="absolute top-1 left-1 gap-0.5 z-20"
             :class="pillar.branchNegatives.length >= 3 ? 'grid grid-cols-2 items-start' : 'flex flex-col items-start'">
           <div v-for="(neg, idx) in pillar.branchNegatives" 
              :key="`branch-neg-${index}-${idx}`"
              class="flex items-center justify-center font-bold transition-transform cursor-help"
              :class="[
               getNegativeBadgeSizeClass(neg.strength),
               isBadgeHighlighted(neg) ? 'scale-125 shadow-lg' : 'hover:scale-110'
              ]"
              :style="getNegativeBadgeStyle(neg)"
              :title="getNegativeBadgeTooltip(neg)"
              @mouseenter="handleBadgeHover(neg)"
              @mouseleave="clearHighlight()">
            <span class="leading-none">{{ getNegativeBadgeSymbol(neg) }}</span>
           </div>
          </div>
          
          <!-- Transformation Badges (top-right corner, stacked vertically) -->
          <div v-if="pillar.branchTransformations && pillar.branchTransformations.length > 0" 
             class="absolute top-1 right-1 gap-0.5 z-10"
             :class="pillar.branchTransformations.length >= 3 ? 'grid grid-cols-2 items-start' : 'flex flex-col items-end'">
           <div v-for="(trans, idx) in pillar.branchTransformations" 
              :key="`branch-trans-${index}-${idx}`"
              class="flex items-center justify-center font-bold rounded-full shadow-md transition-transform cursor-help"
              :class="[
               getTransformationSizeClass(trans.strength),
               isBadgeHighlighted(trans) ? 'scale-125 shadow-lg' : 'hover:scale-110'
              ]"
              :style="getTransformationBadgeStyles(trans)"
              :title="getTransformationTooltip(trans)"
              @mouseenter="handleBadgeHover(trans)"
              @mouseleave="clearHighlight()">
            <span class="leading-none">{{ getTransformBadgeDisplay(trans.badge) }}</span>
           </div>
          </div>
          
          <!-- Main content with proper spacing from bottom -->
          <div class="flex-1 flex flex-col items-center justify-center pb-10">
           <!-- Branch pinyin name (hidden on mobile for compact view) -->
           <div v-if="!pillar.isUnknown && pillar.branchName" class="text-xs text-gray-700 mb-1 hidden-mobile sm:block">
            {{ pillar.branchName }}
           </div>
           <!-- Chinese character (always show original from base) -->
           <div v-if="pillar.branch" class="text-2xl font-bold text-black">
            {{ pillar.branch.chinese }}
           </div>
           <div v-else class="text-xl text-gray-400">-</div>
           <!-- Animal name (hidden on mobile for compact view) -->
           <div
            v-if="!pillar.isUnknown && pillar.branch && !['Fire', 'Water', 'Metal', 'Wood', 'Earth'].includes(pillar.branch.animal)"
            class="text-xs text-gray-800 hidden-mobile sm:block"
           >
            {{ pillar.branch.animal }}
           </div>
          </div>
          
          <!-- Combination Badges (bottom-right corner, above hidden stems) -->
          <div v-if="pillar.branchCombinations && pillar.branchCombinations.length > 0" 
             class="absolute bottom-11 right-1 gap-0.5 z-20 flex items-start content-start"
             :class="pillar.branchCombinations.length >= 3 ? 'flex-wrap-reverse flex-row justify-end' : 'flex-row items-end'"
             :style="pillar.branchCombinations.length >= 3 ? 'max-width: 40px;' : ''">
           <div v-for="(comb, idx) in pillar.branchCombinations" 
              :key="`branch-comb-${index}-${idx}`"
              class="flex items-center justify-center font-bold rounded-full transition-transform cursor-help"
              :class="[
               getCombinationBadgeSizeClass(comb.strength),
               isBadgeHighlighted(comb) ? 'scale-125 shadow-lg' : 'hover:scale-110'
              ]"
              :style="getCombinationBadgeStyle(comb)"
              :title="getCombinationTooltip(comb)"
              @mouseenter="handleBadgeHover(comb)"
              @mouseleave="clearHighlight()">
            <span class="leading-none">{{ getTransformBadgeDisplay(comb.badge) }}</span>
           </div>
          </div>
          
          <!-- Wealth Storage Badges (bottom-left corner) -->
          <div v-if="pillar.branchWealthStorage && pillar.branchWealthStorage.length > 0" 
             class="absolute bottom-11 left-1 gap-0.5 z-20 flex flex-col items-start">
           <div v-for="(ws, idx) in pillar.branchWealthStorage" 
              :key="`branch-ws-${index}-${idx}`"
              class="flex items-center justify-center font-bold transition-transform cursor-help"
              :class="[
               getWealthStorageSizeClass(ws),
               isBadgeHighlighted(ws) ? 'scale-125 shadow-lg' : 'hover:scale-110'
              ]"
              :style="getWealthStorageBadgeStyle(ws)"
              :title="getWealthStorageTooltip(ws)"
              @mouseenter="handleBadgeHover(ws)"
              @mouseleave="clearHighlight()">
            <span class="leading-none">{{ getWealthStorageSymbol(ws) }}</span>
           </div>
          </div>
          
          <!-- Qi Display - Single row at bottom with Primary Qi (本氣) + Hidden Stems (藏干) -->
          <div v-if="pillar.hiddenStems || pillar.hiddenQi" class="absolute bottom-0 left-0 right-0 flex overflow-hidden h-10">
           <!-- Primary Qi (本氣) - index 0, shown with border-r separator -->
           <div
            v-if="getPrimaryQiData(pillar)"
            class="flex flex-col items-center justify-start text-black overflow-hidden pt-1 pb-0.5 h-full border-r-2 border-white/50"
            :style="{
             ...getNodeBgColor(getStemElement(getPrimaryQiData(pillar).stem), getPrimaryQiData(pillar).color),
             width: `${getPrimaryQiData(pillar).weight}%`
            }"
            :title="`Primary Qi (本氣): ${getPrimaryQiData(pillar).stem} - ${getPrimaryQiData(pillar).god ? getPrimaryQiData(pillar).god + ' - ' : ''}Score: ${getPrimaryQiData(pillar).score || 'N/A'} (${getPrimaryQiData(pillar).weight}%)`"
           >
            <div class="text-[8px] text-gray-600 leading-tight hidden-mobile sm:block">{{ getPrimaryQiData(pillar).stem }}</div>
            <div class="text-[11px] font-bold text-black leading-tight">{{ stemMappings[getPrimaryQiData(pillar).stem] || getPrimaryQiData(pillar).stem }}</div>
            <div class="text-[8px] text-gray-800 font-medium leading-tight hidden-mobile sm:block">{{ getPrimaryQiData(pillar).god || '' }}</div>
           </div>
           <!-- Hidden Stems (藏干) - index 1+, smaller display -->
           <div
            v-for="(hidden, idx) in getHiddenStemsData(pillar)"
            :key="idx"
            class="flex flex-col items-center justify-start text-black overflow-hidden pt-1 pb-0.5 h-full"
            :style="{
             ...getNodeBgColor(getStemElement(hidden.stem), hidden.color),
             width: `${hidden.weight}%`
            }"
            :title="`Hidden Stem (藏干): ${hidden.stem} - ${hidden.god ? hidden.god + ' - ' : ''}Score: ${hidden.score || 'N/A'} (${hidden.weight}%)`"
           >
            <div class="text-[7px] text-gray-500 leading-tight hidden-mobile sm:block">{{ hidden.stem }}</div>
            <div class="text-[9px] text-black leading-tight">{{ stemMappings[hidden.stem] || hidden.stem }}</div>
            <div class="text-[7px] text-gray-700 leading-tight hidden-mobile sm:block">{{ hidden.god || '' }}</div>
           </div>
          </div>
          
          
          <!-- Horizontal WuXing Flow to Next Branch (only in post/transformed view) -->
          <div v-if="viewMode !== 'base' && !pillar.isUnknown && pillar.branch && natalPillarsOrdered[index + 1]?.branch && index < natalPillarsOrdered.length - 1 && !natalPillarsOrdered[index + 1].isUnknown && getWuXingRelation(pillar.branch.element, natalPillarsOrdered[index + 1].branch.element)"
             class="absolute -right-3 top-1/3 -translate-y-1/2 text-lg font-bold z-50"
             :class="getWuXingRelationClass(pillar.branch.element, natalPillarsOrdered[index + 1].branch.element)"
             :title="`${pillar.branch.element} to ${natalPillarsOrdered[index + 1].branch.element}`">
           {{ getWuXingRelation(pillar.branch.element, natalPillarsOrdered[index + 1].branch.element) }}
          </div>
         </div>
        </div>
        </template>
       </div>

       <!-- Qi Phase Row (十二長生) -->
       <div class="flex gap-1 mt-1">
        <template v-for="(pillar, index) in natalPillarsOrdered" :key="`natal-qiphase-${index}`">
         <div class="w-28 flex-shrink-0 text-center">
          <div v-if="pillar.qiPhase"
             class="text-[10px] px-1.5 py-0.5 rounded-full inline-flex items-center gap-0.5"
             :class="getQiPhaseClass(pillar.qiPhase.strength)"
             :title="`${pillar.qiPhase.id} (${pillar.qiPhase.english}): ${pillar.qiPhase.description}`">
           <span class="font-semibold">{{ pillar.qiPhase.chinese }}</span>
           <span class="text-gray-500 capitalize hidden-mobile sm:inline">{{ pillar.qiPhase.id }}</span>
          </div>
          <div v-else class="text-[10px] text-gray-400">-</div>
         </div>
        </template>
       </div>

      </div>


      <!-- LUCK PILLARS HEADER ROW - 5 items (4 luck + 10Y) -->
      <div class="mt-12 mb-2">
       <div class="flex gap-1 items-end">
        <!-- Hourly Luck Header (under Hour natal) -->
        <div class="w-28 flex-shrink-0 flex flex-col items-center gap-1">
         <input type="checkbox" v-model="includeHourlyLuck" class="w-3 h-3" @change="triggerChartUpdate" />
         <div class="text-xs font-semibold text-gray-700">時運</div>
         <input v-model="analysisTime" type="time" placeholder="HH:MM"
          class="w-full px-1 py-1 text-xs border border-gray-300 rounded text-center" @change="triggerChartUpdate" />
        </div>

        <!-- Daily Luck Header (under Day natal) -->
        <div class="w-28 flex-shrink-0 flex flex-col items-center gap-1">
         <input type="checkbox" v-model="includeDailyLuck" class="w-3 h-3" @change="triggerChartUpdate" />
         <div class="text-xs font-semibold text-gray-700">日運</div>
         <input v-model.number="analysisDay" type="number" min="1" max="31" placeholder="DD"
          class="w-full px-1 py-1 text-xs border border-gray-300 rounded text-center" @change="triggerChartUpdate" />
        </div>

        <!-- Monthly Luck Header (under Month natal) -->
        <div class="w-28 flex-shrink-0 flex flex-col items-center gap-1">
         <input type="checkbox" v-model="includeMonthlyLuck" class="w-3 h-3" @change="triggerChartUpdate" />
         <div class="text-xs font-semibold text-gray-700">月運</div>
         <input v-model.number="analysisMonth" type="number" min="1" max="12" placeholder="MM"
          class="w-full px-1 py-1 text-xs border border-gray-300 rounded text-center" @change="triggerChartUpdate" />
        </div>

        <!-- Annual Luck Header (under Year natal) -->
        <div class="w-28 flex-shrink-0 flex flex-col items-center gap-1">
         <input type="checkbox" v-model="includeAnnualLuck" class="w-3 h-3" @change="triggerChartUpdate" />
         <div class="text-xs font-semibold text-gray-700">年運</div>
         <input v-model.number="analysisYear" type="number" :min="minAnalysisYear" :max="maxAnalysisYear" placeholder="YYYY"
          class="w-full px-1 py-1 text-xs border border-gray-300 rounded text-center" @change="triggerChartUpdate" />
        </div>

        <!-- Left Purple Divider (before 10Y Luck) -->
        <div v-if="chartData?.analysis_info?.has_luck_pillar" class="luck-divider relative self-stretch">
         <div class="absolute inset-0 bg-gradient-to-b from-transparent via-purple-500 to-transparent opacity-70"></div>
        </div>

        <!-- 10Y Luck Header with Time Travel Toggle -->
        <div class="w-28 flex-shrink-0 flex flex-col items-center gap-1">
         <!-- Time Travel Toggle (above 10Y) -->
         <div class="flex items-center gap-1 mb-2">
          <input type="checkbox" v-model="showAnalysisPeriod" class="w-3 h-3" @change="triggerChartUpdate" />
          <span class="text-[10px]">🔮 Time</span>
         </div>

         <!-- 10Y Luck Header (always show) -->
         <div class="text-xs font-semibold text-purple-700">運 10Y</div>
         <div v-if="currentLuckPillar?.timing" class="text-[10px] text-gray-600">
          {{ currentLuckPillar?.timing?.start_year || '?' }}-{{ currentLuckPillar?.timing?.end_year || '?' }}
         </div>

        </div>
       </div>
      </div>

      <!-- LUCK PILLARS (Stems and Branches) - ALWAYS visible -->
      <div>
       
       <!-- Luck Heavenly Stems Row -->
       <div class="flex gap-1 items-center">
        <template v-for="(pillar, index) in luckPillarsDisplay" :key="`luck-stem-${index}`">
         <!-- Empty slot for alignment -->
         <div v-if="!pillar" class="w-28 flex-shrink-0"></div>

         <template v-else>
          <!-- Left Purple Divider (before 10Y Luck - index 4) -->
          <div v-if="index === 4" class="luck-divider relative self-stretch">
           <div class="absolute inset-0 bg-gradient-to-b from-transparent via-purple-500 to-transparent opacity-70"></div>
          </div>

          <!-- Luck Stem Pillar -->
          <div class="relative w-28 flex-shrink-0">
           <div
            :id="`stem-${getLuckPosition(index)}`"
            class="aspect-square p-3 transition-all duration-300 relative flex flex-col items-center justify-center cursor-pointer"
            :class="[
             pillar.isEmpty || !pillar.stem ? 'border border-dashed border-gray-300 bg-gray-50 opacity-40' : '',
             !pillar.isEmpty && (hoveredNode === `stem-${getLuckPosition(index)}` ? 'shadow-lg scale-105' : 'border border-gray-300'),
             !pillar.isEmpty && getNodeHighlightClass(`stem-${getLuckPosition(index)}`),
             !pillar.isEmpty && highlightedNodes.includes(`stem-${getLuckPosition(index)}`) ? 'z-50' : '',
             !pillar.isEmpty && pillar.isLuckPillar ? 'border-2 border-purple-500' : '',
             !pillar.isEmpty && pillar.isAnnualLuck ? 'border-2 border-orange-500' : '',
             !pillar.isEmpty && pillar.isMonthlyLuck ? 'border-2 border-green-500' : '',
             !pillar.isEmpty && pillar.isDailyLuck ? 'border-2 border-indigo-500' : '',
             !pillar.isEmpty && pillar.isHourlyLuck ? 'border-2 border-pink-500' : ''
            ]"
            :style="!pillar.isEmpty && pillar.stem ? getNodeBgColor(pillar.stem.element, pillar.stem.color) : {}"
           >
            <!-- Negative Badges -->
            <div v-if="pillar.stemNegatives && pillar.stemNegatives.length > 0" 
               class="absolute top-1 left-1 gap-0.5 z-20"
               :class="pillar.stemNegatives.length >= 3 ? 'grid grid-cols-2 items-start' : 'flex flex-col items-start'">
             <div v-for="(neg, idx) in pillar.stemNegatives" 
                :key="`luck-stem-neg-${index}-${idx}`"
                class="flex items-center justify-center font-bold transition-transform cursor-help"
                :class="[getNegativeBadgeSizeClass(neg.strength), isBadgeHighlighted(neg) ? 'scale-125 shadow-lg' : 'hover:scale-110']"
                :style="getNegativeBadgeStyle(neg)"
                :title="getNegativeBadgeTooltip(neg)"
                @mouseenter="handleBadgeHover(neg)"
                @mouseleave="clearHighlight()">
              <span class="leading-none">{{ getNegativeBadgeSymbol(neg) }}</span>
             </div>
            </div>
            
            <!-- Transformation Badges -->
            <div v-if="pillar.stemTransformations && pillar.stemTransformations.length > 0" 
               class="absolute top-1 right-1 gap-0.5"
               :class="pillar.stemTransformations.length >= 3 ? 'grid grid-cols-2 items-start' : 'flex flex-col items-end'">
             <div v-for="(trans, idx) in pillar.stemTransformations" 
                :key="`luck-stem-trans-${index}-${idx}`"
                class="flex items-center justify-center font-bold rounded-full shadow-md transition-transform cursor-help"
                :class="[getTransformationSizeClass(trans.strength), isBadgeHighlighted(trans) ? 'scale-125 shadow-lg' : 'hover:scale-110']"
                :style="getTransformationBadgeStyles(trans)"
                :title="getTransformationTooltip(trans)"
                @mouseenter="handleBadgeHover(trans)"
                @mouseleave="clearHighlight()">
              <span class="leading-none">{{ getTransformBadgeDisplay(trans.badge) }}</span>
             </div>
            </div>
            
            <!-- Content: pinyin hidden on mobile -->
            <div v-if="pillar.stemName" class="text-xs text-gray-700 mb-1 hidden-mobile sm:block">{{ pillar.stemName }}</div>
            <div v-if="pillar.stem" class="text-2xl font-bold text-black">{{ pillar.stem.chinese }}</div>
            <div v-else class="text-xl text-gray-400">-</div>
            <div v-if="pillar.stem" class="text-xs text-gray-700">
             {{ pillar.stem.element.replace('Yang ', '').replace('Yin ', '') }} {{ pillar.stem.element.includes('Yang') ? '+' : '-' }}
            </div>
            <div class="text-xs mt-1 text-gray-900 hidden-mobile sm:block">{{ pillar.tenGod || '' }}</div>
            
            <!-- Combination Badges -->
            <div v-if="pillar.stemCombinations && pillar.stemCombinations.length > 0"
               class="absolute bottom-1 right-1 gap-0.5 flex items-start content-start"
               :class="pillar.stemCombinations.length >= 3 ? 'flex-wrap-reverse flex-row justify-end' : 'flex-row items-end'"
               :style="pillar.stemCombinations.length >= 3 ? 'max-width: 40px;' : ''">
             <div v-for="(comb, idx) in pillar.stemCombinations"
                :key="`luck-stem-comb-${index}-${idx}`"
                class="flex items-center justify-center font-bold rounded-full transition-transform cursor-help"
                :class="[getCombinationBadgeSizeClass(comb.strength), isBadgeHighlighted(comb) ? 'scale-125 shadow-lg' : 'hover:scale-110']"
                :style="getCombinationBadgeStyle(comb)"
                :title="getCombinationTooltip(comb)"
                @mouseenter="handleBadgeHover(comb)"
                @mouseleave="clearHighlight()">
              <span class="leading-none">{{ getTransformBadgeDisplay(comb.badge) }}</span>
             </div>
            </div>

            <!-- Horizontal WuXing Flow -->
            <div v-if="viewMode !== 'base' && pillar.stem && luckPillarsDisplay[index + 1]?.stem && index < luckPillarsDisplay.length - 1 && getWuXingRelation(pillar.stem.element, luckPillarsDisplay[index + 1].stem.element)"
               class="absolute -right-3 top-1/2 -translate-y-1/2 text-lg font-bold z-30"
               :class="getWuXingRelationClass(pillar.stem.element, luckPillarsDisplay[index + 1].stem.element)"
               :title="`${pillar.stem.element} to ${luckPillarsDisplay[index + 1].stem.element}`">
             {{ getWuXingRelation(pillar.stem.element, luckPillarsDisplay[index + 1].stem.element) }}
            </div>
           </div>
          </div>
          
          <!-- Right Purple Divider (after 10Y Luck - index 4) -->
          <div v-if="index === 4" class="luck-divider relative self-stretch">
           <div class="absolute inset-0 bg-gradient-to-b from-transparent via-purple-500 to-transparent opacity-70"></div>
          </div>
         </template>
        </template>
       </div>

       <!-- Vertical Flow Indicators -->
       <div class="flex gap-1 -mt-1.5 -mb-1.5 relative z-40 items-center">
        <template v-for="(pillar, index) in luckPillarsDisplay" :key="`luck-flow-${index}`">
         <div v-if="!pillar" class="w-28 flex-shrink-0"></div>
         <template v-else>
          <div v-if="index === 4" class="luck-divider"></div>
          <div class="flex justify-center items-center h-7 w-28 flex-shrink-0 gap-1">
           <!-- Dong Gong Rating Badge (Daily Luck only) -->
           <div v-if="pillar.isDailyLuck && !pillar.isEmpty && dongGongInfo && dongGongInfo.rating"
              class="flex items-center justify-center w-6 h-6 rounded-full shadow-md cursor-help transition-transform hover:scale-110 font-bold text-xs"
              :style="{
               backgroundColor: getDongGongRatingColor(dongGongInfo.rating.id).bg,
               border: `2px solid ${getDongGongRatingColor(dongGongInfo.rating.id).border}`,
               color: getDongGongRatingColor(dongGongInfo.rating.id).text
              }"
              :title="getDongGongTooltip(dongGongInfo)">
            <span class="leading-none">{{ getDongGongRatingSymbol(dongGongInfo.rating.id) }}</span>
           </div>
           <!-- Vertical WuXing Flow -->
           <div v-if="viewMode !== 'base' && pillar.stem && pillar.branch && getVerticalWuXingRelation(pillar.stem.element, pillar.branch.element)"
              class="text-lg font-bold"
              :class="getVerticalWuXingClass(pillar.stem.element, pillar.branch.element)"
              :title="`${pillar.stem.element} to ${pillar.branch.element}`">
            {{ getVerticalWuXingRelation(pillar.stem.element, pillar.branch.element) }}
           </div>
          </div>
          <div v-if="index === 4" class="luck-divider"></div>
         </template>
        </template>
       </div>

       <!-- Luck Earthly Branches Row -->
       <div class="flex gap-1 overflow-visible items-stretch">
        <template v-for="(pillar, index) in luckPillarsDisplay" :key="`luck-branch-${index}`">
         <!-- Empty slot for alignment -->
         <div v-if="!pillar" class="w-28 flex-shrink-0"></div>

         <template v-else>
          <!-- Left Purple Divider (before 10Y Luck - index 4) -->
          <div v-if="index === 4" class="luck-divider relative self-stretch">
           <div class="absolute inset-0 bg-gradient-to-b from-transparent via-purple-500 to-transparent opacity-70"></div>
          </div>

          <!-- Luck Branch Pillar -->
          <div class="relative w-28 flex-shrink-0">
           <div
            :id="`branch-${getLuckPosition(index)}`"
            class="pb-0 pt-2 px-3 transition-all duration-300 relative flex flex-col items-center justify-start cursor-pointer"
            :class="[
             pillar.isEmpty || !pillar.branch ? 'border border-dashed border-gray-300 bg-gray-50 opacity-40' : '',
             !pillar.isEmpty && (hoveredNode === `branch-${getLuckPosition(index)}` ? 'shadow-lg scale-105' : 'border border-gray-300'),
             !pillar.isEmpty && getNodeHighlightClass(`branch-${getLuckPosition(index)}`),
             !pillar.isEmpty && highlightedNodes.includes(`branch-${getLuckPosition(index)}`) ? 'z-50' : '',
             !pillar.isEmpty && pillar.isLuckPillar ? 'border-2 border-purple-500' : '',
             !pillar.isEmpty && pillar.isAnnualLuck ? 'border-2 border-orange-500' : '',
             !pillar.isEmpty && pillar.isMonthlyLuck ? 'border-2 border-green-500' : '',
             !pillar.isEmpty && pillar.isDailyLuck ? 'border-2 border-indigo-500' : '',
             !pillar.isEmpty && pillar.isHourlyLuck ? 'border-2 border-pink-500' : ''
            ]"
            :style="{ ...(!pillar.isEmpty && pillar.branch ? getNodeBgColor(pillar.branch.element, pillar.branch.color) : {}), aspectRatio: '1/1.2' }"
           >
            <!-- Negative Badges -->
            <div v-if="pillar.branchNegatives && pillar.branchNegatives.length > 0" 
               class="absolute top-1 left-1 gap-0.5 z-20"
               :class="pillar.branchNegatives.length >= 3 ? 'grid grid-cols-2 items-start' : 'flex flex-col items-start'">
             <div v-for="(neg, idx) in pillar.branchNegatives" 
                :key="`luck-branch-neg-${index}-${idx}`"
                class="flex items-center justify-center font-bold transition-transform cursor-help"
                :class="[getNegativeBadgeSizeClass(neg.strength), isBadgeHighlighted(neg) ? 'scale-125 shadow-lg' : 'hover:scale-110']"
                :style="getNegativeBadgeStyle(neg)"
                :title="getNegativeBadgeTooltip(neg)"
                @mouseenter="handleBadgeHover(neg)"
                @mouseleave="clearHighlight()">
              <span class="leading-none">{{ getNegativeBadgeSymbol(neg) }}</span>
             </div>
            </div>
            
            <!-- Transformation Badges -->
            <div v-if="pillar.branchTransformations && pillar.branchTransformations.length > 0" 
               class="absolute top-1 right-1 gap-0.5"
               :class="pillar.branchTransformations.length >= 3 ? 'grid grid-cols-2 items-start' : 'flex flex-col items-end'">
             <div v-for="(trans, idx) in pillar.branchTransformations" 
                :key="`luck-branch-trans-${index}-${idx}`"
                class="flex items-center justify-center font-bold rounded-full shadow-md transition-transform cursor-help"
                :class="[getTransformationSizeClass(trans.strength), isBadgeHighlighted(trans) ? 'scale-125 shadow-lg' : 'hover:scale-110']"
                :style="getTransformationBadgeStyles(trans)"
                :title="getTransformationTooltip(trans)"
                @mouseenter="handleBadgeHover(trans)"
                @mouseleave="clearHighlight()">
              <span class="leading-none">{{ getTransformBadgeDisplay(trans.badge) }}</span>
             </div>
            </div>
            
            <!-- Content -->
            <div v-if="pillar.branchName" class="text-xs text-gray-700 mb-1">{{ pillar.branchName }}</div>
            <div v-if="pillar.branch" class="text-2xl font-bold text-black">{{ pillar.branch.chinese }}</div>
            <div v-else class="text-xl text-gray-400">-</div>
            <div v-if="pillar.branch && pillar.branch.animal" class="text-xs text-gray-700 mt-1">{{ pillar.branch.animal }}</div>
            
            <!-- Combination Badges -->
            <div v-if="pillar.branchCombinations && pillar.branchCombinations.length > 0" 
               class="absolute bottom-1 right-1 gap-0.5 flex items-start content-start"
               :class="pillar.branchCombinations.length >= 3 ? 'flex-wrap-reverse flex-row justify-end' : 'flex-row items-end'"
               :style="pillar.branchCombinations.length >= 3 ? 'max-width: 40px;' : ''">
             <div v-for="(comb, idx) in pillar.branchCombinations" 
                :key="`luck-branch-comb-${index}-${idx}`"
                class="flex items-center justify-center font-bold rounded-full transition-transform cursor-help"
                :class="[getCombinationBadgeSizeClass(comb.strength), isBadgeHighlighted(comb) ? 'scale-125 shadow-lg' : 'hover:scale-110']"
                :style="getCombinationBadgeStyle(comb)"
                :title="getCombinationTooltip(comb)"
                @mouseenter="handleBadgeHover(comb)"
                @mouseleave="clearHighlight()">
              <span class="leading-none">{{ getTransformBadgeDisplay(comb.badge) }}</span>
             </div>
            </div>
            
            <!-- Wealth Storage Badges (bottom-left) -->
            <div v-if="pillar.branchWealthStorage && pillar.branchWealthStorage.length > 0" 
               class="absolute bottom-11 left-1 gap-0.5 z-20 flex flex-col items-start">
             <div v-for="(ws, idx) in pillar.branchWealthStorage" 
                :key="`luck-branch-ws-${index}-${idx}`"
                class="flex items-center justify-center font-bold transition-transform cursor-help"
                :class="[
                 getWealthStorageSizeClass(ws),
                 isBadgeHighlighted(ws) ? 'scale-125 shadow-lg' : 'hover:scale-110'
                ]"
                :style="getWealthStorageBadgeStyle(ws)"
                :title="getWealthStorageTooltip(ws)"
                @mouseenter="handleBadgeHover(ws)"
                @mouseleave="clearHighlight()">
              <span class="leading-none">{{ getWealthStorageSymbol(ws) }}</span>
             </div>
            </div>
            
            <!-- Horizontal WuXing Flow -->
            <div v-if="viewMode !== 'base' && pillar.branch && luckPillarsDisplay[index + 1]?.branch && index < luckPillarsDisplay.length - 1 && getWuXingRelation(pillar.branch.element, luckPillarsDisplay[index + 1].branch.element)"
               class="absolute -right-3 top-1/3 -translate-y-1/2 text-lg font-bold z-50"
               :class="getWuXingRelationClass(pillar.branch.element, luckPillarsDisplay[index + 1].branch.element)"
               :title="`${pillar.branch.element} to ${luckPillarsDisplay[index + 1].branch.element}`">
             {{ getWuXingRelation(pillar.branch.element, luckPillarsDisplay[index + 1].branch.element) }}
            </div>
            
            <!-- Qi Display - Single row at bottom with Primary Qi (本氣) + Hidden Stems (藏干) -->
            <div v-if="!pillar.isEmpty && (pillar.hiddenStems || pillar.hiddenQi)" class="absolute bottom-0 left-0 right-0 flex overflow-hidden h-10">
             <!-- Primary Qi (本氣) - index 0, shown with border-r separator -->
             <div
              v-if="getPrimaryQiData(pillar)"
              class="flex flex-col items-center justify-start text-black overflow-hidden pt-1 pb-0.5 h-full border-r-2 border-white/50"
              :style="{
               ...getNodeBgColor(getStemElement(getPrimaryQiData(pillar).stem), getPrimaryQiData(pillar).color),
               width: `${getPrimaryQiData(pillar).weight}%`
              }"
              :title="`Primary Qi (本氣): ${getPrimaryQiData(pillar).stem} - ${getPrimaryQiData(pillar).god ? getPrimaryQiData(pillar).god + ' - ' : ''}Score: ${getPrimaryQiData(pillar).score || 'N/A'} (${getPrimaryQiData(pillar).weight}%)`"
             >
              <div class="text-[8px] text-gray-600 leading-tight hidden-mobile sm:block">{{ getPrimaryQiData(pillar).stem }}</div>
              <div class="text-[11px] font-bold text-black leading-tight">{{ stemMappings[getPrimaryQiData(pillar).stem] || getPrimaryQiData(pillar).stem }}</div>
              <div class="text-[8px] text-gray-800 font-medium leading-tight hidden-mobile sm:block">{{ getPrimaryQiData(pillar).god || '' }}</div>
             </div>
             <!-- Hidden Stems (藏干) - index 1+, smaller display -->
             <div
              v-for="(hidden, idx) in getHiddenStemsData(pillar)"
              :key="idx"
              class="flex flex-col items-center justify-start text-black overflow-hidden pt-1 pb-0.5 h-full"
              :style="{
               ...getNodeBgColor(getStemElement(hidden.stem), hidden.color),
               width: `${hidden.weight}%`
              }"
              :title="`Hidden Stem (藏干): ${hidden.stem} - ${hidden.god ? hidden.god + ' - ' : ''}Score: ${hidden.score || 'N/A'} (${hidden.weight}%)`"
             >
              <div class="text-[7px] text-gray-500 leading-tight hidden-mobile sm:block">{{ hidden.stem }}</div>
              <div class="text-[9px] text-black leading-tight">{{ stemMappings[hidden.stem] || hidden.stem }}</div>
              <div class="text-[7px] text-gray-700 leading-tight hidden-mobile sm:block">{{ hidden.god || '' }}</div>
             </div>
            </div>
           </div>
          </div>
          
          <!-- Right Purple Divider (after 10Y Luck - index 4) -->
          <div v-if="index === 4" class="luck-divider relative self-stretch">
           <div class="absolute inset-0 bg-gradient-to-b from-transparent via-purple-500 to-transparent opacity-70"></div>
          </div>
         </template>
        </template>
       </div>

       <!-- Qi Phase Row for Luck Pillars (十二長生) -->
       <div class="flex gap-1 mt-1">
        <template v-for="(pillar, index) in luckPillarsDisplay" :key="`luck-qiphase-${index}`">
         <div class="w-28 flex-shrink-0 text-center">
          <div v-if="pillar.qiPhase"
             class="text-[10px] px-1.5 py-0.5 rounded-full inline-flex items-center gap-0.5"
             :class="getQiPhaseClass(pillar.qiPhase.strength)"
             :title="`${pillar.qiPhase.id} (${pillar.qiPhase.english}): ${pillar.qiPhase.description}`">
           <span class="font-semibold">{{ pillar.qiPhase.chinese }}</span>
           <span class="text-gray-500 capitalize hidden-mobile sm:inline">{{ pillar.qiPhase.id }}</span>
          </div>
          <div v-else-if="!pillar.isEmpty" class="text-[10px] text-gray-400">-</div>
         </div>
         <!-- Empty div for purple divider spacing -->
         <div v-if="index === 4" class="w-1"></div>
        </template>
       </div>
      </div>

      <!-- Talisman Configuration - ALWAYS visible -->
      <div class="mt-12 mb-4">
       <div class="flex items-center gap-2 mb-3">
        <label class="cursor-pointer flex items-center gap-1">
         <input 
          type="checkbox" 
          v-model="showTalismans" 
          class="w-3 h-3 text-teal-600 focus:ring-teal-500"
          style="accent-color: #14B8A6;"
          @change="triggerChartUpdate"
         />
         <span class="text-sm font-semibold text-teal-700">符 Talisman Configuration</span>
        </label>
        <span v-if="showTalismans && hasInvalidTalismanPairs" class="text-xs text-red-600 font-semibold">⚠ Invalid Jia-Zi pairs detected</span>
       </div>
       
       <div class="flex gap-1">
        <!-- Talisman Hour -->
        <div class="w-28 flex-shrink-0">
         <div class="flex items-center justify-center gap-1 mb-1">
          <span class="text-[10px] font-semibold text-center text-teal-700">符時<br/>Hour</span>
          <span v-if="!isValidJiaziPair(talismanHourHS, talismanHourEB)" class="text-red-600 text-xs" title="Invalid Jia-Zi pair">⚠️</span>
         </div>
         <div class="flex flex-col gap-1">
          <select 
           v-model="talismanHourHS" 
           :disabled="!showTalismans"
           class="w-full px-1 py-1.5 text-[10px] rounded border-2 transition-all"
           :class="!showTalismans ? 'bg-gray-100 border-gray-300 text-gray-400 cursor-not-allowed' : (isValidJiaziPair(talismanHourHS, talismanHourEB) ? 'bg-teal-50 border-teal-400 text-teal-800' : 'bg-red-50 border-red-400 text-red-800')"
           @change="triggerChartUpdate"
          >
           <option :value="null">-- HS --</option>
           <option v-for="stem in HEAVENLY_STEMS_LIST" :key="stem.id" :value="stem.id">{{ stem.display }}</option>
          </select>
          <select 
           v-model="talismanHourEB" 
           :disabled="!showTalismans"
           class="w-full px-1 py-1.5 text-[10px] rounded border-2 transition-all"
           :class="!showTalismans ? 'bg-gray-100 border-gray-300 text-gray-400 cursor-not-allowed' : (isValidJiaziPair(talismanHourHS, talismanHourEB) ? 'bg-teal-50 border-teal-400 text-teal-800' : 'bg-red-50 border-red-400 text-red-800')"
           @change="triggerChartUpdate"
          >
           <option :value="null">-- EB --</option>
           <option v-for="branch in EARTHLY_BRANCHES_LIST" :key="branch.id" :value="branch.id">{{ branch.display }}</option>
          </select>
         </div>
        </div>
        
        <!-- Talisman Day -->
        <div class="w-28 flex-shrink-0">
         <div class="flex items-center justify-center gap-1 mb-1">
          <span class="text-[10px] font-semibold text-center text-teal-700">符日<br/>Day</span>
          <span v-if="!isValidJiaziPair(talismanDayHS, talismanDayEB)" class="text-red-600 text-xs" title="Invalid Jia-Zi pair">⚠️</span>
         </div>
         <div class="flex flex-col gap-1">
          <select 
           v-model="talismanDayHS"
           :disabled="!showTalismans" 
           class="w-full px-1 py-1.5 text-[10px] rounded border-2 transition-all"
           :class="!showTalismans ? 'bg-gray-100 border-gray-300 text-gray-400 cursor-not-allowed' : (isValidJiaziPair(talismanDayHS, talismanDayEB) ? 'bg-teal-50 border-teal-400 text-teal-800' : 'bg-red-50 border-red-400 text-red-800')"
           @change="triggerChartUpdate"
          >
           <option :value="null">-- HS --</option>
           <option v-for="stem in HEAVENLY_STEMS_LIST" :key="stem.id" :value="stem.id">{{ stem.display }}</option>
          </select>
          <select 
           v-model="talismanDayEB" 
           :disabled="!showTalismans"
           class="w-full px-1 py-1.5 text-[10px] rounded border-2 transition-all"
           :class="!showTalismans ? 'bg-gray-100 border-gray-300 text-gray-400 cursor-not-allowed' : (isValidJiaziPair(talismanDayHS, talismanDayEB) ? 'bg-teal-50 border-teal-400 text-teal-800' : 'bg-red-50 border-red-400 text-red-800')"
           @change="triggerChartUpdate"
          >
           <option :value="null">-- EB --</option>
           <option v-for="branch in EARTHLY_BRANCHES_LIST" :key="branch.id" :value="branch.id">{{ branch.display }}</option>
          </select>
         </div>
        </div>
        
        <!-- Talisman Month -->
        <div class="w-28 flex-shrink-0">
         <div class="flex items-center justify-center gap-1 mb-1">
          <span class="text-[10px] font-semibold text-center text-teal-700">符月<br/>Month</span>
          <span v-if="!isValidJiaziPair(talismanMonthHS, talismanMonthEB)" class="text-red-600 text-xs" title="Invalid Jia-Zi pair">⚠️</span>
         </div>
         <div class="flex flex-col gap-1">
          <select 
           v-model="talismanMonthHS" 
           :disabled="!showTalismans"
           class="w-full px-1 py-1.5 text-[10px] rounded border-2 transition-all"
           :class="!showTalismans ? 'bg-gray-100 border-gray-300 text-gray-400 cursor-not-allowed' : (isValidJiaziPair(talismanMonthHS, talismanMonthEB) ? 'bg-teal-50 border-teal-400 text-teal-800' : 'bg-red-50 border-red-400 text-red-800')"
           @change="triggerChartUpdate"
          >
           <option :value="null">-- HS --</option>
           <option v-for="stem in HEAVENLY_STEMS_LIST" :key="stem.id" :value="stem.id">{{ stem.display }}</option>
          </select>
          <select 
           v-model="talismanMonthEB" 
           :disabled="!showTalismans"
           class="w-full px-1 py-1.5 text-[10px] rounded border-2 transition-all"
           :class="!showTalismans ? 'bg-gray-100 border-gray-300 text-gray-400 cursor-not-allowed' : (isValidJiaziPair(talismanMonthHS, talismanMonthEB) ? 'bg-teal-50 border-teal-400 text-teal-800' : 'bg-red-50 border-red-400 text-red-800')"
           @change="triggerChartUpdate"
          >
           <option :value="null">-- EB --</option>
           <option v-for="branch in EARTHLY_BRANCHES_LIST" :key="branch.id" :value="branch.id">{{ branch.display }}</option>
          </select>
         </div>
        </div>
        
        <!-- Talisman Year -->
        <div class="w-28 flex-shrink-0">
         <div class="flex items-center justify-center gap-1 mb-1">
          <span class="text-[10px] font-semibold text-center text-teal-700">符年<br/>Year</span>
          <span v-if="!isValidJiaziPair(talismanYearHS, talismanYearEB)" class="text-red-600 text-xs" title="Invalid Jia-Zi pair">⚠️</span>
         </div>
         <div class="flex flex-col gap-1">
          <select 
           v-model="talismanYearHS" 
           :disabled="!showTalismans"
           class="w-full px-1 py-1.5 text-[10px] rounded border-2 transition-all"
           :class="!showTalismans ? 'bg-gray-100 border-gray-300 text-gray-400 cursor-not-allowed' : (isValidJiaziPair(talismanYearHS, talismanYearEB) ? 'bg-teal-50 border-teal-400 text-teal-800' : 'bg-red-50 border-red-400 text-red-800')"
           @change="triggerChartUpdate"
          >
           <option :value="null">-- HS --</option>
           <option v-for="stem in HEAVENLY_STEMS_LIST" :key="stem.id" :value="stem.id">{{ stem.display }}</option>
          </select>
          <select 
           v-model="talismanYearEB" 
           :disabled="!showTalismans"
           class="w-full px-1 py-1.5 text-[10px] rounded border-2 transition-all"
           :class="!showTalismans ? 'bg-gray-100 border-gray-300 text-gray-400 cursor-not-allowed' : (isValidJiaziPair(talismanYearHS, talismanYearEB) ? 'bg-teal-50 border-teal-400 text-teal-800' : 'bg-red-50 border-red-400 text-red-800')"
           @change="triggerChartUpdate"
          >
           <option :value="null">-- EB --</option>
           <option v-for="branch in EARTHLY_BRANCHES_LIST" :key="branch.id" :value="branch.id">{{ branch.display }}</option>
          </select>
         </div>
        </div>
       </div>
      </div>
      
      <!-- Talisman Pillars Display (符) - ALWAYS visible -->
      <div>
       <div class="mb-2">
        <span class="text-sm font-semibold text-teal-700">符 Talisman Pillars</span>
       </div>
       
       <!-- Talisman Stems Row -->
       <div class="flex gap-1 items-center">
        <template v-for="(pillar, index) in talismanPillarsDisplay" :key="`talisman-stem-${index}`">
         <!-- Empty slot if no talisman for this position -->
         <div v-if="!pillar" class="w-28 flex-shrink-0"></div>
         
         <!-- Talisman Stem Cell -->
         <div v-else class="relative w-28 flex-shrink-0">
          <div
           :id="`talisman-stem-${index}`"
           class="aspect-square p-3 transition-all duration-300 relative flex flex-col items-center justify-center border-2 border-teal-500 cursor-pointer"
           :class="[
            pillar.isEmpty || !pillar.stem ? 'bg-gray-50 border-dashed opacity-40' : '',
            !pillar.isEmpty && (hoveredNode === `talisman-stem-${index}` ? 'shadow-lg scale-105' : ''),
            !pillar.isEmpty && getNodeHighlightClass(`talisman-stem-${index}`),
            !pillar.isEmpty && highlightedNodes.includes(`talisman-stem-${index}`) ? 'z-50' : '',
            pillar.isUnknown ? 'bg-gray-100 border-dashed opacity-60' : ''
           ]"
           :style="pillar.isUnknown || pillar.isEmpty ? {} : (pillar.stem ? getNodeBgColor(pillar.stem.element, pillar.stem.color) : {})"
          >
           <!-- Negative Badges (top-left) -->
           <div v-if="pillar.stemNegatives && pillar.stemNegatives.length > 0" 
              class="absolute top-1 left-1 gap-0.5 z-20"
              :class="pillar.stemNegatives.length >= 3 ? 'grid grid-cols-2 items-start' : 'flex flex-col items-start'">
            <div v-for="(neg, idx) in pillar.stemNegatives" 
               :key="`talisman-stem-neg-${index}-${idx}`"
               class="flex items-center justify-center font-bold transition-transform cursor-help"
               :class="[
                getNegativeBadgeSizeClass(neg.strength),
                isBadgeHighlighted(neg) ? 'scale-125 shadow-lg' : 'hover:scale-110'
               ]"
               :style="getNegativeBadgeStyle(neg)"
               :title="getNegativeBadgeTooltip(neg)"
               @mouseenter="handleBadgeHover(neg)"
               @mouseleave="clearHighlight()">
             <span class="leading-none">{{ getNegativeBadgeSymbol(neg) }}</span>
            </div>
           </div>
           
           <!-- Transformation Badges (top-right) -->
           <div v-if="pillar.stemTransformations && pillar.stemTransformations.length > 0" 
              class="absolute top-1 right-1 gap-0.5"
              :class="pillar.stemTransformations.length >= 3 ? 'grid grid-cols-2 items-start' : 'flex flex-col items-end'">
            <div v-for="(trans, idx) in pillar.stemTransformations" 
               :key="`talisman-stem-trans-${index}-${idx}`"
               class="flex items-center justify-center font-bold rounded-full shadow-md transition-transform cursor-help"
               :class="[
                getTransformationSizeClass(trans.strength),
                isBadgeHighlighted(trans) ? 'scale-125 shadow-lg' : 'hover:scale-110'
               ]"
               :style="getTransformationBadgeStyles(trans)"
               :title="getTransformationTooltip(trans)"
               @mouseenter="handleBadgeHover(trans)"
               @mouseleave="clearHighlight()">
             <span class="leading-none">{{ getTransformBadgeDisplay(trans.badge) }}</span>
            </div>
           </div>
           
           <!-- Pinyin name (hidden on mobile for compact view) -->
           <div v-if="!pillar.isUnknown && pillar.stemName" class="text-xs text-gray-700 mb-1 hidden-mobile sm:block">{{ pillar.stemName }}</div>
           <!-- Chinese character -->
           <div v-if="pillar.stem" class="text-2xl font-bold text-black">{{ pillar.stem.chinese }}</div>
           <div v-else class="text-xl text-gray-400">-</div>
           <!-- Element type -->
           <div v-if="!pillar.isUnknown && pillar.stem" class="text-xs text-gray-700">
            {{ pillar.stem.element.replace('Yang ', '').replace('Yin ', '') }} {{ pillar.stem.element.includes('Yang') ? '+' : '-' }}
           </div>
           <!-- Ten God (hidden on mobile for compact view) -->
           <div v-if="!pillar.isUnknown" class="text-xs mt-1 text-gray-900 hidden-mobile sm:block">{{ pillar.tenGod || '' }}</div>
           
           <!-- Combination Badges (bottom-right) -->
           <div v-if="pillar.stemCombinations && pillar.stemCombinations.length > 0" 
              class="absolute bottom-1 right-1 gap-0.5 flex items-start content-start"
              :class="pillar.stemCombinations.length >= 3 ? 'flex-wrap-reverse flex-row justify-end' : 'flex-row items-end'"
              :style="pillar.stemCombinations.length >= 3 ? 'max-width: 40px;' : ''">
            <div v-for="(comb, idx) in pillar.stemCombinations" 
               :key="`talisman-stem-comb-${index}-${idx}`"
               class="flex items-center justify-center font-bold rounded-full transition-transform cursor-help"
               :class="[
                getCombinationBadgeSizeClass(comb.strength),
                isBadgeHighlighted(comb) ? 'scale-125 shadow-lg' : 'hover:scale-110'
               ]"
               :style="getCombinationBadgeStyle(comb)"
               :title="getCombinationTooltip(comb)"
               @mouseenter="handleBadgeHover(comb)"
               @mouseleave="clearHighlight()">
             <span class="leading-none">{{ getTransformBadgeDisplay(comb.badge) }}</span>
            </div>
           </div>
          </div>
         </div>
        </template>
       </div>
       
       <!-- Vertical Flow Indicators (Stem to Branch) -->
       <div class="flex gap-1 -mt-1.5 -mb-1.5 relative z-40 items-center">
        <template v-for="(pillar, index) in talismanPillarsDisplay" :key="`talisman-flow-${index}`">
         <div class="flex justify-center items-center h-5 w-28 flex-shrink-0">
          <div v-if="pillar && viewMode !== 'base' && !pillar.isUnknown && pillar.stem && pillar.branch && getVerticalWuXingRelation(pillar.stem.element, pillar.branch.element)"
             class="text-lg font-bold"
             :class="getVerticalWuXingClass(pillar.stem.element, pillar.branch.element)"
             :title="`${pillar.stem.element} to ${pillar.branch.element}`">
           {{ getVerticalWuXingRelation(pillar.stem.element, pillar.branch.element) }}
          </div>
         </div>
        </template>
       </div>
       
       <!-- Talisman Branches Row -->
       <div class="flex gap-1 overflow-visible items-stretch">
        <template v-for="(pillar, index) in talismanPillarsDisplay" :key="`talisman-branch-${index}`">
         <!-- Empty slot if no talisman -->
         <div v-if="!pillar" class="w-28 flex-shrink-0"></div>
         
         <!-- Talisman Branch Cell -->
         <div v-else class="relative w-28 flex-shrink-0">
          <div
           :id="`talisman-branch-${index}`"
           class="pb-0 pt-2 px-3 transition-all duration-300 relative flex flex-col items-center justify-start border-2 border-teal-500 cursor-pointer"
           :class="[
            pillar.isEmpty || !pillar.branch ? 'bg-gray-50 border-dashed opacity-40' : '',
            !pillar.isEmpty && (hoveredNode === `talisman-branch-${index}` ? 'shadow-lg scale-105' : ''),
            !pillar.isEmpty && getNodeHighlightClass(`talisman-branch-${index}`),
            !pillar.isEmpty && highlightedNodes.includes(`talisman-branch-${index}`) ? 'z-50' : '',
            pillar.isUnknown ? 'bg-gray-100 border-dashed opacity-60' : ''
           ]"
           :style="pillar.isUnknown || pillar.isEmpty ? { aspectRatio: '1/1.2' } : {
            ...(pillar.branch ? getNodeBgColor(pillar.branch.element, pillar.branch.color) : {}),
            aspectRatio: '1/1.2'
           }"
          >
           <!-- Negative Badges (top-left) -->
           <div v-if="pillar.branchNegatives && pillar.branchNegatives.length > 0" 
              class="absolute top-1 left-1 gap-0.5 z-20"
              :class="pillar.branchNegatives.length >= 3 ? 'grid grid-cols-2 items-start' : 'flex flex-col items-start'">
            <div v-for="(neg, idx) in pillar.branchNegatives" 
               :key="`talisman-branch-neg-${index}-${idx}`"
               class="flex items-center justify-center font-bold transition-transform cursor-help"
               :class="[
                getNegativeBadgeSizeClass(neg.strength),
                isBadgeHighlighted(neg) ? 'scale-125 shadow-lg' : 'hover:scale-110'
               ]"
               :style="getNegativeBadgeStyle(neg)"
               :title="getNegativeBadgeTooltip(neg)"
               @mouseenter="handleBadgeHover(neg)"
               @mouseleave="clearHighlight()">
             <span class="leading-none">{{ getNegativeBadgeSymbol(neg) }}</span>
            </div>
           </div>
           
           <!-- Transformation Badges (top-right) -->
           <div v-if="pillar.branchTransformations && pillar.branchTransformations.length > 0" 
              class="absolute top-1 right-1 gap-0.5 z-10"
              :class="pillar.branchTransformations.length >= 3 ? 'grid grid-cols-2 items-start' : 'flex flex-col items-end'">
            <div v-for="(trans, idx) in pillar.branchTransformations" 
               :key="`talisman-branch-trans-${index}-${idx}`"
               class="flex items-center justify-center font-bold rounded-full shadow-md transition-transform cursor-help"
               :class="[
                getTransformationSizeClass(trans.strength),
                isBadgeHighlighted(trans) ? 'scale-125 shadow-lg' : 'hover:scale-110'
               ]"
               :style="getTransformationBadgeStyles(trans)"
               :title="getTransformationTooltip(trans)"
               @mouseenter="handleBadgeHover(trans)"
               @mouseleave="clearHighlight()">
             <span class="leading-none">{{ getTransformBadgeDisplay(trans.badge) }}</span>
            </div>
           </div>
           
           <!-- Main content -->
           <div class="flex-1 flex flex-col items-center justify-center pb-10">
           <!-- Branch pinyin name (hidden on mobile for compact view) -->
           <div v-if="!pillar.isUnknown && pillar.branchName" class="text-xs text-gray-700 mb-1 hidden-mobile sm:block">{{ pillar.branchName }}</div>
            <!-- Chinese character -->
            <div v-if="pillar.branch" class="text-2xl font-bold text-black">{{ pillar.branch.chinese }}</div>
            <div v-else class="text-xl text-gray-400">-</div>
            <!-- Animal name (hidden on mobile for compact view) -->
            <div
             v-if="!pillar.isUnknown && pillar.branch && !['Fire', 'Water', 'Metal', 'Wood', 'Earth'].includes(pillar.branch.animal)"
             class="text-xs text-gray-800 hidden-mobile sm:block"
            >
             {{ pillar.branch.animal }}
            </div>
           </div>
           
           <!-- Combination Badges (bottom-right, above hidden stems) -->
           <div v-if="pillar.branchCombinations && pillar.branchCombinations.length > 0" 
              class="absolute bottom-11 right-1 gap-0.5 z-20 flex items-start content-start"
              :class="pillar.branchCombinations.length >= 3 ? 'flex-wrap-reverse flex-row justify-end' : 'flex-row items-end'"
              :style="pillar.branchCombinations.length >= 3 ? 'max-width: 40px;' : ''">
            <div v-for="(comb, idx) in pillar.branchCombinations" 
               :key="`talisman-branch-comb-${index}-${idx}`"
               class="flex items-center justify-center font-bold rounded-full transition-transform cursor-help"
               :class="[
                getCombinationBadgeSizeClass(comb.strength),
                isBadgeHighlighted(comb) ? 'scale-125 shadow-lg' : 'hover:scale-110'
               ]"
               :style="getCombinationBadgeStyle(comb)"
               :title="getCombinationTooltip(comb)"
               @mouseenter="handleBadgeHover(comb)"
               @mouseleave="clearHighlight()">
             <span class="leading-none">{{ getTransformBadgeDisplay(comb.badge) }}</span>
            </div>
           </div>
           
           <!-- Qi Display - Single row at bottom with Primary Qi (本氣) + Hidden Stems (藏干) -->
           <div v-if="pillar.hiddenStems || pillar.hiddenQi" class="absolute bottom-0 left-0 right-0 flex overflow-hidden h-10">
            <!-- Primary Qi (本氣) - index 0, shown with border-r separator -->
            <div
             v-if="getPrimaryQiData(pillar)"
             class="flex flex-col items-center justify-start text-black overflow-hidden pt-1 pb-0.5 h-full border-r-2 border-white/50"
             :style="{
              ...getNodeBgColor(getStemElement(getPrimaryQiData(pillar).stem), getPrimaryQiData(pillar).color),
              width: `${getPrimaryQiData(pillar).weight}%`
             }"
             :title="`Primary Qi (本氣): ${getPrimaryQiData(pillar).stem} - ${getPrimaryQiData(pillar).god ? getPrimaryQiData(pillar).god + ' - ' : ''}Score: ${getPrimaryQiData(pillar).score || 'N/A'} (${getPrimaryQiData(pillar).weight}%)`"
            >
             <div class="text-[8px] text-gray-600 leading-tight hidden-mobile sm:block">{{ getPrimaryQiData(pillar).stem }}</div>
             <div class="text-[11px] font-bold text-black leading-tight">{{ stemMappings[getPrimaryQiData(pillar).stem] || getPrimaryQiData(pillar).stem }}</div>
             <div class="text-[8px] text-gray-800 font-medium leading-tight hidden-mobile sm:block">{{ getPrimaryQiData(pillar).god || '' }}</div>
            </div>
            <!-- Hidden Stems (藏干) - index 1+, smaller display -->
            <div
             v-for="(hidden, idx) in getHiddenStemsData(pillar)"
             :key="idx"
             class="flex flex-col items-center justify-start text-black overflow-hidden pt-1 pb-0.5 h-full"
             :style="{
              ...getNodeBgColor(getStemElement(hidden.stem), hidden.color),
              width: `${hidden.weight}%`
             }"
             :title="`Hidden Stem (藏干): ${hidden.stem} - ${hidden.god ? hidden.god + ' - ' : ''}Score: ${hidden.score || 'N/A'} (${hidden.weight}%)`"
            >
             <div class="text-[7px] text-gray-500 leading-tight hidden-mobile sm:block">{{ hidden.stem }}</div>
             <div class="text-[9px] text-black leading-tight">{{ stemMappings[hidden.stem] || hidden.stem }}</div>
             <div class="text-[7px] text-gray-700 leading-tight hidden-mobile sm:block">{{ hidden.god || '' }}</div>
            </div>
           </div>
          </div>
         </div>
        </template>
       </div>

       <!-- Qi Phase Row for Talisman Pillars (十二長生) -->
       <div class="flex gap-1 mt-1">
        <template v-for="(pillar, index) in talismanPillarsDisplay" :key="`talisman-qiphase-${index}`">
         <div class="w-28 flex-shrink-0 text-center">
          <div v-if="pillar.qiPhase"
             class="text-[10px] px-1.5 py-0.5 rounded-full inline-flex items-center gap-0.5"
             :class="getQiPhaseClass(pillar.qiPhase.strength)"
             :title="`${pillar.qiPhase.id} (${pillar.qiPhase.english}): ${pillar.qiPhase.description}`">
           <span class="font-semibold">{{ pillar.qiPhase.chinese }}</span>
           <span class="text-gray-500 capitalize hidden-mobile sm:inline">{{ pillar.qiPhase.id }}</span>
          </div>
          <div v-else-if="pillar.stem || pillar.branch" class="text-[10px] text-gray-400">-</div>
         </div>
        </template>
       </div>
      </div>
     </div>

      <!-- Location Pillars Display (地) - Display location nodes WITHOUT badges -->
      <div v-if="showLocation && locationPillarsOrdered.length > 0" class="relative max-w-full mb-4">
       <div class="mb-2">
        <span class="text-sm font-semibold" :class="locationType === 'overseas' ? 'text-blue-700' : 'text-amber-700'">
         {{ locationType === 'overseas' ? '海外 Overseas' : '鄉土 Birthplace' }}
        </span>
       </div>
       
       <!-- Location Stems Row -->
       <div class="flex gap-1 items-center">
        <template v-for="(pillar, index) in locationPillarsOrdered" :key="`location-stem-${index}`">
         <div class="relative w-28 flex-shrink-0">
          <div
           :id="`location-stem-${index}`"
           class="aspect-square p-3 transition-all duration-300 relative flex flex-col items-center justify-center border-2 cursor-pointer"
           :class="[
            hoveredNode === `location-stem-${index}` ? 'shadow-lg scale-105' : 'border-gray-300',
            pillar.locationBorderColor,
            getNodeHighlightClass(`location-stem-${index}`),
            highlightedNodes.includes(`location-stem-${index}`) ? 'z-50' : ''
           ]"
           :style="pillar.stem ? getNodeBgColor(pillar.stem.element, pillar.stem.color) : {}"
          >
           <!-- NO BADGES - just content -->
            <!-- Pinyin name (hidden on mobile for compact view) -->
            <div v-if="pillar.stemName" class="text-xs text-gray-700 mb-1 hidden-mobile sm:block">{{ pillar.stemName }}</div>
           <!-- Chinese character -->
           <div v-if="pillar.stem" class="text-2xl font-bold text-black">{{ pillar.stem.chinese }}</div>
           <div v-else class="text-xl text-gray-400">-</div>
           <!-- Element type -->
           <div v-if="pillar.stem" class="text-xs text-gray-700">
            {{ pillar.stem.element.replace('Yang ', '').replace('Yin ', '') }} {{ pillar.stem.element.includes('Yang') ? '+' : '-' }}
           </div>
           <!-- Ten God -->
            <div class="text-xs mt-1 text-gray-900 hidden-mobile sm:block">{{ pillar.tenGod || '' }}</div>
          </div>
         </div>
        </template>
       </div>
       
       <!-- Vertical Flow Indicators (Stem to Branch) -->
       <div class="flex gap-1 -mt-1.5 -mb-1.5 relative z-40 items-center">
        <template v-for="(pillar, index) in locationPillarsOrdered" :key="`location-flow-${index}`">
         <div class="flex justify-center items-center h-5 w-28 flex-shrink-0">
          <div v-if="viewMode !== 'base' && pillar.stem && pillar.branch && getVerticalWuXingRelation(pillar.stem.element, pillar.branch.element)"
             class="text-lg font-bold"
             :class="getVerticalWuXingClass(pillar.stem.element, pillar.branch.element)"
             :title="`${pillar.stem.element} to ${pillar.branch.element}`">
           {{ getVerticalWuXingRelation(pillar.stem.element, pillar.branch.element) }}
          </div>
         </div>
        </template>
       </div>
       
       <!-- Location Branches Row -->
       <div class="flex gap-1 overflow-visible items-stretch">
        <template v-for="(pillar, index) in locationPillarsOrdered" :key="`location-branch-${index}`">
         <div class="relative w-28 flex-shrink-0">
          <div
           :id="`location-branch-${index}`"
           class="pb-0 pt-2 px-3 transition-all duration-300 relative flex flex-col items-center justify-start border-2 cursor-pointer"
           :class="[
            hoveredNode === `location-branch-${index}` ? 'shadow-lg scale-105' : 'border-gray-300',
            pillar.locationBorderColor,
            getNodeHighlightClass(`location-branch-${index}`),
            highlightedNodes.includes(`location-branch-${index}`) ? 'z-50' : ''
           ]"
           :style="{
            ...(pillar.branch ? getNodeBgColor(pillar.branch.element, pillar.branch.color) : {}),
            aspectRatio: '1/1.2'
           }"
          >
           <!-- NO BADGES - just content -->
           <!-- Main content -->
           <div class="flex-1 flex flex-col items-center justify-center pb-10">
            <!-- Branch pinyin name (hidden on mobile for compact view) -->
            <div v-if="pillar.branchName" class="text-xs text-gray-700 mb-1 hidden-mobile sm:block">{{ pillar.branchName }}</div>
            <!-- Chinese character -->
            <div v-if="pillar.branch" class="text-2xl font-bold text-black">{{ pillar.branch.chinese }}</div>
            <div v-else class="text-xl text-gray-400">-</div>
            <!-- Animal name (hidden on mobile for compact view) -->
            <div
             v-if="pillar.branch && !['Fire', 'Water', 'Metal', 'Wood', 'Earth'].includes(pillar.branch.animal)"
             class="text-xs text-gray-800 hidden-mobile sm:block"
            >
             {{ pillar.branch.animal }}
            </div>
           </div>
           
           <!-- Hidden Stems Section (at bottom) -->
           <div class="absolute bottom-0 left-0 right-0 bg-white/80 border-t border-gray-300 p-1">
            <div class="flex flex-wrap justify-center items-center gap-0.5 min-h-[24px]">
             <div v-for="(god, stem) in pillar.hiddenStems" 
                :key="`location-hidden-${index}-${stem}`"
                class="relative flex items-center justify-center text-[10px] px-1 py-0.5 rounded"
                :style="{
                 backgroundColor: stemMappings[stem] ? getElementColorHex(stemMappings[stem]) + '20' : '#F3F4F6',
                 border: `1px solid ${stemMappings[stem] ? getElementColorHex(stemMappings[stem]) + '60' : '#D1D5DB'}`
                }"
                :title="`${stem}: ${god || 'Unknown'} - ${pillar.hiddenQi ? pillar.hiddenQi[stem] || 'N/A' : 'N/A'}`"
             >
              <div class="text-black font-medium">{{ stemMappings[stem] || stem }}</div>
              <div v-if="god" class="ml-0.5 text-gray-600 hidden-mobile sm:block">{{ god }}</div>
             </div>
            </div>
           </div>
          </div>
         </div>
        </template>
       </div>
      </div>
       
      <!-- Interaction Tooltip -->
     

     <!-- Day Master Analysis -->
     <div v-if="chartData?.daymaster_analysis" class="mt-2 p-3 bg-blue-50 max-w-2xl">
      <div class="text-[10px]">
       <span class="font-semibold">Day Master:</span> 
       {{ chartData?.daymaster_analysis?.daymaster }} 
       ({{ chartData?.daymaster_analysis?.daymaster_strength }} - {{ Math.round(chartData?.daymaster_analysis?.daymaster_percentage) }}%)
      </div>
      <div class="text-[10px] mt-1">
       <span class="font-semibold text-green-700">Favorable:</span> 
       {{ chartData?.daymaster_analysis?.favorable_elements?.join(', ') }}
      </div>
      <div class="text-[10px]">
       <span class="font-semibold text-red-700">Unfav:</span> 
       {{ chartData?.daymaster_analysis?.unfavorable_elements?.join(', ') }}
      </div>
     </div>
     
      <!-- Wealth/Influence Storage Analysis -->
      <div v-if="chartData?.wealth_storage_analysis?.storages?.length > 0" class="mt-2 p-3 bg-gradient-to-r from-yellow-50 to-amber-50 border border-yellow-300 max-w-2xl">
       <div class="text-[10px] font-semibold text-amber-900 mb-1">💰 Storage Analysis (财库/官库)</div>
       <div class="text-[10px] text-gray-700">
        {{ chartData.wealth_storage_analysis.summary }}
       </div>
       <div v-for="(storage, idx) in chartData.wealth_storage_analysis.storages" :key="idx"
          class="mt-2 p-2 bg-white/50 rounded border"
          :class="storage.storage_type === 'wealth' ? 'border-yellow-200' : 'border-purple-200'">
        <div class="flex items-center gap-2">
         <!-- Icon based on storage SIZE only (💎 large, 🪙 small) -->
         <span class="text-xl" :style="getStorageIconStyle(storage)">{{ getStorageAnalysisIcon(storage) }}</span>
         <div>
          <div class="text-[10px] font-semibold" :class="storage.storage_type === 'wealth' ? 'text-amber-800' : 'text-purple-800'">
           {{ storage.branch_chinese }} ({{ storage.branch }}) @ {{ storage.position.toUpperCase() }}
           <!-- Storage size badge -->
           <span class="ml-1 px-1 py-0.5 rounded text-[8px]"
              :class="storage.storage_size === 'large' ? 'bg-amber-100 text-amber-800' : 'bg-gray-100 text-gray-700'">
            {{ storage.storage_size === 'large' ? '大财库' : '小财库' }}
           </span>
           <!-- Activation status badge with border color indicating state -->
           <span class="ml-1 px-1.5 py-0.5 rounded text-[8px]"
              :class="storage.is_opened && storage.is_filled
                ? 'bg-yellow-300 text-yellow-900 font-bold border border-yellow-500'
                : storage.is_opened
                  ? 'bg-green-100 text-green-800 border border-green-400'
                  : storage.is_filled
                    ? 'bg-blue-100 text-blue-800 border border-blue-400'
                    : 'bg-gray-100 text-gray-600 border border-dashed border-gray-400'">
            {{ storage.is_opened && storage.is_filled ? '✨ Maximum' : storage.is_opened ? '🔓 Opened' : storage.is_filled ? '💧 Filled' : '⏳ Latent' }}
           </span>
          </div>
          <div class="text-[9px] text-gray-600">
           Stores {{ storage.stored_element }} • Pillar: {{ storage.pillar_chinese }}
          </div>
          <!-- Opener status -->
          <div v-if="storage.is_opened" class="text-[9px] text-green-700 mt-0.5">
           ✓ Opened by {{ storage.opener_branch }} ({{ storage.opener_positions?.join(', ') }})
          </div>
          <div v-else class="text-[9px] text-gray-500 mt-0.5">
           ○ Needs {{ storage.opener_branch }} to open
          </div>
          <!-- Filler status -->
          <div v-if="storage.is_filled" class="text-[9px] text-blue-700 mt-0.5">
           ✓ Filled from {{ storage.filler_positions?.join(', ') }}
          </div>
          <div v-else class="text-[9px] text-gray-500 mt-0.5">
           ○ Needs {{ storage.filler_stems?.join('/') }} ({{ storage.storage_type === 'wealth' ? 'DW/IW' : 'DO/7K' }}) to fill
          </div>
         </div>
        </div>
       </div>
      </div>
      
     <!-- Analysis Period Info -->
     <div v-if="chartData?.analysis_info && (chartData.analysis_info.has_luck_pillar || chartData.analysis_info.has_annual || chartData.analysis_info.has_monthly || chartData.analysis_info.has_daily || chartData.analysis_info.has_hourly)" class="mt-2 p-3 bg-gradient-to-r from-indigo-50 to-purple-50 border border-indigo-200 max-w-2xl">
      <div class="text-[10px] font-semibold text-indigo-900 mb-1">📅 Analysis Period</div>
      <div class="grid grid-cols-2 gap-1 text-[10px]">
       <div v-if="chartData.analysis_info.year">
        <span class="font-medium text-indigo-700">Year:</span> 
        <span class="text-gray-700">{{ chartData.analysis_info.year }}</span>
       </div>
       <div v-if="chartData.analysis_info.month">
        <span class="font-medium text-indigo-700">Month:</span> 
        <span class="text-gray-700">{{ chartData.analysis_info.month }}</span>
       </div>
       <div v-if="chartData.analysis_info.day">
        <span class="font-medium text-indigo-700">Day:</span> 
        <span class="text-gray-700">{{ chartData.analysis_info.day }}</span>
       </div>
       <div v-if="chartData.analysis_info.time">
        <span class="font-medium text-indigo-700">Time:</span> 
        <span class="text-gray-700">{{ chartData.analysis_info.time }}</span>
       </div>
      </div>
      <div class="mt-1.5 pt-1.5 border-t border-indigo-200 text-[10px] text-indigo-600">
       <div class="flex flex-wrap gap-1">
        <span v-if="chartData.analysis_info.has_luck_pillar" class="px-2 py-0.5 bg-purple-100 text-purple-700 ">10-Year Luck</span>
        <span v-if="chartData.analysis_info.has_annual" class="px-2 py-0.5 " style="background: #FEF3C7; color: #92400E; border: 1px solid #D97706;">Annual ✓</span>
        <span v-if="chartData.analysis_info.annual_disabled" class="px-2 py-0.5 bg-gray-100 text-gray-500 opacity-60">Annual (display only)</span>
        <span v-if="chartData.analysis_info.has_monthly" class="px-2 py-0.5 " style="background: #FEF3C7; color: #92400E; border: 1px solid #D97706;">Monthly</span>
        <span v-if="chartData.analysis_info.has_daily" class="px-2 py-0.5 " style="background: #FEF3C7; color: #92400E; border: 1px solid #D97706;">Daily</span>
        <span v-if="chartData.analysis_info.has_hourly" class="px-2 py-0.5 " style="background: #FEF3C7; color: #92400E; border: 1px solid #D97706;">Hourly</span>
       </div>
       <div v-if="chartData.analysis_info.annual_disabled" class="mt-1 text-[8px] text-gray-600 italic">
        💡 Year {{ chartData.analysis_info.year }} determines 10-year luck only. Annual pillar shown but excluded from element balance and interactions.
       </div>
      </div>
     </div>
     
     <!-- Current Luck Pillar Timing Info -->
     <div v-if="currentLuckPillar" class="mt-2 p-3 bg-purple-50 border border-purple-200 max-w-2xl">
      <div class="text-[10px] font-semibold text-purple-900 mb-1">Current 10-Year Luck Pillar</div>
      <div class="text-[10px]">
       <span class="font-medium">Period:</span> 
       {{ currentLuckPillar.timing.start_year }} - {{ currentLuckPillar.timing.end_year }}
      </div>
      <div class="text-[10px]">
       <span class="font-medium">Age Range:</span> 
       {{ Math.floor(currentLuckPillar.timing.start_age) }} - {{ Math.floor(currentLuckPillar.timing.end_age) }} years old
      </div>
      <div class="text-[10px] text-purple-700 mt-1 bg-purple-100 border border-purple-300 p-3 rounded">
       <strong>⏰ Temporal Overlay:</strong> The 10-year luck pillar is a <strong>time period</strong> that overlays your entire natal chart.
       It interacts with <strong>all four natal pillars</strong> (Year, Month, Day, Hour) <strong>equally and adjacently</strong>,
       regardless of its visual position in the UI. This reflects authentic BaZi metaphysics where luck periods are temporal influences, not spatial positions.
      </div>
      
      <!-- Luck Pillar Interactions -->
      <div v-if="luckPillarInteractions.length > 0" class="mt-1.5 pt-1.5 border-t border-purple-200">
       <div class="text-[10px] font-semibold text-purple-900 mb-1">Interactions with Natal Chart:</div>
       <div class="space-y-0.5">
        <div v-for="(interaction, idx) in luckPillarInteractions" :key="idx" 
           class="text-[10px] p-1 rounded"
           :class="interaction.effect === 'positive' ? 'bg-green-50 border border-green-200' : 'bg-red-50 border border-red-200'">
         <span class="font-medium" :class="interaction.effect === 'positive' ? 'text-green-700' : 'text-red-700'">
          {{ interaction.label }}
         </span>
         <span class="text-gray-700 ml-1">{{ interaction.description }}</span>
        </div>
       </div>
      </div>
      <div v-else class="mt-1.5 pt-1.5 border-t border-purple-200 text-[10px] text-gray-600">
       No major interactions (harmonies/clashes) detected with natal chart.
      </div>
     </div>

      <!-- Unit Tracker Timeline (Qi Story Tracking) -->
      <div v-if="chartData?.unit_tracker"
         class="mt-4 p-4 bg-gradient-to-r from-emerald-50 to-teal-50 border border-emerald-200 max-w-2xl rounded-lg">
       <div class="flex items-center justify-between mb-3 cursor-pointer" @click="showUnitTracker = !showUnitTracker">
        <div class="flex items-center gap-2">
         <div class="text-sm font-bold text-emerald-800">⚔️ Qi Story Timeline</div>
         <span class="text-[10px] px-2 py-0.5 bg-emerald-100 text-emerald-700 rounded">
          {{ chartData.unit_tracker.day_master_chinese }} ({{ chartData.unit_tracker.day_master }}) Day Master
         </span>
        </div>
        <div class="flex items-center gap-2">
         <span class="text-[10px] text-emerald-600">
          {{ chartData.unit_tracker.summary?.total_interactions }} interactions • {{ Math.round(chartData.unit_tracker.summary?.final_total_qi) }} qi
         </span>
         <span class="text-emerald-600 transition-transform" :class="showUnitTracker ? 'rotate-180' : ''">▼</span>
        </div>
       </div>

       <!-- Timeline Content (Collapsible) -->
       <div v-show="showUnitTracker" class="space-y-3">
        <!-- Phase Timeline -->
        <div v-for="(phase, phaseIdx) in chartData.unit_tracker.timeline" :key="phaseIdx"
           class="border border-emerald-200 rounded-lg overflow-hidden bg-white">
         <!-- Phase Header -->
         <div class="flex items-center justify-between p-2 bg-emerald-100 cursor-pointer"
            @click="togglePhase(phase.phase)">
          <div class="flex items-center gap-2">
           <span class="text-[10px] font-bold text-emerald-800">{{ phase.phase_label }}</span>
           <span class="text-[9px] px-1.5 py-0.5 bg-emerald-200 text-emerald-700 rounded">
            {{ phase.event_count }} interactions
           </span>
          </div>
          <div class="flex items-center gap-2">
           <span class="text-[9px] text-emerald-600">Total: {{ Math.round(phase.running_total) }} qi</span>
           <span class="text-emerald-600 text-xs transition-transform" :class="expandedPhases[phase.phase] ? 'rotate-180' : ''">▼</span>
          </div>
         </div>

         <!-- Phase Events (Collapsible) -->
         <div v-show="expandedPhases[phase.phase]" class="p-2 space-y-1.5 bg-white">
          <template v-for="(event, eventIdx) in phase.events" :key="eventIdx">
           <!-- Interaction Event -->
           <div v-if="event.type === 'interaction'"
              class="p-2 rounded border text-[9px]"
              :class="event.interaction_type === 'control' ? 'bg-red-50 border-red-200' : 'bg-green-50 border-green-200'">
            <div class="flex items-center justify-between mb-1">
             <span class="font-bold" :class="event.interaction_type === 'control' ? 'text-red-700' : 'text-green-700'">
              {{ event.interaction_type === 'control' ? '⚔️ Control (克)' : '🌱 Generation (生)' }}
             </span>
             <span class="text-gray-500">Step {{ event.step + 1 }}</span>
            </div>
            <div class="grid grid-cols-2 gap-2">
             <!-- Source -->
             <div class="p-1.5 bg-white rounded border border-gray-200">
              <div class="font-semibold text-gray-800">
               <!-- Pillar unity: stem info -->
               <template v-if="event.source?.stem_chinese">
                {{ event.source?.stem_chinese }} {{ event.source?.stem }}
                <span class="text-[8px] px-1 py-0.5 bg-gray-100 text-gray-600 ml-1">{{ event.source?.ten_god }}</span>
               </template>
               <!-- Cross-pillar: element info -->
               <template v-else>
                {{ event.source?.element }}
                <span class="text-[8px] px-1 py-0.5 bg-gray-100 text-gray-600 ml-1">{{ event.source?.node }}</span>
               </template>
              </div>
              <div class="text-gray-600">
               {{ event.source?.qi_before?.toFixed?.(1) || event.source?.qi_before }} → {{ event.source?.qi_after?.toFixed?.(1) || event.source?.qi_after }}
               <span :class="event.source?.qi_change < 0 ? 'text-red-600' : 'text-green-600'">
                ({{ event.source?.qi_change > 0 ? '+' : '' }}{{ event.source?.qi_change?.toFixed(1) }})
               </span>
              </div>
             </div>
             <!-- Target -->
             <div class="p-1.5 bg-white rounded border border-gray-200">
              <div class="font-semibold text-gray-800">
               <!-- Pillar unity: stem info -->
               <template v-if="event.target?.stem_chinese">
                {{ event.target?.stem_chinese }} {{ event.target?.stem }}
                <span class="text-[8px] px-1 py-0.5 bg-gray-100 text-gray-600 ml-1">{{ event.target?.ten_god }}</span>
               </template>
               <!-- Cross-pillar: element info -->
               <template v-else>
                {{ event.target?.element }}
                <span class="text-[8px] px-1 py-0.5 bg-gray-100 text-gray-600 ml-1">{{ event.target?.node }}</span>
               </template>
              </div>
              <div class="text-gray-600">
               {{ event.target?.qi_before?.toFixed?.(1) || event.target?.qi_before }} → {{ event.target?.qi_after?.toFixed?.(1) || event.target?.qi_after }}
               <span :class="event.target?.qi_change < 0 ? 'text-red-600' : 'text-green-600'">
                ({{ event.target?.qi_change > 0 ? '+' : '' }}{{ event.target?.qi_change?.toFixed(1) }})
               </span>
              </div>
             </div>
            </div>
            <!-- Math Formula Display -->
            <div v-if="event.math_formula" class="mt-1.5 flex items-center gap-2">
             <code class="text-[8px] font-mono bg-gray-100 text-gray-600 px-1.5 py-0.5 rounded">
              {{ event.math_formula }}
             </code>
             <span v-if="event.distance && event.distance > 1"
                 class="text-[7px] px-1 py-0.5 bg-amber-100 text-amber-700 rounded">
              d={{ event.distance }} (×{{ event.distance_multiplier }})
             </span>
            </div>
           </div>

           <!-- Seasonal Adjustment Event -->
           <div v-else-if="event.type === 'seasonal'"
              class="p-2 rounded border text-[9px]"
              :class="event.multiplier > 1 ? 'bg-green-50 border-green-200' : 'bg-orange-50 border-orange-200'">
            <div class="flex items-center justify-between mb-1">
             <span class="font-bold" :class="event.multiplier > 1 ? 'text-green-700' : 'text-orange-700'">
              {{ event.multiplier > 1 ? '🌿 Boosted' : '🍂 Weakened' }}
             </span>
             <span :class="[
               'px-1.5 py-0.5 rounded text-[8px] font-medium',
               event.multiplier > 1 ? 'bg-green-100 text-green-700' : 'bg-orange-100 text-orange-700'
             ]">
              {{ event.seasonal_state }}
             </span>
            </div>
            <div class="flex items-center flex-wrap gap-1.5">
             <!-- Stem with polarity and element -->
             <span class="font-semibold">
              {{ event.polarity }} {{ event.element }}
              <span class="text-gray-500">({{ event.stem_chinese }} {{ event.stem }})</span>
             </span>
             <!-- Location -->
             <span class="text-gray-600 text-[8px]">in</span>
             <span class="px-1 py-0.5 bg-gray-100 rounded text-[8px] font-medium text-gray-700">
              {{ event.location || event.node }}
             </span>
            </div>
            <div class="flex items-center gap-2 mt-1 text-[8px]">
             <span class="text-gray-600">×{{ event.multiplier?.toFixed(3) }}</span>
             <span :class="event.qi_change > 0 ? 'text-green-600' : 'text-orange-600'">
              {{ event.qi_before?.toFixed(1) }} → {{ event.qi_after?.toFixed(1) }}
              ({{ event.qi_change > 0 ? '+' : '' }}{{ event.qi_change?.toFixed(1) }})
             </span>
            </div>
           </div>

           <!-- Combination Event -->
           <div v-else-if="event.type === 'combination'"
              class="p-2 rounded border text-[9px] bg-blue-50 border-blue-200">
            <div class="flex items-center justify-between mb-1">
             <span class="font-bold text-blue-700">
              {{ event.is_transformed ? '✨ Transformation' : '🔗 Combination' }}
             </span>
             <span class="text-gray-500">Step {{ event.step + 1 }}</span>
            </div>
            <div class="flex items-center flex-wrap gap-2">
             <span class="px-1.5 py-0.5 bg-blue-100 text-blue-700 rounded text-[8px] font-medium">
              {{ event.combination_type?.replace(/_/g, ' ') }}
             </span>
             <span class="font-mono text-[8px] text-gray-700">{{ event.pattern }}</span>
             <span v-if="event.is_transformed" class="text-purple-600">→ {{ event.element }}</span>
             <span class="text-green-600 font-medium">+{{ event.boost_amount?.toFixed(1) }}</span>
            </div>

            <!-- Calculation Details (Always Visible) -->
            <div v-if="event.calculation_details" class="mt-2 p-2 bg-white rounded border border-blue-200 space-y-2">

             <!-- Combination Type Header -->
             <div class="flex items-center gap-2 pb-1.5 border-b border-blue-100">
              <span class="text-[8px] text-gray-500">📐</span>
              <span class="font-bold text-blue-800">{{ event.calculation_details.combination_type_chinese }}</span>
              <span class="text-gray-500">{{ event.calculation_details.combination_type?.replace(/_/g, ' ') }}</span>
             </div>

             <!-- Step-by-Step Calculation -->
             <div class="space-y-1.5">
              <template v-for="(calcStep, stepIdx) in event.calculation_details.steps" :key="stepIdx">
               <div class="p-1.5 bg-gray-50 rounded">
                <div class="flex items-center gap-2 mb-0.5">
                 <span class="w-4 h-4 flex items-center justify-center bg-blue-500 text-white text-[7px] font-bold rounded-full">
                  {{ calcStep.step }}
                 </span>
                 <span class="font-medium text-gray-700">{{ calcStep.operation }}</span>
                </div>

                <!-- Node Qi Values (Step 1) -->
                <div v-if="calcStep.values" class="ml-5 mt-1">
                 <div v-for="(nodeInfo, nIdx) in calcStep.values" :key="nIdx"
                    class="flex items-center gap-2 text-[8px] py-0.5">
                  <span class="px-1 py-0.5 bg-gray-200 rounded text-[7px]">{{ nodeInfo.node_id }}</span>
                  <span v-if="nodeInfo.branch" class="text-gray-600">{{ nodeInfo.branch }}</span>
                  <span class="text-gray-400">→</span>
                  <span class="font-medium">
                   {{ nodeInfo.primary_qi_stem_chinese || nodeInfo.stem_chinese }}
                   ({{ nodeInfo.primary_qi_element || nodeInfo.element }})
                  </span>
                  <span class="text-gray-400">:</span>
                  <span class="font-mono text-blue-600">{{ nodeInfo.current_qi }}</span>
                 </div>
                </div>

                <!-- Formula (Steps 2+) -->
                <div v-if="calcStep.formula" class="ml-5 mt-1">
                 <code class="font-mono text-[8px] text-gray-600 bg-gray-100 px-1.5 py-0.5 rounded">
                  {{ calcStep.formula }} = {{ calcStep.result }}
                 </code>
                </div>

                <!-- Multiplier Explanation -->
                <div v-if="calcStep.explanation" class="ml-5 mt-0.5 text-[7px] text-gray-500 italic">
                 {{ calcStep.explanation }}
                </div>
               </div>
              </template>
             </div>

             <!-- Final Result Summary -->
             <div class="pt-1.5 border-t border-blue-100 flex items-center justify-between">
              <span class="text-gray-600">Final Score:</span>
              <span class="font-bold text-green-600">+{{ event.calculation_details.final_score }}</span>
             </div>

             <!-- Transformation Status -->
             <div class="text-[7px] text-gray-500 italic">
              {{ event.calculation_details.transformation_reason }}
             </div>
            </div>
           </div>

           <!-- Conflict Event -->
           <div v-else-if="event.type === 'conflict'"
              class="p-2 rounded border text-[9px] bg-red-50 border-red-200">
            <div class="flex items-center justify-between mb-1">
             <span class="font-bold text-red-700">⚠️ {{ event.conflict_type }}</span>
             <span class="text-gray-500">Step {{ event.step + 1 }}</span>
            </div>
            <div class="flex items-center flex-wrap gap-2">
             <span class="font-mono text-[8px] text-gray-700">{{ event.pattern }}</span>
             <span v-if="event.severity" class="text-[8px] text-gray-500">({{ event.severity }})</span>
             <span v-if="event.victim" class="text-red-600 font-medium">
              -{{ event.victim?.damage?.toFixed(1) }}
             </span>
            </div>
           </div>
          </template>

          <!-- No interactions message -->
          <div v-if="phase.event_count === 0" class="text-[9px] text-gray-500 italic p-2">
           No Wu Xing interactions in this phase
          </div>

          <!-- Element Totals at End of Phase -->
          <div v-if="phase.element_totals" class="mt-2 pt-2 border-t border-gray-200">
           <div class="text-[9px] text-gray-500 mb-1">Element Totals after this phase:</div>
           <div class="flex gap-1 flex-wrap">
            <span v-for="(value, elem) in phase.element_totals" :key="elem"
               class="px-1.5 py-0.5 rounded text-[8px] font-medium"
               :class="{
                'bg-green-100 text-green-800': elem === 'Wood',
                'bg-red-100 text-red-800': elem === 'Fire',
                'bg-yellow-100 text-yellow-800': elem === 'Earth',
                'bg-gray-200 text-gray-800': elem === 'Metal',
                'bg-blue-100 text-blue-800': elem === 'Water'
               }">
             {{ elem }}: {{ value }}
            </span>
           </div>
          </div>
         </div>
        </div>

        <!-- Unit Stories Section (Enhanced with Mini-Pillar Visualization) -->
        <div class="border border-teal-200 rounded-lg overflow-hidden bg-white mt-3">
         <div class="flex items-center justify-between p-2 bg-teal-100 cursor-pointer"
            @click="showUnitStories = !showUnitStories">
          <span class="text-[10px] font-bold text-teal-800">📖 Unit Narratives</span>
          <span class="text-teal-600 text-xs transition-transform" :class="showUnitStories ? 'rotate-180' : ''">▼</span>
         </div>
         <div v-show="showUnitStories" class="p-2 space-y-3">
          <template v-for="(stories, nodeId) in chartData.unit_tracker.unit_stories" :key="nodeId">
           <div v-for="story in stories" :key="story.stem"
              class="p-3 bg-gradient-to-br from-gray-50 to-white rounded-lg border border-gray-200 shadow-sm">

            <!-- Header with Mini-Pillar Visualization -->
            <div class="flex items-start gap-3 mb-3">
             <!-- Mini Pillar Chart (4 pillars, focused one highlighted) -->
             <div class="flex gap-0.5 p-1.5 bg-gray-100 rounded-md flex-shrink-0">
              <template v-for="(pillarKey, pIdx) in ['h', 'd', 'm', 'y']" :key="pIdx">
               <div class="flex flex-col gap-0.5">
                <!-- Mini HS cell -->
                <div
                 class="w-6 h-6 rounded-sm flex items-center justify-center text-[8px] font-bold transition-all"
                 :class="[
                  nodeId === `hs_${pillarKey}` ? 'ring-2 ring-blue-500 shadow-md scale-110 z-10' : 'opacity-40 blur-[0.5px]'
                 ]"
                 :style="getMiniPillarStyle(pillarKey, 'hs', nodeId)">
                 {{ getMiniPillarChinese(pillarKey, 'hs') }}
                </div>
                <!-- Mini EB cell with hidden stems support -->
                <div class="flex flex-col gap-0.5">
                 <!-- EB branch cell -->
                 <div
                  class="w-6 h-6 rounded-sm flex items-center justify-center text-[8px] font-bold transition-all"
                  :class="[
                   nodeId === `eb_${pillarKey}` && story.hidden_position === undefined ? 'ring-2 ring-blue-500 shadow-md scale-110 z-10' :
                   nodeId === `eb_${pillarKey}` && story.hidden_position !== undefined ? 'opacity-70' : 'opacity-40 blur-[0.5px]'
                  ]"
                  :style="getMiniPillarStyle(pillarKey, 'eb', nodeId)">
                  {{ getMiniPillarChinese(pillarKey, 'eb') }}
                 </div>
                 <!-- Hidden stems row (only show for matching EB pillar with hidden stems) -->
                 <div v-if="nodeId === `eb_${pillarKey}` && story.hidden_position !== undefined"
                    class="flex gap-0.5 justify-center">
                  <template v-for="(qi, qiIdx) in getEbHiddenStems(pillarKey)" :key="qiIdx">
                   <div
                    class="w-4 h-4 rounded-sm flex items-center justify-center text-[6px] font-bold transition-all"
                    :class="[
                     qiIdx === story.hidden_position ? 'ring-2 ring-blue-500 shadow-md scale-110 z-10' : 'opacity-50'
                    ]"
                    :style="{ backgroundColor: qi.hex_color, color: '#1f2937' }"
                    :title="`${qi.stem_chinese} ${qi.stem} (${qi.element})`">
                    {{ qi.stem_chinese }}
                   </div>
                  </template>
                 </div>
                </div>
               </div>
              </template>
             </div>

             <!-- Unit Info -->
             <div class="flex-1 min-w-0">
              <div class="flex items-center gap-2 flex-wrap">
               <span class="text-lg font-bold" :style="{ color: getElementHexColor(story.element) }">
                {{ story.stem_chinese }}
               </span>
               <span class="text-sm text-gray-700">{{ story.stem }}</span>
               <span class="px-1.5 py-0.5 rounded text-[9px] font-medium"
                  :class="getTenGodBadgeClass(story.ten_god_id)">
                {{ story.ten_god }} {{ story.ten_god_english }}
               </span>
              </div>
              <div class="text-[10px] text-gray-500 mt-0.5">
               {{ getNodeLabel(nodeId) }}{{ story.hidden_position !== undefined ? ' Hidden Stem' : '' }} · {{ story.element }} {{ story.polarity }}
              </div>
             </div>

             <!-- Qi Summary -->
             <div class="text-right flex-shrink-0">
              <div class="text-sm font-bold" :class="story.final_qi >= story.initial_qi ? 'text-green-600' : 'text-red-600'">
               {{ story.final_qi?.toFixed(1) }}
              </div>
              <div class="text-[9px] text-gray-500">
               from {{ story.initial_qi?.toFixed(1) }}
              </div>
              <div class="text-[9px]" :class="(story.final_qi - story.initial_qi) >= 0 ? 'text-green-500' : 'text-red-500'">
               {{ (story.final_qi - story.initial_qi) >= 0 ? '+' : '' }}{{ (story.final_qi - story.initial_qi)?.toFixed(1) }}
              </div>
             </div>
            </div>

            <!-- Event Timeline -->
            <div v-if="story.events && story.events.length > 0" class="mt-2 border-t border-gray-100 pt-2">
             <div class="text-[9px] text-gray-500 mb-1.5 font-medium">Event Timeline ({{ story.events.length }} events)</div>
             <div class="relative pl-3 space-y-1.5">
              <!-- Timeline line -->
              <div class="absolute left-[5px] top-1 bottom-1 w-[2px] bg-gradient-to-b from-gray-300 via-gray-200 to-gray-100 rounded-full"></div>

              <div v-for="(event, evtIdx) in story.events" :key="evtIdx"
                 class="relative flex items-start gap-2 text-[9px]">
               <!-- Timeline dot -->
               <div class="absolute left-[-8px] top-1 w-2 h-2 rounded-full border-2 border-white shadow-sm"
                  :class="getEventDotClass(event)"></div>

               <!-- Event content -->
               <div class="flex-1 pl-2 py-0.5 rounded bg-gray-50/50">
                <div class="flex items-center gap-1.5 flex-wrap">
                 <!-- Event type icon -->
                 <span class="font-medium" :class="getEventTypeClass(event)">
                  {{ getEventIcon(event) }}
                 </span>
                 <!-- Event description -->
                 <span class="text-gray-700">{{ getEventDescription(event) }}</span>
                </div>
                <!-- Qi change -->
                <div v-if="event.qi_change !== undefined && event.qi_change !== 0"
                   class="text-[8px] mt-0.5"
                   :class="event.qi_change >= 0 ? 'text-green-600' : 'text-red-600'">
                 {{ event.qi_change >= 0 ? '+' : '' }}{{ event.qi_change?.toFixed(1) }} qi
                 <span v-if="event.qi_before !== undefined" class="text-gray-400">
                  ({{ event.qi_before?.toFixed(1) }} → {{ event.qi_after?.toFixed(1) }})
                 </span>
                </div>
               </div>
              </div>
             </div>
            </div>

            <!-- Narrative Summary -->
            <div v-if="story.narrative" class="mt-2 pt-2 border-t border-gray-100">
             <div class="text-[9px] text-gray-600 italic leading-relaxed">{{ story.narrative }}</div>
            </div>
           </div>
          </template>
         </div>
        </div>
       </div>
      </div>

      <!-- Palace Danger/Fortune Analysis (宮位吉凶分析) -->
      <div v-if="chartData?.palace_summary && chartData.palace_summary.length > 0" 
         class="mt-4 p-4 bg-gradient-to-r from-slate-50 to-gray-50 border border-slate-200 max-w-2xl rounded-lg">
       <div class="flex items-center justify-between mb-3">
        <div class="text-sm font-bold text-gray-800">🏛️ 宮位吉凶 Palace Analysis</div>
        <div class="text-[10px] text-gray-500">Life areas affected by current period</div>
       </div>
       
       <!-- Palace Cards Grid -->
       <div class="grid grid-cols-2 md:grid-cols-4 gap-2">
        <div v-for="palace in chartData.palace_summary" 
           :key="palace.palace"
           class="p-2 rounded-lg border-2 transition-all hover:shadow-md cursor-pointer"
           :class="getPalaceCardClass(palace)"
           @click="togglePalaceDetail(palace.palace)">
         
         <!-- Palace Header -->
         <div class="flex items-center justify-between mb-1">
          <span class="text-lg font-bold" :class="getPalaceTextClass(palace)">
           {{ getPalaceEmoji(palace.palace) }}
          </span>
          <span class="text-lg font-bold" :class="getPalaceStatusTextClass(palace)">
           {{ palace.status_chinese }}
          </span>
         </div>
         
         <!-- Palace Name -->
         <div class="text-xs font-semibold text-gray-800 capitalize">{{ palace.palace }}</div>
         
         <!-- Primary Person -->
         <div class="text-[10px] text-gray-600 capitalize">{{ palace.primary_person }}</div>
         
         <!-- Score Bar -->
         <div class="mt-1.5 h-1.5 bg-gray-200 rounded-full overflow-hidden">
          <div 
           class="h-full rounded-full transition-all"
           :class="getScoreBarClass(palace.net_score)"
           :style="{ width: getScoreBarWidth(palace.net_score) }">
          </div>
         </div>
         
         <!-- Score Value -->
         <div class="text-[9px] mt-0.5" :class="palace.net_score >= 0 ? 'text-green-600' : 'text-red-600'">
          {{ palace.net_score >= 0 ? '+' : '' }}{{ palace.net_score }}
         </div>
        </div>
       </div>
       
       <!-- Expanded Palace Details -->
       <div v-if="expandedPalace && chartData.palace_analysis" class="mt-3 pt-3 border-t border-slate-200">
        <div v-if="chartData.palace_analysis[expandedPalace]" class="space-y-2">
         <!-- Palace Header -->
         <div class="flex items-center gap-2">
          <span class="text-xl">{{ getPalaceEmoji(expandedPalace) }}</span>
          <div>
           <div class="text-sm font-bold capitalize">{{ expandedPalace }} Palace</div>
           <div class="text-[10px] text-gray-600">
            {{ chartData.palace_analysis[expandedPalace].chinese }} - 
            {{ chartData.palace_analysis[expandedPalace].people_affected.primary }}
           </div>
          </div>
         </div>
         
         <!-- Warnings -->
         <div v-if="chartData.palace_analysis[expandedPalace].insights.warnings.length > 0" 
            class="space-y-1">
          <div v-for="(warning, idx) in chartData.palace_analysis[expandedPalace].insights.warnings" 
             :key="'warn-' + idx"
             class="p-2 rounded text-[10px]"
             :class="warning.severity === 'critical' ? 'bg-red-100 border border-red-300' : 'bg-yellow-50 border border-yellow-300'">
           <div class="flex items-start gap-1">
            <span class="text-sm">{{ warning.severity === 'critical' ? '🚨' : '⚠️' }}</span>
            <div>
             <div class="font-bold" :class="warning.severity === 'critical' ? 'text-red-700' : 'text-yellow-700'">
              {{ warning.chinese }} {{ warning.message }}
             </div>
             <div v-if="warning.health_implication" class="mt-0.5 text-gray-700">
              💊 {{ warning.health_implication }}
             </div>
             <div v-if="warning.detail" class="mt-0.5 text-gray-600 italic">
              {{ warning.detail }}
             </div>
            </div>
           </div>
          </div>
         </div>
         
         <!-- Opportunities -->
         <div v-if="chartData.palace_analysis[expandedPalace].insights.opportunities.length > 0"
            class="space-y-1">
          <div v-for="(opp, idx) in chartData.palace_analysis[expandedPalace].insights.opportunities"
             :key="'opp-' + idx"
             class="p-2 rounded bg-green-50 border border-green-300 text-[10px]">
           <div class="flex items-start gap-1">
            <span class="text-sm">✨</span>
            <div>
             <div class="font-bold text-green-700">{{ opp.chinese }} {{ opp.message }}</div>
             <div v-if="opp.benefit" class="mt-0.5 text-gray-700">{{ opp.benefit }}</div>
            </div>
           </div>
          </div>
         </div>
         
         <!-- Transformation Events -->
         <div v-if="chartData.palace_analysis[expandedPalace].transformation_events.length > 0"
            class="space-y-1">
          <div class="text-[10px] font-semibold text-gray-700">Transformation Events:</div>
          <div v-for="(trans, idx) in chartData.palace_analysis[expandedPalace].transformation_events"
             :key="'trans-' + idx"
             class="p-2 rounded bg-purple-50 border border-purple-300 text-[10px]">
           <div class="font-bold text-purple-700">{{ trans.chinese }} {{ trans.pattern }}</div>
           <div class="text-gray-600">{{ trans.message }}</div>
          </div>
         </div>
         
         <!-- Summary -->
         <div v-if="chartData.palace_analysis[expandedPalace].insights.summary.length > 0"
            class="pt-2 border-t border-slate-200">
          <div v-for="(sum, idx) in chartData.palace_analysis[expandedPalace].insights.summary"
             :key="'sum-' + idx"
             class="p-2 rounded text-[10px]"
             :class="getSummaryClass(sum.level)">
           <div class="font-bold">{{ sum.message }}</div>
           <div class="mt-0.5 text-gray-700">{{ sum.recommendation }}</div>
          </div>
         </div>
        </div>
       </div>
       
       <!-- Click hint -->
       <div class="mt-2 text-[9px] text-gray-400 text-center">
        Click a palace card to see detailed analysis
       </div>
      </div>
    </div>
   </div>
    </div>
   </div>
  
   <!-- Wu Xing Element Chart - Sticky bottom panel (future: tabbed for multiple analyses) -->
   <div
    v-if="chartData?.daymaster_analysis"
    class="wuxing-footer sticky bottom-0"
   >
   <div class="wuxing-footer-inner">
    <div class="flex items-center justify-between mb-1.5">
     <h3 class="text-xs font-semibold text-gray-800">五行 Wu Xing Elements</h3>
    </div>
    <!-- Side-by-side Natal vs Post comparison -->
    <div class="grid grid-cols-2 gap-3">
     <!-- Natal Column -->
     <div>
      <div class="flex items-center justify-between text-[10px] text-purple-700 mb-1">
       <span class="font-medium">Natal</span>
       <span class="text-gray-500">{{ Math.round(natalTotal) }}%</span>
      </div>
      <div class="space-y-1">
       <div v-for="element in fiveElementsWithRelations" :key="'natal-' + element.name">
        <div class="flex justify-between items-center text-[10px] mb-0.5">
         <div class="flex items-center gap-1">
          <span :style="getElementTextStyle(element.name)" class="font-medium">{{ element.name }}</span>
          <span v-if="element.relationship" class="text-[8px] px-0.5 py-0 bg-gray-100 text-gray-600">{{ element.relationship }}</span>
         </div>
         <span class="text-gray-500 text-[9px]">{{ Math.round(element.natal) }}%</span>
        </div>
        <div class="relative h-3 bg-gray-100 overflow-hidden">
         <div class="absolute inset-0 flex"><div class="w-1/5 border-r border-gray-200"></div><div class="w-1/5 border-r border-gray-200"></div><div class="w-1/5 border-r border-gray-200"></div><div class="w-1/5 border-r border-gray-200"></div><div class="w-1/5"></div></div>
         <!-- Yang bar (solid, darker) -->
         <div class="absolute top-0 left-0 h-full transition-all duration-500" :style="{ ...getYangBgStyle(element.name), width: `${Math.min((element.yangNatal / maxElementScore) * 100, 100)}%` }" :title="`Yang: ${Math.round(element.yangNatalRaw)}`"></div>
         <!-- Yin bar (striped, lighter) stacked after Yang -->
         <div v-if="element.yinNatal > 0" class="absolute top-0 h-full transition-all duration-500" :style="{ ...getYinBgStyle(element.name), left: `${Math.min((element.yangNatal / maxElementScore) * 100, 100)}%`, width: `${Math.min((element.yinNatal / maxElementScore) * 100, 100)}%` }" :title="`Yin: ${Math.round(element.yinNatalRaw)}`"></div>
        </div>
       </div>
      </div>
     </div>
     <!-- Post Column -->
     <div>
      <div class="flex items-center justify-between text-[10px] text-indigo-700 mb-1">
       <span class="font-medium">Post</span>
       <span class="text-gray-500">{{ Math.round(finalTotal) }}%</span>
      </div>
      <div class="space-y-1">
       <div v-for="element in fiveElementsWithRelations" :key="'post-' + element.name">
        <div class="flex justify-between items-center text-[10px] mb-0.5">
         <div class="flex items-center gap-1">
          <span :style="getElementTextStyle(element.name)" class="font-medium">{{ element.name }}</span>
          <!-- Change indicator -->
          <span v-if="element.postChange > 0" class="text-[8px] px-0.5 py-0 bg-green-50 text-green-600">+{{ Math.round(element.postChange) }}%</span>
          <span v-else-if="element.postChange < 0" class="text-[8px] px-0.5 py-0 bg-red-50 text-red-600">{{ Math.round(element.postChange) }}%</span>
         </div>
         <span class="text-gray-500 text-[9px]">{{ Math.round(element.final) }}%</span>
        </div>
        <div class="relative h-3 bg-gray-100 overflow-hidden">
         <div class="absolute inset-0 flex"><div class="w-1/5 border-r border-gray-200"></div><div class="w-1/5 border-r border-gray-200"></div><div class="w-1/5 border-r border-gray-200"></div><div class="w-1/5 border-r border-gray-200"></div><div class="w-1/5"></div></div>
         <!-- Show natal as ghost bar for comparison -->
         <div class="absolute top-0 left-0 h-full transition-all duration-500 opacity-20" :style="{ ...getElementBgStyle(element.name), width: `${Math.min((element.natal / maxElementScore) * 100, 100)}%` }"></div>
         <!-- Yang bar (solid, darker) -->
         <div class="absolute top-0 left-0 h-full transition-all duration-500" :style="{ ...getYangBgStyle(element.name), width: `${Math.min((element.yangFinal / maxElementScore) * 100, 100)}%` }" :title="`Yang: ${Math.round(element.yangFinalRaw)}`"></div>
         <!-- Yin bar (striped, lighter) stacked after Yang -->
         <div v-if="element.yinFinal > 0" class="absolute top-0 h-full transition-all duration-500" :style="{ ...getYinBgStyle(element.name), left: `${Math.min((element.yangFinal / maxElementScore) * 100, 100)}%`, width: `${Math.min((element.yinFinal / maxElementScore) * 100, 100)}%` }" :title="`Yin: ${Math.round(element.yinFinalRaw)}`"></div>
        </div>
       </div>
      </div>
     </div>
    </div>
   </div>
   </div>
  </main>

 </div>
</template>

<script setup>
import { ref, shallowRef, markRaw, computed, onMounted, watch, nextTick } from 'vue'

// API Base URL - uses environment variable for Capacitor native apps
const API_BASE_URL = import.meta.env.VITE_API_URL || ''

// LocalStorage keys
const STORAGE_KEY = 'bazingse_form_data'

// Helper to load from localStorage
function loadFromStorage() {
 if (typeof window === 'undefined') return null
 try {
  const saved = localStorage.getItem(STORAGE_KEY)
  return saved ? JSON.parse(saved) : null
 } catch (e) {
  console.error('Error loading from localStorage:', e)
  return null
 }
}

// Helper to save to localStorage
function saveToStorage() {
 if (typeof window === 'undefined') return
 try {
  const data = {
   birthDate: birthDate.value,
   birthTime: birthTime.value,
   gender: gender.value,
   unknownHour: unknownHour.value,
   yearInput: yearInput.value,
   monthInput: monthInput.value,
   dayInput: dayInput.value,
   analysisYear: analysisYear.value,
   analysisMonth: analysisMonth.value,
   analysisDay: analysisDay.value,
   analysisTime: analysisTime.value,
   showAnalysisPeriod: showAnalysisPeriod.value,
   includeAnnualLuck: includeAnnualLuck.value,
   includeMonthlyLuck: includeMonthlyLuck.value,
   includeDailyLuck: includeDailyLuck.value,
   includeHourlyLuck: includeHourlyLuck.value,
   showTalismans: showTalismans.value,
   talismanYearHS: talismanYearHS.value,
   talismanYearEB: talismanYearEB.value,
   talismanMonthHS: talismanMonthHS.value,
   talismanMonthEB: talismanMonthEB.value,
   talismanDayHS: talismanDayHS.value,
   talismanDayEB: talismanDayEB.value,
   talismanHourHS: talismanHourHS.value,
   talismanHourEB: talismanHourEB.value,
   showLocation: showLocation.value,
   locationType: locationType.value,
   viewMode: viewMode.value
  }
  localStorage.setItem(STORAGE_KEY, JSON.stringify(data))
 } catch (e) {
  console.error('Error saving to localStorage:', e)
 }
}

// Load saved values or use defaults
const savedData = loadFromStorage()

// Quick test presets
const testPresets = [
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
 { date: '1910-12-06', time: '19:00', gender: 'male' }
]

// Heavenly Stems for dropdowns (10 stems)
const HEAVENLY_STEMS_LIST = [
  { id: 'Jia', display: '甲 Jia (Yang Wood)' },
  { id: 'Yi', display: '乙 Yi (Yin Wood)' },
  { id: 'Bing', display: '丙 Bing (Yang Fire)' },
  { id: 'Ding', display: '丁 Ding (Yin Fire)' },
  { id: 'Wu', display: '戊 Wu (Yang Earth)' },
  { id: 'Ji', display: '己 Ji (Yin Earth)' },
  { id: 'Geng', display: '庚 Geng (Yang Metal)' },
  { id: 'Xin', display: '辛 Xin (Yin Metal)' },
  { id: 'Ren', display: '壬 Ren (Yang Water)' },
  { id: 'Gui', display: '癸 Gui (Yin Water)' }
]

// Earthly Branches for dropdowns (12 branches)
const EARTHLY_BRANCHES_LIST = [
  { id: 'Zi', display: '子 Zi (Rat)' },
  { id: 'Chou', display: '丑 Chou (Ox)' },
  { id: 'Yin', display: '寅 Yin (Tiger)' },
  { id: 'Mao', display: '卯 Mao (Rabbit)' },
  { id: 'Chen', display: '辰 Chen (Dragon)' },
  { id: 'Si', display: '巳 Si (Snake)' },
  { id: 'Wu', display: '午 Wu (Horse)' },
  { id: 'Wei', display: '未 Wei (Goat)' },
  { id: 'Shen', display: '申 Shen (Monkey)' },
  { id: 'You', display: '酉 You (Rooster)' },
  { id: 'Xu', display: '戌 Xu (Dog)' },
  { id: 'Hai', display: '亥 Hai (Pig)' }
]

// 60 Jia-Zi combinations (traditional order) - for validation
const JIAZI_60 = [
  { stem: 'Jia', branch: 'Zi', display: '甲子 Jia-Zi' },
  { stem: 'Yi', branch: 'Chou', display: '乙丑 Yi-Chou' },
  { stem: 'Bing', branch: 'Yin', display: '丙寅 Bing-Yin' },
  { stem: 'Ding', branch: 'Mao', display: '丁卯 Ding-Mao' },
  { stem: 'Wu', branch: 'Chen', display: '戊辰 Wu-Chen' },
  { stem: 'Ji', branch: 'Si', display: '己巳 Ji-Si' },
  { stem: 'Geng', branch: 'Wu', display: '庚午 Geng-Wu' },
  { stem: 'Xin', branch: 'Wei', display: '辛未 Xin-Wei' },
  { stem: 'Ren', branch: 'Shen', display: '壬申 Ren-Shen' },
  { stem: 'Gui', branch: 'You', display: '癸酉 Gui-You' },
  { stem: 'Jia', branch: 'Xu', display: '甲戌 Jia-Xu' },
  { stem: 'Yi', branch: 'Hai', display: '乙亥 Yi-Hai' },
  { stem: 'Bing', branch: 'Zi', display: '丙子 Bing-Zi' },
  { stem: 'Ding', branch: 'Chou', display: '丁丑 Ding-Chou' },
  { stem: 'Wu', branch: 'Yin', display: '戊寅 Wu-Yin' },
  { stem: 'Ji', branch: 'Mao', display: '己卯 Ji-Mao' },
  { stem: 'Geng', branch: 'Chen', display: '庚辰 Geng-Chen' },
  { stem: 'Xin', branch: 'Si', display: '辛巳 Xin-Si' },
  { stem: 'Ren', branch: 'Wu', display: '壬午 Ren-Wu' },
  { stem: 'Gui', branch: 'Wei', display: '癸未 Gui-Wei' },
  { stem: 'Jia', branch: 'Shen', display: '甲申 Jia-Shen' },
  { stem: 'Yi', branch: 'You', display: '乙酉 Yi-You' },
  { stem: 'Bing', branch: 'Xu', display: '丙戌 Bing-Xu' },
  { stem: 'Ding', branch: 'Hai', display: '丁亥 Ding-Hai' },
  { stem: 'Wu', branch: 'Zi', display: '戊子 Wu-Zi' },
  { stem: 'Ji', branch: 'Chou', display: '己丑 Ji-Chou' },
  { stem: 'Geng', branch: 'Yin', display: '庚寅 Geng-Yin' },
  { stem: 'Xin', branch: 'Mao', display: '辛卯 Xin-Mao' },
  { stem: 'Ren', branch: 'Chen', display: '壬辰 Ren-Chen' },
  { stem: 'Gui', branch: 'Si', display: '癸巳 Gui-Si' },
  { stem: 'Jia', branch: 'Wu', display: '甲午 Jia-Wu' },
  { stem: 'Yi', branch: 'Wei', display: '乙未 Yi-Wei' },
  { stem: 'Bing', branch: 'Shen', display: '丙申 Bing-Shen' },
  { stem: 'Ding', branch: 'You', display: '丁酉 Ding-You' },
  { stem: 'Wu', branch: 'Xu', display: '戊戌 Wu-Xu' },
  { stem: 'Ji', branch: 'Hai', display: '己亥 Ji-Hai' },
  { stem: 'Geng', branch: 'Zi', display: '庚子 Geng-Zi' },
  { stem: 'Xin', branch: 'Chou', display: '辛丑 Xin-Chou' },
  { stem: 'Ren', branch: 'Yin', display: '壬寅 Ren-Yin' },
  { stem: 'Gui', branch: 'Mao', display: '癸卯 Gui-Mao' },
  { stem: 'Jia', branch: 'Chen', display: '甲辰 Jia-Chen' },
  { stem: 'Yi', branch: 'Si', display: '乙巳 Yi-Si' },
  { stem: 'Bing', branch: 'Wu', display: '丙午 Bing-Wu' },
  { stem: 'Ding', branch: 'Wei', display: '丁未 Ding-Wei' },
  { stem: 'Wu', branch: 'Shen', display: '戊申 Wu-Shen' },
  { stem: 'Ji', branch: 'You', display: '己酉 Ji-You' },
  { stem: 'Geng', branch: 'Xu', display: '庚戌 Geng-Xu' },
  { stem: 'Xin', branch: 'Hai', display: '辛亥 Xin-Hai' },
  { stem: 'Ren', branch: 'Zi', display: '壬子 Ren-Zi' },
  { stem: 'Gui', branch: 'Chou', display: '癸丑 Gui-Chou' },
  { stem: 'Jia', branch: 'Yin', display: '甲寅 Jia-Yin' },
  { stem: 'Yi', branch: 'Mao', display: '乙卯 Yi-Mao' },
  { stem: 'Bing', branch: 'Chen', display: '丙辰 Bing-Chen' },
  { stem: 'Ding', branch: 'Si', display: '丁巳 Ding-Si' },
  { stem: 'Wu', branch: 'Wu', display: '戊午 Wu-Wu' },
  { stem: 'Ji', branch: 'Wei', display: '己未 Ji-Wei' },
  { stem: 'Geng', branch: 'Shen', display: '庚申 Geng-Shen' },
  { stem: 'Xin', branch: 'You', display: '辛酉 Xin-You' },
  { stem: 'Ren', branch: 'Xu', display: '壬戌 Ren-Xu' },
  { stem: 'Gui', branch: 'Hai', display: '癸亥 Gui-Hai' }
]

// Validation: Check if HS+EB combination is valid Jia-Zi pair
function isValidJiaziPair(hs, eb) {
  // If either is null, it's valid (partial selection allowed)
  if (!hs || !eb) return true

  // Check if the combination exists in JIAZI_60
  return JIAZI_60.some(pair => pair.stem === hs && pair.branch === eb)
}

// Validation: Check if a date is valid (handles leap years, month lengths)
function isValidDate(year, month, day) {
  // Basic range checks
  if (!year || !month || !day) return false
  if (month < 1 || month > 12) return false
  if (day < 1 || day > 31) return false
  if (year < 1900 || year > 2100) return false

  // Create date and check if it's valid
  const date = new Date(year, month - 1, day)
  return date.getFullYear() === year &&
         date.getMonth() === month - 1 &&
         date.getDate() === day
}

// Computed: Check if current birth date inputs are valid
const isValidBirthDate = computed(() => {
  return isValidDate(yearInput.value, monthInput.value, dayInput.value)
})

// Helper: Map luck pillar display index to backend position for node IDs
// Display: [0=HourLuck, 1=DayLuck, 2=MonthLuck, 3=AnnualLuck, 4=10YLuck]
// Backend: [8=HourLuck, 7=DayLuck, 6=MonthLuck, 5=AnnualLuck, 4=10YLuck]
function getLuckPosition(displayIndex) {
 const positions = [8, 7, 6, 5, 4]
 return positions[displayIndex] ?? displayIndex
}

// Computed: Check if any talisman pair is invalid
const hasInvalidTalismanPairs = computed(() => {
  return !isValidJiaziPair(talismanYearHS.value, talismanYearEB.value) ||
         !isValidJiaziPair(talismanMonthHS.value, talismanMonthEB.value) ||
         !isValidJiaziPair(talismanDayHS.value, talismanDayEB.value) ||
         !isValidJiaziPair(talismanHourHS.value, talismanHourEB.value)
})

// Form data
const birthDate = ref(savedData?.birthDate || '1992-07-06')
const birthTime = ref(savedData?.birthTime || '09:30')
const gender = ref(savedData?.gender || 'female')
const isLoading = ref(false)
const chartData = ref(null) // Keep as ref for reactivity
const chartGeneration = ref(0) // Generation counter to force minimal re-renders
const currentLuckPillar = ref(null) // Current 10-year luck pillar

// Valid year range for analysis: birth year to birth year + 120
const minAnalysisYear = computed(() => {
 if (!birthDate.value) return 1900
 return new Date(birthDate.value).getFullYear()
})
const maxAnalysisYear = computed(() => {
 if (!birthDate.value) return 2100
 return new Date(birthDate.value).getFullYear() + 120
})
const annualLuckPillar = ref(null) // Current annual luck pillar
const unknownHour = ref(savedData?.unknownHour || false)

// Individual pillar inputs
const yearInput = ref(savedData?.yearInput || 1992)
const monthInput = ref(savedData?.monthInput || 7)
const dayInput = ref(savedData?.dayInput || 6)

// Analysis period controls (for time travel functionality)
const analysisYear = ref(savedData?.analysisYear || null)
const analysisMonth = ref(savedData?.analysisMonth || null)
const analysisDay = ref(savedData?.analysisDay || null)
const analysisTime = ref(savedData?.analysisTime || '')
const showAnalysisPeriod = ref(savedData?.showAnalysisPeriod || false)
const includeAnnualLuck = ref(savedData?.includeAnnualLuck !== undefined ? savedData.includeAnnualLuck : true)
const includeMonthlyLuck = ref(savedData?.includeMonthlyLuck !== undefined ? savedData.includeMonthlyLuck : true)
const includeDailyLuck = ref(savedData?.includeDailyLuck !== undefined ? savedData.includeDailyLuck : true)
const includeHourlyLuck = ref(savedData?.includeHourlyLuck !== undefined ? savedData.includeHourlyLuck : true)

// Talisman selection (符) - Separate HS and EB selection
const showTalismans = ref(savedData?.showTalismans || false)
const talismanYearHS = ref(savedData?.talismanYearHS || null)
const talismanYearEB = ref(savedData?.talismanYearEB || null)
const talismanMonthHS = ref(savedData?.talismanMonthHS || null)
const talismanMonthEB = ref(savedData?.talismanMonthEB || null)
const talismanDayHS = ref(savedData?.talismanDayHS || null)
const talismanDayEB = ref(savedData?.talismanDayEB || null)
const talismanHourHS = ref(savedData?.talismanHourHS || null)
const talismanHourEB = ref(savedData?.talismanHourEB || null)

// Location (overseas/birthplace) - Residence status
const showLocation = ref(savedData?.showLocation || false)
const locationType = ref(savedData?.locationType || null) // 'overseas' or 'birthplace'

// Unit Tracker Timeline UI state
const showUnitTracker = ref(false)  // Main timeline collapsed by default
const showUnitStories = ref(false)  // Unit narratives collapsed by default
const expandedPhases = ref({})      // Track which phases are expanded
const expandedCalculations = ref({}) // Track which calculation details are expanded

// Toggle phase expansion
function togglePhase(phaseId) {
  expandedPhases.value[phaseId] = !expandedPhases.value[phaseId]
}

// Toggle calculation details expansion
function toggleCalculationDetails(calcId) {
  expandedCalculations.value[calcId] = !expandedCalculations.value[calcId]
}

// Get Ten God badge styling - uses API mappings
function getTenGodBadgeStyle(tenGodId) {
  const styling = chartData.value?.mappings?.ten_gods_styling?.[tenGodId]
  if (styling) {
    const style = {
      backgroundColor: styling.bg_hex,
      color: styling.hex_color,
    }
    // Add border for Day Master
    if (tenGodId === 'DM') {
      style.border = `1px solid ${styling.hex_color}`
    }
    return style
  }
  // Fallback
  return { backgroundColor: '#f3f4f6', color: '#4b5563' }
}

// Get Ten God badge class (legacy, for gradual migration)
function getTenGodBadgeClass(tenGodId) {
  // Return minimal class since we now use inline styles via getTenGodBadgeStyle
  return ''
}

// ========== Mini-Pillar Visualization Helpers (Unit Narratives) ==========

// Get mini pillar style (background color based on element)
function getMiniPillarStyle(pillarKey, type, focusedNodeId) {
  if (!chartData.value?.mappings) return { backgroundColor: '#e5e7eb' }

  const nodeId = `${type}_${pillarKey}`
  let stemName = null

  // Get stem name from chart data
  if (type === 'hs') {
    stemName = chartData.value?.[nodeId]?.id
  } else {
    // For EB, get the branch name and use its element color
    const branchName = chartData.value?.[nodeId]?.id
    const branchData = chartData.value?.mappings?.earthly_branches?.[branchName]
    return {
      backgroundColor: branchData?.hex_color || '#e5e7eb',
      color: '#1f2937'
    }
  }

  const stemData = chartData.value?.mappings?.heavenly_stems?.[stemName]
  return {
    backgroundColor: stemData?.hex_color || '#e5e7eb',
    color: '#1f2937'
  }
}

// Get mini pillar Chinese character
function getMiniPillarChinese(pillarKey, type) {
  if (!chartData.value) return '-'

  const nodeId = `${type}_${pillarKey}`
  const nodeName = chartData.value?.[nodeId]?.id

  if (!nodeName) return '-'

  if (type === 'hs') {
    return chartData.value?.mappings?.heavenly_stems?.[nodeName]?.chinese || nodeName.charAt(0)
  } else {
    return chartData.value?.mappings?.earthly_branches?.[nodeName]?.chinese || nodeName.charAt(0)
  }
}

// Get hidden stems (qi list) for an EB pillar
function getEbHiddenStems(pillarKey) {
  if (!chartData.value?.mappings) return []

  const nodeId = `eb_${pillarKey}`
  const branchName = chartData.value?.[nodeId]?.id

  if (!branchName) return []

  const branchData = chartData.value?.mappings?.earthly_branches?.[branchName]
  return branchData?.qi || []
}

// Get node label for display
function getNodeLabel(nodeId) {
  const labels = {
    'hs_y': 'Year Stem',
    'hs_m': 'Month Stem',
    'hs_d': 'Day Stem',
    'hs_h': 'Hour Stem',
    'eb_y': 'Year Branch',
    'eb_m': 'Month Branch',
    'eb_d': 'Day Branch',
    'eb_h': 'Hour Branch',
    'hs_10yl': '10Y Luck Stem',
    'eb_10yl': '10Y Luck Branch',
    'hs_yl': 'Annual Stem',
    'eb_yl': 'Annual Branch'
  }
  return labels[nodeId] || nodeId
}

// Get element hex color for display - uses API mappings
function getElementHexColor(element) {
  // Use API-provided element colors if available
  const elementData = chartData.value?.mappings?.elements?.[element]
  if (elementData?.hex_color) {
    return elementData.hex_color
  }
  // Fallback to gray if element not found
  return '#6b7280'
}

// Get event type data from API mappings
function getEventTypeData(event) {
  if (!event) return null
  const type = (event.event_type || event.type || event.interaction_type || '').toLowerCase()
  return chartData.value?.mappings?.event_types?.[type] || null
}

// Get event timeline dot style based on event type - uses API mappings
function getEventDotStyle(event) {
  const eventData = getEventTypeData(event)
  if (eventData?.hex_color) {
    return { backgroundColor: eventData.hex_color }
  }
  return { backgroundColor: '#9ca3af' } // gray-400 fallback
}

// Get event timeline dot class based on event type (legacy, for gradual migration)
function getEventDotClass(event) {
  // Return empty string since we now use inline styles via getEventDotStyle
  return ''
}

// Get event type styling - uses API mappings
function getEventTypeStyle(event) {
  const eventData = getEventTypeData(event)
  if (eventData?.hex_color) {
    return { color: eventData.hex_color }
  }
  return { color: '#4b5563' } // gray-600 fallback
}

// Get event type styling class (legacy, for gradual migration)
function getEventTypeClass(event) {
  // Return empty string since we now use inline styles via getEventTypeStyle
  return ''
}

// Get event icon based on type - uses API mappings
function getEventIcon(event) {
  const eventData = getEventTypeData(event)
  if (eventData?.icon) {
    return eventData.icon
  }
  return '•'
}

// Get event description
function getEventDescription(event) {
  if (!event) return ''

  // Use description if available
  if (event.description) return event.description

  const type = event.event_type || event.type || event.interaction_type

  // Build description from event data
  if (type === 'registration') {
    return `Initialized with ${event.qi || event.initial_qi || 100} qi`
  }

  if (type === 'seasonal') {
    const state = event.seasonal_state || 'Unknown'
    const mult = event.multiplier || 1
    return `${state} (×${mult.toFixed(3)})`
  }

  if (type === 'controlled') {
    const partner = event.partner_stem || 'source'
    const tenGod = event.partner_ten_god ? ` (${event.partner_ten_god})` : ''
    return `Controlled by ${partner}${tenGod}, lost ${Math.abs(event.qi_change || 0).toFixed(1)}`
  }

  if (type === 'controlling' || type === 'control' || type === 'CONTROLLING') {
    const partner = event.partner_stem || event.target?.stem || 'target'
    const tenGod = event.partner_ten_god ? ` (${event.partner_ten_god})` : ''
    return `Controlled ${partner}${tenGod}, cost ${Math.abs(event.qi_change || 0).toFixed(1)}`
  }

  if (type === 'produced') {
    const partner = event.partner_stem || 'source'
    const tenGod = event.partner_ten_god ? ` (${event.partner_ten_god})` : ''
    return `Produced by ${partner}${tenGod}, gained ${(event.qi_change || 0).toFixed(1)}`
  }

  if (type === 'producing' || type === 'generation' || type === 'GENERATING') {
    const partner = event.partner_stem || event.target?.stem || 'target'
    const tenGod = event.partner_ten_god ? ` (${event.partner_ten_god})` : ''
    return `Produced ${partner}${tenGod}, cost ${Math.abs(event.qi_change || 0).toFixed(1)}`
  }

  if (type === 'combination') {
    const comboType = event.combination_type?.replace(/_/g, ' ') || 'Combination'
    const element = event.element || ''
    const status = event.is_transformed ? '(Transformed)' : '(Combined)'
    return `${comboType}: ${event.pattern || ''} → ${element} ${status}`
  }

  if (type === 'conflict_aggressor' || type === 'conflict_victim') {
    const conflictType = event.conflict_type || 'Conflict'
    const pattern = event.pattern || ''
    const severity = event.severity ? ` (${event.severity})` : ''
    return `${conflictType}: ${pattern}${severity}`
  }

  if (type === 'conflict') {
    return `Conflict: ${event.pattern || ''}`
  }

  if (type === 'same_element') {
    const relType = event.same_element_type || 'connection'
    const strength = event.strength || 'normal'
    return `${strength} ${relType}`
  }

  return event.phase || type || 'Event'
}

// Calculate grid columns for luck pillars (backward compatibility)
const luckPillarCount = computed(() => {
 let count = 0
 if (currentLuckPillar.value) count++
 if (annualLuckPillar.value) count++
 return count
})

// Total pillar count (dynamic: 4 natal + analysis pillars)
const totalPillarCount = computed(() => {
 // If no chart data yet, return 4 (natal only)
 if (!chartData.value) return 4
 
 let count = 4 // Base natal pillars (hour, day, month, year)
 
 if (chartData.value?.analysis_info) {
  const info = chartData.value.analysis_info
  if (info.has_luck_pillar) count++ // 10-year luck
  if (info.has_annual) count++    // Annual
  if (info.has_monthly) count++   // Monthly
  if (info.has_daily) count++    // Daily
  if (info.has_hourly) count++    // Hourly
 }
 
 // Add talisman pillars (use ty/tm/td/th node IDs)
 if (chartData.value?.hs_ty || chartData.value?.eb_ty) count++ // Talisman year
 if (chartData.value?.hs_tm || chartData.value?.eb_tm) count++ // Talisman month
 if (chartData.value?.hs_td || chartData.value?.eb_td) count++ // Talisman day
 if (chartData.value?.hs_th || chartData.value?.eb_th) count++ // Talisman hour
 
 // Add location pillars (overseas: o1-o2, birthplace: b1-b4)
 if (chartData.value?.hs_o1 || chartData.value?.eb_o1) count++ // Overseas 1
 if (chartData.value?.hs_o2 || chartData.value?.eb_o2) count++ // Overseas 2
 if (chartData.value?.hs_b1 || chartData.value?.eb_b1) count++ // Birthplace 1
 if (chartData.value?.hs_b2 || chartData.value?.eb_b2) count++ // Birthplace 2
 if (chartData.value?.hs_b3 || chartData.value?.eb_b3) count++ // Birthplace 3
 if (chartData.value?.hs_b4 || chartData.value?.eb_b4) count++ // Birthplace 4
 
 // Ensure count is within valid range (4-19 with talismans and location)
 return Math.max(4, Math.min(19, count))
})

// Update birthDate from individual pillar inputs
function updateDateFromPillars() {
 const year = yearInput.value || new Date().getFullYear()
 const month = String(monthInput.value || 1).padStart(2, '0')
 const day = String(dayInput.value || 1).padStart(2, '0')
 birthDate.value = `${year}-${month}-${day}`
}

// Initialize pillar inputs from birthDate
function initializePillarInputs() {
 if (birthDate.value) {
  const [year, month, day] = birthDate.value.split('-')
  yearInput.value = parseInt(year)
  monthInput.value = parseInt(month)
  dayInput.value = parseInt(day)
 }
}

// Debounce timer
let debounceTimer = null

// Save scroll position before updates
let savedScrollPosition = 0

// Handle input changes WITHOUT triggering chart updates
function handleInputChange() {
 updateDateFromPillars()
 // Save to localStorage only
 saveToStorage()
 // DO NOT generate chart - wait for blur event
}

// Trigger chart update INSTANTLY on blur (no debounce)
function triggerChartUpdate() {
 updateDateFromPillars()
 saveToStorage()

 // Validate date before generating chart
 if (!isValidDate(yearInput.value, monthInput.value, dayInput.value)) {
  // Don't generate chart for invalid dates - the UI will show validation state
  return
 }

 // Save current scroll position
 savedScrollPosition = window.scrollY

 // Generate chart IMMEDIATELY - no delays
 generateChart()
}

// Handle unknown hour toggle
function handleUnknownHourChange() {
 if (!unknownHour.value) {
  // Restore to default time when unchecking unknown
  birthTime.value = '12:00'
 }
 triggerChartUpdate()
}

// Load a preset test case
function loadPreset(preset) {
 // Set birth date and time
 birthDate.value = preset.date
 birthTime.value = preset.time
 gender.value = preset.gender
 unknownHour.value = preset.unknownHour || false
 
 // Update individual pillar inputs
 const [year, month, day] = preset.date.split('-')
 yearInput.value = parseInt(year)
 monthInput.value = parseInt(month)
 dayInput.value = parseInt(day)
 
 // Reset time travel mode
 showAnalysisPeriod.value = false
 includeAnnualLuck.value = true
 includeMonthlyLuck.value = false
 includeDailyLuck.value = false
 includeHourlyLuck.value = false
 
 // Clear analysis inputs
 analysisYear.value = null
 analysisMonth.value = null
 analysisDay.value = null
 analysisTime.value = ''
 
 // Save and generate
 saveToStorage()
 generateChart()
}

// Auto-set year to current year when Time Travel is enabled
watch(showAnalysisPeriod, (newValue) => {
 if (newValue && !analysisYear.value) {
  analysisYear.value = new Date().getFullYear()
  handleInputChange()
 }
})

// Auto-fill year when deleted/empty
watch(analysisYear, (newValue) => {
 if (showAnalysisPeriod.value && !newValue) {
  analysisYear.value = new Date().getFullYear()
  handleInputChange()
 }
})

// Watch for cascading resets when toggles are disabled
watch(includeAnnualLuck, (newValue) => {
 if (!newValue) {
  // Clear monthly and all dependent values
  analysisMonth.value = null
  analysisDay.value = null
  analysisTime.value = ''
 }
})

watch(includeMonthlyLuck, (newValue) => {
 if (!newValue) {
  // Clear daily and hourly
  analysisDay.value = null
  analysisTime.value = ''
 }
})

watch(includeDailyLuck, (newValue) => {
 if (!newValue) {
  // Clear hourly
  analysisTime.value = ''
 }
})

// Clear analysis period
function clearAnalysisPeriod() {
 analysisYear.value = null
 analysisMonth.value = null
 analysisDay.value = null
 analysisTime.value = ''
 handleInputChange()
}

// Initialize on mount (client-side only)
onMounted(() => {
 console.log('Component mounted, initializing...')
 initializePillarInputs()

 // Validate stored date - if invalid, reset to defaults
 if (!isValidDate(yearInput.value, monthInput.value, dayInput.value)) {
  console.log('Invalid stored date, resetting to defaults')
  yearInput.value = 1992
  monthInput.value = 7
  dayInput.value = 6
  updateDateFromPillars()
  saveToStorage()
 }

 // Generate initial chart after component mounts
 setTimeout(() => {
  console.log('Calling generateChart from onMounted')
  generateChart()
 }, 100)
})

// Interactive UI state
const hoveredNode = ref(null)
const hoveredInteraction = ref(null)
const highlightedNodes = ref([])
const highlightContext = ref(null) // NEW: Stores interaction context for element-based coloring
const hoveredTransformationId = ref(null) // NEW: Track which transformation is hovered
const activeConnections = ref([])
const showConnections = ref(true)
const tooltipContent = ref(null)
const tooltipPosition = ref({ x: 0, y: 0 })
const expandedPalace = ref(null) // Palace analysis expansion state

// Get pillar label based on index and type
function getPillarLabel(index, pillarType) {
  if (pillarType === 'natal') {
    return ['Hour', 'Day', 'Month', 'Year'][index] || ''
  } else if (pillarType === 'luck') {
    return ['Hourly', 'Daily', 'Monthly', 'Annual', '10Y'][index] || ''
  } else if (pillarType === 'talisman') {
    return ['Hour', 'Day', 'Month', 'Year'][index] || ''
  } else if (pillarType === 'location') {
    return `Location ${index + 1}`
  }
  return ''
}

// View mode state - now always 'post' since Wu Xing shows both Natal and Post side-by-side
// This controls interaction badges and hidden qi display on pillars
const viewMode = ref('post')
const showTransformed = computed(() => true)  // Always show interactions

// Interactions display state
const highlightedInteraction = ref(null)

// Watch for view mode changes
watch(viewMode, () => {
 // Save view mode preference
 saveToStorage()
})

// Stem and Branch mappings
const stemMappings = {
 'Jia': '甲', 'Yi': '乙', 'Bing': '丙', 'Ding': '丁', 'Wu': '戊',
 'Ji': '己', 'Geng': '庚', 'Xin': '辛', 'Ren': '壬', 'Gui': '癸'
}

// Ten God abbreviation to full name mappings
const tenGodMappings = {
 'F': 'Companion',
 'RW': 'Robbery',
 'EG': 'Output',
 'HO': 'Hurting',
 'IW': 'Wealth',
 'DW': 'Direct Wealth',
 '7K': 'Officer',
 'DO': 'Direct Officer',
 'IR': 'Resource',
 'DR': 'Direct Resource',
 // Keep full names as is
 'Companion': 'Companion',
 'Robbery': 'Robbery',
 'Output': 'Output',
 'Hurting': 'Hurting',
 'Wealth': 'Wealth',
 'Direct Wealth': 'Direct Wealth',
 'Officer': 'Officer',
 'Direct Officer': 'Direct Officer',
 'Resource': 'Resource',
 'Direct Resource': 'Direct Resource'
}

// Branch name to Chinese character mappings
const branchMappings = {
 'Zi': '子', 'Chou': '丑', 'Yin': '寅', 'Mao': '卯',
 'Chen': '辰', 'Si': '巳', 'Wu': '午', 'Wei': '未',
 'Shen': '申', 'You': '酉', 'Xu': '戌', 'Hai': '亥'
}

// Branch polarity mappings based on BaZi theory
const branchPolarities = {
 'Zi': 'Yang',  // Yang Water
 'Chou': 'Yin', // Yin Earth
 'Yin': 'Yang', // Yang Wood
 'Mao': 'Yin',  // Yin Wood
 'Chen': 'Yang', // Yang Earth
 'Si': 'Yang',  // Yang Fire
 'Wu': 'Yang',  // Yang Fire
 'Wei': 'Yin',  // Yin Earth
 'Shen': 'Yang', // Yang Metal
 'You': 'Yin',  // Yin Metal
 'Xu': 'Yang',  // Yang Earth
 'Hai': 'Yin'  // Yin Water
}

// Element to Chinese character mappings (for transformed display)
const elementCharacterMappings = {
 'Wood': '木',
 'Fire': '火',
 'Earth': '土',
 'Metal': '金',
 'Water': '水',
 'Yang Wood': '木',
 'Yin Wood': '木',
 'Yang Fire': '火',
 'Yin Fire': '火',
 'Yang Earth': '土',
 'Yin Earth': '土',
 'Yang Metal': '金',
 'Yin Metal': '金',
 'Yang Water': '水',
 'Yin Water': '水'
}

const HEAVENLY_STEMS = {
 'Jia': { chinese: '甲', element: 'Yang Wood' },
 'Yi': { chinese: '乙', element: 'Yin Wood' },
 'Bing': { chinese: '丙', element: 'Yang Fire' },
 'Ding': { chinese: '丁', element: 'Yin Fire' },
 'Wu': { chinese: '戊', element: 'Yang Earth' },
 'Ji': { chinese: '己', element: 'Yin Earth' },
 'Geng': { chinese: '庚', element: 'Yang Metal' },
 'Xin': { chinese: '辛', element: 'Yin Metal' },
 'Ren': { chinese: '壬', element: 'Yang Water' },
 'Gui': { chinese: '癸', element: 'Yin Water' }
}

const EARTHLY_BRANCHES = {
 'Zi': { chinese: '子', animal: 'Rat', element: 'Yang Water' },
 'Chou': { chinese: '丑', animal: 'Ox', element: 'Yin Earth' },
 'Yin': { chinese: '寅', animal: 'Tiger', element: 'Yang Wood' },
 'Mao': { chinese: '卯', animal: 'Rabbit', element: 'Yin Wood' },
 'Chen': { chinese: '辰', animal: 'Dragon', element: 'Yang Earth' },
 'Si': { chinese: '巳', animal: 'Snake', element: 'Yin Fire' },
 'Wu': { chinese: '午', animal: 'Horse', element: 'Yang Fire' },
 'Wei': { chinese: '未', animal: 'Goat', element: 'Yin Earth' },
 'Shen': { chinese: '申', animal: 'Monkey', element: 'Yang Metal' },
 'You': { chinese: '酉', animal: 'Rooster', element: 'Yin Metal' },
 'Xu': { chinese: '戌', animal: 'Dog', element: 'Yang Earth' },
 'Hai': { chinese: '亥', animal: 'Pig', element: 'Yin Water' }
}

// Check if there are transformations
const hasTransformations = computed(() => {
 if (!chartData.value?.nodes) return false
 
 // Check if any node has badges array with transformation items
 for (const node of Object.values(chartData.value.nodes)) {
  if (node.badges && node.badges.some(b => b.type === 'transformation')) return true
 }
 return false
})

// Count number of transformations (total across all nodes)
const transformationCount = computed(() => {
 if (!chartData.value?.nodes) return 0
 
 let count = 0
 for (const node of Object.values(chartData.value.nodes)) {
  if (node.badges && node.badges.length > 0) {
   count += node.badges.filter(b => b.type === 'transformation').length
  }
 }
 return count
})

// Get the active chart (original or transformed)
const activeChart = computed(() => {
 // Since API now returns nodes directly, we don't need natal_chart
 // Return null to force using the nodes-based approach
 return null
})

// Helper to parse pillar (handles both normal and transformed format)
function parsePillarForDisplay(pillarStr, isTransformed = false) {
 const parts = pillarStr.split(' ')
 
 // Handle transformed format like "Bing Fire" where branch is replaced by element
 if (parts.length === 2 && (parts[1] === 'Fire' || parts[1] === 'Water' || parts[1] === 'Wood' || parts[1] === 'Metal' || parts[1] === 'Earth')) {
  const stemName = parts[0]
  const element = parts[1]
  
  // Create a special display for transformed element branches
  return {
   stemName,
   stem: HEAVENLY_STEMS[stemName] || { chinese: stemName, element: 'Unknown' },
   branchName: element,
   branch: {
    chinese: element === 'Fire' ? '火' : element === 'Water' ? '水' : element === 'Wood' ? '木' : element === 'Metal' ? '金' : '土',
    animal: element,
    element: `Yang ${element}` // Default to Yang for transformed elements
   }
  }
 }
 
 // Normal pillar format
 const [stemName, branchName] = parts
 return {
  stemName,
  stem: HEAVENLY_STEMS[stemName] || { chinese: stemName, element: 'Unknown' },
  branchName,
  branch: EARTHLY_BRANCHES[branchName] || { chinese: branchName, animal: branchName, element: 'Unknown' }
 }
}

// Node-based chart data - now directly at top level
const nodes = computed(() => {
 if (!chartData.value) return null
 
 // Extract node data (hs_y, eb_y, etc.) from top level
 const nodeKeys = ['hs_y', 'eb_y', 'hs_m', 'eb_m', 'hs_d', 'eb_d', 'hs_h', 'eb_h', 
          'hs_10yl', 'eb_10yl', 'hs_yl', 'eb_yl',
          'hs_month', 'eb_month', 'hs_day', 'eb_day']
 
 const nodesData = {}
 for (const key of nodeKeys) {
  if (chartData.value[key]) {
   nodesData[key] = chartData.value[key]
  }
 }
 
 return Object.keys(nodesData).length > 0 ? nodesData : null
})

// Get node by ID
function getNode(nodeId) {
 return nodes.value?.[nodeId] || null
}

// Helper function to enrich badge with interaction data
function enrichBadgeWithInteraction(badge) {
 if (!badge || !badge.interaction_id) return badge
 
 // Map size to strength for backward compatibility
 const sizeToStrength = {
  'xs': 'weak',
  'sm': 'normal',
  'md': 'normal',      // Medium = normal
  'lg': 'strong',
  'xl': 'ultra_strong'
 }
 
 // Normalize interaction_id to match the interactions object keys
 // Badge format: HS_COMBINATION_Ding-Ren_hs_h-hs_y
 // Interaction key: STEM_COMBINATION~Ding-Ren~hs_h-hs_y
 let normalizedId = badge.interaction_id
 
 // Replace HS_COMBINATION with STEM_COMBINATION
 normalizedId = normalizedId.replace('HS_COMBINATION', 'STEM_COMBINATION')
 
 // Split by underscore and identify parts
 // Pattern: TYPE_Pattern_nodes where nodes contain underscores
 const parts = normalizedId.split('_')
 if (parts.length >= 3) {
  // Reconstruct: TYPE~Pattern~nodes
  // The first part is the type (may have multiple words joined by underscores)
  // Find where the pattern starts (contains dash or is a node ID)
  let typeEndIndex = 1
  for (let i = 1; i < parts.length; i++) {
   if (parts[i].includes('-') || parts[i].match(/^(hs|eb)$/)) {
    typeEndIndex = i
    break
   }
  }
  const type = parts.slice(0, typeEndIndex).join('_')
  const restParts = parts.slice(typeEndIndex)
  // Find where nodes start (after pattern)
  let patternEndIndex = 0
  for (let i = 0; i < restParts.length; i++) {
   if (restParts[i].match(/^(hs|eb)$/)) {
    patternEndIndex = i
    break
   }
  }
  const pattern = restParts.slice(0, patternEndIndex).join('_')
  const nodes = restParts.slice(patternEndIndex).join('_')
  normalizedId = `${type}~${pattern}~${nodes}`
 }
 
 // Get interaction data from chartData
 const interaction = chartData.value?.interactions?.[normalizedId] || chartData.value?.interactions?.[badge.interaction_id] || {}
 
 return {
  badge: badge.badge || '',
  type: interaction.type || badge.type || '',
  element: interaction.element || '',
  pattern: interaction.pattern || '',
  strength: sizeToStrength[badge.size] || 'normal',
  interaction_id: badge.interaction_id,
  interactionKey: normalizedId,
  tooltip: interaction.description || badge.type || ''
 }
}

// Computed properties
const pillars = computed(() => {
 // Simple direct access to node data as requested
 if (!chartData.value) {
  console.log('pillars computed: no chartData')
  return null
 }
 
 const data = chartData.value
 const mappings = data.mappings || {}
 console.log('pillars computed: has chartData, mappings:', !!mappings)
 
 // Helper to build pillar from node data
 const buildPillar = (hsKey, ebKey, label, isDayMaster = false) => {
  const hsNode = data[hsKey]
  const ebNode = data[ebKey]
  
  if (!hsNode && !ebNode) return null
  
  // Use viewMode to determine which state to show (base or post)
  const usePost = viewMode.value === 'post'
  
  // For stems: always use the base ID for the main character
  // Store badges array and split by type
  const stemId = hsNode?.id
  const stemBadges = usePost ? (hsNode?.badges || []) : []
  const stemTransformations = stemBadges.filter(b => b.type === 'transformation').map(b => enrichBadgeWithInteraction(b))
  const stemCombinations = stemBadges.filter(b => b.type === 'combination').map(b => enrichBadgeWithInteraction(b))
  const stemNegatives = stemBadges.filter(b => ['clash', 'harm', 'punishment', 'destruction', 'stem_conflict'].includes(b.type)).map(b => enrichBadgeWithInteraction(b))
  
  // Check if stem transformed to element name (like "Yang Metal")
  const isElementName = stemId && stemId.includes(' ') && ['Yang', 'Yin'].some(p => stemId.startsWith(p))
  
  let stemChinese, stemElement, stemColor
  
  if (isElementName) {
   // Handle element name transformations - map back to proper stem ID
   const elementToStemMap = {
    'Yang Metal': 'Geng',
    'Yin Metal': 'Xin',
    'Yang Water': 'Ren',
    'Yin Water': 'Gui',
    'Yang Wood': 'Jia',
    'Yin Wood': 'Yi',
    'Yang Fire': 'Bing',
    'Yin Fire': 'Ding',
    'Yang Earth': 'Wu',
    'Yin Earth': 'Ji'
   }
   const actualStemId = elementToStemMap[stemId] || stemId
   const stemMapping = mappings.heavenly_stems?.[actualStemId] || {}
   stemChinese = stemMapping.chinese || actualStemId || '?'
   stemElement = stemMapping.english || stemId
   // Use regular color from mapping for stem transformations
   stemColor = stemMapping.hex_color || hsNode?.hex_color || hsNode?.color || '#808080'
  } else {
   // Normal stem mapping
   const stemMapping = mappings.heavenly_stems?.[stemId] || {}
   stemChinese = stemMapping.chinese || stemId || '?'
   stemElement = stemMapping.english || hsNode?.element || 'Unknown'
   stemColor = stemMapping.hex_color || hsNode?.hex_color || hsNode?.color || '#808080'
  }
  
  const stem = {
   chinese: stemChinese,
   element: stemElement,
   color: stemColor
  }
  
  // Get the proper stem name (pinyin) for display
  let stemName
  if (isElementName) {
   // If it's an element name, get the corresponding stem ID
   const elementToStemMap = {
    'Yang Metal': 'Geng',
    'Yin Metal': 'Xin',
    'Yang Water': 'Ren',
    'Yin Water': 'Gui',
    'Yang Wood': 'Jia',
    'Yin Wood': 'Yi',
    'Yang Fire': 'Bing',
    'Yin Fire': 'Ding',
    'Yang Earth': 'Wu',
    'Yin Earth': 'Ji'
   }
   stemName = elementToStemMap[stemId] || stemId
  } else {
   stemName = stemId || '?'
  }
  
  // For branches: always use the base ID for the main character
  // Store badges array and split by type
  const branchId = ebNode?.id
  const branchBadges = usePost ? (ebNode?.badges || []) : []
  const branchTransformations = branchBadges.filter(b => b.type === 'transformation').map(b => enrichBadgeWithInteraction(b))
  const branchCombinations = branchBadges.filter(b => b.type === 'combination').map(b => enrichBadgeWithInteraction(b))
  const branchNegatives = branchBadges.filter(b => ['clash', 'harm', 'punishment', 'destruction', 'stem_conflict'].includes(b.type)).map(b => enrichBadgeWithInteraction(b))
  const branchWealthStorage = branchBadges.filter(b => b.type === 'wealth_storage').map(b => enrichBadgeWithInteraction(b))
  
  // Check if branch transformed to pure element (Fire, Water, etc)
  const isElementTransformation = usePost && ['Fire', 'Water', 'Metal', 'Wood', 'Earth'].includes(branchId)
  
  let branchChinese, branchAnimal, branchElement, branchColor
  
  if (isElementTransformation) {
   // Handle pure element transformation - use emphasized colors
   const elementMap = {
    'Wood': { chinese: '木', color: '#c2d4be' },  // matches Jia (Yang Wood)
    'Fire': { chinese: '火', color: '#f3adae' },  // matches Bing (Yang Fire)
    'Earth': { chinese: '土', color: '#e6ceb7' }, // matches Wu (Yang Earth)
    'Metal': { chinese: '金', color: '#ccd8e6' }, // matches Geng (Yang Metal)
    'Water': { chinese: '水', color: '#b9cbff' }  // matches Ren (Yang Water)
   }
   branchChinese = elementMap[branchId]?.chinese || branchId
   branchAnimal = branchId // Show element name instead of animal
   branchElement = branchId
   // Use emphasized color for pure element transformations
   branchColor = elementMap[branchId]?.color || '#808080'
  } else {
   // Normal branch mapping
   const branchMapping = mappings.earthly_branches?.[branchId] || {}
   branchChinese = branchMapping.chinese || branchId || '?'
   branchAnimal = branchMapping.animal || '?'
   
   // Map branch ID to element (branches have dominant elements)
   const branchToElement = {
    'Zi': 'Water',  // Rat - Water
    'Chou': 'Earth', // Ox - Earth
    'Yin': 'Wood',  // Tiger - Wood
    'Mao': 'Wood',  // Rabbit - Wood
    'Chen': 'Earth', // Dragon - Earth
    'Si': 'Fire',  // Snake - Fire
    'Wu': 'Fire',  // Horse - Fire
    'Wei': 'Earth', // Goat - Earth
    'Shen': 'Metal', // Monkey - Metal
    'You': 'Metal', // Rooster - Metal
    'Xu': 'Earth',  // Dog - Earth
    'Hai': 'Water'  // Pig - Water
   }
   branchElement = branchToElement[branchId] || 'Unknown'
   branchColor = ebNode?.hex_color || ebNode?.color || branchMapping.hex_color || '#808080'
  }
  
  const branch = {
   chinese: branchChinese,
   animal: branchAnimal,
   element: branchElement,
   color: branchColor
  }
  
  // Hidden stems from eb.qi - use post_interaction_qi for post view, base_qi for base view
  // Check for non-empty objects to properly fall back when one is empty
  const postQi = ebNode?.post_interaction_qi && Object.keys(ebNode.post_interaction_qi).length > 0 ? ebNode.post_interaction_qi : null
  const baseQi = ebNode?.base_qi && Object.keys(ebNode.base_qi).length > 0 ? ebNode.base_qi : null
  const hiddenQi = usePost ? (postQi || baseQi || {}) : (baseQi || {})
  
  // Map hidden stems to Ten Gods using frontend mappings
  const hiddenStems = {}
  if (hiddenQi && data.mappings?.ten_gods) {
   const dayMasterStem = data.hs_d?.id || 'Yi'
   for (const stemName of Object.keys(hiddenQi)) {
    const tenGodData = data.mappings?.ten_gods?.[dayMasterStem]?.[stemName]
    hiddenStems[stemName] = tenGodData?.abbreviation || tenGodData?.id || ''
   }
  }
  
  // Calculate Ten God for the Heavenly Stem
  let stemTenGod = null
  if (isDayMaster) {
   stemTenGod = 'DM'
  } else if (hsNode?.id && data.mappings?.ten_gods) {
   const dayMasterStem = data.hs_d?.id || 'Yi'
   const tenGodData = data.mappings?.ten_gods?.[dayMasterStem]?.[hsNode.id]
   stemTenGod = tenGodData?.abbreviation || tenGodData?.id || null
  }
  
  // Qi Phase (十二長生) - lifecycle stage of stem in this branch
  const qiPhase = hsNode?.qi_phase || ebNode?.qi_phase || null

  return {
   label,
   stem,
   stemName: stemName,
   branch,
   branchName: branchId,
   stemKey: hsKey,
   branchKey: ebKey,
   hiddenStems,
   hiddenQi,
   tenGod: stemTenGod,
   isUnknown: !hsNode && !ebNode,
   // Qi Phase (十二長生)
   qiPhase,
   // Transformation badges
   stemTransformations,
   branchTransformations,
   // Combination badges
   stemCombinations,
   branchCombinations,
    // Negative badges
    stemNegatives,
    branchNegatives,
    // Wealth storage badges
    branchWealthStorage
   }
 }
 
 const yearPillar = buildPillar('hs_y', 'eb_y', 'Year 年')
 const monthPillar = buildPillar('hs_m', 'eb_m', 'Month 月')
 const dayPillar = buildPillar('hs_d', 'eb_d', 'Day 日', true)
 const hourPillar = buildPillar('hs_h', 'eb_h', 'Hour 時')
 
 // Check if we have at least the essential pillars (year, month, day)
 if (!yearPillar || !monthPillar || !dayPillar) {
  return null
 }
 
 const result = {
  year: yearPillar,
  month: monthPillar, 
  day: dayPillar,
  hour: hourPillar || {
   label: 'Hour 時',
   stem: { chinese: '?', element: 'Unknown' },
   stemName: '?',
   branch: { chinese: '?', animal: '?', element: 'Unknown' },
   branchName: '?',
   stemKey: 'hs_h',
   branchKey: 'eb_h',
   hiddenStems: null,
   tenGod: null,
   transformed: false,
   isUnknown: true
  }
 }
 
 console.log('Simplified pillars from direct node access:', result)
 return result
})

// Natal pillars only (4 columns: Hour, Day, Month, Year)
const natalPillarsOrdered = computed(() => {
 if (!pillars.value) return null
 
 return [
  pillars.value.hour,
  pillars.value.day,
  pillars.value.month,
  pillars.value.year
 ]
})

// Luck pillars only (for separate display below natal chart)
const luckPillarsOrdered = computed(() => {
 if (!chartData.value?.mappings) return []
 
 const luckPillars = []
 
 // Add 10-year luck pillar if available
 if (currentLuckPillar.value) {
  const luckPillarStr = currentLuckPillar.value.pillar
  const [hsName, ebName] = luckPillarStr.split(' ')
  const mappings = chartData.value.mappings
  
  const hsMapping = mappings.heavenly_stems?.[hsName] || {}
  const ebMapping = mappings.earthly_branches?.[ebName] || {}
  
  // Get hidden stems from backend node data
  const ebLuckNode = chartData.value?.eb_10yl
  const hsLuckNode = chartData.value?.hs_10yl
  
  // Calculate Ten God for 10Y luck HS
  const dayMasterStem = chartData.value?.hs_d?.id || 'Yi'
  const tenGodData = mappings.ten_gods?.[dayMasterStem]?.[hsName]
  const tenGodLabel = tenGodData?.abbreviation || tenGodData?.id || ''
  
  // Map hidden stems to Ten Gods using frontend mappings (use post_interaction_qi in post view, base_qi in base view)
  const usePost = viewMode.value === 'post' || viewMode.value === 'transformed'
  // Check for non-empty objects to properly fall back when one is empty
  const luckPostQi = ebLuckNode?.post_interaction_qi && Object.keys(ebLuckNode.post_interaction_qi).length > 0 ? ebLuckNode.post_interaction_qi : null
  const luckBaseQi = ebLuckNode?.base_qi && Object.keys(ebLuckNode.base_qi).length > 0 ? ebLuckNode.base_qi : null
  const luckQi = usePost ? (luckPostQi || luckBaseQi || {}) : (luckBaseQi || {})
  const hiddenStems = {}
  if (luckQi && mappings.ten_gods) {
   for (const stemName of Object.keys(luckQi)) {
    const tenGodData = mappings.ten_gods?.[dayMasterStem]?.[stemName]
    hiddenStems[stemName] = tenGodData?.abbreviation || tenGodData?.id || ''
   }
  }
  
  luckPillars.push({
   label: '10Y Luck 運',
   stem: {
    chinese: hsMapping.chinese || hsName,
    element: currentLuckPillar.value.hs_element || hsMapping.english || 'Unknown',
    color: hsMapping.hex_color || '#808080'
   },
   stemName: hsName,
   branch: {
    chinese: ebMapping.chinese || ebName,
    animal: currentLuckPillar.value.eb_animal || ebMapping.animal || 'Unknown',
    element: currentLuckPillar.value.eb_animal || 'Unknown',
    color: ebMapping.hex_color || '#808080'
   },
   branchName: ebName,
   stemKey: 'hs_10yl',
   branchKey: 'eb_10yl',
   hiddenStems: hiddenStems,
   hiddenQi: ebLuckNode?.base_qi || null, // Get hidden stems qi from backend
   tenGod: tenGodLabel,
   isUnknown: false,
   stemTransformations: (hsLuckNode?.badges || []).filter(b => b.type === 'transformation').map(b => enrichBadgeWithInteraction(b)),
   branchTransformations: (ebLuckNode?.badges || []).filter(b => b.type === 'transformation').map(b => enrichBadgeWithInteraction(b)),
   stemCombinations: (hsLuckNode?.badges || []).filter(b => b.type === 'combination').map(b => enrichBadgeWithInteraction(b)),
   branchCombinations: (ebLuckNode?.badges || []).filter(b => b.type === 'combination').map(b => enrichBadgeWithInteraction(b)),
   stemNegatives: (hsLuckNode?.badges || []).filter(b => ['clash', 'harm', 'punishment', 'destruction', 'stem_conflict'].includes(b.type)).map(b => enrichBadgeWithInteraction(b)),
   branchNegatives: (ebLuckNode?.badges || []).filter(b => ['clash', 'harm', 'punishment', 'destruction', 'stem_conflict'].includes(b.type)).map(b => enrichBadgeWithInteraction(b)),
   branchWealthStorage: (ebLuckNode?.badges || []).filter(b => b.type === 'wealth_storage').map(b => enrichBadgeWithInteraction(b)),
   isLuckPillar: true,
   timing: currentLuckPillar.value.timing,
   qiPhase: hsLuckNode?.qi_phase || ebLuckNode?.qi_phase || null
  })
 }
 
 // Add annual luck pillar if available
 if (annualLuckPillar.value && chartData.value?.mappings) {
  const annualPillarStr = annualLuckPillar.value.pillar
  const [hsName, ebName] = annualPillarStr.split(' ')
  const mappings = chartData.value.mappings
  
  const hsMapping = mappings.heavenly_stems?.[hsName] || {}
  const ebMapping = mappings.earthly_branches?.[ebName] || {}
  
  // Get hidden stems from backend node data
  const ebAnnualNode = chartData.value?.eb_yl
  const hsAnnualNode = chartData.value?.hs_yl
  
  // Calculate Ten God for annual luck HS
  const dayMasterStem = chartData.value?.hs_d?.id || 'Yi'
  const tenGodData = mappings.ten_gods?.[dayMasterStem]?.[hsName]
  const tenGodLabel = tenGodData?.abbreviation || tenGodData?.id || ''
  
  // Map hidden stems to Ten Gods using frontend mappings (use post.qi in post view, base.qi in base view)
  const usePost = viewMode.value === 'post' || viewMode.value === 'transformed'
  // Check for non-empty objects to properly fall back when one is empty
  const annualPostQi = ebAnnualNode?.post_interaction_qi && Object.keys(ebAnnualNode.post_interaction_qi).length > 0 ? ebAnnualNode.post_interaction_qi : null
  const annualBaseQi = ebAnnualNode?.base_qi && Object.keys(ebAnnualNode.base_qi).length > 0 ? ebAnnualNode.base_qi : null
  const annualQi = usePost ? (annualPostQi || annualBaseQi || {}) : (annualBaseQi || {})
  const hiddenStems = {}
  if (annualQi && mappings.ten_gods) {
   for (const stemName of Object.keys(annualQi)) {
    const tenGodData = mappings.ten_gods?.[dayMasterStem]?.[stemName]
    hiddenStems[stemName] = tenGodData?.abbreviation || tenGodData?.id || ''
   }
  }
  
  luckPillars.push({
   label: 'Annual 年運',
   stem: {
    chinese: hsMapping.chinese || hsName,
    element: annualLuckPillar.value.hs_element || hsMapping.english || 'Unknown',
    color: hsMapping.hex_color || '#808080'
   },
   stemName: hsName,
   branch: {
    chinese: ebMapping.chinese || ebName,
    animal: annualLuckPillar.value.eb_animal || ebMapping.animal || 'Unknown',
    element: annualLuckPillar.value.eb_animal || 'Unknown',
    color: ebMapping.hex_color || '#808080'
   },
   branchName: ebName,
   stemKey: 'hs_yl',
   branchKey: 'eb_yl',
   hiddenStems: hiddenStems,
   hiddenQi: ebAnnualNode?.base_qi || null, // Get hidden stems qi from backend
   tenGod: tenGodLabel,
   isUnknown: false,
   stemTransformations: (hsAnnualNode?.badges || []).filter(b => b.type === 'transformation').map(b => enrichBadgeWithInteraction(b)),
   branchTransformations: (ebAnnualNode?.badges || []).filter(b => b.type === 'transformation').map(b => enrichBadgeWithInteraction(b)),
   stemCombinations: (hsAnnualNode?.badges || []).filter(b => b.type === 'combination').map(b => enrichBadgeWithInteraction(b)),
   branchCombinations: (ebAnnualNode?.badges || []).filter(b => b.type === 'combination').map(b => enrichBadgeWithInteraction(b)),
   stemNegatives: (hsAnnualNode?.badges || []).filter(b => ['clash', 'harm', 'punishment', 'destruction', 'stem_conflict'].includes(b.type)).map(b => enrichBadgeWithInteraction(b)),
   branchNegatives: (ebAnnualNode?.badges || []).filter(b => ['clash', 'harm', 'punishment', 'destruction', 'stem_conflict'].includes(b.type)).map(b => enrichBadgeWithInteraction(b)),
   branchWealthStorage: (ebAnnualNode?.badges || []).filter(b => b.type === 'wealth_storage').map(b => enrichBadgeWithInteraction(b)),
   isAnnualLuck: true,
   year: annualLuckPillar.value.year,
   qiPhase: hsAnnualNode?.qi_phase || ebAnnualNode?.qi_phase || null
  })
 }
 
 // Extract Monthly Pillar (if available)
 if (chartData.value?.analysis_info?.has_monthly && chartData.value?.hs_ml && chartData.value?.eb_ml) {
  const hsMonthlyNode = chartData.value.hs_ml
  const ebMonthlyNode = chartData.value.eb_ml
  const [hsName, ebName] = [hsMonthlyNode.id, ebMonthlyNode.id]
  
  if (hsName && ebName) {
   const mappings = chartData.value.mappings
   const hsMapping = mappings.heavenly_stems?.[hsName] || {}
   const ebMapping = mappings.earthly_branches?.[ebName] || {}
   
   const dayMasterStem = chartData.value?.hs_d?.id || 'Yi'
   const tenGodData = mappings.ten_gods?.[dayMasterStem]?.[hsName]
   const tenGodLabel = tenGodData?.abbreviation || tenGodData?.id || ''
   
   // Map hidden stems to Ten Gods using frontend mappings (use post_interaction_qi in post view, base_qi in base view)
   const usePost = viewMode.value === 'post' || viewMode.value === 'transformed'
   // Check for non-empty objects to properly fall back when one is empty
   const monthlyPostQi = ebMonthlyNode?.post_interaction_qi && Object.keys(ebMonthlyNode.post_interaction_qi).length > 0 ? ebMonthlyNode.post_interaction_qi : null
   const monthlyBaseQi = ebMonthlyNode?.base_qi && Object.keys(ebMonthlyNode.base_qi).length > 0 ? ebMonthlyNode.base_qi : null
   const monthlyQi = usePost ? (monthlyPostQi || monthlyBaseQi || {}) : (monthlyBaseQi || {})
   const hiddenStems = {}
   if (monthlyQi && mappings.ten_gods) {
    for (const stemName of Object.keys(monthlyQi)) {
     const tenGodData = mappings.ten_gods?.[dayMasterStem]?.[stemName]
     hiddenStems[stemName] = tenGodData?.abbreviation || tenGodData?.id || ''
    }
   }
   
   luckPillars.push({
    label: 'Monthly 月運',
    stem: {
     chinese: hsMapping.chinese || hsName,
     element: hsMapping.english || 'Unknown',
     color: hsMapping.hex_color || '#808080'
    },
    stemName: hsName,
    branch: {
     chinese: ebMapping.chinese || ebName,
     animal: ebMapping.animal || 'Unknown',
     element: ebMapping.animal || 'Unknown',
     color: ebMapping.hex_color || '#808080'
    },
    branchName: ebName,
    stemKey: 'hs_ml',
    branchKey: 'eb_ml',
    hiddenStems: hiddenStems,
    hiddenQi: ebMonthlyNode?.base_qi || null,
    tenGod: tenGodLabel,
    isUnknown: false,
    stemTransformations: (hsMonthlyNode?.badges || []).filter(b => b.type === 'transformation').map(b => enrichBadgeWithInteraction(b)),
    branchTransformations: (ebMonthlyNode?.badges || []).filter(b => b.type === 'transformation').map(b => enrichBadgeWithInteraction(b)),
    stemCombinations: (hsMonthlyNode?.badges || []).filter(b => b.type === 'combination').map(b => enrichBadgeWithInteraction(b)),
    branchCombinations: (ebMonthlyNode?.badges || []).filter(b => b.type === 'combination').map(b => enrichBadgeWithInteraction(b)),
    stemNegatives: (hsMonthlyNode?.badges || []).filter(b => ['clash', 'harm', 'punishment', 'destruction', 'stem_conflict'].includes(b.type)).map(b => enrichBadgeWithInteraction(b)),
    branchNegatives: (ebMonthlyNode?.badges || []).filter(b => ['clash', 'harm', 'punishment', 'destruction', 'stem_conflict'].includes(b.type)).map(b => enrichBadgeWithInteraction(b)),
    branchWealthStorage: (ebMonthlyNode?.badges || []).filter(b => b.type === 'wealth_storage').map(b => enrichBadgeWithInteraction(b)),
    isMonthlyLuck: true,
    qiPhase: hsMonthlyNode?.qi_phase || ebMonthlyNode?.qi_phase || null
   })
  }
 }
 
 // Extract Daily Pillar (if available)
 if (chartData.value?.analysis_info?.has_daily && chartData.value?.hs_dl && chartData.value?.eb_dl) {
  const hsDailyNode = chartData.value.hs_dl
  const ebDailyNode = chartData.value.eb_dl
  const [hsName, ebName] = [hsDailyNode.id, ebDailyNode.id]
  
  if (hsName && ebName) {
   const mappings = chartData.value.mappings
   const hsMapping = mappings.heavenly_stems?.[hsName] || {}
   const ebMapping = mappings.earthly_branches?.[ebName] || {}
   
   const dayMasterStem = chartData.value?.hs_d?.id || 'Yi'
   const tenGodData = mappings.ten_gods?.[dayMasterStem]?.[hsName]
   const tenGodLabel = tenGodData?.abbreviation || tenGodData?.id || ''
   
   // Map hidden stems to Ten Gods using frontend mappings (use post_interaction_qi in post view, base_qi in base view)
   const usePost = viewMode.value === 'post' || viewMode.value === 'transformed'
   // Check for non-empty objects to properly fall back when one is empty
   const dailyPostQi = ebDailyNode?.post_interaction_qi && Object.keys(ebDailyNode.post_interaction_qi).length > 0 ? ebDailyNode.post_interaction_qi : null
   const dailyBaseQi = ebDailyNode?.base_qi && Object.keys(ebDailyNode.base_qi).length > 0 ? ebDailyNode.base_qi : null
   const dailyQi = usePost ? (dailyPostQi || dailyBaseQi || {}) : (dailyBaseQi || {})
   const hiddenStems = {}
   if (dailyQi && mappings.ten_gods) {
    for (const stemName of Object.keys(dailyQi)) {
     const tenGodData = mappings.ten_gods?.[dayMasterStem]?.[stemName]
     hiddenStems[stemName] = tenGodData?.abbreviation || tenGodData?.id || ''
    }
   }
   
   luckPillars.push({
    label: 'Daily 日運',
    stem: {
     chinese: hsMapping.chinese || hsName,
     element: hsMapping.english || 'Unknown',
     color: hsMapping.hex_color || '#808080'
    },
    stemName: hsName,
    branch: {
     chinese: ebMapping.chinese || ebName,
     animal: ebMapping.animal || 'Unknown',
     element: ebMapping.animal || 'Unknown',
     color: ebMapping.hex_color || '#808080'
    },
    branchName: ebName,
    stemKey: 'hs_dl',
    branchKey: 'eb_dl',
    hiddenStems: hiddenStems,
    hiddenQi: ebDailyNode?.base_qi || null,
    tenGod: tenGodLabel,
    isUnknown: false,
    stemTransformations: (hsDailyNode?.badges || []).filter(b => b.type === 'transformation').map(b => enrichBadgeWithInteraction(b)),
    branchTransformations: (ebDailyNode?.badges || []).filter(b => b.type === 'transformation').map(b => enrichBadgeWithInteraction(b)),
    stemCombinations: (hsDailyNode?.badges || []).filter(b => b.type === 'combination').map(b => enrichBadgeWithInteraction(b)),
    branchCombinations: (ebDailyNode?.badges || []).filter(b => b.type === 'combination').map(b => enrichBadgeWithInteraction(b)),
    stemNegatives: (hsDailyNode?.badges || []).filter(b => ['clash', 'harm', 'punishment', 'destruction', 'stem_conflict'].includes(b.type)).map(b => enrichBadgeWithInteraction(b)),
    branchNegatives: (ebDailyNode?.badges || []).filter(b => ['clash', 'harm', 'punishment', 'destruction', 'stem_conflict'].includes(b.type)).map(b => enrichBadgeWithInteraction(b)),
    branchWealthStorage: (ebDailyNode?.badges || []).filter(b => b.type === 'wealth_storage').map(b => enrichBadgeWithInteraction(b)),
    isDailyLuck: true,
    qiPhase: hsDailyNode?.qi_phase || ebDailyNode?.qi_phase || null
   })
  }
 }
 
 // Extract Hourly Pillar (if available)
 if (chartData.value?.analysis_info?.has_hourly && chartData.value?.hs_hl && chartData.value?.eb_hl) {
  const hsHourlyNode = chartData.value.hs_hl
  const ebHourlyNode = chartData.value.eb_hl
  const [hsName, ebName] = [hsHourlyNode.id, ebHourlyNode.id]
  
  if (hsName && ebName) {
   const mappings = chartData.value.mappings
   const hsMapping = mappings.heavenly_stems?.[hsName] || {}
   const ebMapping = mappings.earthly_branches?.[ebName] || {}
   
   const dayMasterStem = chartData.value?.hs_d?.id || 'Yi'
   const tenGodData = mappings.ten_gods?.[dayMasterStem]?.[hsName]
   const tenGodLabel = tenGodData?.abbreviation || tenGodData?.id || ''
   
   // Map hidden stems to Ten Gods using frontend mappings (use post_interaction_qi in post view, base_qi in base view)
   const usePost = viewMode.value === 'post' || viewMode.value === 'transformed'
   // Check for non-empty objects to properly fall back when one is empty
   const hourlyPostQi = ebHourlyNode?.post_interaction_qi && Object.keys(ebHourlyNode.post_interaction_qi).length > 0 ? ebHourlyNode.post_interaction_qi : null
   const hourlyBaseQi = ebHourlyNode?.base_qi && Object.keys(ebHourlyNode.base_qi).length > 0 ? ebHourlyNode.base_qi : null
   const hourlyQi = usePost ? (hourlyPostQi || hourlyBaseQi || {}) : (hourlyBaseQi || {})
   const hiddenStems = {}
   if (hourlyQi && mappings.ten_gods) {
    for (const stemName of Object.keys(hourlyQi)) {
     const tenGodData = mappings.ten_gods?.[dayMasterStem]?.[stemName]
     hiddenStems[stemName] = tenGodData?.abbreviation || tenGodData?.id || ''
    }
   }
   
   luckPillars.push({
    label: 'Hourly 時運',
    stem: {
     chinese: hsMapping.chinese || hsName,
     element: hsMapping.english || 'Unknown',
     color: hsMapping.hex_color || '#808080'
    },
    stemName: hsName,
    branch: {
     chinese: ebMapping.chinese || ebName,
     animal: ebMapping.animal || 'Unknown',
     element: ebMapping.animal || 'Unknown',
     color: ebMapping.hex_color || '#808080'
    },
    branchName: ebName,
    stemKey: 'hs_hl',
    branchKey: 'eb_hl',
    hiddenStems: hiddenStems,
    hiddenQi: ebHourlyNode?.base_qi || null,
    tenGod: tenGodLabel,
    isUnknown: false,
    stemTransformations: (hsHourlyNode?.badges || []).filter(b => b.type === 'transformation').map(b => enrichBadgeWithInteraction(b)),
    branchTransformations: (ebHourlyNode?.badges || []).filter(b => b.type === 'transformation').map(b => enrichBadgeWithInteraction(b)),
    stemCombinations: (hsHourlyNode?.badges || []).filter(b => b.type === 'combination').map(b => enrichBadgeWithInteraction(b)),
    branchCombinations: (ebHourlyNode?.badges || []).filter(b => b.type === 'combination').map(b => enrichBadgeWithInteraction(b)),
    stemNegatives: (hsHourlyNode?.badges || []).filter(b => ['clash', 'harm', 'punishment', 'destruction', 'stem_conflict'].includes(b.type)).map(b => enrichBadgeWithInteraction(b)),
    branchNegatives: (ebHourlyNode?.badges || []).filter(b => ['clash', 'harm', 'punishment', 'destruction', 'stem_conflict'].includes(b.type)).map(b => enrichBadgeWithInteraction(b)),
    branchWealthStorage: (ebHourlyNode?.badges || []).filter(b => b.type === 'wealth_storage').map(b => enrichBadgeWithInteraction(b)),
    isHourlyLuck: true,
    qiPhase: hsHourlyNode?.qi_phase || ebHourlyNode?.qi_phase || null
   })
  }
 }
 
 return luckPillars
})

// Talisman pillars (符) - User-selected pillars for harmony/balance
const talismanPillarsOrdered = computed(() => {
 if (!chartData.value?.mappings) return []
 
 const talismanPillars = []
 const mappings = chartData.value.mappings
 const dayMasterStem = chartData.value?.hs_d?.id || 'Yi'
 
 // Helper function to create talisman pillar (supports partial: HS-only, EB-only, or both)
 const createTalismanPillar = (label, hsNode, ebNode, hsKey, ebKey, isYear, isMonth, isDay, isHour) => {
  // Must have at least one node (HS or EB)
  if (!hsNode && !ebNode) return null
  
  const hsName = hsNode?.id || null
  const ebName = ebNode?.id || null
  
  const hsMapping = hsName ? (mappings.heavenly_stems?.[hsName] || {}) : {}
  const ebMapping = ebName ? (mappings.earthly_branches?.[ebName] || {}) : {}
  const tenGodData = hsName ? mappings.ten_gods?.[dayMasterStem]?.[hsName] : null
  const tenGodLabel = tenGodData?.abbreviation || tenGodData?.id || ''
  
  // Hidden stems from eb.qi - use post_interaction_qi for post view, base_qi for base view (EXACT same as natal)
  const usePost = viewMode.value === 'post'
  // Check for non-empty objects to properly fall back when one is empty
  const talismanPostQi = ebNode?.post_interaction_qi && Object.keys(ebNode.post_interaction_qi).length > 0 ? ebNode.post_interaction_qi : null
  const talismanBaseQi = ebNode?.base_qi && Object.keys(ebNode.base_qi).length > 0 ? ebNode.base_qi : null
  const hiddenQi = usePost ? (talismanPostQi || talismanBaseQi || {}) : (talismanBaseQi || {})
  
  // Map hidden stems to Ten Gods using frontend mappings (EXACT same as natal)
  const hiddenStems = {}
  if (hiddenQi && mappings.ten_gods) {
   for (const stemName of Object.keys(hiddenQi)) {
    const tenGodData = mappings.ten_gods?.[dayMasterStem]?.[stemName]
    hiddenStems[stemName] = tenGodData?.abbreviation || tenGodData?.id || ''
   }
  }
  
  return {
   label,
   stem: hsName ? {
    chinese: hsMapping.chinese || hsName,
    element: hsMapping.english || 'Unknown',
    color: hsMapping.hex_color || '#808080'
   } : null,
   stemName: hsName || null,
   branch: ebName ? {
    chinese: ebMapping.chinese || ebName,
    animal: ebMapping.animal || 'Unknown',
    element: ebMapping.animal || 'Unknown',
    color: ebMapping.hex_color || '#808080'
   } : null,
   branchName: ebName || null,
   stemKey: hsKey,
   branchKey: ebKey,
   hiddenStems,
   hiddenQi,
   tenGod: tenGodLabel,
   isUnknown: false,
   stemTransformations: (hsNode?.badges || []).filter(b => b.type === 'transformation').map(b => enrichBadgeWithInteraction(b)),
   branchTransformations: (ebNode?.badges || []).filter(b => b.type === 'transformation').map(b => enrichBadgeWithInteraction(b)),
   stemCombinations: (hsNode?.badges || []).filter(b => b.type === 'combination').map(b => enrichBadgeWithInteraction(b)),
   branchCombinations: (ebNode?.badges || []).filter(b => b.type === 'combination').map(b => enrichBadgeWithInteraction(b)),
   stemNegatives: (hsNode?.badges || []).filter(b => ['clash', 'harm', 'punishment', 'destruction', 'stem_conflict'].includes(b.type)).map(b => enrichBadgeWithInteraction(b)),
   branchNegatives: (ebNode?.badges || []).filter(b => ['clash', 'harm', 'punishment', 'destruction', 'stem_conflict'].includes(b.type)).map(b => enrichBadgeWithInteraction(b)),
   branchWealthStorage: (ebNode?.badges || []).filter(b => b.type === 'wealth_storage').map(b => enrichBadgeWithInteraction(b)),
   isTalismanYear: isYear,
   isTalismanMonth: isMonth,
   isTalismanDay: isDay,
   isTalismanHour: isHour,
   qiPhase: hsNode?.qi_phase || ebNode?.qi_phase || null
  }
 }
 
 // Add talisman pillars if they exist (use ty/tm/td/th node IDs)
 const tyPillar = createTalismanPillar('Talisman Y 符年', chartData.value.hs_ty, chartData.value.eb_ty, 'hs_ty', 'eb_ty', true, false, false, false)
 if (tyPillar) talismanPillars.push(tyPillar)
 
 const tmPillar = createTalismanPillar('Talisman M 符月', chartData.value.hs_tm, chartData.value.eb_tm, 'hs_tm', 'eb_tm', false, true, false, false)
 if (tmPillar) talismanPillars.push(tmPillar)
 
 const tdPillar = createTalismanPillar('Talisman D 符日', chartData.value.hs_td, chartData.value.eb_td, 'hs_td', 'eb_td', false, false, true, false)
 if (tdPillar) talismanPillars.push(tdPillar)
 
 const thPillar = createTalismanPillar('Talisman H 符時', chartData.value.hs_th, chartData.value.eb_th, 'hs_th', 'eb_th', false, false, false, true)
 if (thPillar) talismanPillars.push(thPillar)
 
 return talismanPillars
})

// Location pillars (地) - Overseas or birthplace nodes (NO badges)
const locationPillarsOrdered = computed(() => {
 if (!chartData.value?.mappings) return []
 
 const locationPillars = []
 const mappings = chartData.value.mappings
 const dayMasterStem = chartData.value?.hs_d?.id || 'Yi'
 
 // Helper function to create location pillar (NO badges - only display)
 const createLocationPillar = (label, hsNode, ebNode, hsKey, ebKey, borderColor) => {
  // Must have at least one node (HS or EB)
  if (!hsNode && !ebNode) return null
  
  const hsName = hsNode?.id || null
  const ebName = ebNode?.id || null
  
  const hsMapping = hsName ? (mappings.heavenly_stems?.[hsName] || {}) : {}
  const ebMapping = ebName ? (mappings.earthly_branches?.[ebName] || {}) : {}
  const tenGodData = hsName ? mappings.ten_gods?.[dayMasterStem]?.[hsName] : null
  const tenGodLabel = tenGodData?.abbreviation || tenGodData?.id || ''
  
  // Hidden stems from eb.qi - use post_interaction_qi for post view, base_qi for base view
  const usePost = viewMode.value === 'post'
  // Check for non-empty objects to properly fall back when one is empty
  const locationPostQi = ebNode?.post_interaction_qi && Object.keys(ebNode.post_interaction_qi).length > 0 ? ebNode.post_interaction_qi : null
  const locationBaseQi = ebNode?.base_qi && Object.keys(ebNode.base_qi).length > 0 ? ebNode.base_qi : null
  const hiddenQi = usePost ? (locationPostQi || locationBaseQi || {}) : (locationBaseQi || {})
  
  // Map hidden stems to Ten Gods
  const hiddenStems = {}
  if (hiddenQi && mappings.ten_gods) {
   for (const stemName of Object.keys(hiddenQi)) {
    const tenGodData = mappings.ten_gods?.[dayMasterStem]?.[stemName]
    hiddenStems[stemName] = tenGodData?.abbreviation || tenGodData?.id || ''
   }
  }
  
  return {
   label,
   stem: hsName ? {
    chinese: hsMapping.chinese || hsName,
    element: hsMapping.english || 'Unknown',
    color: hsMapping.hex_color || '#808080'
   } : null,
   stemName: hsName || null,
   branch: ebName ? {
    chinese: ebMapping.chinese || ebName,
    animal: ebMapping.animal || 'Unknown',
    element: ebMapping.animal || 'Unknown',
    color: ebMapping.hex_color || '#808080'
   } : null,
   branchName: ebName || null,
   stemKey: hsKey,
   branchKey: ebKey,
   hiddenStems,
   hiddenQi,
   tenGod: tenGodLabel,
   isUnknown: false,
   isLocationNode: true,
   locationBorderColor: borderColor,
   // NO badges for location nodes
   stemTransformations: [],
   branchTransformations: [],
   stemCombinations: [],
   branchCombinations: [],
   stemNegatives: [],
   branchNegatives: [],
   branchWealthStorage: []
  }
 }
 
 // Add overseas pillars (o1, o2) - blue border for water
 const o1Pillar = createLocationPillar('Overseas 1', chartData.value.hs_o1, chartData.value.eb_o1, 'hs_o1', 'eb_o1', 'border-blue-600')
 if (o1Pillar) locationPillars.push(o1Pillar)
 
 const o2Pillar = createLocationPillar('Overseas 2', chartData.value.hs_o2, chartData.value.eb_o2, 'hs_o2', 'eb_o2', 'border-blue-600')
 if (o2Pillar) locationPillars.push(o2Pillar)
 
 // Add birthplace pillars (b1-b4) - amber border for earth
 const b1Pillar = createLocationPillar('Birthplace 1', chartData.value.hs_b1, chartData.value.eb_b1, 'hs_b1', 'eb_b1', 'border-amber-600')
 if (b1Pillar) locationPillars.push(b1Pillar)
 
 const b2Pillar = createLocationPillar('Birthplace 2', chartData.value.hs_b2, chartData.value.eb_b2, 'hs_b2', 'eb_b2', 'border-amber-600')
 if (b2Pillar) locationPillars.push(b2Pillar)
 
 const b3Pillar = createLocationPillar('Birthplace 3', chartData.value.hs_b3, chartData.value.eb_b3, 'hs_b3', 'eb_b3', 'border-amber-600')
 if (b3Pillar) locationPillars.push(b3Pillar)
 
 const b4Pillar = createLocationPillar('Birthplace 4', chartData.value.hs_b4, chartData.value.eb_b4, 'hs_b4', 'eb_b4', 'border-amber-600')
 if (b4Pillar) locationPillars.push(b4Pillar)
 
 return locationPillars
})

// Natal pillars only (4 columns: hour, day, month, year)
const natalPillarsOnly = computed(() => {
 if (!pillars.value) return null
 
 return [
  pillars.value.hour,
  pillars.value.day,
  pillars.value.month,
  pillars.value.year
 ]
})

// Combined ordered pillars (natal + luck + talismans - all need to be here for interaction calculations)
const pillarsOrdered = computed(() => {
 if (!pillars.value) return null
 
 const basePillars = [
  pillars.value.hour,
  pillars.value.day,
  pillars.value.month,
  pillars.value.year
 ]
 
 // Use luckPillarsOrdered to get all luck pillars (10Y, annual, monthly, daily, hourly)
 const allLuckPillars = luckPillarsOrdered.value || []
 
 // Get talisman pillars
 const allTalismanPillars = talismanPillarsOrdered.value || []
 
 // Combine natal + luck + talisman pillars (all must be in array for interactions)
 return [...basePillars, ...allLuckPillars, ...allTalismanPillars]
})

// Filter natal + luck pillars (exclude talismans for main chart display)
const natalAndLuckPillars = computed(() => {
 if (!pillarsOrdered.value) return null
 return pillarsOrdered.value.filter(p => 
  !p.isTalismanYear && !p.isTalismanMonth && !p.isTalismanDay && !p.isTalismanHour
 )
})

// Talisman display row (4 slots aligned: hour, day, month, year)
// ALWAYS show structure (skeleton when showTalismans is OFF)
const talismanPillarsDisplay = computed(() => {
 // Always return 4 slots: [hour, day, month, year]
 const display = [null, null, null, null]
 
 // Fill in actual data ONLY if showTalismans is enabled AND data available
 if (showTalismans.value && talismanPillarsOrdered.value) {
  talismanPillarsOrdered.value.forEach(t => {
   if (t.isTalismanHour) display[0] = t
   else if (t.isTalismanDay) display[1] = t
   else if (t.isTalismanMonth) display[2] = t
   else if (t.isTalismanYear) display[3] = t
  })
 }
 
 // Create skeleton pillars - ALWAYS show structure
 if (!display[0]) display[0] = { isTalismanHour: true, isEmpty: true }
 if (!display[1]) display[1] = { isTalismanDay: true, isEmpty: true }
 if (!display[2]) display[2] = { isTalismanMonth: true, isEmpty: true }
 if (!display[3]) display[3] = { isTalismanYear: true, isEmpty: true }
 
 return display
})

// Luck pillars display grid (5 slots aligned with natal)
// [Hourly, Daily, Monthly, Annual, 10Y] - aligned with [Hour, Day, Month, Year] natal above
// ALWAYS show structure (skeleton pillars when showAnalysisPeriod is OFF)
const luckPillarsDisplay = computed(() => {
 // Always return structure, even when Time Travel is OFF
 
 // 5 slots: [Hourly, Daily, Monthly, Annual, 10Y]
 const display = [null, null, null, null, null]
 
 // Fill in actual data ONLY if Time Travel is ON and checkbox is enabled
 if (showAnalysisPeriod.value && luckPillarsOrdered.value) {
  luckPillarsOrdered.value.forEach(lp => {
   if (lp.isHourlyLuck && includeHourlyLuck.value) display[0] = lp
   else if (lp.isDailyLuck && includeDailyLuck.value) display[1] = lp
   else if (lp.isMonthlyLuck && includeMonthlyLuck.value) display[2] = lp
   else if (lp.isAnnualLuck && includeAnnualLuck.value) display[3] = lp
   else if (lp.isLuckPillar) display[4] = lp  // 10Y doesn't have checkbox (always show if available)
  })
 }
 
 // Create skeleton pillars - ALWAYS show structure
 if (!display[0]) display[0] = { isHourlyLuck: true, isEmpty: true }
 if (!display[1]) display[1] = { isDailyLuck: true, isEmpty: true }
 if (!display[2]) display[2] = { isMonthlyLuck: true, isEmpty: true }
 if (!display[3]) display[3] = { isAnnualLuck: true, isEmpty: true }
 // 10Y skeleton always shows (even when Time Travel is OFF)
 if (!display[4]) display[4] = { isLuckPillar: true, isEmpty: true }
 
 return display
})

// Dong Gong Date Selection info (from API response)
const dongGongInfo = computed(() => {
 if (!chartData.value?.dong_gong) return null
 return chartData.value.dong_gong
})

// Dong Gong rating colors and styles
const getDongGongRatingColor = (rating) => {
 const colors = {
  'excellent': { bg: '#FEF08A', border: '#EAB308', text: '#854D0E' },    // Gold/Yellow
  'auspicious': { bg: '#BBF7D0', border: '#22C55E', text: '#166534' },   // Green
  'fair': { bg: '#E5E7EB', border: '#9CA3AF', text: '#374151' },         // Gray
  'inauspicious': { bg: '#FED7AA', border: '#F97316', text: '#9A3412' }, // Orange
  'dire': { bg: '#FECACA', border: '#EF4444', text: '#991B1B' }          // Red
 }
 return colors[rating] || colors['fair']
}

const getDongGongRatingSymbol = (rating) => {
 const symbols = {
  'excellent': '★',
  'auspicious': '✓',
  'fair': '●',
  'inauspicious': '▲',
  'dire': '✗'
 }
 return symbols[rating] || '●'
}

const getDongGongTooltip = (dongGong) => {
 if (!dongGong) return ''
 const parts = []

 // Day Officer
 if (dongGong.officer) {
  parts.push(`${dongGong.officer.chinese} ${dongGong.officer.english} Day`)
 }

 // Rating
 if (dongGong.rating) {
  parts.push(`Rating: ${dongGong.rating.chinese} (${dongGong.rating.id})`)
 }

 // Good for
 if (dongGong.good_for && dongGong.good_for.length > 0) {
  parts.push(`Good for: ${dongGong.good_for.join(', ')}`)
 }

 // Bad for
 if (dongGong.bad_for && dongGong.bad_for.length > 0) {
  parts.push(`Avoid: ${dongGong.bad_for.join(', ')}`)
 }

 // Description
 if (dongGong.description_english) {
  parts.push(dongGong.description_english)
 }

 return parts.join('\n')
}

// Old manual pillar building logic removed - now using luckPillarsOrdered
// (Simplified from 150+ lines to just using luckPillarsOrdered above)

const tenElements = computed(() => {
 // 3-tier element scoring: Base → Natal → Post
 // Base = natal chart only (8 nodes, no interactions)
 // Natal = natal chart only (8 nodes, WITH interactions) - internal dynamics
 // Post = all nodes (natal + luck + talisman + location) with all interactions
 if (!chartData.value) return []

 // Base: Pure natal chart (8 nodes, no interactions)
 const baseScores = chartData.value.natal_base_elements || chartData.value.base_element_score || {}

 // Natal: Natal chart only (8 nodes, WITH interactions) - internal dynamics
 const natalScores = chartData.value.natal_element_score || {}

 // Post: All nodes (natal + luck + talisman + location) with all interactions
 const postScores = chartData.value.advanced_post_elements || chartData.value.post_element_score || {}

 // Map stem IDs to display names
 const stemToDisplay = {
  'Jia': 'Yang Wood',
  'Yi': 'Yin Wood',
  'Bing': 'Yang Fire',
  'Ding': 'Yin Fire',
  'Wu': 'Yang Earth',
  'Ji': 'Yin Earth',
  'Geng': 'Yang Metal',
  'Xin': 'Yin Metal',
  'Ren': 'Yang Water',
  'Gui': 'Yin Water'
 }

 return Object.entries(stemToDisplay).map(([stem, displayName]) => ({
  name: displayName,
  naive: baseScores[stem] || 0,
  natal: natalScores[stem] || 0,
  final: postScores[stem] || 0,
  change: (postScores[stem] || 0) - (baseScores[stem] || 0),
  natalChange: (natalScores[stem] || 0) - (baseScores[stem] || 0),
  postChange: (postScores[stem] || 0) - (natalScores[stem] || 0)
 }))
})

const fiveElements = computed(() => {
 // 3-tier element scoring: Base → Natal → Post
 // Base = natal chart only (8 nodes, no interactions)
 // Natal = natal chart only (8 nodes, WITH interactions) - internal dynamics
 // Post = all nodes (natal + luck + talisman + location) with all interactions
 if (!chartData.value) return []

 // Base: Pure natal chart (8 nodes, no interactions)
 const baseScores = chartData.value.natal_base_elements || chartData.value.base_element_score || {}

 // Natal: Natal chart only (8 nodes, WITH interactions) - internal dynamics
 const natalScores = chartData.value.natal_element_score || {}

 // Post: All nodes (natal + luck + talisman + location) with all interactions
 const postScores = chartData.value.advanced_post_elements || chartData.value.post_element_score || {}

 // Map stems to elements with Yang/Yin distinction
 const yangStems = {
  'Wood': 'Jia',
  'Fire': 'Bing',
  'Earth': 'Wu',
  'Metal': 'Geng',
  'Water': 'Ren'
 }
 const yinStems = {
  'Wood': 'Yi',
  'Fire': 'Ding',
  'Earth': 'Ji',
  'Metal': 'Xin',
  'Water': 'Gui'
 }

 const elements = ['Wood', 'Fire', 'Earth', 'Metal', 'Water']

 // Calculate grand totals for percentage normalization
 const naiveTotal = Object.values(baseScores).reduce((sum, val) => sum + (val || 0), 0)
 const natalTotal = Object.values(natalScores).reduce((sum, val) => sum + (val || 0), 0)
 const finalTotal = Object.values(postScores).reduce((sum, val) => sum + (val || 0), 0)

 // Build element data with Yang/Yin breakdown
 return elements.map(name => {
  const yangStem = yangStems[name]
  const yinStem = yinStems[name]

  // Raw scores for Yang and Yin
  const yangNaiveRaw = baseScores[yangStem] || 0
  const yinNaiveRaw = baseScores[yinStem] || 0
  const yangNatalRaw = natalScores[yangStem] || 0
  const yinNatalRaw = natalScores[yinStem] || 0
  const yangFinalRaw = postScores[yangStem] || 0
  const yinFinalRaw = postScores[yinStem] || 0

  // Combined raw scores
  const naiveRaw = yangNaiveRaw + yinNaiveRaw
  const natalRaw = yangNatalRaw + yinNatalRaw
  const finalRaw = yangFinalRaw + yinFinalRaw

  // Convert raw scores to percentages (of grand total)
  const naive = naiveTotal > 0 ? (naiveRaw / naiveTotal) * 100 : 0
  const natal = natalTotal > 0 ? (natalRaw / natalTotal) * 100 : 0
  const final = finalTotal > 0 ? (finalRaw / finalTotal) * 100 : 0

  // Yang/Yin percentages (of grand total for bar display)
  const yangNatal = natalTotal > 0 ? (yangNatalRaw / natalTotal) * 100 : 0
  const yinNatal = natalTotal > 0 ? (yinNatalRaw / natalTotal) * 100 : 0
  const yangFinal = finalTotal > 0 ? (yangFinalRaw / finalTotal) * 100 : 0
  const yinFinal = finalTotal > 0 ? (yinFinalRaw / finalTotal) * 100 : 0

  return {
   name,
   naive,
   natal,
   final,
   change: final - naive,        // Change from base to post (legacy)
   natalChange: natal - naive,   // Change from base to natal
   postChange: final - natal,    // Change from natal to post
   naiveRaw,   // Keep raw points
   natalRaw,   // Keep raw points
   finalRaw,   // Keep raw points
   // Yang/Yin breakdown for stacked bar display
   yangNatal,
   yinNatal,
   yangFinal,
   yinFinal,
   yangNatalRaw,
   yinNatalRaw,
   yangFinalRaw,
   yinFinalRaw
  }
 })
})

const fiveElementsWithRelations = computed(() => {
 if (!fiveElements.value.length) return []
 
 // If no daymaster_analysis, return elements without relationships
 if (!chartData.value?.daymaster_analysis) {
  return fiveElements.value.map(element => ({
   ...element,
   relationship: ''
  }))
 }
 
 const daymaster = chartData.value.daymaster_analysis.daymaster
 const daymasterElement = daymaster.split(' ')[1] // Get element from "Yang Fire" -> "Fire"
 
 return fiveElements.value.map(element => ({
  ...element,
  relationship: getElementRelationship(daymasterElement, element.name)
 }))
})

// Calculate totals for different views (now these are already percentages that sum to 100)
const naiveTotal = computed(() => {
 if (!fiveElements.value.length) return 100
 return fiveElements.value.reduce((sum, e) => sum + e.naive, 0)
})

const natalTotal = computed(() => {
 if (!fiveElements.value.length) return 100
 return fiveElements.value.reduce((sum, e) => sum + e.natal, 0)
})

const finalTotal = computed(() => {
 if (!fiveElements.value.length) return 100
 return fiveElements.value.reduce((sum, e) => sum + e.final, 0)
})

const maxElementScore = computed(() => {
 // Since scores are now normalized to 100%, always use 100 as the max
 return 100
})

const maxTenElementScore = computed(() => {
 if (!tenElements.value.length) return 100
 // Find the maximum single element score for scaling
 const maxScore = Math.max(...tenElements.value.map(e => e.final))
 return Math.max(maxScore, 100)
})

const totalChange = computed(() => {
 if (!fiveElements.value.length) return 0
 return fiveElements.value.reduce((sum, e) => sum + e.change, 0)
})

const interactions = computed(() => {
 // Handle both new format (direct interactions object) and wrapped format
 const interactionsData = chartData.value?.interactions || chartData.value?.interaction_analysis?.interactions
 if (!interactionsData) return []
 
 // If it's an object (new format), convert to array
 if (typeof interactionsData === 'object' && !Array.isArray(interactionsData)) {
  return Object.entries(interactionsData).map(([id, data]) => ({
   id,
   ...data
  }))
 }
 
 // If it's already an array, return as-is
 return interactionsData
})

const nonNaturalInteractions = computed(() => {
 if (!interactions.value || !Array.isArray(interactions.value)) return []
 return interactions.value.filter(i => {
  return !i.type?.includes('NATURAL') && !i.type?.includes('ENERGY_FLOW') && i.type !== 'SEASONAL_ADJUSTMENT'
 })
})

// Extract luck pillar interactions from backend-calculated interactions
// Backend returns interactions as a DICTIONARY (not array), with keys like "TYPE~Pattern~nodes"
const luckPillarInteractions = computed(() => {
 if (!chartData.value?.interactions || (!currentLuckPillar.value && !annualLuckPillar.value)) return []
 
 const interactionsDict = chartData.value.interactions
 const luckInteractions = []
 
 // Iterate through interaction dictionary keys
 for (const [key, interactionData] of Object.entries(interactionsDict)) {
  // Check if this interaction involves luck pillar nodes (10-year, annual, monthly, daily, hourly)
  const nodes = interactionData.nodes || []
  const hasLuckNode = nodes.some(nodeId => 
   nodeId === 'hs_10yl' || nodeId === 'eb_10yl' ||
   nodeId === 'hs_yl' || nodeId === 'eb_yl' ||
   nodeId === 'hs_ml' || nodeId === 'eb_ml' ||
   nodeId === 'hs_dl' || nodeId === 'eb_dl' ||
   nodeId === 'hs_hl' || nodeId === 'eb_hl'
  )
  
  if (hasLuckNode) {
   // Parse the key format: "TYPE~Pattern~nodes"
   const [type, pattern, nodesStr] = key.split('~')
   
   // Determine effect based on interaction type
   let effect = 'positive'
   if (type && (
    type.includes('CLASH') || 
    type.includes('HARM') || 
    type.includes('PUNISHMENT') ||
    type.includes('CONFLICT') ||
    type.includes('DESTRUCTION')
   )) {
    effect = 'negative'
   }
   
   // Get label from type
   const labelMap = {
    'SIX_HARMONIES': '六合',
    'CLASHES': '相冲',
    'HARMS': '相害',
    'PUNISHMENTS': '相刑',
    'STEM_COMBINATION': '天干合',
    'STEM_CONFLICT': '天干沖',
    'THREE_COMBINATIONS': '三合',
    'ARCHED_COMBINATION': '拱合',
    'DESTRUCTION': '相破'
   }
   const label = labelMap[type] || type
   
   luckInteractions.push({
    type,
    label,
    description: interactionData.pattern || pattern || `${type} interaction`,
    branches: interactionData.branches || interactionData.stems || [],
    nodes,
    effect
   })
  }
 }
 
 return luckInteractions
})

// Methods
async function generateChart() {
 const startTime = performance.now()
 console.log('🚀 generateChart() started')
 
 if (!birthDate.value) {
  if (typeof window !== 'undefined') {
   alert('Please fill in birth date')
  }
  return
 }
 
 // Use 'unknown' for birth_time when hour is unknown
 const timeParam = unknownHour.value ? 'unknown' : birthTime.value
 
 if (!timeParam && !unknownHour.value) {
  if (typeof window !== 'undefined') {
   alert('Please fill in birth time or mark as unknown')
  }
  return
 }
 
 // DO NOT show loading indicator - it causes flicker
 // isLoading.value = true
 try {
  // Build API URL with analyze_bazi endpoint (underscore, not hyphen)
  // Call via Vite proxy to avoid CORS issues
  let apiUrl = `${API_BASE_URL}/api/analyze_bazi?birth_date=${birthDate.value}&birth_time=${encodeURIComponent(timeParam)}&gender=${gender.value}`
  
  // Only add analysis parameters if time travel mode is enabled (🔮 toggle is ON)
  if (showAnalysisPeriod.value) {
   // Add analysis_year to get luck pillars (default to current year if not specified)
   const yearToAnalyze = analysisYear.value || new Date().getFullYear()
   apiUrl += `&analysis_year=${yearToAnalyze}`
   
   // Add include_annual_luck parameter (controls whether annual luck affects calculations)
   apiUrl += `&include_annual_luck=${includeAnnualLuck.value}`
   
   // Only send month/day/time if toggles are enabled (respects checkbox state)
   if (analysisMonth.value && includeMonthlyLuck.value) {
    apiUrl += `&analysis_month=${analysisMonth.value}`
   }
   
   if (analysisDay.value && includeDailyLuck.value) {
    apiUrl += `&analysis_day=${analysisDay.value}`
   }
   
   if (analysisTime.value && includeHourlyLuck.value) {
    apiUrl += `&analysis_time=${encodeURIComponent(analysisTime.value)}`
   }
  }
  
  // Add talisman parameters if talismans are enabled (only send defined values)
  if (showTalismans.value) {
   // Year talisman
   if (talismanYearHS.value) apiUrl += `&talisman_year_hs=${talismanYearHS.value}`
   if (talismanYearEB.value) apiUrl += `&talisman_year_eb=${talismanYearEB.value}`
   
   // Month talisman
   if (talismanMonthHS.value) apiUrl += `&talisman_month_hs=${talismanMonthHS.value}`
   if (talismanMonthEB.value) apiUrl += `&talisman_month_eb=${talismanMonthEB.value}`
   
   // Day talisman
   if (talismanDayHS.value) apiUrl += `&talisman_day_hs=${talismanDayHS.value}`
   if (talismanDayEB.value) apiUrl += `&talisman_day_eb=${talismanDayEB.value}`
   
   // Hour talisman
   if (talismanHourHS.value) apiUrl += `&talisman_hour_hs=${talismanHourHS.value}`
   if (talismanHourEB.value) apiUrl += `&talisman_hour_eb=${talismanHourEB.value}`
  }
  
  // Add location parameter if location is enabled
  if (showLocation.value && locationType.value) {
   apiUrl += `&location=${locationType.value}`
  }
  
  console.log('Calling analyze_bazi endpoint:', apiUrl)
  
  // Call the backend endpoint via proxy
  const response = await fetch(apiUrl)
  
  if (!response.ok) throw new Error('Chart API request failed')
  
  const data = await response.json()
  const parseTime = performance.now()
  console.log(`⏱️  API call + JSON parse: ${(parseTime - startTime).toFixed(2)}ms`)
  
  // Deep freeze the data to prevent Vue from making it reactive
  // This stops Vue from creating getters/setters for every nested property
  const frozenData = Object.freeze(JSON.parse(JSON.stringify(data)))
  const freezeTime = performance.now()
  console.log(`❄️  Data freeze: ${(freezeTime - parseTime).toFixed(2)}ms`)
  
  // Update chart data with frozen object
  chartData.value = frozenData
  chartGeneration.value++ // Increment to trigger targeted re-renders
  const updateTime = performance.now()
  console.log(`🔄 Vue update: ${(updateTime - freezeTime).toFixed(2)}ms`)
  console.log(`✅ TOTAL TIME: ${(updateTime - startTime).toFixed(2)}ms`)
  
  // Extract 10-year luck pillar info from response (if has_luck_pillar flag is true)
  if (data.analysis_info?.has_luck_pillar && data.hs_10yl && data.eb_10yl) {
   const luckHs = data.hs_10yl.id
   const luckEb = data.eb_10yl.id
   
   if (luckHs && luckEb) {
    currentLuckPillar.value = {
     pillar: `${luckHs} ${luckEb}`,
     hs_element: data.mappings?.heavenly_stems?.[luckHs]?.english || 'Unknown',
     eb_animal: data.mappings?.earthly_branches?.[luckEb]?.animal || 'Unknown',
     ten_god_hs: data.hs_10yl?.base?.ten_god || 'Unknown',
     ten_god_hidden: {},
     timing: (() => {
      const misc = data.hs_10yl?.misc || data.eb_10yl?.misc
      if (misc && misc.start_date && misc.end_date) {
       // Extract years from date strings (format: "YYYY-MM-DD")
       const startYear = misc.start_date.split('-')[0]
       const endYear = misc.end_date.split('-')[0]
       return {
        start_year: parseInt(startYear),
        end_year: parseInt(endYear),
        start_age: misc.start_age || 0,
        end_age: misc.end_age || 10,
        start_date: misc.start_date,
        end_date: misc.end_date
       }
      }
      // Fallback if no misc data
      return {
       start_year: data.analysis_info?.year || new Date().getFullYear(),
       end_year: (data.analysis_info?.year || new Date().getFullYear()) + 10,
       start_age: 0,
       end_age: 10
      }
     })(),
     is_current: true
    }
    console.log('10-year luck pillar extracted:', currentLuckPillar.value)
   } else {
    currentLuckPillar.value = null
   }
  } else {
   currentLuckPillar.value = null
  }
  
  // Extract annual luck pillar info from response (if year is set, even if disabled)
  if (data.analysis_info?.year && data.hs_yl && data.eb_yl) {
   const annualHs = data.hs_yl.id
   const annualEb = data.eb_yl.id
   
   if (annualHs && annualEb) {
    annualLuckPillar.value = {
     pillar: `${annualHs} ${annualEb}`,
     hs_element: data.mappings?.heavenly_stems?.[annualHs]?.english || 'Unknown',
     eb_animal: data.mappings?.earthly_branches?.[annualEb]?.animal || 'Unknown',
     ten_god_hs: data.hs_yl?.base?.ten_god || 'Unknown',
     ten_god_hidden: {},
     year: data.analysis_info?.year,
     is_current: true,
     disabled: data.hs_yl.disabled || false // Track if it's disabled
    }
    console.log('Annual luck pillar extracted:', annualLuckPillar.value)
   } else {
    annualLuckPillar.value = null
   }
  } else {
   annualLuckPillar.value = null
  }
  
  console.log('chartData.value set with backend interactions, pillarsOrdered:', pillarsOrdered.value)
 } catch (error) {
  console.error('Error generating chart:', error)
  console.error('Error details:', {
   message: error.message,
   stack: error.stack,
   apiUrl: `/api/analyze_bazi?birth_date=${birthDate.value}&birth_time=${encodeURIComponent(birthTime.value || 'unknown')}&gender=${gender.value}`
  })
  if (typeof window !== 'undefined') {
   alert(`Failed to generate chart: ${error.message || 'Unknown error'}. Check console for details.`)
  }
 } finally {
  // isLoading.value = false
  const loadingEndTime = performance.now()
  console.log(`⌛ Loading indicator off: ${(loadingEndTime - startTime).toFixed(2)}ms`)
  
  // Restore scroll position after render completes using nextTick and requestAnimationFrame
  await nextTick()
  const nextTickTime = performance.now()
  console.log(`⏳ nextTick complete: ${(nextTickTime - loadingEndTime).toFixed(2)}ms`)
  
  requestAnimationFrame(() => {
   const rafTime = performance.now()
   console.log(`🎬 requestAnimationFrame: ${(rafTime - nextTickTime).toFixed(2)}ms`)
   console.log(`🏁 GRAND TOTAL: ${(rafTime - startTime).toFixed(2)}ms\n`)
   
   if (savedScrollPosition > 0) {
    window.scrollTo({ top: savedScrollPosition, behavior: 'instant' })
   }
  })
 }
}

// ============= COLOR FUNCTIONS =============

// Returns inline style object for text color using API mappings
function getElementTextStyle(element) {
 const mappings = chartData.value?.mappings

 // Handle polarized elements like "Yang Wood"
 if (element && element.includes(' ')) {
  const [polarity, elemName] = element.split(' ')
  const colorKey = polarity === 'Yang' ? 'hex_color_yang' : 'hex_color_yin'
  const color = mappings?.elements?.[elemName]?.[colorKey] || mappings?.elements?.[elemName]?.hex_color || '#4b5563'
  return { color }
 }

 // Handle simple elements like "Wood"
 const color = mappings?.elements?.[element]?.hex_color || '#4b5563'
 return { color }
}

// Legacy function - DEPRECATED, use getElementTextStyle
function getElementColor(element) {
 return ''  // Return empty, use getElementTextStyle instead
}

// Returns inline style object using API mappings
function getElementBgStyle(element) {
 const mappings = chartData.value?.mappings
 const color = mappings?.elements?.[element]?.hex_color || '#9ca3af'
 return { backgroundColor: color }
}

// Legacy function - DEPRECATED, use getElementBgStyle
function getElementBgColor(element) {
 return ''  // Return empty, use getElementBgStyle instead
}

// Yang element colors for Wu Xing chart (solid darker colors)
// Returns inline style object using API mappings
function getYangBgStyle(element) {
 const mappings = chartData.value?.mappings
 const color = mappings?.elements?.[element]?.hex_color_yang || '#4b5563'
 return { backgroundColor: color }
}

// Legacy function for backward compatibility - DEPRECATED
function getYangBgColor(element) {
 return ''  // Return empty, use getYangBgStyle instead
}

// Yin element colors for Wu Xing chart (lighter colors with stripe pattern)
function getYinBgStyle(element) {
 // Get Yin element color from API mappings
 const mappings = chartData.value?.mappings
 const color = mappings?.elements?.[element]?.hex_color_yin || '#d1d5db'
 // Diagonal stripes pattern for Yin distinction
 return {
  background: `repeating-linear-gradient(
   45deg,
   ${color},
   ${color} 2px,
   transparent 2px,
   transparent 4px
  ), ${color}`
 }
}

// Get node background color from API hex color
function getNodeBgColor(elementWithPolarity, apiHexColor = null) {
 // If API provided a hex color, use it directly
 if (apiHexColor) {
  // Handle pure element colors (gradient object)
  if (typeof apiHexColor === 'object' && apiHexColor.bg) {
   if (apiHexColor.bg.includes('gradient')) {
    return {
     background: 'linear-gradient(to right, #ef4444, #a855f7, #ec4899)',
     border: '2px solid #9333ea'
    }
   }
  }
  // Use hex color directly from API
  if (typeof apiHexColor === 'string' && apiHexColor.startsWith('#')) {
   return { backgroundColor: apiHexColor }
  }
 }

 // Fallback color map - matches API STEMS colors (soft pastels)
 // These should match api/library/core.py STEMS colors
 const polarizedHex = {
  'Yang Wood': '#c2d4be', 'Yin Wood': '#d6e2bb',  // Jia, Yi
  'Yang Fire': '#f3adae', 'Yin Fire': '#f9d3ad',  // Bing, Ding
  'Yang Earth': '#e6ceb7', 'Yin Earth': '#efe3cc', // Wu, Ji
  'Yang Metal': '#ccd8e6', 'Yin Metal': '#e6e8f7', // Geng, Xin
  'Yang Water': '#b9cbff', 'Yin Water': '#e0e9ff'  // Ren, Gui
 }

 if (polarizedHex[elementWithPolarity]) {
  return { backgroundColor: polarizedHex[elementWithPolarity] }
 }

 // Fallback
 return { backgroundColor: '#f9fafb' }
}

// Get element for a stem name
function getStemElement(stemName) {
 const stemElements = {
  'Jia': 'Yang Wood', 'Yi': 'Yin Wood',
  'Bing': 'Yang Fire', 'Ding': 'Yin Fire',
  'Wu': 'Yang Earth', 'Ji': 'Yin Earth',
  'Geng': 'Yang Metal', 'Xin': 'Yin Metal',
  'Ren': 'Yang Water', 'Gui': 'Yin Water'
 }
 return stemElements[stemName] || ''
}


// Get hidden stems with proportional weights based on qi scores
function getHiddenStemsWithWeights(pillar) {
 // Get the appropriate qi data based on view mode
 const ebNode = nodes.value?.[pillar.branchKey]

 // Both natal and post views use post_interaction_qi (with interactions applied)
 // Check for non-empty objects using Object.keys() to properly handle {}
 let qiData = null
 const hasPostQi = ebNode?.post_interaction_qi && Object.keys(ebNode.post_interaction_qi).length > 0
 const hasBaseQi = ebNode?.base_qi && Object.keys(ebNode.base_qi).length > 0
 const hasPillarQi = pillar.hiddenQi && (Array.isArray(pillar.hiddenQi) ? pillar.hiddenQi.length > 0 : Object.keys(pillar.hiddenQi).length > 0)

 if (hasPostQi) {
  // Use post_interaction_qi for natal and post views
  qiData = ebNode.post_interaction_qi
 } else if (hasBaseQi) {
  // Fallback to base_qi if post_interaction_qi not available or empty
  qiData = ebNode.base_qi
 } else if (hasPillarQi) {
  // Fallback to pillar.hiddenQi (could be object or array)
  qiData = pillar.hiddenQi
 }
 
 // Handle both object format {Yi: 100.0, Jia: 20.0} and array format
 if (qiData) {
  // Convert object to array format if needed
  let qiArray = []
  if (Array.isArray(qiData)) {
   qiArray = qiData
  } else if (typeof qiData === 'object') {
   // Convert {Yi: 100.0, Jia: 20.0} to [{stem: 'Yi', score: 100.0}, ...]
   qiArray = Object.entries(qiData).map(([stem, score]) => ({
    stem,
    score,
    count: 1
   }))
  }
  
 if (qiArray && qiArray.length > 0) {
  const result = {}
  const totalScore = qiArray.reduce((sum, qi) => sum + qi.score, 0)
  
  for (const qi of qiArray) {
   const percentage = Math.round((qi.score / totalScore) * 100)
   // Get ten god for this stem if available
   // Handle both string format and object format
   const tenGodData = pillar.hiddenStems?.[qi.stem]
   const tenGod = typeof tenGodData === 'string' 
    ? tenGodData 
    : tenGodData?.abbreviation || tenGodData?.id || ''
   // Use hex color from API mappings as source of truth
   const stemColor = qi.hex_color || qi.color || chartData.value?.mappings?.heavenly_stems?.[qi.stem]?.hex_color || null
   result[qi.stem] = {
    god: tenGod,
    weight: percentage,
    score: qi.score,
    count: qi.count,
    color: stemColor
   }
  }
  return result
 }
 }
 
 // Fallback: use API mappings for qi percentages instead of hardcoding
 if (!pillar.hiddenStems) return {}

 // Get branch name and fetch qi data from API mappings
 const branchName = pillar.branchName
 const branchData = chartData.value?.mappings?.earthly_branches?.[branchName]

 if (branchData?.qi && branchData.qi.length > 0) {
  // Use API-provided qi data
  const totalScore = branchData.qi.reduce((sum, qi) => sum + qi.score, 0)
  const result = {}
  for (const qi of branchData.qi) {
   const percentage = Math.round((qi.score / totalScore) * 100)
   const tenGodData = pillar.hiddenStems?.[qi.stem]
   const tenGod = typeof tenGodData === 'string'
    ? tenGodData
    : tenGodData?.abbreviation || tenGodData?.id || ''
   result[qi.stem] = {
    god: tenGod,
    weight: percentage,
    score: qi.score,
    color: qi.hex_color || null
   }
  }
  return result
 }

 // Final fallback: distribute evenly if API qi not available
 const stems = Object.entries(pillar.hiddenStems)
 const result = {}
 const evenWeight = Math.floor(100 / stems.length)
 for (const [stem, tenGod] of stems) {
  result[stem] = { god: tenGod, weight: evenWeight }
 }
 return result
}

// Get Primary Qi (本氣) - the main energy at index 0
// Weight is proportional to TOTAL qi (Primary + Hidden combined)
function getPrimaryQiData(pillar) {
 const ebNode = nodes.value?.[pillar.branchKey]

 // Get qi data (same logic as getHiddenStemsWithWeights)
 let qiData = null
 const hasPostQi = ebNode?.post_interaction_qi && Object.keys(ebNode.post_interaction_qi).length > 0
 const hasBaseQi = ebNode?.base_qi && Object.keys(ebNode.base_qi).length > 0
 const hasPillarQi = pillar.hiddenQi && (Array.isArray(pillar.hiddenQi) ? pillar.hiddenQi.length > 0 : Object.keys(pillar.hiddenQi).length > 0)

 if (hasPostQi) {
  qiData = ebNode.post_interaction_qi
 } else if (hasBaseQi) {
  qiData = ebNode.base_qi
 } else if (hasPillarQi) {
  qiData = pillar.hiddenQi
 }

 if (!qiData) return null

 // Convert to array format
 let qiArray = []
 if (Array.isArray(qiData)) {
  qiArray = qiData
 } else if (typeof qiData === 'object') {
  qiArray = Object.entries(qiData).map(([stem, score]) => ({
   stem,
   score,
   count: 1
  }))
 }

 if (qiArray.length === 0) return null

 // Calculate TOTAL qi for percentage
 const totalScore = qiArray.reduce((sum, qi) => sum + qi.score, 0)

 // Primary Qi is index 0
 const primaryQi = qiArray[0]
 const percentage = Math.round((primaryQi.score / totalScore) * 100)

 // Get ten god
 const tenGodData = pillar.hiddenStems?.[primaryQi.stem]
 const tenGod = typeof tenGodData === 'string'
  ? tenGodData
  : tenGodData?.abbreviation || tenGodData?.id || ''

 // Get color - use API mappings as source of truth
 const stemColor = primaryQi.hex_color || primaryQi.color || chartData.value?.mappings?.heavenly_stems?.[primaryQi.stem]?.hex_color || null

 return {
  stem: primaryQi.stem,
  god: tenGod,
  weight: percentage,
  score: primaryQi.score,
  color: stemColor
 }
}

// Get Hidden Stems (藏干) - secondary/tertiary energies at index 1+
// Weights are proportional to TOTAL qi (Primary + Hidden combined)
function getHiddenStemsData(pillar) {
 const ebNode = nodes.value?.[pillar.branchKey]

 // Get qi data (same logic as getHiddenStemsWithWeights)
 let qiData = null
 const hasPostQi = ebNode?.post_interaction_qi && Object.keys(ebNode.post_interaction_qi).length > 0
 const hasBaseQi = ebNode?.base_qi && Object.keys(ebNode.base_qi).length > 0
 const hasPillarQi = pillar.hiddenQi && (Array.isArray(pillar.hiddenQi) ? pillar.hiddenQi.length > 0 : Object.keys(pillar.hiddenQi).length > 0)

 if (hasPostQi) {
  qiData = ebNode.post_interaction_qi
 } else if (hasBaseQi) {
  qiData = ebNode.base_qi
 } else if (hasPillarQi) {
  qiData = pillar.hiddenQi
 }

 if (!qiData) return []

 // Convert to array format
 let qiArray = []
 if (Array.isArray(qiData)) {
  qiArray = qiData
 } else if (typeof qiData === 'object') {
  qiArray = Object.entries(qiData).map(([stem, score]) => ({
   stem,
   score,
   count: 1
  }))
 }

 // Need at least 2 entries to have hidden stems
 if (qiArray.length < 2) return []

 // Calculate TOTAL qi for percentage
 const totalScore = qiArray.reduce((sum, qi) => sum + qi.score, 0)

 // Hidden Stems are index 1+
 const hiddenStems = qiArray.slice(1)

 return hiddenStems.map(qi => {
  const percentage = Math.round((qi.score / totalScore) * 100)
  const tenGodData = pillar.hiddenStems?.[qi.stem]
  const tenGod = typeof tenGodData === 'string'
   ? tenGodData
   : tenGodData?.abbreviation || tenGodData?.id || ''
  // Get color - use API mappings as source of truth
  const stemColor = qi.hex_color || qi.color || chartData.value?.mappings?.heavenly_stems?.[qi.stem]?.hex_color || null

  return {
   stem: qi.stem,
   god: tenGod,
   weight: percentage,
   score: qi.score,
   color: stemColor
  }
 })
}

function getElementBorderColor(element) {
 const colorMap = {
  'Wood': 'border-green-500',
  'Fire': 'border-red-500',
  'Earth': 'border-yellow-500',
  'Metal': 'border-gray-500',
  'Water': 'border-blue-500'
 }
 return colorMap[element] || 'border-gray-400'
}

function getInteractionBorderColor(type) {
 if (type.includes('NATURAL')) return 'border-purple-400'
 if (type.includes('CONFLICT') || type.includes('CLASH') || type.includes('HARM') || type.includes('DESTRUCTION') || type.includes('PUNISHMENT')) return 'border-red-400'
 if (type.includes('COMBINATION') || type.includes('HARMONY')) return 'border-green-400'
 if (type.includes('MEETING')) return 'border-blue-400'
 return 'border-gray-400'
}

// Get subtle left border class for log entries
function getLogBorderClass(type) {
 if (type.includes('NATURAL')) return 'border-l-4 border-l-purple-300'
 if (type.includes('CONFLICT') || type.includes('CLASH') || type.includes('HARM') || type.includes('DESTRUCTION') || type.includes('PUNISHMENT')) return 'border-l-4 border-l-red-300'
 if (type.includes('COMBINATION') || type.includes('HARMONY')) return 'border-l-4 border-l-green-300'
 if (type.includes('MEETING')) return 'border-l-4 border-l-blue-300'
 return 'border-l-4 border-l-gray-300'
}

function getInteractionTextColor(type) {
 if (type.includes('NATURAL')) return 'text-purple-700'
 if (type.includes('CONFLICT') || type.includes('CLASH') || type.includes('HARM') || type.includes('DESTRUCTION') || type.includes('PUNISHMENT')) return 'text-red-700'
 if (type.includes('COMBINATION') || type.includes('HARMONY')) return 'text-green-700'
 if (type.includes('MEETING')) return 'text-blue-700'
 return 'text-gray-700'
}

function formatInteractionType(type) {
 const typeMap = {
  'THREE_MEETINGS': '三會 Three Meetings',
  'HALF_MEETING': '半會 Half Meeting',
  'PUNISHMENTS': '相刑 Punishments',
  'THREE_COMBINATIONS': '三合 Three Combinations',
  'SIX_HARMONIES': '六合 Six Harmonies',
  'ARCHED_COMBINATIONS': '拱合 Arched Combinations',
  'ARCHED_COMBINATION': '拱合 Arched Combination',
  'CLASHES': '沖 Clashes',
  'HARMS': '害 Harms',
  'DESTRUCTIONS': '破 Destructions',
  'DESTRUCTION': '破 Destruction',
  'HS_CONFLICT': '天干沖 Stem Conflicts',
  'STEM_CONFLICT': '天干沖 Stem Conflict',
  'HS_COMBINATION': '天干合 Stem Combinations',
  'STEM_COMBINATION': '天干合 Stem Combination',
  'NATURAL_GENERATING': '生 Energy Flow (Generation)',
  'NATURAL_CONTROLLING': '剋 Energy Flow (Control)',
  'ENERGY_FLOW_GENERATING': '生 Energy Flow (Generation)',
  'ENERGY_FLOW_CONTROLLING': '剋 Energy Flow (Control)',
  'ENERGY_FLOW': '氣 Energy Flow',
  'SEASONAL_ADJUSTMENT': '季節調整 Seasonal Adjustment'
 }
 return typeMap[type] || type
}

function formatInteractionDescription(interaction) {
 if (interaction.description) return interaction.description
 
 if (interaction.type === 'HS_CONFLICT' && interaction.conflictor) {
  return `${interaction.conflictor.stem} (conflictor, -${interaction.conflictor.reduction}%) conflicts with ${interaction.conflicted.stem} (conflicted, -${interaction.conflicted.reduction}%)`
 }
 
 if (interaction.relationship) return interaction.relationship
 
 if (interaction.branches) {
  return `Branches: ${interaction.branches.join(', ')}`
 }
 
 if (interaction.stems) {
  return `Stems: ${interaction.stems.join(', ')}`
 }
 
 return ''
}

// Get pre/post element scores for an interaction
function getInteractionElementScores(interaction) {
 if (!chartData.value) return null
 
 // Get base (pre) and post element scores from chartData
 const baseScores = chartData.value.base_element_score || {}
 const postScores = chartData.value.post_element_score || {}
 
 // If no element changes in this interaction, return null
 if (!interaction.element_changes || Object.keys(interaction.element_changes).length === 0) {
  return null
 }
 
 // Build scores object for affected elements
 const scores = {}
 const fiveElements = ['Wood', 'Fire', 'Earth', 'Metal', 'Water']
 
 for (const element of fiveElements) {
  // Get all stems for this element from baseScores
  const stemIds = Object.keys(baseScores).filter(stemId => {
   const mapping = chartData.value.mappings?.heavenly_stems?.[stemId]
   if (!mapping) return false
   const stemElement = mapping.english || ''
   // Match "Yang Fire" or "Yin Fire" to "Fire"
   return stemElement.includes(element)
  })
  
  // Sum up scores for this element
  let preTotal = 0
  let postTotal = 0
  
  for (const stemId of stemIds) {
   preTotal += baseScores[stemId] || 0
   postTotal += postScores[stemId] || 0
  }
  
  // Only include if there's a change
  const change = postTotal - preTotal
  if (Math.abs(change) > 0.1) { // Small threshold to avoid floating point noise
   scores[element] = {
    pre: preTotal,
    post: postTotal,
    change: change
   }
  }
 }
 
 return Object.keys(scores).length > 0 ? scores : null
}

function formatNodeName(node) {
 const nodeMap = {
  'hs_y': 'Year Stem',
  'hs_m': 'Month Stem',
  'hs_d': 'Day Stem',
  'hs_h': 'Hour Stem',
  'hs_10yl': '10-Year Luck Stem',
  'hs_yl': 'Annual Luck Stem',
  'hs_ml': 'Monthly Luck Stem',
  'hs_dl': 'Daily Luck Stem',
  'hs_hl': 'Hourly Luck Stem',
  'eb_y': 'Year Branch',
  'eb_m': 'Month Branch',
  'eb_d': 'Day Branch',
  'eb_h': 'Hour Branch',
  'eb_10yl': '10-Year Luck Branch',
  'eb_yl': 'Annual Luck Branch',
  'eb_ml': 'Monthly Luck Branch',
  'eb_dl': 'Daily Luck Branch',
  'eb_hl': 'Hourly Luck Branch',
  'hs_o1': 'Overseas 1 Stem',
  'eb_o1': 'Overseas 1 Branch',
  'hs_o2': 'Overseas 2 Stem',
  'eb_o2': 'Overseas 2 Branch',
  'hs_b1': 'Birthplace 1 Stem',
  'eb_b1': 'Birthplace 1 Branch',
  'hs_b2': 'Birthplace 2 Stem',
  'eb_b2': 'Birthplace 2 Branch',
  'hs_b3': 'Birthplace 3 Stem',
  'eb_b3': 'Birthplace 3 Branch',
  'hs_b4': 'Birthplace 4 Stem',
  'eb_b4': 'Birthplace 4 Branch'
 }
 return nodeMap[node] || node
}

function getPillarPosition(position) {
 const positions = ['Year', 'Month', 'Day', 'Hour', '10-Year Luck', 'Annual Luck', 'Monthly Luck', 'Daily Luck', 'Hourly Luck']
 return positions[position] || position
}

function getTenGodLabel(element) {
 if (!chartData.value?.daymaster_analysis) return ''
 
 const daymaster = chartData.value.daymaster_analysis.daymaster
 const daymasterElement = daymaster.split(' ')[1] // Get element part
 const daymasterPolarity = daymaster.split(' ')[0] // Get polarity (Yang/Yin)
 const elementName = element.split(' ')[1] // Get element part
 const elementPolarity = element.split(' ')[0] // Get polarity
 
 // WuXing cycle: Wood -> Fire -> Earth -> Metal -> Water -> Wood
 const cycle = ['Wood', 'Fire', 'Earth', 'Metal', 'Water']
 const dmIndex = cycle.indexOf(daymasterElement)
 const elIndex = cycle.indexOf(elementName)
 
 // Calculate relationship distance
 const distance = (elIndex - dmIndex + 5) % 5
 
 // Determine Ten God based on distance and polarity match
 const polarityMatch = daymasterPolarity === elementPolarity
 
 switch(distance) {
  case 0: // Same element
   return polarityMatch ? '比肩 Friend' : '劫財 Rob Wealth'
  case 1: // Element I generate (child)
   return polarityMatch ? '食神 Eating God' : '傷官 Hurting Officer'
  case 2: // Element that generates my child (wealth)
   return polarityMatch ? '偏財 Indirect Wealth' : '正財 Direct Wealth'
  case 3: // Element that controls me (officer)
   return polarityMatch ? '偏官 Seven Killings' : '正官 Direct Officer'
  case 4: // Element that generates me (resource)
   return polarityMatch ? '偏印 Indirect Resource' : '正印 Direct Resource'
  default:
   return ''
 }
}

function getElementRelationship(daymasterElement, element) {
 // WuXing cycle relationships
 const cycle = ['Wood', 'Fire', 'Earth', 'Metal', 'Water']
 const dmIndex = cycle.indexOf(daymasterElement)
 const elIndex = cycle.indexOf(element)
 
 const distance = (elIndex - dmIndex + 5) % 5
 
 switch(distance) {
  case 0:
   return 'Self/Companion'
  case 1:
   return 'Output/Expression'
  case 2:
   return 'Wealth'
  case 3:
   return 'Officer/Status'
  case 4:
   return 'Resource/Support'
  default:
   return ''
 }
}

// Interactive handlers
function handleNodeHover(nodeId, nodeKey) {
 hoveredNode.value = nodeId
 highlightedNodes.value = []
 
 // Find interactions involving this node
 const nodeInteractions = getNodeInteractions(nodeKey)
 
 // Highlight connected nodes
 nodeInteractions.forEach(interaction => {
  if (interaction.nodes) {
   interaction.nodes.forEach(node => {
    if (node !== nodeKey) {
     const nodeIndex = getNodeIndex(node)
     if (nodeIndex !== -1) {
      const nodeType = node.startsWith('hs') ? 'stem' : 'branch'
      highlightedNodes.value.push(`${nodeType}-${nodeIndex}`)
     }
    }
   })
  }
 })
 
 // Show tooltip
 if (nodeInteractions.length > 0) {
  const event = window.event
  tooltipContent.value = {
   title: `${nodeInteractions.length} Interactions`,
   description: nodeInteractions.map(i => formatShortInteraction(i)).join(', '),
   effect: nodeInteractions.some(i => i.effect === 'High') ? 'Strong influence' : 'Moderate influence'
  }
  tooltipPosition.value = {
   x: event.pageX + 10,
   y: event.pageY - 50
  }
 }
}

function handleNodeLeave() {
 hoveredNode.value = null
 highlightedNodes.value = []
 highlightContext.value = null // Clear context
 hoveredTransformationId.value = null // Clear transformation highlight
 tooltipContent.value = null
}

function handleInteractionHover(interaction) {
 hoveredInteraction.value = interaction.id
 highlightedNodes.value = []
 highlightContext.value = interaction // Set context for element-based coloring
 
 // Highlight nodes involved in this interaction
 if (interaction.nodes) {
  interaction.nodes.forEach(node => {
   const nodeIndex = getNodeIndex(node)
   if (nodeIndex !== -1) {
    const nodeType = node.startsWith('hs') ? 'stem' : 'branch'
    highlightedNodes.value.push(`${nodeType}-${nodeIndex}`)
   }
  })
 }
 
 // Show detailed tooltip
 const event = window.event
 tooltipContent.value = {
  title: formatInteractionType(interaction.type),
  description: formatInteractionDescription(interaction),
  effect: interaction.effect || 'Modifies element energies'
 }
 tooltipPosition.value = {
  x: event.pageX + 10,
  y: event.pageY - 50
 }
}

function getTransformBadgeDisplay(badge) {
 if (!badge) return ''
 
 // Map stem IDs to their Chinese characters
 const stemToChinese = {
  'Jia': '甲', 'Yi': '乙', 'Bing': '丙', 'Ding': '丁',
  'Wu': '戊', 'Ji': '己', 'Geng': '庚', 'Xin': '辛',
  'Ren': '壬', 'Gui': '癸'
 }
 
 // Map pure elements to their Chinese characters
 const elementToChinese = {
  'Wood': '木', 'Fire': '火', 'Earth': '土',
  'Metal': '金', 'Water': '水'
 }
 
 // Check if it's a stem ID
 if (stemToChinese[badge]) {
  return stemToChinese[badge]
 }
 
 // Check if it's a pure element
 if (elementToChinese[badge]) {
  return elementToChinese[badge]
 }
 
 // If it contains 'Yang' or 'Yin', extract the element part
 if (badge.includes('Yang') || badge.includes('Yin')) {
  const element = badge.replace('Yang ', '').replace('Yin ', '')
  return elementToChinese[element] || badge
 }
 
 // Default: return as is
 return badge
}

function getTransformBadgeStyle(badge) {
 if (!badge) return {}

 const mappings = chartData.value?.mappings

 // Get color from API mappings - source of truth
 let bgColor = null

 // Try stem color from API mappings
 if (badge && mappings?.heavenly_stems?.[badge]?.hex_color) {
  bgColor = mappings.heavenly_stems[badge].hex_color
 }
 // Try element color from API mappings
 else if (badge && mappings?.elements?.[badge]?.hex_color) {
  bgColor = mappings.elements[badge].hex_color
 }
 // Try polarized element (e.g., "Yang Wood") - parse and look up
 else if (badge && badge.includes(' ')) {
  const [polarity, element] = badge.split(' ')
  const colorKey = polarity === 'Yang' ? 'hex_color_yang' : 'hex_color_yin'
  bgColor = mappings?.elements?.[element]?.[colorKey] || mappings?.elements?.[element]?.hex_color
 }
 // Fallback to default
 if (!bgColor) {
  bgColor = '#fbbf24'
 }
 
 // Calculate a darker text color for contrast
 const textColor = getLightnessPercent(bgColor) > 70 ? '#1f2937' : '#ffffff'
 
 return {
  backgroundColor: bgColor,
  color: textColor,
  border: `2px solid ${adjustBrightness(bgColor, -20)}`,
  boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)'
 }
}

// Helper function to calculate lightness percentage
function getLightnessPercent(hexColor) {
 const hex = hexColor.replace('#', '')
 const r = parseInt(hex.substr(0, 2), 16)
 const g = parseInt(hex.substr(2, 2), 16)
 const b = parseInt(hex.substr(4, 2), 16)
 return (0.299 * r + 0.587 * g + 0.114 * b) / 255 * 100
}

// Helper function to adjust brightness
function adjustBrightness(hexColor, percent) {
 const hex = hexColor.replace('#', '')
 const r = Math.max(0, Math.min(255, parseInt(hex.substr(0, 2), 16) + percent * 2.55))
 const g = Math.max(0, Math.min(255, parseInt(hex.substr(2, 2), 16) + percent * 2.55))
 const b = Math.max(0, Math.min(255, parseInt(hex.substr(4, 2), 16) + percent * 2.55))
 return '#' + [r, g, b].map(x => Math.round(x).toString(16).padStart(2, '0')).join('')
}

// NEW: Multi-transformation badge functions with strength-based styling
function getTransformationBadgeStyles(transformation) {
 if (!transformation) return {}

 const { badge, strength, element } = transformation
 const mappings = chartData.value?.mappings

 // Get color from API mappings - source of truth
 let baseBgColor = null

 // First try stem color from API mappings
 if (badge && mappings?.heavenly_stems?.[badge]?.hex_color) {
  baseBgColor = mappings.heavenly_stems[badge].hex_color
 }
 // Then try element color from API mappings
 else if (element && mappings?.elements?.[element]?.hex_color) {
  baseBgColor = mappings.elements[element].hex_color
 }
 // Fallback to default
 else {
  baseBgColor = '#fbbf24'
 }
 const textColor = getLightnessPercent(baseBgColor) > 70 ? '#1f2937' : '#ffffff'
 const borderColor = adjustBrightness(baseBgColor, -20)
 
 // Strength differentiation: SIZE (via CSS class) + GLOW only
 const strengthStyles = {
  ultra_strong: {
   bgColor: baseBgColor,
   textColor: textColor,
   border: `2px solid ${borderColor}`,
   boxShadow: `0 0 10px ${baseBgColor}, 0 2px 4px rgba(0, 0, 0, 0.1)`, // Strong glow
   opacity: 1
  },
  strong: {
   bgColor: baseBgColor,
   textColor: textColor,
   border: `2px solid ${borderColor}`,
   boxShadow: `0 0 6px ${baseBgColor}, 0 2px 4px rgba(0, 0, 0, 0.1)`, // Medium glow
   opacity: 1
  },
  normal: {
   bgColor: baseBgColor,
   textColor: textColor,
   border: `2px solid ${borderColor}`,
   boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)', // Subtle shadow only
   opacity: 1
  },
  weak: {
   bgColor: baseBgColor,
   textColor: textColor,
   border: `2px solid ${borderColor}`,
   boxShadow: '0 1px 2px rgba(0, 0, 0, 0.05)',
   opacity: 0.7
  }
 }
 
 const style = strengthStyles[strength] || strengthStyles.normal
 
 return {
  backgroundColor: style.bgColor,
  color: style.textColor,
  border: style.border,
  boxShadow: style.boxShadow,
  opacity: style.opacity
 }
}

function getTransformationSizeClass(strength) {
 const sizeClasses = {
  ultra_strong: 'w-8 h-10 text-xs',   // 32px
  strong: 'w-7 h-7 text-xs',    // 28px
  normal: 'w-5 h-5 text-[10px]',    // 24px (current default)
  weak: 'w-5 h-5 text-[10px]'      // 20px
 }
 return sizeClasses[strength] || sizeClasses.normal
}

function getStrengthIndicator(strength) {
 const indicators = {
  ultra_strong: '★★', // 2 stars
  strong: '★',     // 1 star
  normal: '●',     // Filled dot
  weak: '○'      // Hollow dot
 }
 return indicators[strength] || indicators.normal
}

// Combination badge size classes
function getCombinationBadgeSizeClass(strength) {
 const sizeClasses = {
  ultra_strong: 'w-5 h-5 text-xs',      // 24px
  strong: 'w-5 h-5 text-[10px]',        // 20px
  normal: 'w-5 h-5 text-[8px]',         // 16px (default)
  weak: 'w-3 h-3 text-[8px]'            // 12px
 }
 return sizeClasses[strength] || sizeClasses.normal
}

// Combination badge styling
function getCombinationBadgeStyle(combination) {
 if (!combination) return {}

 const { badge, element } = combination
 const mappings = chartData.value?.mappings

 // Get color from API mappings - source of truth
 let baseBgColor = null

 // First try stem color from API mappings
 if (badge && mappings?.heavenly_stems?.[badge]?.hex_color) {
  baseBgColor = mappings.heavenly_stems[badge].hex_color
 }
 // Then try element color from API mappings
 else if (element && mappings?.elements?.[element]?.hex_color) {
  baseBgColor = mappings.elements[element].hex_color
 }
 // Fallback to default
 else {
  baseBgColor = '#e5e7eb'
 }
 const textColor = '#6b7280' // Gray-500 for subtle effect
 
 return {
  backgroundColor: baseBgColor,
  color: textColor,
  border: `1.5px dashed ${adjustBrightness(baseBgColor, -30)}`,
  boxShadow: 'none',
  opacity: 0.6,
  background: `repeating-linear-gradient(45deg, ${baseBgColor}, ${baseBgColor} 2px, ${adjustBrightness(baseBgColor, -5)} 2px, ${adjustBrightness(baseBgColor, -5)} 4px)`
 }
}

function getCombinationTooltip(combination) {
 if (!combination) return ''

 // Get full interaction data from chartData using interaction_id
 const fullInteraction = getFullInteractionData(combination)

 const typeLabels = {
  THREE_MEETINGS: '三會 (Three Meetings)',
  THREE_COMBINATIONS: '三合 (Three Combinations)',
  HALF_MEETING: '半會 (Half Meeting)',
  SIX_HARMONIES: '六合 (Six Harmonies)',
  ARCHED_COMBINATIONS: '拱合 (Arched Combinations)',
  STEM_COMBINATION: '天干合 (Stem Combination)'
 }

 let tooltip = `${typeLabels[combination.type] || combination.type}\n` +
     `Pattern: ${combination.pattern || fullInteraction.pattern || 'N/A'}\n` +
     `→ ${combination.element || fullInteraction.element || 'Partial transformation'}`
 
 // Add detailed debugging information from full interaction data
 if (fullInteraction) {
  tooltip += `\n\n━━━ Debug Info ━━━`
  
  // Interaction ID first
  if (combination.interaction_id) {
   tooltip += `\nInteraction ID: ${combination.interaction_id}`
  }
  
  if (fullInteraction.nodes && fullInteraction.nodes.length > 0) {
   tooltip += `\nNodes: ${fullInteraction.nodes.join(', ')}`
  }
  
  if (fullInteraction.distance !== undefined) {
   tooltip += `\nDistance: ${fullInteraction.distance}`
  }
  
  if (fullInteraction.transformed !== undefined) {
   tooltip += `\nTransformed: ${fullInteraction.transformed ? 'Yes' : 'No'}`
  }
  
  if (fullInteraction.branches && fullInteraction.branches.length > 0) {
   tooltip += `\nBranches: ${fullInteraction.branches.join(', ')}`
  }
  
  if (fullInteraction.stems && fullInteraction.stems.length > 0) {
   tooltip += `\nStems: ${fullInteraction.stems.join(', ')}`
  }
  
  // Show any additional fields that might exist
  const knownFields = ['type', 'pattern', 'nodes', 'positions', 'transformed', 'element', 'distance', 'branches', 'stems', 'stage', 'effect', 'description']
  Object.keys(fullInteraction).forEach(key => {
   if (!knownFields.includes(key) && fullInteraction[key] !== undefined && fullInteraction[key] !== null) {
    tooltip += `\n${key}: ${JSON.stringify(fullInteraction[key])}`
   }
  })
 }
 
 return tooltip
}

// Negative badge functions - same as transformations, just display the badge character
// Helper to get Chinese character for stem name (for hidden stems display)
function getStemChinese(stemName) {
 const stemToChinese = {
  'Jia': '甲', 'Yi': '乙', 'Bing': '丙', 'Ding': '丁',
  'Wu': '戊', 'Ji': '己', 'Geng': '庚', 'Xin': '辛',
  'Ren': '壬', 'Gui': '癸'
 }
 return stemToChinese[stemName] || ''
}

function getNegativeBadgeSymbol(negative) {
 if (!negative || !negative.badge) return '●'
 
 // Map stem IDs to their Chinese characters (same as getTransformBadgeDisplay)
 const stemToChinese = {
  'Jia': '甲', 'Yi': '乙', 'Bing': '丙', 'Ding': '丁',
  'Wu': '戊', 'Ji': '己', 'Geng': '庚', 'Xin': '辛',
  'Ren': '壬', 'Gui': '癸'
 }
 
 // Map branch IDs to their Chinese characters
 const branchToChinese = {
  'Zi': '子', 'Chou': '丑', 'Yin': '寅', 'Mao': '卯',
  'Chen': '辰', 'Si': '巳', 'Wu': '午', 'Wei': '未',
  'Shen': '申', 'You': '酉', 'Xu': '戌', 'Hai': '亥'
 }
 
 // Map pure elements to their Chinese characters
 const elementToChinese = {
  'Wood': '木', 'Fire': '火', 'Earth': '土',
  'Metal': '金', 'Water': '水'
 }
 
 // Map special negative interaction symbols
 const specialSymbols = {
  'KE': '剋'  // Stem conflict control/restrain symbol
 }
 
 return stemToChinese[negative.badge] || 
        branchToChinese[negative.badge] || 
        elementToChinese[negative.badge] || 
        specialSymbols[negative.badge] ||
        negative.badge
}

function getNegativeBadgeSizeClass(strength) {
 const sizeClasses = {
  ultra_strong: 'w-5 h-5 text-[10px]',      // 24px container, smaller text
  strong: 'w-5 h-5 text-[8px]',            // 20px container, smaller text
  normal: 'w-5 h-5 text-[8px]',            // 16px container, smaller text
  weak: 'w-5 h-5 text-[8px]'               // 12px container, smaller text
 }
 return sizeClasses[strength] || sizeClasses.normal
}

function getNegativeBadgeStyle(negative) {
 if (!negative) return {}

 const { badge, type, strength } = negative
 const mappings = chartData.value?.mappings

 // Get color from API mappings - source of truth
 let baseBgColor = null

 // Special handling for KE (stem conflict) - transparent
 if (badge === 'KE') {
  baseBgColor = 'transparent'
 }
 // Try stem color from API mappings
 else if (badge && mappings?.heavenly_stems?.[badge]?.hex_color) {
  baseBgColor = mappings.heavenly_stems[badge].hex_color
 }
 // Try branch color from API mappings
 else if (badge && mappings?.earthly_branches?.[badge]?.hex_color) {
  baseBgColor = mappings.earthly_branches[badge].hex_color
 }
 // Try element color from API mappings
 else if (mappings?.elements?.Earth?.hex_color) {
  baseBgColor = mappings.elements.Earth.hex_color
 }
 // Fallback to default
 else {
  baseBgColor = '#fbbf24'
 }
 // Special handling for transparent KE badge - use black text
 const textColor = badge === 'KE' ? '#000000' : (getLightnessPercent(baseBgColor) > 70 ? '#1f2937' : '#ffffff')
 const borderColor = badge === 'KE' ? '#000000' : adjustBrightness(baseBgColor, -20)
 
 // Type-based border styling (different visual flair for each type)
 const typeStyles = {
  'clash': {
   borderStyle: 'solid',
   borderWidth: '3px',
   shape: 'square'  // Square with sharp corners
  },
  'harm': {
   borderStyle: 'dashed',
   borderWidth: '2.5px',
   shape: 'square'
  },
  'punishment': {
   borderStyle: 'double',
   borderWidth: '3px',
   shape: 'square'
  },
  'destruction': {
   borderStyle: 'dotted',
   borderWidth: '3px',
   shape: 'square'
  },
  'stem_conflict': {
   borderStyle: 'solid',
   borderWidth: '3px',
   shape: 'square'  // Stem conflict (天干沖)
  }
 }
 
 const typeStyle = typeStyles[type] || typeStyles.clash
 
 // Strength-based glow intensity (similar to transformations)
 const strengthStyles = {
  ultra_strong: {
   bgColor: baseBgColor,
   textColor: textColor,
   border: `${typeStyle.borderWidth} ${typeStyle.borderStyle} ${borderColor}`,
   boxShadow: `0 0 12px ${baseBgColor}, 0 4px 6px rgba(0, 0, 0, 0.2)`,
   opacity: 1
  },
  strong: {
   bgColor: baseBgColor,
   textColor: textColor,
   border: `${typeStyle.borderWidth} ${typeStyle.borderStyle} ${borderColor}`,
   boxShadow: `0 0 8px ${baseBgColor}, 0 2px 4px rgba(0, 0, 0, 0.15)`,
   opacity: 1
  },
  normal: {
   bgColor: baseBgColor,
   textColor: textColor,
   border: `2px ${typeStyle.borderStyle} ${borderColor}`,
   boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)',
   opacity: 1
  },
  weak: {
   bgColor: baseBgColor,
   textColor: textColor,
   border: `2px ${typeStyle.borderStyle} ${borderColor}`,
   boxShadow: '0 1px 2px rgba(0, 0, 0, 0.05)',
   opacity: 0.8
  }
 }
 
 const style = strengthStyles[strength] || strengthStyles.normal
 
 return {
  backgroundColor: style.bgColor,
  color: style.textColor,
  border: style.border,
  boxShadow: style.boxShadow,
  opacity: style.opacity,
  borderRadius: '0'  // Square with sharp edges
 }
}

// Helper function to fetch full interaction data from chartData using interaction_id
function getFullInteractionData(badge) {
 if (!badge || !badge.interaction_id || !chartData.value?.interactions) {
  return {}
 }
 
 // Try direct lookup first
 let interaction = chartData.value.interactions[badge.interaction_id]
 if (interaction) return interaction
 
 // If not found, try normalizing the interaction_id
 // Badge format examples: HS_COMBINATION_Ding-Ren_hs_h-hs_y, SIX_HARMONIES_Si-Shen_eb_h-eb_y
 // Interaction key examples: STEM_COMBINATION~Ding-Ren~hs_h-hs_y, SIX_HARMONIES~Si-Shen~eb_h-eb_y
 
 let normalizedId = badge.interaction_id
 
 // Replace HS_COMBINATION with STEM_COMBINATION
 normalizedId = normalizedId.replace('HS_COMBINATION', 'STEM_COMBINATION')
 
 // Try replacing underscores with tildes for the key format
 const parts = normalizedId.split('_')
 if (parts.length >= 3) {
  // Find where the pattern starts (after type, before nodes)
  const type = parts[0]
  
  // Check if it's a compound type like THREE_MEETINGS, STEM_COMBINATION, etc.
  let typeEndIndex = 1
  const compoundTypes = ['THREE_MEETINGS', 'THREE_COMBINATIONS', 'SIX_HARMONIES',
              'ARCHED_COMBINATIONS', 'STEM_COMBINATION', 'STEM_CONFLICT']
  
  for (const compoundType of compoundTypes) {
   if (normalizedId.startsWith(compoundType)) {
    typeEndIndex = compoundType.split('_').length
    break
   }
  }
  
  const typeParts = parts.slice(0, typeEndIndex)
  const restParts = parts.slice(typeEndIndex)
  
  // Find where pattern ends (look for node pattern like hs_ or eb_)
  let patternEndIndex = 0
  for (let i = 0; i < restParts.length; i++) {
   if (restParts[i].match(/^(hs|eb)$/)) {
    patternEndIndex = i
    break
   }
  }
  
  if (patternEndIndex > 0) {
   const pattern = restParts.slice(0, patternEndIndex).join('-')
   const nodes = restParts.slice(patternEndIndex).join('_')
   normalizedId = `${typeParts.join('_')}~${pattern}~${nodes}`
  }
 }
 
 // Try the normalized lookup
 interaction = chartData.value.interactions[normalizedId]
 if (interaction) return interaction
 
 // If still not found, try iterating through all interactions to find a match
 for (const [key, value] of Object.entries(chartData.value.interactions)) {
  if (key.includes(badge.pattern) || badge.interaction_id.includes(key)) {
   // Check if nodes match
   if (value.nodes && badge.interaction_id) {
    const badgeNodes = badge.interaction_id.match(/(hs|eb)_[a-z0-9]+/g) || []
    const matchingNodes = badgeNodes.filter(node => value.nodes.includes(node))
    if (matchingNodes.length >= 2) {
     return value
    }
   }
  }
 }
 
 return {}
}

function getNegativeBadgeTooltip(negative) {
 if (!negative) return ''
 
 // Get full interaction data from chartData using interaction_id
 const fullInteraction = getFullInteractionData(negative)
 
 const typeLabels = {
  'clash': '沖 (Clash)',
  'harm': '害 (Harm)',
  'punishment': '刑 (Punishment)',
  'destruction': '破 (Destruction)',
  'stem_conflict': '剋 (Stem Conflict)',
  'CLASHES': '沖 (Clash)',
  'HARMS': '害 (Harm)',
  'PUNISHMENTS': '刑 (Punishment)',
  'DESTRUCTIONS': '破 (Destruction)',
  'STEM_CONFLICT': '天干沖 (Stem Conflict)'
 }
 
 const strengthLabels = {
  ultra_strong: 'Severe',
  strong: 'Strong',
  normal: 'Moderate',
  weak: 'Weak'
 }
 
 let tooltip = `⚠️ ${typeLabels[negative.type] || negative.type}\n` +
     `Pattern: ${negative.pattern || fullInteraction.pattern || 'N/A'}\n` +
     `Severity: ${strengthLabels[negative.strength] || negative.strength}\n` +
     `Negative influence on energies`
 
 // Add detailed debugging information from full interaction data
 if (fullInteraction && Object.keys(fullInteraction).length > 0) {
  tooltip += `\n\n━━━ Debug Info ━━━`
  
  // Interaction ID first
  if (negative.interaction_id) {
   tooltip += `\nInteraction ID: ${negative.interaction_id}`
  }
  
  if (fullInteraction.nodes && fullInteraction.nodes.length > 0) {
   tooltip += `\nNodes: ${fullInteraction.nodes.join(', ')}`
  }
  
  if (fullInteraction.distance !== undefined) {
   tooltip += `\nDistance: ${fullInteraction.distance}`
  }
  
  if (fullInteraction.element !== undefined) {
   tooltip += `\nElement: ${fullInteraction.element}`
  }
  
  if (fullInteraction.branches && fullInteraction.branches.length > 0) {
   tooltip += `\nBranches: ${fullInteraction.branches.join(', ')}`
  }
  
  if (fullInteraction.stems && fullInteraction.stems.length > 0) {
   tooltip += `\nStems: ${fullInteraction.stems.join(', ')}`
  }
  
  if (fullInteraction.reduction_percentage !== undefined) {
   tooltip += `\nReduction: ${fullInteraction.reduction_percentage}%`
  }
  
  // Show any additional fields that might exist
  const knownFields = ['type', 'pattern', 'nodes', 'positions', 'element', 'distance', 'branches', 'stems', 'stage', 'effect', 'description', 'reduction_percentage', 'transformed']
  Object.keys(fullInteraction).forEach(key => {
   if (!knownFields.includes(key) && fullInteraction[key] !== undefined && fullInteraction[key] !== null) {
    tooltip += `\n${key}: ${JSON.stringify(fullInteraction[key])}`
   }
  })
 }
 
 return tooltip
}

// Wealth Storage badge functions
function getWealthStorageSymbol(ws) {
 if (!ws) return '📦'

 // Get detailed storage info from analysis
 const analysis = chartData.value?.wealth_storage_analysis
 let storageInfo = analysis?.storages?.find(s => s.interaction_id === ws.interaction_id)
 if (!storageInfo) {
  storageInfo = analysis?.pillar_storages?.find(s => s.interaction_id === ws.interaction_id)
 }

 const isLarge = (storageInfo?.storage_size === 'large') || (ws?.storage_size === 'large')

 // Simple icon based on storage SIZE only
 // Status (filled/opened) is shown via transparency, border, highlight
 // Large storage (大财库): 💎 treasure/gem
 // Small storage (小财库): 🪙 coin
 return isLarge ? '💎' : '🪙'
}

// Helper for Storage Analysis section (uses storage object directly, not badge)
function getStorageAnalysisIcon(storage) {
 if (!storage) return '📦'

 const isLarge = storage.storage_size === 'large' || storage.size === 'large'

 // Simple icon based on storage SIZE only
 // Status (filled/opened) is shown via transparency, border, highlight
 return isLarge ? '💎' : '🪙'
}

// Style for storage icon based on filled/opened state
function getStorageIconStyle(storage) {
 if (!storage) return {}

 const isOpened = storage.is_opened || false
 const isFilled = storage.is_filled || false

 // 4 distinct visual states via opacity, filter, and text-shadow
 if (isOpened && isFilled) {
  // Maximum - full brightness, golden glow
  return {
   opacity: '1',
   filter: 'drop-shadow(0 0 6px #ffd700) drop-shadow(0 0 10px rgba(255, 215, 0, 0.5))',
   transform: 'scale(1.1)'
  }
 } else if (isOpened) {
  // Opened but not filled - bright, green glow
  return {
   opacity: '0.9',
   filter: 'drop-shadow(0 0 4px #22c55e)',
   transform: 'scale(1.0)'
  }
 } else if (isFilled) {
  // Filled but not opened - bright, blue glow
  return {
   opacity: '0.85',
   filter: 'drop-shadow(0 0 3px #3b82f6)',
   transform: 'scale(1.0)'
  }
 } else {
  // Latent - low opacity, grayscale, no glow
  return {
   opacity: '0.4',
   filter: 'grayscale(50%)',
   transform: 'scale(0.9)'
  }
 }
}

function getWealthStorageSizeClass(ws) {
 if (!ws) return 'w-6 h-6 text-sm'

 // Get detailed storage info to determine exact activation level
 const analysis = chartData.value?.wealth_storage_analysis
 // Check both storages and pillar_storages
 let storageInfo = analysis?.storages?.find(s => s.interaction_id === ws.interaction_id)
 if (!storageInfo) {
  storageInfo = analysis?.pillar_storages?.find(s => s.interaction_id === ws.interaction_id)
 }

 const isOpened = storageInfo?.is_opened || false
 const isFilled = storageInfo?.is_filled || false
 const isLarge = (storageInfo?.storage_size === 'large') || (ws?.storage_size === 'large')

 // Size based on activation level AND storage size
 if (isOpened && isFilled) {
  return isLarge ? 'w-8 h-8 text-lg' : 'w-7 h-7 text-base' // Maximum
 } else if (isOpened || isFilled) {
  return isLarge ? 'w-7 h-7 text-base' : 'w-6 h-6 text-sm' // Partially activated
 } else {
  return isLarge ? 'w-6 h-6 text-sm' : 'w-5 h-5 text-xs'   // Latent
 }
}

function getWealthStorageBadgeStyle(ws) {
 if (!ws) return {}

 // Get detailed storage info to determine exact activation level
 const analysis = chartData.value?.wealth_storage_analysis
 // Check both storages and pillar_storages
 let storageInfo = analysis?.storages?.find(s => s.interaction_id === ws.interaction_id)
 if (!storageInfo) {
  storageInfo = analysis?.pillar_storages?.find(s => s.interaction_id === ws.interaction_id)
 }

 const isOpened = storageInfo?.is_opened || false
 const isFilled = storageInfo?.is_filled || false
 
 // Colors based on wealth element - using backend core.py colors (Yang polarity)
 const wealthColors = {
  'Wood': { bg: '#c2d4be', border: '#9ab894' },  // matches Jia (Yang Wood)
  'Fire': { bg: '#f3adae', border: '#e08384' },  // matches Bing (Yang Fire)
  'Earth': { bg: '#e6ceb7', border: '#c9a987' }, // matches Wu (Yang Earth)
  'Metal': { bg: '#ccd8e6', border: '#a3b8cc' }, // matches Geng (Yang Metal)
  'Water': { bg: '#b9cbff', border: '#8aa5e6' }  // matches Ren (Yang Water)
 }
 
 // Get wealth element from interaction data
 const wealthElem = analysis?.wealth_element || 'Metal'
 const colors = wealthColors[wealthElem] || wealthColors.Metal
 
 // Base style
 const baseStyle = {
  backgroundColor: colors.bg,
  borderRadius: '6px',
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center'
 }
 
 // Four distinct visual states based on filled + opened
 if (isOpened && isFilled) {
  // MAXIMUM (filled + opened) - gold border, strong glow, full opacity
  return {
   ...baseStyle,
   border: `3px solid #ffd700`,
   opacity: 1,
   boxShadow: `0 0 12px #ffd70080, 0 0 20px rgba(255, 215, 0, 0.4), 0 2px 6px rgba(0, 0, 0, 0.2)`
  }
 } else if (isOpened) {
  // OPENED but not filled - solid green border, medium glow, high opacity
  return {
   ...baseStyle,
   border: `2px solid #22c55e`,
   opacity: 0.9,
   boxShadow: `0 0 8px rgba(34, 197, 94, 0.5), 0 2px 4px rgba(0, 0, 0, 0.1)`
  }
 } else if (isFilled) {
  // FILLED but not opened - solid blue border, subtle glow, high opacity
  return {
   ...baseStyle,
   border: `2px solid #3b82f6`,
   opacity: 0.85,
   boxShadow: `0 0 6px rgba(59, 130, 246, 0.4), 0 1px 3px rgba(0, 0, 0, 0.1)`
  }
 } else {
  // LATENT (not filled, not opened) - dashed gray border, no glow, low opacity
  return {
   ...baseStyle,
   border: `2px dashed #9ca3af`,
   opacity: 0.4,
   boxShadow: 'none'
  }
 }
}

function getWealthStorageTooltip(ws) {
 if (!ws) return ''

 const analysis = chartData.value?.wealth_storage_analysis
 // Check both storages and pillar_storages
 let storageInfo = analysis?.storages?.find(s => s.interaction_id === ws.interaction_id)
 if (!storageInfo) {
  storageInfo = analysis?.pillar_storages?.find(s => s.interaction_id === ws.interaction_id)
 }

 const isOpened = storageInfo?.is_opened || false
 const isFilled = storageInfo?.is_filled || false
 const isLarge = (storageInfo?.storage_size === 'large') || (ws?.storage_size === 'large')
 const storageType = storageInfo?.storage_type || ws.storage_type || 'wealth'

 // Determine status text and icon
 const sizeLabel = isLarge ? '大财库 (Large)' : '小财库 (Small)'
 const statusIcon = isLarge ? '💎' : '🪙'

 let statusText = ''
 if (isOpened && isFilled) {
  statusText = 'Maximum (已开已填)'
 } else if (isOpened) {
  statusText = 'Opened (已开未填)'
 } else if (isFilled) {
  statusText = 'Filled (已填未开)'
 } else {
  statusText = 'Latent (潜在)'
 }
 
 const typeLabel = storageType === 'wealth' ? '财库 (Wealth Storage)' : '官库 (Influence Storage)'
 let tooltip = `${statusIcon} ${sizeLabel} - ${typeLabel}\n`
 tooltip += `Stores: ${storageInfo?.stored_element || 'Unknown'}\n`
 tooltip += `Status: ${statusText}\n`
 
 if (storageInfo?.branch_chinese) {
  tooltip += `Branch: ${storageInfo.branch_chinese} (${storageInfo.branch})\n`
 }
 
 // Activation details
 tooltip += `\n━━━ Activation Requirements ━━━`
 
 if (storageInfo) {
  // Opener status
  if (isOpened) {
   tooltip += `\n✓ Opened by: ${storageInfo.opener_branch} (${storageInfo.opener_positions?.join(', ')})`
  } else {
   tooltip += `\n○ Needs opener: ${storageInfo.opener_branch || 'clash branch'} to unlock`
  }
  
  // Filler status - use storage-specific filler stems
  if (isFilled) {
   tooltip += `\n✓ Filled from: ${storageInfo.filler_positions?.join(', ')}`
  } else {
   const fillerStems = storageInfo.filler_stems?.join('/') || (storageType === 'wealth' ? 'wealth stems' : 'influence stems')
   const fillerLabel = storageType === 'wealth' ? 'DW/IW' : 'DO/7K'
   tooltip += `\n○ Needs filler: ${fillerStems} (${fillerLabel}) in other pillars`
  }
 }
 
 // Summary tip
 if (isOpened && isFilled) {
  tooltip += `\n\n✨ Maximum ${storageType} storage power!`
 } else if (isOpened || isFilled) {
  tooltip += `\n\n💡 Partially activated - ${isOpened ? 'needs filler' : 'needs opener clash'}`
 } else {
  tooltip += `\n\n💡 Latent - needs both opener and filler to activate`
 }
 
 return tooltip
}

function getTransformationTooltip(transformation) {
 if (!transformation) return ''
 
 // Get full interaction data from chartData using interaction_id
 const fullInteraction = getFullInteractionData(transformation)

 const typeLabels = {
  THREE_MEETINGS: '三會 (Three Meetings)',
  THREE_COMBINATIONS: '三合 (Three Combinations)',
  HALF_MEETING: '半會 (Half Meeting)',
  SIX_HARMONIES: '六合 (Six Harmonies)',
  ARCHED_COMBINATIONS: '拱合 (Arched Combinations)',
  STEM_COMBINATION: '天干合 (Stem Combination)'
 }

 const strengthLabels = {
  ultra_strong: 'Ultra Strong - Seasonal Directional',
  strong: 'Strong - Triangular Combo',
  normal: 'Normal - Pair Combo',
  weak: 'Weak - Partial Combo'
 }
 
 let tooltip = `${typeLabels[transformation.type] || transformation.type}\n` +
     `Pattern: ${transformation.pattern || fullInteraction.pattern || 'N/A'}\n` +
     `→ ${transformation.element || fullInteraction.element || 'N/A'}\n` +
     `Strength: ${strengthLabels[transformation.strength] || transformation.strength}`
 
 // Add detailed debugging information from full interaction data
 if (fullInteraction) {
  tooltip += `\n\n━━━ Debug Info ━━━`
  
  // Interaction ID first
  if (transformation.interaction_id) {
   tooltip += `\nInteraction ID: ${transformation.interaction_id}`
  }
  
  if (fullInteraction.nodes && fullInteraction.nodes.length > 0) {
   tooltip += `\nNodes: ${fullInteraction.nodes.join(', ')}`
  }
  
  if (fullInteraction.distance !== undefined) {
   tooltip += `\nDistance: ${fullInteraction.distance}`
  }
  
  if (fullInteraction.transformed !== undefined) {
   tooltip += `\nTransformed: ${fullInteraction.transformed ? 'Yes' : 'No'}`
  }
  
  if (fullInteraction.branches && fullInteraction.branches.length > 0) {
   tooltip += `\nBranches: ${fullInteraction.branches.join(', ')}`
  }
  
  if (fullInteraction.stems && fullInteraction.stems.length > 0) {
   tooltip += `\nStems: ${fullInteraction.stems.join(', ')}`
  }
  
  // Show any additional fields that might exist
  const knownFields = ['type', 'pattern', 'nodes', 'positions', 'transformed', 'element', 'distance', 'branches', 'stems', 'stage', 'effect', 'description']
  Object.keys(fullInteraction).forEach(key => {
   if (!knownFields.includes(key) && fullInteraction[key] !== undefined && fullInteraction[key] !== null) {
    tooltip += `\n${key}: ${JSON.stringify(fullInteraction[key])}`
   }
  })
 }
 
 return tooltip
}

// NEW: Get highlight ring class based on interaction context
function getNodeHighlightClass(nodeId) {
 if (!highlightedNodes.value.includes(nodeId)) return ''
 
 const context = highlightContext.value
 if (!context) return 'ring-1 ring-blue-400' // Default subtle blue
 
 // Check if negative interaction (exact type match to avoid false positives)
 const isNegative = context.type && (
  context.type === 'CLASHES' ||
  context.type === 'HARMS' ||
  context.type === 'DESTRUCTION' ||
  context.type === 'DESTRUCTIONS' ||
  context.type === 'PUNISHMENTS' ||
  context.type === 'STEM_CONFLICT' ||
  context.type === 'clash' ||
  context.type === 'harm' ||
  context.type === 'destruction' ||
  context.type === 'punishment'
 )
 
 if (isNegative) {
  // White border for negative interactions
  return 'ring-1 ring-white'
 }
 
 // Element-based colors for positive interactions (transformations/combinations)
 const element = context.element || context.pattern?.split('-').pop() // Try to extract element
 
 // Get polarity - check if node is Yang or Yin based on node ID
 const isYangNode = nodeId.includes('stem') ? 
  isYangStem(nodeId) : isYangBranch(nodeId)
 
 // Element color mapping with polarity
 const elementColors = {
  'Fire': isYangNode ? 'ring-red-500' : 'ring-orange-400',
  'Water': isYangNode ? 'ring-blue-600' : 'ring-blue-300',
  'Wood': isYangNode ? 'ring-green-600' : 'ring-green-300',
  'Metal': isYangNode ? 'ring-gray-500' : 'ring-gray-300',
  'Earth': isYangNode ? 'ring-yellow-700' : 'ring-yellow-400'
 }
 
 const ringColor = elementColors[element] || 'ring-blue-400'
 return `ring-1 ${ringColor}`
}

// Helper: Check if stem is Yang
function isYangStem(nodeId) {
 const yangStems = ['Jia', 'Bing', 'Wu', 'Geng', 'Ren']
 // Extract stem name from pillar data
 const index = parseInt(nodeId.split('-')[1])
 if (isNaN(index) || !pillarsOrdered.value || index >= pillarsOrdered.value.length) return true
 const stemName = pillarsOrdered.value[index]?.stemName || ''
 return yangStems.includes(stemName)
}

// Helper: Check if branch is Yang
function isYangBranch(nodeId) {
 const yangBranches = ['Zi', 'Yin', 'Chen', 'Wu', 'Shen', 'Xu']
 // Extract branch name from pillar data
 const index = parseInt(nodeId.split('-')[1])
 if (isNaN(index) || !pillarsOrdered.value || index >= pillarsOrdered.value.length) return true
 const branchName = pillarsOrdered.value[index]?.branchName || ''
 return yangBranches.includes(branchName)
}

// Handle badge hover - highlight involved nodes and related badges
function handleBadgeHover(badge) {
 if (!badge || !badge.interaction_id) return
 
 // Set context for element-based coloring
 highlightContext.value = badge
 hoveredTransformationId.value = badge.interaction_id // Track which badge is hovered
 highlightedNodes.value = []
 
 // Extract node IDs from interaction_id using regex
 // Matches patterns like: hs_y, eb_m, hs_10yl, eb_yl, etc.
 const nodeIdPattern = /(hs|eb)_[a-z0-9]+/g
 const matches = badge.interaction_id.match(nodeIdPattern)
 
 if (!matches) return
 
 // Convert to display format and highlight
 matches.forEach(nodeId => {
  const nodeIndex = getNodeIndex(nodeId)
  if (nodeIndex !== -1) {
   const nodeType = nodeId.startsWith('hs') ? 'stem' : 'branch'
   highlightedNodes.value.push(`${nodeType}-${nodeIndex}`)
  }
 })
}

// Check if a badge should be highlighted (same transformation group)
function isBadgeHighlighted(transformation) {
 if (!transformation || !hoveredTransformationId.value) return false
 return transformation.interaction_id === hoveredTransformationId.value
}

function handleInteractionLeave() {
 hoveredInteraction.value = null
 highlightedNodes.value = []
 highlightContext.value = null // Clear context
 hoveredTransformationId.value = null // Clear transformation highlight
 tooltipContent.value = null
}

function getNodeInteractions(nodeKey) {
 if (!interactions.value) return []
 return interactions.value.filter(i => i.nodes && i.nodes.includes(nodeKey))
}

function getNonNaturalInteractions(nodeKey) {
 if (!interactions.value) return []
 return interactions.value.filter(i => {
  if (!i.nodes || !i.nodes.includes(nodeKey)) return false
  return !i.type.includes('NATURAL')
 })
}

// Removed unused functions: getPillarInteractions, getPillarInteractionData, getPillarInteractionText

function getEnergyFlowBetweenNodes(node1, node2, isHeavenlyStem = false) {
 if (!interactions.value || !node1 || !node2) return null
 
 // Look for ENERGY_FLOW interactions that involve these nodes
 for (const interaction of interactions.value) {
  if (!interaction.type?.includes('ENERGY_FLOW')) continue
  
  const desc = interaction.description || ''
  
  // Check if this interaction involves our nodes
  if (desc.includes(node1) && desc.includes(node2)) {
   if (interaction.type === 'ENERGY_FLOW_GENERATING') {
    // Check direction from description
    if (desc.includes(`${node1} exhausts`) || desc.includes(`${node1} uses`)) {
     return '→' // node1 generates for node2
    } else if (desc.includes(`${node2} exhausts`) || desc.includes(`${node2} uses`)) {
     return '←' // node2 generates for node1
    }
   } else if (interaction.type === 'ENERGY_FLOW_CONTROLLING') {
    // Check direction from description
    if (desc.includes(`${node1} uses energy`) && desc.includes(`control ${node2}`)) {
     return '⇢' // node1 controls node2
    } else if (desc.includes(`${node2} uses energy`) && desc.includes(`control ${node1}`)) {
     return '⇠' // node2 controls node1
    }
   }
  }
 }
 
 return null
}

function getWuXingRelation(element1, element2) {
 // Extract base element names (remove Yang/Yin)
 const elem1 = element1.split(' ').pop()
 const elem2 = element2.split(' ').pop()
 
 const cycle = ['Wood', 'Fire', 'Earth', 'Metal', 'Water']
 const idx1 = cycle.indexOf(elem1)
 const idx2 = cycle.indexOf(elem2)
 
 if (idx1 === -1 || idx2 === -1) return null
 
 // Check if elem1 generates elem2
 if ((idx1 + 1) % 5 === idx2) {
  return '→' // Generation arrow
 }
 
 // Check if elem1 controls elem2
 if ((idx1 + 2) % 5 === idx2) {
  return '⇢' // Control arrow pointing right
 }
 
 // Check if elem2 generates elem1
 if ((idx2 + 1) % 5 === idx1) {
  return '←' // Being generated (reverse arrow)
 }
 
 // Check if elem2 controls elem1
 if ((idx2 + 2) % 5 === idx1) {
  return '⇠' // Being controlled arrow pointing left
 }
 
 return null
}

function getWuXingRelationClass(element1, element2) {
 const relation = getWuXingRelation(element1, element2)
 
 switch(relation) {
  case '→': // Generation forward
  case '←': // Generation backward
   return 'text-green-600'
  case '⇢': // Control right
  case '⇠': // Control left
   return 'text-red-600'
  default:
   return 'text-gray-600'
 }
}

// Qi Phase (十二長生) styling based on strength category
function getQiPhaseClass(strength) {
 const classes = {
  'peak': 'bg-green-100 text-green-800 border border-green-300',      // 帝旺 - Emperor
  'strong': 'bg-lime-100 text-lime-800 border border-lime-300',       // 長生/臨官 - Birth/Official
  'growing': 'bg-emerald-50 text-emerald-700 border border-emerald-200', // 冠帶 - Capping
  'declining': 'bg-amber-100 text-amber-800 border border-amber-300', // 衰 - Decline
  'weak': 'bg-orange-100 text-orange-800 border border-orange-300',   // 沐浴/病 - Bathing/Sickness
  'dead': 'bg-red-100 text-red-800 border border-red-300',           // 死/絕 - Death/Extinction
  'stored': 'bg-purple-100 text-purple-800 border border-purple-300', // 墓 - Tomb
  'nascent': 'bg-cyan-100 text-cyan-800 border border-cyan-300'       // 胎/養 - Embryo/Nurturing
 }
 return classes[strength] || 'bg-gray-100 text-gray-700 border border-gray-200'
}


function getVerticalWuXingRelation(stemElement, branchElement) {
 // Extract base element names (remove Yang/Yin)
 const stem = stemElement.split(' ').pop()
 const branch = branchElement.split(' ').pop()
 
 const cycle = ['Wood', 'Fire', 'Earth', 'Metal', 'Water']
 const stemIdx = cycle.indexOf(stem)
 const branchIdx = cycle.indexOf(branch)
 
 if (stemIdx === -1 || branchIdx === -1) return null
 
 // Check if stem generates branch (energy flows down)
 if ((stemIdx + 1) % 5 === branchIdx) {
  return '↓' // Down arrow - stem generating branch
 }
 
 // Check if stem controls branch (energy suppresses down)
 if ((stemIdx + 2) % 5 === branchIdx) {
  return '⇣' // Control arrow pointing down
 }
 
 // Check if branch generates stem (energy flows up)
 if ((branchIdx + 1) % 5 === stemIdx) {
  return '↑' // Up arrow - branch generating stem
 }
 
 // Check if branch controls stem (energy suppresses up)
 if ((branchIdx + 2) % 5 === stemIdx) {
  return '⇡' // Control arrow pointing up
 }
 
 return null
}

function getVerticalWuXingClass(stemElement, branchElement) {
 const relation = getVerticalWuXingRelation(stemElement, branchElement)
 
 switch(relation) {
  case '↓': // Stem generating branch (down)
  case '↑': // Branch generating stem (up)
   return 'text-green-600'
  case '⇣': // Control down
  case '⇡': // Control up
   return 'text-red-600'
  default:
   return 'text-gray-600'
 }
}

function getNodeIndex(nodeKey) {
 // Map to display order: Hour, Day, Month, Year, 10Y Luck, Annual, Monthly, Daily, Hourly (left to right)
 const pillarMap = { 'h': 0, 'd': 1, 'm': 2, 'y': 3, '10yl': 4, 'yl': 5, 'ml': 6, 'dl': 7, 'hl': 8 }
 
 // Extract pillar type from node ID (e.g., "hs_h" -> "h", "eb_10yl" -> "10yl", "hs_yl" -> "yl", "hs_ml" -> "ml")
 const parts = nodeKey.split('_')
 const pillarType = parts.length > 2 ? parts.slice(1).join('_') : parts[1]
 
 return pillarMap[pillarType] ?? -1
}

function formatShortInteraction(interaction) {
 const typeMap = {
  'THREE_MEETINGS': '三會',
  'PUNISHMENTS': '刑',
  'THREE_COMBINATIONS': '三合',
  'SIX_HARMONIES': '六合',
  'ARCHED_COMBINATIONS': '拱合',
  'CLASHES': '沖',
  'HARMS': '害',
  'DESTRUCTIONS': '破',
  'HS_CONFLICT': '天干沖',
  'HS_COMBINATION': '天干合',
  'NATURAL_GENERATING': '生',
  'NATURAL_CONTROLLING': '剋'
 }
 return typeMap[interaction.type] || interaction.type
}

// Interaction highlighting functions
function highlightInteraction(interaction) {
 highlightedInteraction.value = interaction
 highlightedNodes.value = []
 highlightContext.value = interaction // Set context for element-based coloring
 
 // Highlight nodes in the chart based on interaction
 if (interaction.type === 'HS_CONFLICT') {
  // For HS_CONFLICT, add both conflictor and conflicted nodes
  if (interaction.conflictor?.node) {
   const nodeIndex = getNodeIndex(interaction.conflictor.node)
   if (nodeIndex !== -1) {
    highlightedNodes.value.push(`stem-${nodeIndex}`)
   }
  }
  if (interaction.conflicted?.node) {
   const nodeIndex = getNodeIndex(interaction.conflicted.node)
   if (nodeIndex !== -1) {
    highlightedNodes.value.push(`stem-${nodeIndex}`)
   }
  }
 } else if (interaction.nodes) {
  // For other interactions, use the nodes array
  interaction.nodes.forEach(node => {
   const nodeIndex = getNodeIndex(node)
   if (nodeIndex !== -1) {
    const nodeType = node.startsWith('hs') ? 'stem' : 'branch'
    highlightedNodes.value.push(`${nodeType}-${nodeIndex}`)
   }
  })
 }
}

function clearHighlight() {
 highlightedInteraction.value = null
 highlightedNodes.value = []
 highlightContext.value = null // Clear context
 hoveredTransformationId.value = null // Clear transformation highlight
}



function isInteractionHighlighted(interaction) {
 // Check if this interaction is highlighted
 const current = highlightedInteraction.value
 if (!current) return false
 
 // Direct reference match
 if (current === interaction) return true
 
 // Special handling for HS_CONFLICT - match if same stems are involved
 if (current.type === 'HS_CONFLICT' && interaction.type === 'HS_CONFLICT') {
  // Get the stems involved in both interactions
  const currentStems = []
  if (current.conflictor?.node) currentStems.push(current.conflictor.node)
  if (current.conflicted?.node) currentStems.push(current.conflicted.node)
  
  const interactionStems = []
  if (interaction.conflictor?.node) interactionStems.push(interaction.conflictor.node)
  if (interaction.conflicted?.node) interactionStems.push(interaction.conflicted.node)
  
  // Check if they involve the same stems (regardless of order)
  const currentSorted = currentStems.sort().join(',')
  const interactionSorted = interactionStems.sort().join(',')
  return currentSorted === interactionSorted
 }
 
 // Check if they have the same nodes (for highlighting related boxes)
 if (current.nodes && interaction.nodes) {
  const currentNodes = current.nodes.sort().join(',')
  const interactionNodes = interaction.nodes.sort().join(',')
  return currentNodes === interactionNodes
 }
 
 return false
}
</script>

<style scoped>
/* Eliminate all transitions - instant updates */
* {
  transition: none !important;
  animation: none !important;
}

/* Force GPU acceleration for smooth rendering */
.w-28, .relative {
  will-change: contents;
  transform: translateZ(0);
  backface-visibility: hidden;
}

/* Prevent layout thrashing */
.relative {
  contain: layout paint style;
}
</style>