/**
 * Future Mall - Phishing Quiz
 * Interactive quiz with 15 questions, immediate feedback, and scoring.
 */

// Quiz Questions Database
const QUIZ_QUESTIONS = [
  {
    id: 1,
    category: "Bank Phishing",
    difficulty: "Easy",
    email: {
      from: "security@bankofamerica-security.com",
      subject: "URGENT: Your Account Will Be Closed",
      body: `Dear Customer,

We have detected suspicious activity on your Bank of America account. For your security, we need you to verify your identity immediately.

Click the link below to confirm your account details:
https://bankofamerica-verify-account.xyz/login

If you do not verify within 24 hours, your account will be permanently closed.

Thank you,
Bank of America Security Team`
    },
    answer: "phishing",
    explanation: "This is a classic phishing email. Red flags: 1) Sender domain 'bankofamerica-security.com' is not the official bankofamerica.com domain. 2) Urgent threat of account closure. 3) Generic 'Dear Customer' greeting. 4) Suspicious link domain 'bankofamerica-verify-account.xyz' - legitimate banks use their official domain. 5) Threat of permanent closure creates pressure to act quickly without thinking."
  },
  {
    id: 2,
    category: "Legitimate Email",
    difficulty: "Easy",
    email: {
      from: "notifications@github.com",
      subject: "New sign-in to your GitHub account",
      body: `Hello Sarah,

We detected a new sign-in to your GitHub account from a new device.

Device: Chrome on Windows
Location: New York, NY (approximate)
Time: March 15, 2024, 2:34 PM UTC

If this was you, no action is needed. If this wasn't you, please secure your account immediately by visiting: https://github.com/settings/security

Thanks,
The GitHub Team`
    },
    answer: "legitimate",
    explanation: "This is a legitimate security notification from GitHub. Green flags: 1) Official 'github.com' sender domain. 2) Specific details about the sign-in (device, location, time). 3) No urgent threats or demands. 4) Links to official github.com domain for account security. 5) Professional formatting and personalized greeting."
  },
  {
    id: 3,
    category: "Package Delivery Phishing",
    difficulty: "Medium",
    email: {
      from: "tracking@fedex-delivery-notifications.com",
      subject: "Delivery Failed - Action Required",
      body: `Dear Customer,

We attempted to deliver your package (Tracking: FX123456789) but no one was available to sign.

Please reschedule delivery within 48 hours or the package will be returned to sender:
https://fedex-reschedule.xyz/claim/FX123456789

A $15 redelivery fee applies if not claimed within 24 hours.

FedEx Delivery Services`
    },
    answer: "phishing",
    explanation: "Phishing attempt. Red flags: 1) Sender domain 'fedex-delivery-notifications.com' is not fedex.com. 2) Urgent 24-hour deadline with fee threat. 3) Suspicious link domain 'fedex-reschedule.xyz' - not fedex.com. 4) Generic 'Dear Customer' greeting. 5) Legitimate carriers typically leave a physical notice or use their official app for rescheduling."
  },
  {
    id: 4,
    category: "Legitimate Email",
    difficulty: "Medium",
    email: {
      from: "security@google.com",
      subject: "Security alert: New sign-in from unknown device",
      body: `Hi Michael,

We noticed a sign-in to your Google Account from a device you don't usually use.

Device: Samsung Galaxy S23
Location: Los Angeles, CA (based on IP)
Time: March 14, 2024, 8:12 PM PDT

If this was you, you can ignore this email. If not, please review your account activity:
https://myaccount.google.com/device-activity

You can also run a Security Checkup:
https://myaccount.google.com/security-checkup

Best regards,
The Google Security Team`
    },
    answer: "legitimate",
    explanation: "Legitimate Google security alert. Green flags: 1) Official 'google.com' domain. 2) Specific device and location details. 3) Links to official google.com domains (myaccount.google.com). 4) No urgency or threats - allows you to ignore if it was you. 4) Professional tone with specific details about the sign-in."
  },
  {
    id: 5,
    category: "Tax/IRS Phishing",
    difficulty: "Medium",
    email: {
      from: "refunds@irs-tax-refund.gov",
      subject: "Tax Refund Notification - $2,847.00",
      body: `Taxpayer,

You are eligible for a tax refund of $2,847.00 for the 2023 tax year.

To claim your refund, please verify your banking information:
https://irs-refund-claim.net/banking

This offer expires in 72 hours. After this period, the refund will be forfeited.

Internal Revenue Service`
    },
    answer: "phishing",
    explanation: "Classic IRS phishing scam. Red flags: 1) IRS never initiates contact via email about refunds. 2) Sender domain 'irs-tax-refund.gov' is not irs.gov. 3) Urgent 72-hour deadline. 4) Request for banking information via email. 5) Suspicious link domain 'irs-refund-claim.net' - not irs.gov. 6) The IRS never demands immediate action or threatens forfeiture via email."
  },
  {
    id: 6,
    category: "Microsoft/Office 365 Phishing",
    difficulty: "Medium",
    email: {
      from: "admin@microsoft-security-alerts.com",
      subject: "Your password expires today",
      body: `Dear User,

Your Microsoft 365 password will expire today. To maintain access to your email and documents, please update your password immediately.

Update your password: https://microsoft-password-renewal.xyz/renew

If you do not update within 2 hours, your account will be locked.

Microsoft Security Team`
    },
    answer: "phishing",
    explanation: "Microsoft phishing attempt. Red flags: 1) Sender domain 'microsoft-security-alerts.com' is not microsoft.com. 2) Extreme 2-hour deadline with account lock threat. 3) Suspicious link domain 'microsoft-password-renewal.xyz' - not microsoft.com. 4) Generic 'Dear User' greeting. 5) Microsoft typically sends password expiration notices well in advance (14+ days) and doesn't lock accounts after 2 hours."
  },
  {
    id: 7,
    category: "LinkedIn Phishing",
    difficulty: "Easy",
    email: {
      from: "notifications@linkedin.com",
      subject: "You have 3 new connection requests",
      body: `Hi Alex,

You have 3 new connection requests waiting for your review:

• Jane Smith - Senior Developer at TechCorp
• Robert Chen - Product Manager at StartupXYZ
• Maria Garcia - UX Designer at DesignStudio

View all requests: https://www.linkedin.com/mynetwork/invitations/

Stay connected,
The LinkedIn Team`
    },
    answer: "legitimate",
    explanation: "Legitimate LinkedIn notification. Green flags: 1) Official 'linkedin.com' domain. 2) Specific personalized content (names, titles, companies). 3) Link goes to official linkedin.com domain. 3) No urgency or threats. 4) Professional formatting matching LinkedIn's actual notification style."
  },
  {
    id: 8,
    category: "CEO Fraud / BEC",
    difficulty: "Hard",
    email: {
      from: "john.smith@company-ceo.com",
      subject: "URGENT: Wire Transfer Needed",
      body: `Hi Jennifer,

I'm in a board meeting and need you to process an urgent wire transfer for a confidential acquisition.

Amount: $47,500.00
Beneficiary: Global Acquisitions Ltd.
Account: 9876543210
Routing: 021000021
Reference: ACQ-2024-CONFIDENTIAL

Please process immediately and send confirmation. I'll explain details after the meeting.

Sent from my iPhone
John Smith
CEO`
    },
    answer: "phishing",
    explanation: "Business Email Compromise (CEO Fraud). Red flags: 1) Sender domain 'company-ceo.com' doesn't match your company's actual domain. 2) Extreme urgency with 'board meeting' excuse. 3) Request to bypass normal approval processes. 4) Request for wire transfer to unfamiliar account. 5) 'Sent from my iPhone' - attempting to create authenticity. 5) CEO would never request urgent wire transfers via email without proper authorization chain."
  },
  {
    id: 9,
    category: "Netflix/Subscription Phishing",
    difficulty: "Easy",
    email: {
      from: "support@netflix.com",
      subject: "Your Netflix membership is on hold",
      body: `Hi Taylor,

We couldn't process your payment for this month's subscription. To continue enjoying Netflix, please update your payment method.

Update payment: https://www.netflix.com/update-payment

If you don't update within 7 days, your account will be paused.

Questions? Visit our Help Center: https://help.netflix.com

The Netflix Team`
    },
    answer: "legitimate",
    explanation: "Legitimate Netflix payment notification. Green flags: 1) Official 'netflix.com' domain. 2) Reasonable 7-day grace period (not hours). 3) Links to official netflix.com domain. 4) Professional tone without threats. 5) Links to official help center. 5) No request for sensitive info directly in email - directs to account page."
  },
  {
    id: 10,
    category: "Fake Job Offer",
    difficulty: "Medium",
    email: {
      from: "hr@google-careers-recruitment.com",
      subject: "Job Offer: Senior Software Engineer - $180,000/year",
      body: `Dear Candidate,

Congratulations! After reviewing your profile, we're pleased to offer you a Senior Software Engineer position at Google.

Salary: $180,000/year + $50,000 signing bonus
Remote work available
Start date: Immediate

To proceed, we need to verify your identity. Please reply with:
- Government ID (passport/driver's license)
- Social Security Number
- Bank account details for direct deposit setup

Reply to this email with the documents attached.

Google Recruitment Team`
    },
    answer: "phishing",
    explanation: "Job offer scam. Red flags: 1) Sender domain 'google-careers-recruitment.com' is not google.com or careers.google.com. 2) Request for highly sensitive personal information (SSN, ID, bank details) via email BEFORE any interview or formal offer. 3) Legitimate companies never request SSN or ID via email before formal onboarding. 4) 'Immediate start' pressure. 5) Unusually high signing bonus as lure."
  },
  {
    id: 11,
    category: "Apple/iCloud Phishing",
    difficulty: "Medium",
    email: {
      from: "appleid@apple.com",
      subject: "Your Apple ID has been locked",
      body: `Dear Apple User,

Your Apple ID has been locked for security reasons due to multiple failed login attempts.

To unlock your account, please verify your identity:
https://iforgot.apple.com/unlock

If you don't unlock within 24 hours, your account will be permanently deleted.

Apple Support`
    },
    answer: "phishing",
    explanation: "Apple phishing. Red flags: 1) While sender appears as 'appleid@apple.com', email headers can be spoofed. 2) Extreme 24-hour threat with 'permanent deletion' - Apple doesn't work this way. 3) Legitimate Apple account recovery uses iforgot.apple.com but doesn't threaten permanent deletion in 24 hours. 4) Generic 'Dear Apple User' greeting. 5) Always go directly to apple.com or use the Apple Support app instead of clicking email links."
  },
  {
    id: 12,
    category: "Amazon Phishing",
    difficulty: "Easy",
    email: {
      from: "orders@amazon.com",
      subject: "Your Amazon.com order #112-3456789-1234567",
      body: `Hello Casey,

Thank you for your order. Your estimated delivery date is March 20, 2024.

Order Details:
• Wireless Bluetooth Headphones - $79.99
• Shipping: FREE Prime Delivery
• Order Total: $79.99

Track your package: https://www.amazon.com/your-orders

If you didn't place this order, contact us: https://www.amazon.com/contact-us

Amazon.com`
    },
    answer: "legitimate",
    explanation: "Legitimate Amazon order confirmation. Green flags: 1) Official 'amazon.com' domain. 2) Specific order details (order number, item, price, delivery date). 3) Links to official amazon.com domains. 4) No urgency or threats. 5) Clear instructions for if you didn't place the order. 5) Professional formatting matching Amazon's actual order emails."
  },
  {
    id: 13,
    category: "Social Media Phishing",
    difficulty: "Medium",
    email: {
      from: "security@instagram-support.com",
      subject: "Copyright Violation Notice - Account at Risk",
      body: `Instagram User,

We've received a copyright infringement report against your account. Your account will be permanently disabled in 48 hours unless you appeal.

Appeal here: https://instagram-appeal-form.xyz/copyright

You must provide:
- Government-issued ID
- Proof of content ownership
- Written statement

Instagram Legal Team`
    },
    answer: "phishing",
    explanation: "Instagram phishing. Red flags: 1) Sender domain 'instagram-support.com' is not instagram.com or meta.com. 2) Extreme 48-hour deadline with permanent disable threat. 3) Suspicious link domain 'instagram-appeal-form.xyz' - not instagram.com. 4) Request for government ID via external form. 5) Legitimate copyright appeals go through Instagram's official in-app process, not external links."
  },
  {
    id: 14,
    category: "IT Support Scam",
    difficulty: "Medium",
    email: {
      from: "it-support@company-tech-services.com",
      subject: "Mandatory Security Update - Action Required",
      body: `Dear Employee,

Our security team has identified a critical vulnerability affecting all company devices. You must install the security patch immediately.

Download patch: https://company-security-patch.xyz/install.exe

Installation deadline: Today by 5:00 PM
Devices without patch will be disconnected from network.

IT Security Department`
    },
    answer: "phishing",
    explanation: "IT support scam. Red flags: 1) Sender domain 'company-tech-services.com' - not your actual company domain. 2) Executable file download (.exe) from external link - legitimate IT deploys patches through managed systems, not email links. 3) Extreme same-day deadline. 5) Generic 'IT Security Department' signature. 6) Threat of network disconnection. 6) Legitimate IT updates are pushed automatically or through approved internal channels."
  },
  {
    id: 15,
    category: "Charity/Disaster Phishing",
    difficulty: "Easy",
    email: {
      from: "donations@redcross-disaster-relief.org",
      subject: "URGENT: Earthquake Victims Need Your Help",
      body: `Dear Friend,

A devastating 7.8 magnitude earthquake has struck Turkey and Syria. Thousands are injured and homeless.

The Red Cross is on the ground providing emergency shelter, medical care, and clean water. But we need your help NOW.

Donate immediately: https://redcross-emergency-fund.net/donate

$50 provides emergency shelter for a family
$100 provides medical supplies for 10 people
$250 provides clean water for a village

Every minute counts. Donate now.

American Red Cross`
    },
    answer: "phishing",
    explanation: "Disaster relief phishing exploiting tragedy. Red flags: 1) Sender domain 'redcross-disaster-relief.org' is not redcross.org. 2) Emotional manipulation with urgent 'NOW' language. 3) Suspicious link domain 'redcross-emergency-fund.net' - not redcross.org. 4) Specific donation amounts with emotional appeals. 5) Legitimate charities use their official domain and don't pressure via unsolicited email. 5) Always donate directly through the charity's official website."
  }
];

// Quiz State
let currentQuestionIndex = 0;
let score = 0;
let answers = [];
let questionOrder = [];

// DOM Elements
const quizIntro = document.getElementById('quiz-intro');
const quizArea = document.getElementById('quiz-area');
const resultsArea = document.getElementById('results-area');
const startBtn = document.getElementById('start-quiz');
const nextBtn = document.getElementById('next-btn');
const retryBtn = document.getElementById('retry-btn');
const shareBtn = document.getElementById('share-btn');
const answerBtns = document.querySelectorAll('.answer-btn');
const feedbackArea = document.getElementById('feedback-area');
const questionCard = document.getElementById('question-card');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
  initQuiz();
});

function initQuiz() {
  // Shuffle questions for variety
  questionOrder = [...Array(QUIZ_QUESTIONS.length).keys()];
  shuffleArray(questionOrder);

  // Event listeners
  startBtn.addEventListener('click', startQuiz);
  nextBtn.addEventListener('click', nextQuestion);
  retryBtn.addEventListener('click', retryQuiz);
  shareBtn.addEventListener('click', shareResults);

  answerBtns.forEach(btn => {
    btn.addEventListener('click', () => selectAnswer(btn.dataset.answer));
  });
}

function shuffleArray(array) {
  for (let i = array.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [array[i], array[j]] = [array[j], array[i]];
  }
}

function startQuiz() {
  currentQuestionIndex = 0;
  score = 0;
  answers = [];

  quizIntro.style.display = 'none';
  quizArea.style.display = 'block';
  resultsArea.style.display = 'none';

  loadQuestion();
}

function loadQuestion() {
  const question = QUIZ_QUESTIONS[questionOrder[currentQuestionIndex]];

  // Update progress
  document.getElementById('current-q').textContent = currentQuestionIndex + 1;
  document.getElementById('total-q').textContent = QUIZ_QUESTIONS.length;
  document.getElementById('current-score').textContent = score;

  const progress = ((currentQuestionIndex) / QUIZ_QUESTIONS.length) * 100;
  document.getElementById('progress-fill').style.width = `${progress}%`;

  // Update question header
  document.getElementById('question-number').textContent = `Question ${currentQuestionIndex + 1}`;
  document.getElementById('question-category').textContent = question.category;

  // Render email scenario
  const email = question.email;
  document.getElementById('email-scenario').innerHTML = `
    <div class="email-header">
      <div class="email-field"><strong>From:</strong> <span class="email-from">${email.from}</span></div>
      <div class="email-field"><strong>Subject:</strong> <span class="email-subject">${email.subject}</span></div>
    </div>
    <div class="email-body">
      ${email.body.split('\n').map(line => `<p>${escapeHtml(line)}</p>`).join('')}
    </div>
  `;

  // Reset buttons
  document.querySelectorAll('.answer-btn').forEach(btn => {
    btn.classList.remove('correct', 'incorrect', 'disabled');
    btn.disabled = false;
  });

  // Hide feedback
  document.getElementById('feedback-area').style.display = 'none';
  document.getElementById('next-btn').style.display = 'none';
}

function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

function selectAnswer(userAnswer) {
  const question = QUIZ_QUESTIONS[questionOrder[currentQuestionIndex]];
  const isCorrect = userAnswer === question.answer;

  // Record answer
  answers.push({
    questionId: question.id,
    userAnswer,
    correct: isCorrect,
    category: question.category
  });

  if (isCorrect) {
    score++;
  }

  // Update score display
  document.getElementById('current-score').textContent = score;

  // Disable buttons and show feedback
  document.querySelectorAll('.answer-btn').forEach(btn => {
    btn.disabled = true;
    btn.classList.add('disabled');

    if (btn.dataset.answer === question.answer) {
      btn.classList.add('correct');
    } else if (btn.dataset.answer === userAnswer && !isCorrect) {
      btn.classList.add('incorrect');
    }
  });

  // Show feedback
  showFeedback(question, isCorrect, userAnswer);

  // Update progress bar
  const progress = ((currentQuestionIndex + 1) / QUIZ_QUESTIONS.length) * 100;
  document.getElementById('progress-fill').style.width = `${progress}%`;

  // Show next button
  document.getElementById('next-btn').style.display = 'inline-flex';
}

function showFeedback(question, isCorrect, userAnswer) {
  const feedbackArea = document.getElementById('feedback-area');
  const feedbackIcon = feedbackArea.querySelector('.feedback-icon');
  const feedbackTitle = feedbackArea.querySelector('.feedback-title');
  const feedbackExplanation = document.getElementById('feedback-explanation');
  const feedbackDetails = document.getElementById('feedback-details');

  if (isCorrect) {
    feedbackIcon.innerHTML = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>`;
    feedbackTitle.textContent = 'Correct!';
    feedbackArea.className = 'feedback-area correct';
  } else {
    feedbackIcon.innerHTML = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>`;
    feedbackTitle.textContent = 'Incorrect';
    feedbackArea.className = 'feedback-area incorrect';
  }

  feedbackExplanation.textContent = question.explanation;

  // Add category tag
  feedbackDetails.innerHTML = `
    <div class="feedback-category">
      <span class="category-label">Category:</span>
      <span class="category-value">${question.category}</span>
    </div>
    <div class="feedback-category">
      <span class="category-label">Difficulty:</span>
      <span class="category-value">${question.difficulty}</span>
    </div>
    <div class="feedback-category">
      <span class="category-label">Your Answer:</span>
      <span class="category-value ${userAnswer === question.answer ? 'correct' : 'incorrect'}">${userAnswer.charAt(0).toUpperCase() + userAnswer.slice(1)}</span>
    </div>
  `;

  document.getElementById('feedback-area').style.display = 'block';
}

function nextQuestion() {
  currentQuestionIndex++;

  if (currentQuestionIndex >= QUIZ_QUESTIONS.length) {
    showResults();
  } else {
    loadQuestion();
  }
}

function showResults() {
  quizArea.style.display = 'none';
  resultsArea.style.display = 'block';

  const correct = answers.filter(a => a.correct).length;
  const incorrect = answers.filter(a => !a.correct).length;
  const accuracy = Math.round((correct / QUIZ_QUESTIONS.length) * 100);

  // Score display
  document.getElementById('final-score').textContent = correct;
  document.getElementById('correct-count').textContent = correct;
  document.getElementById('incorrect-count').textContent = incorrect;
  document.getElementById('accuracy').textContent = `${accuracy}%`;

  // Score label
  let scoreLabel = '';
  let resultsIcon = '';

  if (accuracy >= 90) {
    scoreLabel = 'Phishing Expert! 🏆';
    resultsIcon = '🏆';
  } else if (accuracy >= 70) {
    scoreLabel = 'Well Done! 🎉';
    resultsIcon = '🎉';
  } else if (accuracy >= 50) {
    scoreLabel = 'Good Effort! 👍';
    resultsIcon = '👍';
  } else {
    scoreLabel = 'Keep Learning! 📚';
    resultsIcon = '📚';
  }

  document.getElementById('score-label').textContent = scoreLabel;
  document.getElementById('results-icon').textContent = resultsIcon;

  // Category breakdown
  const categoryBreakdown = document.getElementById('category-breakdown');
  const categories = {};

  answers.forEach(answer => {
    if (!categories[answer.category]) {
      categories[answer.category] = { correct: 0, total: 0 };
    }
    categories[answer.category].total++;
    if (answer.correct) categories[answer.category].correct++;
  });

  categoryBreakdown.innerHTML = '<h3>Performance by Category</h3>';
  Object.entries(categories).forEach(([category, stats]) => {
    const catAccuracy = Math.round((stats.correct / stats.total) * 100);
    const div = document.createElement('div');
    div.className = 'category-stat';
    div.innerHTML = `
      <span class="category-name">${category}</span>
      <span class="category-score">${stats.correct}/${stats.total} (${catAccuracy}%)</span>
    `;
    categoryBreakdown.appendChild(div);
  });

  // Personalized tips
  const resultsTips = document.getElementById('results-tips');
  let tips = [];

  if (accuracy < 70) {
    tips.push('Review the threat library to learn more about each threat type');
  }
  if (answers.some(a => a.category === 'Phishing' && !a.correct)) {
    tips.push('Practice identifying phishing red flags: urgency, generic greetings, suspicious links');
  }
  if (answers.some(a => a.category === 'CEO Fraud / BEC' && !a.correct)) {
    tips.push('Verify urgent requests from executives through a separate communication channel');
  }
  if (accuracy >= 90) {
    tips.push('Excellent! You have strong phishing detection skills. Share this quiz with colleagues!');
  }

  resultsTips.innerHTML = '<h3>Personalized Recommendations</h3><ul>' +
    tips.map(tip => `<li>${tip}</li>`).join('') + '</ul>';
}

function retryQuiz() {
  // Re-shuffle
  shuffleArray(questionOrder);
  currentQuestionIndex = 0;
  score = 0;
  answers = [];

  resultsArea.style.display = 'none';
  quizArea.style.display = 'block';

  loadQuestion();
}

function shareResults() {
  const correct = answers.filter(a => a.correct).length;
  const accuracy = Math.round((correct / QUIZ_QUESTIONS.length) * 100);

  const shareText = `I scored ${correct}/15 (${accuracy}%) on the Future Mall Phishing Quiz! 🎣 Test your phishing detection skills: ${window.location.origin}/digital_awareness/quiz.html`;

  if (navigator.share) {
    navigator.share({
      title: 'Phishing Quiz Results',
      text: shareText,
      url: window.location.href
    });
  } else {
    navigator.clipboard.writeText(shareText).then(() => {
      alert('Results copied to clipboard! Share your score with friends.');
    });
  }
}

// Utility
function shuffleArray(array) {
  for (let i = array.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [array[i], array[j]] = [array[j], array[i]];
  }
}