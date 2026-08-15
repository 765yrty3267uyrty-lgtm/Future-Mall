/**
 * Future Mall - Shared Brand Constants (JavaScript)
 * Used by all web modules for consistent branding.
 * Can be imported as ES module or used globally.
 */

const BRAND = {
  name: "Future Mall",
  slogan: "Shopping for Tomorrow",

  colors: {
    // Primary - Future Blue
    primary: "#2563EB",
    primaryHover: "#1D4ED8",
    primaryLight: "#DBEAFE",
    primaryText: "#FFFFFF",

    // Secondary - Innovation Teal
    secondary: "#0D9488",
    secondaryHover: "#0F766E",
    secondaryLight: "#CCFBF1",

    // Accent - Energy Orange
    accent: "#F97316",
    accentHover: "#EA580C",
    accentLight: "#FFEDD5",

    // Semantic
    success: "#10B981",
    warning: "#F59E0B",
    danger: "#EF4444",
    info: "#3B82F6",

    // Neutral
    bg: "#F8FAFC",
    surface: "#FFFFFF",
    text: "#1E293B",
    textMuted: "#64748B",
    border: "#E2E8F0",
    borderLight: "#F1F5F9",
  },

  fonts: {
    display: "Space Grotesk",
    heading: "Space Grotesk",
    body: "Inter",
    mono: "JetBrains Mono",
  },

  spacing: {
    xs: "4px",
    sm: "8px",
    md: "16px",
    lg: "24px",
    xl: "32px",
  },

  radius: {
    sm: "4px",
    md: "8px",
    lg: "12px",
    xl: "16px",
    full: "9999px",
  },

  shadows: {
    sm: "0 1px 2px rgba(15, 23, 42, 0.05)",
    md: "0 4px 6px rgba(15, 23, 42, 0.07)",
    lg: "0 10px 15px rgba(15, 23, 42, 0.1)",
    xl: "0 20px 25px rgba(15, 23, 42, 0.15)",
  },

  transitions: {
    fast: "150ms ease",
    normal: "250ms ease",
    slow: "350ms ease",
  },
};

const ATTENDANCE = {
  workStart: "08:00",
  workEnd: "17:00",
  lateThreshold: "08:15",
  standardHours: 8.0,
  maxOvertime: 2.0,
  roles: ["employee", "supervisor", "admin"],
  statuses: ["present", "late", "absent", "on_leave", "holiday"],
  departments: ["IT", "HR", "Finance", "Operations", "Marketing", "Customer Service"],
};

const CASHIER = {
  storeName: "Future Mall",
  taxRate: 0.10,
  discountTiers: [
    { threshold: 200, percentage: 0.05 },
    { threshold: 500, percentage: 0.10 },
    { threshold: 1000, percentage: 0.15 },
  ],
  products: [
    { name: "Milk", price: 25.00 },
    { name: "Bread", price: 15.00 },
    { name: "Rice", price: 80.00 },
    { name: "Eggs", price: 45.00 },
    { name: "Sugar", price: 30.00 },
    { name: "Tea", price: 60.00 },
    { name: "Coffee", price: 120.00 },
    { name: "Juice", price: 35.00 },
    { name: "Water", price: 10.00 },
    { name: "Chocolate", price: 50.00 },
  ],
};

const VISITORS = {
  daysOfWeek: ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
  minDays: 1,
};

const CLASSIFIER = {
  priceTiers: {
    Premium: { min: 1000, max: Infinity },
    Standard: { min: 300, max: 1000 },
    Budget: { min: 0, max: 300 },
  },
  weightTiers: {
    Light: { min: 0, max: 1 },
    Medium: { min: 1, max: 10 },
    Heavy: { min: 10, max: Infinity },
  },
  stockTiers: {
    "In Stock": { min: 11, max: Infinity },
    "Low Stock": { min: 1, max: 10 },
    "Out of Stock": { min: 0, max: 0 },
  },
};

const DIGITAL_AWARENESS = {
  threats: [
    "Phishing",
    "Malware",
    "Viruses",
    "Ransomware",
    "Spyware",
    "Identity Theft",
    "Data Breaches",
    "Social Engineering",
  ],
  passwordRules: [
    "At least 12 characters",
    "Uppercase letters",
    "Lowercase letters",
    "Numbers",
    "Special symbols",
    "Avoid personal information",
    "Never reuse passwords",
    "Use a password manager",
    "Enable Multi-Factor Authentication (MFA)",
  ],
  safeBrowsingTips: [
    "Verify website URLs",
    "Look for HTTPS",
    "Avoid suspicious downloads",
    "Don't click unknown links",
    "Keep software updated",
    "Use antivirus software",
    "Log out from shared devices",
  ],
};

// Utility Functions
function formatCurrency(amount, symbol = "$") {
  return `${symbol}${amount.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
}

function formatNumber(num) {
  return num.toLocaleString();
}

function getColor(name) {
  return BRAND.colors[name] || "#000000";
}

function applyBrandTheme(root = document.documentElement) {
  Object.entries(BRAND.colors).forEach(([key, value]) => {
    root.style.setProperty(`--color-${kebabCase(key)}`, value);
  });

  function kebabCase(str) {
    return str.replace(/([a-z])([A-Z])/g, "$1-$2").toLowerCase();
  }
}

function createBrandElement(tag, className, content) {
  const el = document.createElement(tag);
  if (className) el.className = className;
  if (content) el.textContent = content;
  return el;
}

// Logo SVG (inline for easy embedding)
const LOGO_SVG = `
<svg width="40" height="40" viewBox="0 0 80 50" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
  <rect x="8" y="10" width="64" height="35" stroke="currentColor" stroke-width="1.5" rx="2"/>
  <rect x="35" y="28" width="10" height="17" stroke="currentColor" stroke-width="1.5"/>
  <line x1="40" y1="28" x2="40" y2="45" stroke="currentColor" stroke-width="1" stroke-dasharray="2 2"/>
  <rect x="14" y="16" width="8" height="8" stroke="currentColor" stroke-width="1"/>
  <rect x="14" y="27" width="8" height="8" stroke="currentColor" stroke-width="1"/>
  <rect x="25" y="16" width="8" height="8" stroke="currentColor" stroke-width="1"/>
  <rect x="25" y="27" width="8" height="8" stroke="currentColor" stroke-width="1"/>
  <rect x="47" y="16" width="8" height="8" stroke="currentColor" stroke-width="1"/>
  <rect x="47" y="27" width="8" height="8" stroke="currentColor" stroke-width="1"/>
  <rect x="58" y="16" width="8" height="8" stroke="currentColor" stroke-width="1"/>
  <rect x="58" y="27" width="8" height="8" stroke="currentColor" stroke-width="1"/>
  <line x1="5" y1="10" x2="75" y2="10" stroke="currentColor" stroke-width="1.5"/>
  <line x1="40" y1="5" x2="40" y2="10" stroke="currentColor" stroke-width="1"/>
  <polygon points="40,5 50,8 40,11" fill="currentColor"/>
</svg>
`;

// Export for different module systems
if (typeof module !== "undefined" && module.exports) {
  // CommonJS
  module.exports = {
    BRAND,
    ATTENDANCE,
    CASHIER,
    VISITORS,
    CLASSIFIER,
    DIGITAL_AWARENESS,
    formatCurrency,
    formatNumber,
    getColor,
    applyBrandTheme,
    createBrandElement,
    LOGO_SVG,
  };
} else if (typeof define === "function" && define.amd) {
  // AMD
  define([], function() {
    return {
      BRAND,
      ATTENDANCE,
      CASHIER,
      VISITORS,
      CLASSIFIER,
      DIGITAL_AWARENESS,
      formatCurrency,
      formatNumber,
      getColor,
      applyBrandTheme,
      createBrandElement,
      LOGO_SVG,
    };
  });
} else {
  // Global
  window.FutureMall = window.FutureMall || {};
  Object.assign(window.FutureMall, {
    BRAND,
    ATTENDANCE,
    CASHIER,
    VISITORS,
    CLASSIFIER,
    DIGITAL_AWARENESS,
    formatCurrency,
    formatNumber,
    getColor,
    applyBrandTheme,
    createBrandElement,
    LOGO_SVG,
  });
}