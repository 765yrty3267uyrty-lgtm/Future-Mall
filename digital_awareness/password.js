/**
 * Future Mall - Password Strength Checker
 * Real-time password analysis with entropy calculation and improvement suggestions.
 */

// Character sets
const CHAR_SETS = {
  lowercase: 'abcdefghijklmnopqrstuvwxyz',
  uppercase: 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
  numbers: '0123456789',
  symbols: '!@#$%^&*()_+-=[]{}|;:,.<>?',
  common_symbols: '!@#$%^&*'
};

// Common patterns to detect
const COMMON_PATTERNS = [
  /^(?:password|admin|welcome|login|qwerty|asdf|zxcv)/i,
  /^(?:123|abc|111|000|abc123|123abc)/i,
  /(.)\1{2,}/,  // Repeated characters (aaa, 111)
  /(?:0123|1234|2345|3456|4567|5678|6789|7890|9876|8765|7654|6543|5432|4321|3210)/, // Sequential
  /(?:qwer|wert|erty|rtyu|tyui|yuio|uiop|asdf|sdfg|dfgh|fghj|ghjk|hjkl|zxcv|xcvb|cvbn|bnmm)/i // Keyboard patterns
];

// Common passwords (top 100 most common - simplified)
const COMMON_PASSWORDS = new Set([
  'password', '123456', '123456789', '12345678', '12345', '1234567',
  'password123', 'admin', 'qwerty', 'qwertyuiop', 'letmein', 'welcome',
  'monkey', 'dragon', 'master', 'hello', 'login', 'passw0rd', 'abc123',
  'football', 'iloveyou', 'starwars', 'trustno1', 'sunshine', 'princess',
  'superman', 'batman', 'whatever', 'shadow', 'michael', 'charlie'
]);

/**
 * Calculate password entropy in bits
 */
function calculateEntropy(password) {
  if (!password) return 0;

  let poolSize = 0;
  const hasLower = /[a-z]/.test(password);
  const hasUpper = /[A-Z]/.test(password);
  const hasNumber = /[0-9]/.test(password);
  const hasSymbol = /[^a-zA-Z0-9]/.test(password);

  if (hasLower) poolSize += 26;
  if (hasUpper) poolSize += 26;
  if (hasNumber) poolSize += 10;
  if (hasSymbol) poolSize += 32; // Common symbols

  // If no character types detected, assume minimal pool
  if (poolSize === 0) poolSize = 10;

  // Entropy = log2(poolSize^length) = length * log2(poolSize)
  return password.length * Math.log2(poolSize);
}

/**
 * Estimate crack time based on entropy
 */
function estimateCrackTime(entropy) {
  // Online attack: 1000 guesses/second (rate limited)
  // Offline attack: 100 billion guesses/second (modern GPU)
  const onlineGuessesPerSec = 1000;
  const offlineGuessesPerSec = 1e11;

  const combinations = Math.pow(2, entropy);
  const onlineTime = combinations / (2 * onlineGuessesPerSec); // Average case
  const offlineTime = combinations / (2 * offlineGuessesPerSec);

  return { online: onlineTime, offline: offlineTime };
}

/**
 * Format time in human readable format
 */
function formatTime(seconds) {
  if (seconds < 1) return 'Instant';
  if (seconds < 60) return `${Math.round(seconds)} seconds`;
  if (seconds < 3600) return `${Math.round(seconds / 60)} minutes`;
  if (seconds < 86400) return `${Math.round(seconds / 3600)} hours`;
  if (seconds < 31536000) return `${Math.round(seconds / 86400)} days`;
  if (seconds < 315360000) return `${Math.round(seconds / 31536000)} years`;
  return 'Centuries';
}

/**
 * Check requirements
 */
function checkRequirements(password) {
  const results = {
    length: password.length >= 12,
    uppercase: /[A-Z]/.test(password),
    lowercase: /[a-z]/.test(password),
    number: /[0-9]/.test(password),
    symbol: /[^a-zA-Z0-9]/.test(password),
    noCommon: !hasCommonPattern(password),
    noPersonal: !hasPersonalInfo(password) // Simplified
  };
  return results;
}

/**
 * Check for common patterns
 */
function hasCommonPattern(password) {
  const lower = password.toLowerCase();

  // Check common passwords
  if (COMMON_PASSWORDS.has(lower)) return true;

  // Check patterns
  for (const pattern of COMMON_PATTERNS) {
    if (pattern.test(password)) return true;
  }

  // Check for keyboard walks (simplified)
  const keyboardRows = [
    'qwertyuiop',
    'asdfghjkl',
    'zxcvbnm',
    '1234567890'
  ];

  for (const row of keyboardRows) {
    for (let i = 0; i <= row.length - 4; i++) {
      const seq = row.slice(i, i + 4);
      if (lower.includes(seq) || lower.includes(seq.split('').reverse().join(''))) {
        return true;
      }
    }
  }

  return false;
}

/**
 * Check for personal info (simplified - would need user data in real app)
 */
function hasPersonalInfo(password) {
  // In a real app, this would check against user's name, email, birthdate, etc.
  // For demo, we'll check for common personal patterns
  const personalPatterns = [
    /\b\d{4}\b/, // Years like 1990, 2000
    /\b\d{2}\/\d{2}\/\d{4}\b/, // Dates
    /\b\d{2}-\d{2}-\d{4}\b/
  ];

  for (const pattern of personalPatterns) {
    if (pattern.test(password)) return true;
  }

  return false;
}

/**
 * Get suggestions for improvement
 */
function getSuggestions(password, requirements) {
  const suggestions = [];

  if (!requirements.length) {
    suggestions.push('Increase password length to at least 12 characters (16+ recommended)');
  }
  if (!requirements.uppercase) {
    suggestions.push('Add uppercase letters (A-Z)');
  }
  if (!requirements.lowercase) {
    suggestions.push('Add lowercase letters (a-z)');
  }
  if (!requirements.number) {
    suggestions.push('Add numbers (0-9)');
  }
  if (!requirements.symbol) {
    suggestions.push('Add special symbols (!@#$%^&*)');
  }
  if (!requirements.noCommon) {
    suggestions.push('Avoid common patterns, sequences, and dictionary words');
  }
  if (!requirements.noPersonal) {
    suggestions.push('Avoid personal information (names, birthdays, years)');
  }

  // Additional suggestions based on password analysis
  if (password.length > 0 && password.length < 16) {
    suggestions.push('Consider 16+ characters for high-value accounts');
  }

  if (/^[a-z]+$/i.test(password)) {
    suggestions.push('Mix character types for stronger protection');
  }

  if (/(.)\1{2,}/.test(password)) {
    suggestions.push('Avoid repeating characters (aaa, 111)');
  }

  // Remove duplicates
  return [...new Set(suggestions)];
}

/**
 * Get security warnings
 */
function getWarnings(password) {
  const warnings = [];

  if (COMMON_PASSWORDS.has(password.toLowerCase())) {
    warnings.push('This password is in the top 100 most common passwords - extremely vulnerable');
  }

  if (/(.)\1{2,}/.test(password)) {
    warnings.push('Contains repeated characters (e.g., aaa, 111)');
  }

  if (/\b\d{4}\b/.test(password)) {
    warnings.push('Contains what appears to be a year (e.g., birth year)');
  }

  if (/(?:1234|abcd|qwerty|asdf)/i.test(password)) {
    warnings.push('Contains sequential keyboard/alphabet patterns');
  }

  if (password.length < 8) {
    warnings.push('Extremely short - vulnerable to instant brute force');
  }

  if (!/[^a-zA-Z0-9]/.test(password) && password.length > 0) {
    warnings.push('No special symbols - only letters and numbers');
  }

  return warnings;
}

/**
 * Determine strength label
 */
function getStrengthLabel(entropy) {
  if (entropy < 28) return { label: 'Very Weak', class: 'very-weak', color: '#ef4444' };
  if (entropy < 36) return { label: 'Weak', class: 'weak', color: '#ef4444' };
  if (entropy < 60) return { label: 'Fair', class: 'fair', color: '#f59e0b' };
  if (entropy < 72) return { label: 'Good', class: 'good', color: '#10b981' };
  if (entropy < 100) return { label: 'Strong', class: 'strong', color: '#10b981' };
  return { label: 'Very Strong', class: 'very-strong', color: '#059669' };
}

/**
 * Generate strong password
 */
function generatePassword(length = 16) {
  const charset = CHAR_SETS.lowercase + CHAR_SETS.uppercase + CHAR_SETS.numbers + CHAR_SETS.common_symbols;
  let password = '';

  // Ensure at least one of each required type
  password += CHAR_SETS.uppercase[Math.floor(Math.random() * CHAR_SETS.uppercase.length)];
  password += CHAR_SETS.lowercase[Math.floor(Math.random() * CHAR_SETS.lowercase.length)];
  password += CHAR_SETS.numbers[Math.floor(Math.random() * CHAR_SETS.numbers.length)];
  password += CHAR_SETS.common_symbols[Math.floor(Math.random() * CHAR_SETS.common_symbols.length)];

  // Fill remaining length
  for (let i = password.length; i < length; i++) {
    password += charset[Math.floor(Math.random() * charset.length)];
  }

  // Shuffle
  return password.split('').sort(() => Math.random() - 0.5).join('');
}

/**
 * Main Password Checker Class
 */
class PasswordChecker {
  constructor() {
    this.passwordInput = document.getElementById('password-input');
    this.toggleBtn = document.getElementById('toggle-visibility');
    this.generateBtn = document.getElementById('generate-btn');
    this.meterFill = document.getElementById('meter-fill');
    this.strengthText = document.getElementById('strength-text');
    this.entropyText = document.getElementById('entropy-text');
    this.entropyValue = document.getElementById('entropy-value');
    this.crackOnline = document.getElementById('crack-online');
    this.crackOffline = document.getElementById('crack-offline');
    this.entropyDetails = document.getElementById('entropy-details');
    this.requirementsList = document.getElementById('requirements-list');
    this.suggestionsList = document.getElementById('suggestions-list');
    this.suggestionsCard = document.getElementById('suggestions-card');
    this.warningList = document.getElementById('warning-list');
    this.warningCard = document.getElementById('warning-card');
    this.eyeIcon = this.toggleBtn.querySelector('.eye-icon');
    this.eyeOffIcon = this.toggleBtn.querySelector('.eye-off-icon');

    this.initEventListeners();
  }

  initEventListeners() {
    this.passwordInput.addEventListener('input', () => this.analyze());
    this.toggleBtn.addEventListener('click', () => this.toggleVisibility());
    this.generateBtn.addEventListener('click', () => this.generatePassword());

    // Paste event
    this.passwordInput.addEventListener('paste', (e) => {
      setTimeout(() => this.analyze(), 0);
    });
  }

  analyze() {
    const password = this.passwordInput.value;

    // Clear if empty
    if (!password) {
      this.resetUI();
      return;
    }

    // Calculate entropy
    const entropy = calculateEntropy(password);

    // Check requirements
    const requirements = checkRequirements(password);

    // Get suggestions and warnings
    const suggestions = getSuggestions(password, requirements);
    const warnings = getWarnings(password);

    // Get strength label
    const strength = getStrengthLabel(entropy);

    // Estimate crack times
    const crackTimes = estimateCrackTime(entropy);

    // Update UI
    this.updateStrengthMeter(entropy, strength);
    this.updateStrengthLabel(strength, entropy);
    this.updateEntropyDetails(entropy, crackTimes);
    this.updateRequirements(requirements);
    this.updateSuggestions(suggestions);
    this.updateWarnings(warnings);
  }

  resetUI() {
    this.meterFill.style.width = '0%';
    this.meterFill.className = 'meter-fill';
    this.strengthText.textContent = 'Enter a password';
    this.entropyText.style.display = 'none';
    this.entropyDetails.style.display = 'none';
    this.suggestionsCard.style.display = 'none';
    this.warningCard.style.display = 'none';

    // Reset requirements
    document.querySelectorAll('.requirements-list li').forEach(li => {
      li.className = 'unmet';
      li.querySelector('.req-icon').innerHTML = '<circle cx="12" cy="12" r="10"/>';
    });

    this.suggestionsList.innerHTML = '';
    this.warningList.innerHTML = '';
  }

  updateStrengthMeter(entropy, strength) {
    // Map entropy to percentage (0-100)
    // 0 bits = 0%, 100+ bits = 100%
    const percentage = Math.min(100, (entropy / 100) * 100);
    this.meterFill.style.width = `${percentage}%`;
    this.meterFill.className = `meter-fill ${strength.class}`;
  }

  updateStrengthLabel(strength, entropy) {
    this.strengthText.textContent = strength.label;
    this.strengthText.className = `strength-text ${strength.class}`;
    this.entropyText.textContent = `${entropy.toFixed(1)} bits entropy`;
    this.entropyText.style.display = 'inline';
    this.entropyDetails.style.display = 'grid';
  }

  updateEntropyDetails(entropy, crackTimes) {
    this.entropyValue.textContent = entropy.toFixed(1);
    this.crackOnline.textContent = formatTime(crackTimes.online);
    this.crackOffline.textContent = formatTime(crackTimes.offline);
  }

  updateRequirements(requirements) {
    const icons = {
      met: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 6L9 17l-5-5"/></svg>',
      unmet: '<circle cx="12" cy="12" r="10"/>'
    };

    document.querySelectorAll('.requirements-list li').forEach(li => {
      const req = li.dataset.requirement;
      const met = requirements[req];
      li.className = met ? 'met' : 'unmet';
      li.querySelector('.req-icon').innerHTML = icons[met ? 'met' : 'unmet'];
    });
  }

  updateSuggestions(suggestions) {
    this.suggestionsList.innerHTML = '';

    if (suggestions.length === 0) {
      this.suggestionsCard.style.display = 'none';
      return;
    }

    this.suggestionsCard.style.display = 'block';
    suggestions.forEach(suggestion => {
      const li = document.createElement('li');
      li.innerHTML = `
        <svg class="suggestion-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">
          <circle cx="12" cy="12" r="10"/>
          <line x1="12" y1="8" x2="12" y2="12"/>
          <line x1="12" y1="16" x2="12.01" y2="16"/>
        </svg>
        <span>${suggestion}</span>
      `;
      this.suggestionsList.appendChild(li);
    });
  }

  updateWarnings(warnings) {
    this.warningList.innerHTML = '';

    if (warnings.length === 0) {
      this.warningCard.style.display = 'none';
      return;
    }

    this.warningCard.style.display = 'block';
    warnings.forEach(warning => {
      const li = document.createElement('li');
      li.innerHTML = `
        <svg class="warning-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">
          <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>
          <line x1="12" y1="9" x2="12" y2="13"/>
          <line x1="12" y1="17" x2="12.01" y2="17"/>
        </svg>
        <span>${warning}</span>
      `;
      this.warningList.appendChild(li);
    });
  }

  toggleVisibility() {
    const type = this.passwordInput.type === 'password' ? 'text' : 'password';
    this.passwordInput.type = type;

    this.eyeIcon.style.display = type === 'password' ? 'block' : 'none';
    this.eyeOffIcon.style.display = type === 'password' ? 'none' : 'block';
    this.toggleBtn.setAttribute('aria-label', type === 'password' ? 'Show password' : 'Hide password');
  }

  generatePassword() {
    const newPassword = generatePassword(16);
    this.passwordInput.value = newPassword;
    this.analyze();
    this.passwordInput.focus();
  }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  // Initialize password checker if on password page
  if (document.getElementById('password-input')) {
    window.passwordChecker = new PasswordChecker();
  }
});