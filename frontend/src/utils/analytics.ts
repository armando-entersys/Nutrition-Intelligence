/**
 * Google Analytics Integration
 * =============================
 *
 * Tracks user interactions and page views in Google Analytics 4.
 */

declare global {
  interface Window {
    gtag?: (...args: any[]) => void;
    dataLayer?: any[];
  }
}

export const GA_TRACKING_ID = process.env.NEXT_PUBLIC_GA_ID || '';

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
    window.dataLayer?.push(arguments);
  };
  window.gtag('js', new Date());
  window.gtag('config', GA_TRACKING_ID, {
    page_path: window.location.pathname,
    send_page_view: true,
  });

  console.log('Google Analytics initialized:', GA_TRACKING_ID);
};

// Track page views
export const pageview = (url: string) => {
  if (typeof window === 'undefined' || !window.gtag || !GA_TRACKING_ID) {
    return;
  }

  window.gtag('config', GA_TRACKING_ID, {
    page_path: url,
  });
};

// Track events
interface EventParams {
  action: string;
  category: string;
  label?: string;
  value?: number;
  [key: string]: any;
}

export const event = ({ action, category, label, value, ...params }: EventParams) => {
  if (typeof window === 'undefined' || !window.gtag || !GA_TRACKING_ID) {
    return;
  }

  window.gtag('event', action, {
    event_category: category,
    event_label: label,
    value: value,
    ...params,
  });
};

// Pre-defined event trackers
export const trackSignup = (method: string = 'email') => {
  event({
    action: 'sign_up',
    category: 'engagement',
    label: method,
  });
};

export const trackLogin = (method: string = 'email') => {
  event({
    action: 'login',
    category: 'engagement',
    label: method,
  });
};

export const trackLogout = () => {
  event({
    action: 'logout',
    category: 'engagement',
  });
};

export const trackSearch = (searchTerm: string, category: 'foods' | 'recipes' | 'products') => {
  event({
    action: 'search',
    category: 'engagement',
    label: category,
    search_term: searchTerm,
  });
};

export const trackProductScan = (success: boolean) => {
  event({
    action: 'scan_product',
    category: 'features',
    label: success ? 'success' : 'failure',
  });
};

export const trackAIChat = (messageCount: number) => {
  event({
    action: 'ai_chat_message',
    category: 'features',
    value: messageCount,
  });
};

export const trackMealPlanCreate = (daysCount: number) => {
  event({
    action: 'create_meal_plan',
    category: 'features',
    value: daysCount,
  });
};

export const trackRecipeView = (recipeId: string, recipeName: string) => {
  event({
    action: 'view_recipe',
    category: 'content',
    label: recipeName,
    recipe_id: recipeId,
  });
};

export const trackError = (error: Error, errorInfo?: any) => {
  event({
    action: 'exception',
    category: 'error',
    label: error.message,
    fatal: false,
    error_name: error.name,
    error_stack: error.stack?.substring(0, 150), // Limit stack trace
  });
};

// Track user properties
export const setUserProperties = (userId: string, role: string, properties?: Record<string, any>) => {
  if (typeof window === 'undefined' || !window.gtag || !GA_TRACKING_ID) {
    return;
  }

  window.gtag('set', 'user_properties', {
    user_id: userId,
    user_role: role,
    ...properties,
  });
};

// Track custom dimensions
export const setCustomDimensions = (dimensions: Record<string, any>) => {
  if (typeof window === 'undefined' || !window.gtag || !GA_TRACKING_ID) {
    return;
  }

  window.gtag('set', dimensions);
};

// E-commerce tracking (if needed for premium features)
export const trackPurchase = (transactionId: string, value: number, items: any[]) => {
  if (typeof window === 'undefined' || !window.gtag || !GA_TRACKING_ID) {
    return;
  }

  window.gtag('event', 'purchase', {
    transaction_id: transactionId,
    value: value,
    currency: 'MXN',
    items: items,
  });
};

export default {
  initGA,
  pageview,
  event,
  trackSignup,
  trackLogin,
  trackLogout,
  trackSearch,
  trackProductScan,
  trackAIChat,
  trackMealPlanCreate,
  trackRecipeView,
  trackError,
  setUserProperties,
  setCustomDimensions,
  trackPurchase,
};
