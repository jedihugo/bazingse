# BaZingSe - Chinese BaZi Astrology SPA

Full-stack Chinese BaZi (Four Pillars/八字) astrology application.

## Tech Stack

**Frontend:** Vue 3 + Vite (Pure SPA)
**Backend:** Python FastAPI + sxtwl calendar library
**Styling:** Custom CSS (converted from Tailwind)

## Quick Start

### Prerequisites
- Node.js 18+ (for frontend)
- Python 3.13+ (for backend)
- Backend running on `http://localhost:8008`

### Frontend Development
```bash
# Install dependencies
npm install

# Start dev server (runs on http://localhost:3000)
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

### Backend Development
```bash
# Navigate to backend directory
cd api

# Activate virtual environment
source .venv/bin/activate

# Run backend server
python run_bazingse.py
# Backend runs on http://localhost:8008
```

## Project Structure

```
bazingse-app/
├── api/                # Backend (Python FastAPI)
│   ├── run_bazingse.py # Backend entry point
│   ├── requirements.txt
│   └── ...
├── index.html          # Entry point
├── vite.config.js      # Vite configuration + API proxy
├── package.json        # Dependencies
├── src/
│   ├── main.js         # Vue app initialization
│   ├── App.vue         # Main component (4743 lines)
│   ├── styles.css      # Custom CSS (~600 lines)
│   ├── utils/          # Helper functions
│   └── types/          # TypeScript type definitions
├── public/
│   └── bazingse-logo.png
└── AGENTS.md           # Development guidelines
```

## Features

### Core Functionality
- ✅ Natal chart calculation (4 pillars: Year, Month, Day, Hour)
- ✅ Time Travel mode (analyze different time periods)
- ✅ 10-Year Luck pillars (大运)
- ✅ Annual Luck (年運)
- ✅ Monthly Luck (月運)
- ✅ Daily Luck (日運)
- ✅ Hourly Luck (時運)
- ✅ Talisman system (manual pillar override)
- ✅ Location feature (overseas/birthplace)

### UI Features
- ✅ Quick test presets (9 pre-configured charts)
- ✅ View mode toggle (Base vs Post-interaction)
- ✅ Wu Xing element graphs (before/after comparison)
- ✅ Interactive badges with detailed tooltips
- ✅ Smooth CSS transitions (no stuttering)
- ✅ localStorage persistence
- ✅ Responsive design
- ✅ Mobile-optimized

### Backend Integration
- ✅ Real-time calculation via FastAPI
- ✅ 18-node interaction system
- ✅ Element scoring (pre and post-interaction)
- ✅ Daymaster analysis
- ✅ Pattern detection (harmonies, clashes, transformations)

## Architecture

### Frontend (Vue 3 SPA)
- **Pure Client-Side:** No SSR, no server components
- **Explicit Imports:** No auto-imports, everything is clear
- **Custom CSS:** No preprocessor, flat structure
- **Vite Proxy:** `/api/*` → `http://localhost:8008/*`

### Backend (Python FastAPI)
- **Calculation Engine:** All BaZi logic in Python
- **Single Endpoint:** `/analyze_bazi` with parameters
- **JSON API:** Returns complete chart data
- **No Frontend Logic:** Frontend only displays data

## Development Guidelines

See [AGENTS.md](./AGENTS.md) for detailed guidelines including:
- Backend-driven architecture principles
- 18-node system architecture
- Temporal overlay metaphysics
- UI/UX design patterns
- Coding conventions
- Testing procedures

## API Endpoint

### Main Endpoint: `/analyze_bazi`

**Parameters:**
- `birth_date` (required): YYYY-MM-DD
- `birth_time` (optional): HH:MM or "unknown"
- `gender` (required): "male" or "female"
- `analysis_year` (optional): Year for 10-year + annual luck
- `include_annual_luck` (optional): boolean, default true
- `analysis_month` (optional): 1-12 for monthly luck
- `analysis_day` (optional): 1-31 for daily luck
- `analysis_time` (optional): HH:MM for hourly luck

**Example:**
```bash
curl "http://localhost:8008/analyze_bazi?birth_date=1992-07-06&birth_time=09:30&gender=female&analysis_year=2025"
```

## Key Files

### Configuration
- `vite.config.js` - Vite + Vue setup, API proxy
- `index.html` - HTML entry point
- `src/main.js` - Vue app initialization

### Components
- `src/App.vue` - Main application component
- `src/styles.css` - All styling (custom CSS)

### Utilities
- `src/utils/baziHelpers.ts` - Helper functions
- `src/types/bazi.ts` - TypeScript interfaces

### Documentation
- `AGENTS.md` - Development guidelines
- `CONVERSION_TO_VUE3_SPA.md` - Migration notes
- `BADGE_TOOLTIP_ENHANCEMENT.md` - Tooltip feature docs

## Performance

### Build Size
- **Bundle Size:** ~800KB (minified)
- **Dependencies:** 30 packages
- **node_modules:** ~40MB

### Dev Server
- **Startup Time:** <200ms
- **HMR:** Instant (<50ms)
- **Build Time:** ~5 seconds

## Browser Support

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Mobile browsers (iOS Safari, Chrome Android)

## Troubleshooting

### Frontend won't start
```bash
# Clean install
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### API calls fail
1. Check backend is running: `curl http://localhost:8008/`
2. Check Vite proxy in `vite.config.js`
3. Check browser console for CORS errors

### Styling looks broken
1. Verify `src/styles.css` is loaded
2. Check browser console for CSS errors
3. Clear browser cache

### State not persisting
1. Check localStorage in browser DevTools
2. Verify key `bazingse_form_data` exists
3. Check for localStorage quota errors

## License

Private project - All rights reserved

## Contact

For questions or issues, see [AGENTS.md](./AGENTS.md) for development guidelines.

---

**Version:** 2.0 (Vue 3 SPA)
**Last Updated:** November 9, 2025
