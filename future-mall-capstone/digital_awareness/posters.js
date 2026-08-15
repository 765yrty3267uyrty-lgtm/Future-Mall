/**
 * Future Mall - Posters Page JavaScript
 * Handles poster downloads, previews, and interactions.
 */

document.addEventListener('DOMContentLoaded', () => {
  initPosterInteractions();
  initDownloadButtons();
});

function initPosterInteractions() {
  // Preview buttons
  document.querySelectorAll('[data-poster]').forEach(btn => {
    if (btn.textContent.includes('Preview')) {
      btn.addEventListener('click', (e) => {
        const posterId = e.target.dataset.poster;
        showPosterPreview(posterId);
      });
    }
  });

  // Download buttons
  document.querySelectorAll('[data-poster]').forEach(btn => {
    if (btn.textContent.includes('Download')) {
      btn.addEventListener('click', (e) => {
        const posterId = e.target.dataset.poster;
        downloadPoster(posterId);
      });
    }
  });
}

function initDownloadButtons() {
  // Download all individual
  const downloadIndividual = document.getElementById('download-individual');
  if (downloadIndividual) {
    downloadIndividual.addEventListener('click', () => {
      downloadAllPosters('pdf');
    });
  }

  // Download PNG
  const downloadPng = document.getElementById('download-png');
  if (downloadPng) {
    downloadPng.addEventListener('click', () => {
      downloadAllPosters('png');
    });
  }

  // Download bundle
  const downloadBundle = document.getElementById('download-bundle');
  if (downloadBundle) {
    downloadBundle.addEventListener('click', () => {
      downloadBundleFiles();
    });
  }

  // Download all button in CTA
  const downloadAllBtn = document.getElementById('download-all-btn');
  if (downloadAllBtn) {
    downloadAllBtn.addEventListener('click', () => {
      downloadAllPosters('pdf');
    });
  }
}

function showPosterPreview(posterId) {
  const posters = {
    'think-before-click': {
      title: 'Think Before You Click',
      description: 'Hover over links. Check the URL. Verify the sender.',
      color: 'linear-gradient(135deg, #1e3a5f 0%, #2563eb 100%)',
      icon: '🤔',
      topics: ['Hover to inspect URLs', 'Check sender authenticity', 'Report suspicious links']
    },
    'protect-password': {
      title: 'Protect Your Password',
      description: '12+ chars. Mixed case. Numbers. Symbols. Unique per site.',
      color: 'linear-gradient(135deg, #064e3b 0%, #0d9488 100%)',
      icon: '🔐',
      topics: ['Length over complexity', 'Password managers', 'MFA everywhere']
    },
    'stay-safe-online': {
      title: 'Stay Safe Online',
      description: 'HTTPS everywhere. VPN on public Wi-Fi. Update regularly.',
      color: 'linear-gradient(135deg, #7c2d12 0%, #f97316 100%)',
      icon: '🛡️',
      topics: ['HTTPS everywhere', 'VPN on public Wi-Fi', 'Auto updates enabled']
    },
    'verify-before-trust': {
      title: 'Verify Before You Trust',
      description: 'Check the source. Verify the request. Use another channel.',
      color: 'linear-gradient(135deg, #7c2d12 0%, #f97316 100%)',
      icon: '✅',
      topics: ['Verify sender identity', 'Use separate channel', 'Report suspicious requests']
    },
    'privacy-matters': {
      title: 'Privacy Matters',
      description: 'Limit sharing. Check permissions. Use privacy settings.',
      color: 'linear-gradient(135deg, #7c2d12 0%, #f97316 100%)',
      icon: '🔒',
      topics: ['Social media privacy', 'App permissions audit', 'Data minimization']
    },
    'keep-updated': {
      title: 'Keep Software Updated',
      description: 'Auto-updates on. Patch promptly. Restart when prompted.',
      color: 'linear-gradient(135deg, #1e3a5f 0%, #2563eb 100%)',
      icon: '🔄',
      topics: ['Auto-updates enabled', 'Patch promptly', 'Restart when needed']
    }
  };

  const poster = posters[posterId];
  if (!poster) return;

  // Create modal
  const modal = document.createElement('div');
  modal.className = 'modal-overlay';
  modal.innerHTML = `
    <div class="modal" role="dialog" aria-modal="true" aria-labelledby="modal-title">
      <button class="modal-close" aria-label="Close preview">&times;</button>
      <div class="modal-content">
        <div class="modal-poster" style="background: ${poster.color};">
          <div class="poster-icon" aria-hidden="true">${poster.icon}</div>
          <h3>${poster.title}</h3>
          <p>${poster.description}</p>
        </div>
        <div class="modal-details">
          <h3>${poster.title}</h3>
          <ul>
            ${poster.topics.map(topic => `<li>${topic}</li>`).join('')}
          </ul>
          <div class="modal-actions">
            <button class="btn btn-primary" onclick="downloadPoster('${posterId}')">Download PDF</button>
            <button class="btn btn-outline" onclick="this.closest('.modal-overlay').remove()">Close</button>
          </div>
        </div>
      </div>
    </div>
  `;

  document.body.appendChild(modal);
  document.body.style.overflow = 'hidden';

  // Close handlers
  const closeBtn = modal.querySelector('.modal-close');
  closeBtn.addEventListener('click', () => closeModal(modal));

  modal.addEventListener('click', (e) => {
    if (e.target === modal) closeModal(modal);
  });

  document.addEventListener('keydown', function handleEsc(e) {
    if (e.key === 'Escape') {
      closeModal(modal);
      document.removeEventListener('keydown', handleEsc);
    }
  });
}

function closeModal(modal) {
  modal.remove();
  document.body.style.overflow = '';
}

function downloadPoster(posterId) {
  const posters = {
    'think-before-click': 'Think Before You Click',
    'protect-password': 'Protect Your Password',
    'stay-safe-online': 'Stay Safe Online',
    'verify-before-trust': 'Verify Before You Trust',
    'privacy-matters': 'Privacy Matters',
    'keep-updated': 'Keep Software Updated'
  };

  const title = posters[posterId] || 'Poster';

  // Create a simple PDF-like content
  const content = generatePosterContent(posterId);

  // Create blob and download
  const blob = new Blob([content], { type: 'text/plain' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `${posterId.replace(/-/g, '_')}_poster.txt`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);

  // Show notification
  showNotification(`Downloaded ${posters[posterId]} poster`);
}

function generatePosterContent(posterId) {
  const posters = {
    'think-before-click': {
      title: 'Think Before You Click',
      description: 'Hover over links. Check the URL. Verify the sender.',
      topics: ['Hover to inspect URLs', 'Check sender authenticity', 'Report suspicious links']
    },
    'protect-password': {
      title: 'Protect Your Password',
      description: '12+ chars. Mixed case. Numbers. Symbols. Unique per site.',
      topics: ['Length over complexity', 'Password managers', 'MFA everywhere']
    },
    'stay-safe-online': {
      title: 'Stay Safe Online',
      description: 'HTTPS everywhere. VPN on public Wi-Fi. Update regularly.',
      topics: ['HTTPS everywhere', 'VPN on public Wi-Fi', 'Auto updates enabled']
    },
    'verify-before-trust': {
      title: 'Verify Before You Trust',
      description: 'Check the source. Verify the request. Use another channel.',
      topics: ['Verify sender identity', 'Use separate channel', 'Report suspicious requests']
    },
    'privacy-matters': {
      title: 'Privacy Matters',
      description: 'Limit sharing. Check permissions. Use privacy settings.',
      topics: ['Social media privacy', 'App permissions audit', 'Data minimization']
    },
    'keep-updated': {
      title: 'Keep Software Updated',
      description: 'Auto-updates on. Patch promptly. Restart when prompted.',
      topics: ['Auto-updates enabled', 'Patch promptly', 'Restart when needed']
    }
  };

  const poster = posters[posterId];
  let content = `FUTURE MALL - DIGITAL AWARENESS POSTER\n`;
  content += `===========================================\n\n`;
  content += `Title: ${poster.title}\n`;
  content += `Tagline: ${poster.description}\n\n`;
  content += `Key Points:\n`;
  poster.topics.forEach((topic, i) => {
    content += `${i + 1}. ${topic}\n`;
  });
  content += `\n`;
  content += `Part of Future Mall Capstone Project\n`;
  content += `Digital Awareness Platform\n`;
  content += `https://github.com/futuremall\n\n`;
  content += `Free for educational and non-commercial use.\n`;
  content += `Part of Future Mall Capstone Project.\n`;

  return content;
}

function downloadAllPosters(format) {
  const posters = [
    'think-before-click',
    'protect-password',
    'stay-safe-online',
    'verify-before-trust',
    'privacy-matters',
    'keep-updated'
  ];

  let content = `FUTURE MALL - DIGITAL AWARENESS POSTERS COLLECTION\n`;
  content += `====================================================\n\n`;
  content += `Format: ${format.toUpperCase()}\n`;
  content += `Generated: ${new Date().toISOString()}\n\n`;

  posters.forEach((id, index) => {
    content += `\n${'='.repeat(50)}\n`;
    content += `${index + 1}. ${generatePosterContent(id)}`;
  });

  content += `\n\n${'='.repeat(50)}\n`;
  content += `Future Mall Capstone Project\n`;
  content += `Digital Awareness Platform\n`;
  content += `Free for educational and non-commercial use.\n`;

  const blob = new Blob([content], { type: 'text/plain' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `future_mall_posters_${format}_${new Date().toISOString().split('T')[0]}.txt`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);

  showNotification(`Downloaded all 6 posters as ${format.toUpperCase()}`);
}

function downloadBundleFiles() {
  const content = `FUTURE MALL - DIGITAL AWARENESS COMPLETE BUNDLE
=================================================

CONTENTS:
1. Posters (6) - PDF + PNG formats
2. Source Files - Figma/SVG editable sources
3. Brand Guidelines - BRAND_GUIDELINES.md
4. Style Guide - CSS variables and components
5. Documentation - README, DEPLOYMENT, ARCHITECTURE

POSTERS INCLUDED:
1. Think Before You Click
2. Protect Your Password
3. Stay Safe Online
4. Verify Before You Trust
5. Privacy Matters
6. Keep Software Updated

FORMATS INCLUDED:
- High-resolution PDF (300 DPI, A3/A4)
- PNG (300 DPI, transparent background)
- SVG (scalable vector)
- Figma source files

BRAND ASSETS:
- Logo (6 variations: primary, stacked, icon, mono, white, responsive)
- Color Palette (Primary, Secondary, Accent, Semantic)
- Typography (Space Grotesk + Inter)
- Advertisement Templates (5 formats)

LICENSE:
Free for educational and non-commercial use.
Attribution required for commercial use.

Part of Future Mall Capstone Project
Digital Awareness Platform
https://github.com/futuremall

Generated: ${new Date().toISOString()}
`;

  const blob = new Blob([content], { type: 'text/plain' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `future_mall_digital_awareness_bundle_${new Date().toISOString().split('T')[0]}.txt`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);

  showNotification('Downloaded complete bundle with all assets');
}

function showNotification(message) {
  // Remove existing notifications
  const existing = document.querySelector('.notification-toast');
  if (existing) existing.remove();

  const toast = document.createElement('div');
  toast.className = 'notification-toast';
  toast.textContent = message;
  toast.style.cssText = `
    position: fixed;
    bottom: 24px;
    right: 24px;
    background: #1e293b;
    color: white;
    padding: 12px 24px;
    border-radius: 8px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.2);
    z-index: 10000;
    animation: slideIn 0.3s ease;
    font-size: 14px;
    font-weight: 500;
  `;

  const style = document.createElement('style');
  style.textContent = `
    @keyframes slideIn {
      from { transform: translateX(100%); opacity: 0; }
      to { transform: translateX(0); opacity: 1; }
    }
  `;
  document.head.appendChild(style);

  document.body.appendChild(toast);

  setTimeout(() => {
    toast.style.animation = 'slideIn 0.3s ease reverse';
    setTimeout(() => toast.remove(), 300);
  }, 3000);
}