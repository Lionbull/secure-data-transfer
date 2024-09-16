<script lang="ts">
    let decryptionKey = "";
    let iv = "";
    let tag = "";
    let messageId = 0;
    let decryptedMessage = "";
    let errorMessage = "";

    async function decryptMessage() {
        try {
            const response = await fetch(`http://localhost:5000/decrypt/${messageId}`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ key: decryptionKey, iv, tag })
            });
            
            const data = await response.json();
            if (response.ok) {
                decryptedMessage = data.message || "Error: Could not decrypt message";
            } else {
                errorMessage = data.error || "An error occurred";
            }
        } catch (error) {
            errorMessage = "An error occurred while decrypting.";
        }
    }
</script>

<input bind:value={decryptionKey} placeholder="Decryption key" />
<input bind:value={iv} placeholder="IV" />
<input bind:value={tag} placeholder="Tag" />
<input bind:value={messageId} placeholder="Message ID" />

<button on:click={decryptMessage}>Decrypt</button>

<p>{decryptedMessage}</p>
<p>{errorMessage}</p>
