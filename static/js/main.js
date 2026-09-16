/* ==========================================================================
   SKILLBRIDGE MAIN APPLICATION JAVASCRIPT
   Bilingual translation engine, theme switcher, voice recording modal,
   mobile drawer navigation, and toast system.
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
  initTheme();
  initLanguage();
  initMobileDrawer();
  initVoiceSearch();
});

/* --------------------------------------------------------------------------
   Theme Switcher (Light / Dark)
   -------------------------------------------------------------------------- */
function initTheme() {
  const savedTheme = localStorage.getItem('sk_theme') || 'light';
  if (savedTheme === 'dark') {
    document.documentElement.classList.add('dark');
  } else {
    document.documentElement.classList.remove('dark');
  }
}

function toggleTheme() {
  const isDark = document.documentElement.classList.toggle('dark');
  localStorage.setItem('sk_theme', isDark ? 'dark' : 'light');
  showToast(isDark ? 'Dark mode enabled' : 'Light mode enabled', 'info');
}

/* --------------------------------------------------------------------------
   Bilingual Switcher (English / Hindi Devanagari)
   -------------------------------------------------------------------------- */
function initLanguage() {
  const savedLang = localStorage.getItem('sk_lang') || 'en';
  switchLanguage(savedLang, false);
}

function switchLanguage(lang, notify = true) {
  localStorage.setItem('sk_lang', lang);
  document.documentElement.setAttribute('lang', lang);

  // Update active state on language toggle buttons
  document.querySelectorAll('[data-lang-btn]').forEach(btn => {
    if (btn.dataset.langBtn === lang) {
      btn.classList.add('bg-amber-600', 'text-white');
      btn.classList.remove('bg-gray-100', 'text-gray-700', 'dark:bg-slate-800', 'dark:text-slate-300');
    } else {
      btn.classList.remove('bg-amber-600', 'text-white');
      btn.classList.add('bg-gray-100', 'text-gray-700', 'dark:bg-slate-800', 'dark:text-slate-300');
    }
  });

  // Update data-en / data-hi DOM elements
  const elements = document.querySelectorAll('[data-en]');
  elements.forEach(el => {
    const text = (lang === 'hi') ? el.dataset.hi : el.dataset.en;
    if (text) {
      if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
        el.placeholder = text;
      } else {
        el.innerText = text;
      }
    }
  });

  if (notify) {
    showToast(lang === 'hi' ? 'भाषा बदलकर हिंदी कर दी गई है' : 'Language switched to English', 'success');
  }
}

/* --------------------------------------------------------------------------
   Mobile Drawer Navigation
   -------------------------------------------------------------------------- */
function initMobileDrawer() {
  const drawerBtn = document.getElementById('sk-drawer-btn');
  const drawer = document.getElementById('sk-mobile-drawer');
  const overlay = document.getElementById('sk-drawer-overlay');
  const closeBtn = document.getElementById('sk-drawer-close');

  if (!drawerBtn || !drawer) return;

  function openDrawer() {
    drawer.classList.remove('translate-x-full');
    overlay.classList.remove('hidden');
    document.body.style.overflow = 'hidden';
  }

  function closeDrawer() {
    drawer.classList.add('translate-x-full');
    overlay.classList.add('hidden');
    document.body.style.overflow = '';
  }

  drawerBtn.addEventListener('click', openDrawer);
  if (closeBtn) closeBtn.addEventListener('click', closeDrawer);
  if (overlay) overlay.addEventListener('click', closeDrawer);
}

/* --------------------------------------------------------------------------
   Voice Search Modal & Audio Recorder
   -------------------------------------------------------------------------- */
function initVoiceSearch() {
  const micBtn = document.getElementById('voice-search-btn');
  const modal = document.getElementById('sk-voice-modal');
  const closeVoiceBtn = document.getElementById('sk-close-voice-modal');
  const voiceStatusText = document.getElementById('sk-voice-status');
  const searchInput = document.getElementById('search-input');
  const searchForm = document.getElementById('search-form');

  if (!micBtn || !modal) return;

  let mediaRecorder;
  let audioChunks = [];
  let isRecording = false;

  function openVoiceModal() {
    modal.classList.remove('hidden');
    modal.classList.add('flex');
    startRecording();
  }

  function closeVoiceModal() {
    modal.classList.add('hidden');
    modal.classList.remove('flex');
    if (isRecording && mediaRecorder) {
      mediaRecorder.stop();
    }
  }

  micBtn.addEventListener('click', openVoiceModal);
  if (closeVoiceBtn) closeVoiceBtn.addEventListener('click', closeVoiceModal);

  async function startRecording() {
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
      voiceStatusText.innerText = 'Voice search is not supported in this browser.';
      showToast('Voice search not supported', 'error');
      return;
    }

    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorder = new MediaRecorder(stream);
      audioChunks = [];

      mediaRecorder.onstart = () => {
        isRecording = true;
        const currentLang = localStorage.getItem('sk_lang') || 'en';
        voiceStatusText.innerText = (currentLang === 'hi') ? 'सुन रहे हैं... बोलिए! (Listening...)' : 'Listening... Speak now!';
      };

      mediaRecorder.ondataavailable = (e) => {
        audioChunks.push(e.data);
      };

      mediaRecorder.onstop = async () => {
        isRecording = false;
        voiceStatusText.innerText = 'Processing your voice query...';

        const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
        const formData = new FormData();
        formData.append('audio_data', audioBlob);

        try {
          const res = await fetch('/transcribe', {
            method: 'POST',
            body: formData
          });

          if (!res.ok) throw new Error('Transcription error');

          const data = await res.json();
          if (data.transcript) {
            if (searchInput) searchInput.value = data.transcript;
            closeVoiceModal();
            showToast(`Voice query: "${data.transcript}"`, 'success');
            if (searchForm) searchForm.submit();
          } else {
            voiceStatusText.innerText = data.error || 'Could not understand audio. Try again.';
          }
        } catch (err) {
          console.error(err);
          voiceStatusText.innerText = 'Could not process audio. Please try again.';
        }
      };

      mediaRecorder.start();

      // Auto stop recording after 6 seconds if active
      setTimeout(() => {
        if (isRecording && mediaRecorder.state === 'recording') {
          mediaRecorder.stop();
        }
      }, 6000);

    } catch (err) {
      console.error(err);
      voiceStatusText.innerText = 'Microphone permission denied.';
      showToast('Microphone access denied', 'error');
    }
  }
}

/* --------------------------------------------------------------------------
   Toast Notification Helper
   -------------------------------------------------------------------------- */
function showToast(message, type = 'info') {
  let toastContainer = document.getElementById('sk-toast-container');
  if (!toastContainer) {
    toastContainer = document.createElement('div');
    toastContainer.id = 'sk-toast-container';
    toastContainer.className = 'fixed bottom-5 right-5 z-50 flex flex-col gap-2 pointer-events-none';
    document.body.appendChild(toastContainer);
  }

  const toast = document.createElement('div');
  toast.className = 'sk-toast show pointer-events-auto bg-white dark:bg-slate-800 text-slate-900 dark:text-white shadow-xl rounded-xl border border-slate-200 dark:border-slate-700 px-4 py-3 flex items-center gap-3 text-sm font-medium';

  let iconSvg = '';
  if (type === 'success') {
    iconSvg = `<svg class="w-5 h-5 text-emerald-500 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg>`;
  } else if (type === 'error') {
    iconSvg = `<svg class="w-5 h-5 text-red-500 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>`;
  } else {
    iconSvg = `<svg class="w-5 h-5 text-amber-500 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>`;
  }

  toast.innerHTML = `${iconSvg}<span>${message}</span>`;
  toastContainer.appendChild(toast);

  setTimeout(() => {
    toast.classList.remove('show');
    setTimeout(() => toast.remove(), 300);
  }, 3500);
}
