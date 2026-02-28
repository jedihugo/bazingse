import type { CapacitorConfig } from '@capacitor/cli';

// Set to true for development (live reload from dev server)
// Set to false for production build (uses bundled files)
const USE_DEV_SERVER = true;

const config: CapacitorConfig = {
  appId: 'com.bazingse.app',
  appName: 'BaZingSe',
  webDir: 'build',
  server: USE_DEV_SERVER ? {
    // Development: Load from SvelteKit dev server for live reload
    url: 'http://localhost:5173',
    cleartext: true,
  } : {
    // Production: Load from bundled files
    androidScheme: 'https'
  },
  plugins: {
    SplashScreen: {
      launchShowDuration: 2000,
      backgroundColor: '#ffffff',
      showSpinner: false
    },
    StatusBar: {
      style: 'dark',
      backgroundColor: '#ffffff'
    }
  },
  ios: {
    contentInset: 'automatic'
  },
  android: {
    allowMixedContent: false
  }
};

export default config;
