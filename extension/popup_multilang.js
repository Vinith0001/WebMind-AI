document.getElementById('askBtn').addEventListener('click', async () => {
  const query = document.getElementById('userQuery').value.trim();
  const responseBox = document.getElementById('responseBox');
  const askBtn = document.getElementById('askBtn');
  const targetLanguage = document.getElementById('targetLanguage');

  if (!query) {
    responseBox.innerHTML = '<div class="error">Please enter your question first!</div>';
    return;
  }

  askBtn.disabled = true;
  askBtn.textContent = 'Analyzing...';
  responseBox.innerHTML = '<div class="loading"><div class="spinner"></div>Processing your request...</div>';

  try {
    const tabs = await chrome.tabs.query({ active: true, currentWindow: true });
    const currentTab = tabs[0];
    
    if (currentTab.url.startsWith('chrome://') || 
        currentTab.url.startsWith('chrome-extension://') ||
        currentTab.url.startsWith('edge://') ||
        currentTab.url.startsWith('about:')) {
      throw new Error('Cannot analyze browser internal pages. Please visit a regular website first.');
    }

    const results = await chrome.scripting.executeScript({
      target: { tabId: currentTab.id },
      function: () => {
        const content = document.body.innerText || document.documentElement.innerText || '';
        return content.substring(0, 5000);
      }
    });
    const content = results[0].result;
    
    if (!content || content.trim().length < 10) {
      throw new Error('No content found on this page to analyze.');
    }

    const response = await fetch('http://localhost:8000/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        text: content,
        query: query,
        target_language: targetLanguage.value
      })
    });

    if (!response.ok) {
      throw new Error(`Server error: ${response.status}`);
    }

    const data = await response.json();
    const answer = data.answer || data;
    responseBox.innerHTML = `<div class="success">${answer}</div>`;
    
    // Show language info
    const languageInfo = document.getElementById('languageInfo');
    if (languageInfo && data.detected_language && data.target_language) {
      const langNames = {
        'en': '🇺🇸 EN', 'es': '🇪🇸 ES', 'fr': '🇫🇷 FR', 'de': '🇩🇪 DE',
        'it': '🇮🇹 IT', 'pt': '🇵🇹 PT', 'ru': '🇷🇺 RU', 'ja': '🇯🇵 JA',
        'ko': '🇰🇷 KO', 'zh': '🇨🇳 ZH', 'ar': '🇸🇦 AR', 'hi': '🇮🇳 HI'
      };
      const detected = langNames[data.detected_language] || data.detected_language;
      const target = langNames[data.target_language] || data.target_language;
      languageInfo.textContent = `${detected} → ${target}`;
    }

  } catch (error) {
    responseBox.innerHTML = `
      <div class="error">
        <strong>❌ ${error.message}</strong><br><br>
        <small>💡 Ensure the backend server is running on localhost:8000</small>
      </div>
    `;
  } finally {
    askBtn.disabled = false;
    askBtn.textContent = '🔍 Analyze Content';
  }
});