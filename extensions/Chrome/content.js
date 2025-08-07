(function () {
  "use strict";

  const platformName = getPlatformName();
  console.log(`Multi-AI Chat Manager Assistant loaded for: ${platformName}`);

  function getPlatformName() {
    const hostname = window.location.hostname;
    if (hostname.includes("chatgpt") || hostname.includes("openai"))
      return "ChatGPT";
    if (hostname.includes("claude")) return "Claude";
    if (hostname.includes("gemini") || hostname.includes("bard"))
      return "Gemini";
    if (hostname.includes("perplexity")) return "Perplexity";
    if (hostname.includes("grok") || hostname.includes("x.com")) return "Grok";
    if (hostname.includes("deepseek")) return "DeepSeek";
    if (hostname.includes("copilot") || hostname.includes("microsoft"))
      return "Copilot";
    return "Unknown";
  }

  function findInput() {
    // Platform-specific selectors for better targeting
    const selectors = [
      // ChatGPT
      "#prompt-textarea",
      'textarea[data-id="root"]',
      'textarea[placeholder*="Message"]',

      // Claude
      'div[contenteditable="true"][data-testid="composer-input"]',
      'div[contenteditable="true"]',
      'textarea[placeholder*="Talk to Claude"]',

      // Gemini/Bard
      'textarea[placeholder*="Enter a prompt"]',
      'textarea[aria-label*="Enter a prompt"]',
      'div[contenteditable="true"][aria-label*="Message"]',

      // Perplexity
      'textarea[placeholder*="Ask anything"]',
      'textarea[placeholder*="Follow up"]',
      'div[contenteditable="true"][data-testid="search-input"]',

      // Grok
      'textarea[placeholder*="Ask Grok"]',
      'div[contenteditable="true"][data-testid="tweetTextarea"]',

      // DeepSeek
      'textarea[placeholder*="Send a message"]',
      'div[contenteditable="true"][placeholder*="Type a message"]',

      // Microsoft Copilot
      'textarea[placeholder*="Ask me anything"]',
      'div[contenteditable="true"][role="textbox"]',

      // Generic fallbacks
      'textarea[placeholder*="message" i]',
      'textarea[placeholder*="chat" i]',
      'textarea[placeholder*="ask" i]',
      'textarea[placeholder*="prompt" i]',
      'div[contenteditable="true"]:not([aria-hidden="true"])',
      'textarea:not([aria-hidden="true"])',
      "textarea",
    ];

    for (let selector of selectors) {
      const elements = document.querySelectorAll(selector);
      for (let element of elements) {
        // Check if element is visible and interactable
        if (
          element &&
          element.offsetParent !== null &&
          !element.disabled &&
          !element.readOnly &&
          element.style.display !== "none" &&
          element.style.visibility !== "hidden"
        ) {
          return element;
        }
      }
    }
    return null;
  }

  function focusInput() {
    const input = findInput();
    if (input) {
      console.log(`Focusing input for ${platformName}:`, input);
      input.focus();

      // For contenteditable elements, set cursor to end
      if (input.contentEditable === "true") {
        const range = document.createRange();
        const sel = window.getSelection();

        // Handle empty contenteditable
        if (input.childNodes.length === 0) {
          input.appendChild(document.createTextNode(""));
        }

        range.selectNodeContents(input);
        range.collapse(false);
        sel.removeAllRanges();
        sel.addRange(range);
      } else if (input.tagName === "TEXTAREA") {
        // For textarea, set cursor to end
        input.setSelectionRange(input.value.length, input.value.length);
      }

      return true;
    } else {
      console.log(`No input found for ${platformName}`);
    }
    return false;
  }

  function isInInputField() {
    const activeEl = document.activeElement;
    if (!activeEl) return false;

    return (
      activeEl.tagName === "INPUT" ||
      activeEl.tagName === "TEXTAREA" ||
      activeEl.contentEditable === "true" ||
      activeEl.getAttribute("role") === "textbox"
    );
  }

  function handleKeyDown(e) {
    // Check for Ctrl+V or Cmd+V
    if ((e.ctrlKey || e.metaKey) && e.key === "v") {
      // Skip if already in an input field
      if (isInInputField()) {
        return;
      }

      // Try to focus the input
      focusInput();
    }
  }

  // Add event listener
  document.addEventListener("keydown", handleKeyDown, true);

  // For SPAs, re-initialize on navigation
  let lastUrl = location.href;
  const observer = new MutationObserver(() => {
    const currentUrl = location.href;
    if (currentUrl !== lastUrl) {
      lastUrl = currentUrl;
      console.log(`Navigation detected for ${platformName}, reinitializing...`);
      // Small delay to let the new page load
      setTimeout(() => {
        const input = findInput();
        if (input) {
          console.log(`Input re-detected after navigation:`, input);
        }
      }, 1000);
    }
  });

  observer.observe(document, {
    subtree: true,
    childList: true,
  });

  // Debug: Log available inputs after page load
  setTimeout(() => {
    console.log(
      `${platformName} - Available textareas:`,
      document.querySelectorAll("textarea")
    );
    console.log(
      `${platformName} - Available contenteditable:`,
      document.querySelectorAll('[contenteditable="true"]')
    );
    const foundInput = findInput();
    if (foundInput) {
      console.log(`${platformName} - Successfully found input:`, foundInput);
    } else {
      console.log(`${platformName} - No input found during initialization`);
    }
  }, 2000);
})();
