/**
 * Google Analytics Integration
 * =============================
 *
 * Tracks user interactions and page views in Google Analytics 4.
 */

export const GA_TRACKING_ID = process.env.REACT_APP_GA_ID || '';

// Initialize Google Analytics
export const initGA = () => {
  if (typeof window === 'undefined' || !GA_TRACKING_ID) {
    return;
  }

  // Load gtag.js
  const script = document.createElement('script');
  script.async = true;
  script.src = `https://www.googletagmanager.com/gtag/js?id=${GA_TRACKING_ID}`;
  document.head.appendChild(script);

  // Initialize dataLayer
  window.dataLayer = window.dataLayer || [];
  window.gtag = function gtag() {
    window.dataLayer.push(arguments);
  };
  window.gtag('js', new Date());
  window.gtag('config', GA_TRACKING_ID, {
    page_path: window.location.pathname,
  });
};

// Track page views
export const pageView = (url) => {
  if (typeof window !== 'undefined' && window.gtag) {
    window.gtag('config', GA_TRACKING_ID, {
      page_path: url,
    });
  }
};

// Track custom events
export const event = ({ action, category, label, value }) => {
  if (typeof window !== 'undefined' && window.gtag) {
    window.gtag('event', action, {
      event_category: category,
      event_label: label,
      value: value,
    });
  }
};

// Track user signup
export const trackSignup = (source) => {
  event({
    action: 'sign_up',
    category: 'engagement',
    label: source,
  });
};

// Track user login
export const trackLogin = (method) => {
  event({
    action: 'login',
    category: 'engagement',
    label: method,
  });
};

// Track product scan
export const trackProductScan = (success) => {
  event({
    action: 'scan_product',
    category: 'features',
    label: success ? 'success' : 'failure',
  });
};

// Track AI chat
export const trackAIChat = (messageCount) => {
  event({
    action: 'ai_chat_message',
    category: 'features',
    value: messageCount,
  });
};

// Track meal plan creation
export const trackMealPlanCreated = () => {
  event({
    action: 'meal_plan_created',
    category: 'features',
  });
};

// Track food search
export const trackFoodSearch = (query) => {
  event({
    action: 'food_search',
    category: 'search',
    label: query,
  });
};

// Track PDF export
export const trackPDFExport = (type) => {
  event({
    action: 'pdf_export',
    category: 'export',
    label: type,
  });
};

// Track user journey
export const trackUserJourney = (step) => {
  event({
    action: 'user_journey',
    category: 'onboarding',
    label: step,
  });
};

// Track feature usage
export const trackFeatureUsage = (featureName) => {
  event({
    action: 'feature_usage',
    category: 'engagement',
    label: featureName,
  });
};

// Set user properties
export const setUserProperties = (properties) => {
  if (typeof window !== 'undefined' && window.gtag) {
    window.gtag('set', 'user_properties', properties);
  }
};

// Track conversions
export const trackConversion = (conversionType) => {
  event({
    action: 'conversion',
    category: 'conversion',
    label: conversionType,
  });
};
