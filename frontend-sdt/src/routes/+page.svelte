<script lang="ts">
  let message = "";
  let expiration = 3600; // 1 hour
  let expirationDate: Date | null;
  let key: any, url: any; 

  let showCopiedNotification: boolean = false;

  // Replace with actual API URL of the backend
  // Consider using environment variables / svelte environment for automatically setting prod and dev URLs
  let apiURL = "http://localhost:5000";

  /**
   * Function to encrypt the message using the backend API
   * Sends a POST request to the /encrypt endpoint with the message and expiration time
   * API returns the encryption key and URL to access the encrypted message via decrypt page
   */
  async function encryptMessage() {
    const response = await fetch(`${apiURL}/encrypt`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message, expiration })
    });

    const data = await response.json();

    expirationDate = new Date();
    expirationDate.setSeconds(expirationDate.getSeconds() + expiration);

    key = data.key;
    url = data.url;

    console.log("Encrypted!", "Key:", key, "URL:", url);
  }

  /**
   * Function to copy the text to the clipboard
   * Creates a temporary textarea element, sets the text to be copied, selects it, copies it to the clipboard, and removes the element
   * Shows a notification that the text has been copied
   * @param textToCopy - The text to be copied to the clipboard
   */
  function copyToClipboard(textToCopy: string) {
    const el = document.createElement("textarea");
    el.value = textToCopy;
    document.body.appendChild(el);
    el.select();
    navigator.clipboard.writeText(el.value);
    document.body.removeChild(el);

    showCopiedNotification = true;
    setTimeout(() => {
      showCopiedNotification = false;
    }, 2000);
  }
</script>

<div class="main-content">
  <div class="encryption-field">
    <textarea bind:value={message} placeholder="Enter message"></textarea>
    <div class="row">
      <select bind:value={expiration}>
        <!-- Add more expiration options if needed -->
        <option value={1 * 60}>1 Minute</option>
        <option value={30 * 60}>30 Minutes</option>
        <option value={60 * 60}>1 Hour</option>
        <option value={24 * 60 * 60}>1 Day</option>
        <option value={7 * 24 * 60 * 60}>1 Week</option>
        <option value={30 * 24 * 60 * 60}>1 Month</option>
      </select>
      <button on:click={encryptMessage}>Encrypt</button>
    </div>
  </div>
  {#if key}
    <div class="result">
      <div class="info">
        <p>The message has been encrypted and stored!</p>
        <p>It will expire at {expirationDate}</p>
        <p>Share the following URL and Key with the recipient:</p>
      </div>
      <div class="key-container">
        <p>Key</p>
        <!-- svelte-ignore a11y-click-events-have-key-events -->
        <!-- svelte-ignore a11y-no-static-element-interactions -->
        <div id="key" on:click={() => copyToClipboard(key)}>{key}</div>
      </div>
      <div class="url-container">
        <p>URL</p>
        <!-- svelte-ignore a11y-click-events-have-key-events -->
        <!-- svelte-ignore a11y-no-static-element-interactions -->
        <div id="url" on:click={() => copyToClipboard(url)}>{url}</div>
      </div>
    </div>
  {/if}

  {#if showCopiedNotification}
    <div class="toast">Copied to clipboard!</div>
  {/if}
</div>

<style lang="scss">

  .main-content {
    max-width: 600px;
    margin: 50px auto;
  }

  .encryption-field {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;

    button {
      padding: 10px 20px;
      background-color: #007bff;
      color: white;
      border: none;
      border-radius: 5px;
      cursor: pointer;

      &:hover {
        background-color: #0056b3;
      }
    }
  }

  textarea {
    width: 100%;
    max-width: 90vw;
    height: 100px;
    margin-bottom: 10px;
    box-sizing: border-box;
    padding: 10px;
  }
  .row {
    display: flex;
    justify-content: center;
    gap: 10px;
    margin-bottom: 10px;
  }
  select {
    width: 100px;
    padding: 5px;
  }

  .result {
    margin-top: 20px;
    padding: 20px;
    border: 2px solid #007bff;
    border-radius: 5px;
    background-color: #f9f9f9;

    .info {
      margin-bottom: 10px;
      p {
        margin-bottom: 15px;
        margin-top: 0;
      }
    }

    .key-container, .url-container {
      display: flex;
      flex-direction: column;
      p {
        font-size: 0.9rem;
        margin-bottom: 5px;
      }
      #key, #url {
        padding: 5px;
        font-size: 1rem;
        word-break: break-all;
        border: 1px solid #ccc;
        border-radius: 5px;
        box-sizing: border-box;
        cursor: pointer;

        &:hover {
          background-color: #e6e6e6;
        }
      }
    }
  }

  .toast {
    position: fixed;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%);
    background-color: #007bff;
    color: white;
    padding: 10px 20px;
    border-radius: 5px;
    box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.1);
    font-size: 1rem;
    z-index: 9999;
    animation: fadein 0.5s, fadeout 0.5s 1.5s;
  }

  /* Fade in and out animations */
  @keyframes fadein {
    from { opacity: 0; }
    to { opacity: 1; }
  }

  @keyframes fadeout {
    from { opacity: 1; }
    to { opacity: 0; }
  }
</style>
  