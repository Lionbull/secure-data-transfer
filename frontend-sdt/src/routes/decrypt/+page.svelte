<script lang="ts">
    import { onMount } from "svelte";

    let decryptionKey = "";
    let messageId: string | null, iv: string | null, tag: string | null;
    let decryptedMessage = "";

    onMount(() => {
        // Get URL parameters
        const urlParams = new URLSearchParams(window.location.search);
        messageId = urlParams.get("id");
        iv = urlParams.get("iv");
        tag = urlParams.get("tag");
    });

    async function decryptMessage() {
      const response = await fetch(`http://localhost:5000/decrypt/${messageId}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ key: decryptionKey, iv, tag })
      });

      const data = await response.json();
      decryptedMessage = data.message || "Error: Could not decrypt message";
    }
</script>

<input bind:value={decryptionKey} placeholder="Enter decryption key" />
<button on:click={decryptMessage}>Decrypt</button>

<p>{decryptedMessage}</p>
