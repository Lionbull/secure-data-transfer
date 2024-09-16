<script lang="ts">
    let message = "";
    let expiration = 3600; // 1 hour
    let key, iv, tag, id;
  
    async function encryptMessage() {
      const response = await fetch("http://localhost:5000/encrypt", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message, expiration })
      });
  
      const data = await response.json();
      key = data.key;
      iv = data.iv;
      tag = data.tag;
      id = data.id;
  
      console.log("Encrypted! ID:", id, "Key:", key, "IV:", iv, "Tag:", tag);
    }
  </script>
  
  <textarea bind:value={message} placeholder="Enter message"></textarea>
  <select bind:value={expiration}>
    <option value="3600">1 Hour</option>
    <option value="86400">1 Day</option>
    <option value="604800">1 Week</option>
  </select>
  
  <button on:click={encryptMessage}>Encrypt</button>
  