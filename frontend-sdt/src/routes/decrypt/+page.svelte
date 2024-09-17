<script lang="ts">
    import { onMount } from "svelte";

    let decryptionKey: string = "";
    let messageId: string | null, iv: string | null, tag: string | null;
    let decryptedMessage = "";
    let decryptionError: boolean = false;

    // Replace with actual API URL of the backend
    // Consider using environment variables / svelte environment for automatically setting prod and dev URLs
    let apiURL = "http://localhost:5000";

    onMount(() => {
        // Get URL parameters
        const urlParams = new URLSearchParams(window.location.search);
        messageId = urlParams.get("id");
        iv = urlParams.get("iv");
        tag = urlParams.get("tag");
    });

    /**
     * Function to decrypt the message using the backend API
     * Sends a POST request to the /decrypt endpoint with the message ID, decryption key, IV, and tag
     * API returns the decrypted message or an error message if message doesn't exist or expired
     */
    async function decryptMessage() {
        const response = await fetch(`${apiURL}/decrypt/${messageId}`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ key: decryptionKey, iv, tag })
        });

        const data = await response.json();

        if (data.error) {
            decryptedMessage = "Error: " + data.error;
            decryptionError = true;
        } else {
            decryptedMessage = data.message;
        }
    }
</script>

<div class="main-content">
    <div class="decryption-field">
        <input bind:value={decryptionKey} placeholder="Enter decryption key" />
        <button on:click={decryptMessage}>Decrypt</button>
    </div>
    {#if decryptedMessage}
    <div class="result {decryptionError ? "error" : ""}">
        {#if !decryptionError}
            <p>Decrypted message:</p>
        {/if}
        <p class="message">{decryptedMessage}</p>
    </div>
    {/if}
</div>

<style lang="scss">
  .main-content {
    max-width: 600px;
    margin: 50px auto;
  }

  .decryption-field {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    margin-bottom: 20px;

    input {
      width: 100%;
      max-width: 90vw;
      height: 40px;
      margin-bottom: 10px;
      padding: 10px;
      box-sizing: border-box;
      border: 1px solid #ccc;
      border-radius: 5px;
    }

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

  .result {
    padding: 20px;
    border: 2px solid #007bff;
    border-radius: 5px;
    background-color: #f9f9f9;
    margin-top: 20px;

    &.error {
      border-color: #dc3545;
    }

    p {
      margin-bottom: 15px;
      font-size: 1rem;
    }

    .message {
      font-size: 1.2rem;
      word-break: break-all;
      border: 1px solid #ccc;
      padding: 10px;
      border-radius: 5px;
      background-color: #e6e6e6;
    }
  }
</style>
