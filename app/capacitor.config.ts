import type { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
  appId: 'com.bazingse.app',
  appName: 'BaZingSe',
  webDir: 'dist',
  server: {
    // For development, you can enable this to load from dev server
    // url: 'http://localhost:3000',
    // cleartext: true,

    // For production, the app loads from the bundled dist folder
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
