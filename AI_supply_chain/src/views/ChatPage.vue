<template>
  <div class="chat-container">
    <div class="header">
        <div class="logo-section">
          <img src="/logo.png" alt="Logo" class="logo" />
        </div>
        <div class="welcome-section">
          <h2>Welcome, {{ username }} ({{ role }})</h2>
        </div>
    </div>


    <div class="chat-box">
      <div class="response-area">
  <div v-if="conversation.length === 0" class="default-text">
    🤖 I'm your AI Agent to assist with supply chain decisions.<br />
    Syngenta

We are a leading, science-based agriculture company, empowering farmers to meet the demands of modern agriculture. Using cutting-edge innovation, we help farmers to grow resilient, healthy crops that can feed a growing global population, while promoting sustainable farming practices that protect and enhance our planet. Headquartered in Switzerland, we are a global agritech leader with more than 30,000 employees across over 90 countries.
  </div>

  <div class="formatted-text" v-else>
    <div v-for="(msg, index) in conversation" :key="index">
      <b>{{ msg.sender }}:</b> <span v-html="formatText(msg.text)"></span>
    </div>
  </div>
</div>


      <div class="input-area">
        <textarea
          v-model="userQuestion"
          rows="2"
          placeholder="Type your question here..."
        ></textarea>
        <button @click="askQuery" :disabled="loading">
  <span v-if="loading">⏳</span>
  <span v-else>➤</span>
</button>
      </div>
    </div>
  </div>
</template>



<script>
export default {
  data() {
  return {
    username: localStorage.getItem('username') || 'Guest',
    role: localStorage.getItem('role') || 'Unknown',
    userQuestion: '',
    response: '',
    conversation: [],
    loading: false,
  };
  },
  computed: {
    formattedResponse() {
       if (!this.response) return ''; // Guard clause to prevent errors
      return this.response
        .replace(/\n/g, '<br>')                         // new lines
        .replace(/•/g, '• ')                            // bullet points
        .replace(/✓/g, '✅')                            // checkmark
        .replace(/(\d+\.)/g, '<b>$1</b>');   
    }
  },
  methods: {
    formatText(text) {
    return text
      .replace(/\n/g, '<br>')
      .replace(/•/g, '• ')
      .replace(/✓/g, '✅')
      .replace(/(\d+\.)/g, '<b>$1</b>');
  },
    async askQuery() {
      const user_question = this.userQuestion.trim();

      if (!this.userQuestion.trim()) {
        alert("Please enter a question.");
        return;
      }
      this.loading = true;
       // Add user's question to conversation
      this.conversation.push({
        sender: 'User',
        text: user_question
      });

     
       const payload = {
      question: user_question,
      history: this.conversation.map(msg => `${msg.sender}: ${msg.text}`).join('\n') // Optional: send entire convo
      };

      try {
        const response = await fetch("http://127.0.0.1:8000/ask", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify(payload)
        });

        const text = await response.json();

        // Double parse: First parse the stringified JSON, then access fields
        const parsed = JSON.parse(text);
        // OPTIONAL: show nicely formatted in <pre> or format specific fields
        this.conversation.push({
      sender: 'Assistant',
      text: parsed.answer
    });
        this.response = parsed.answer;
        this.userQuestion = '';
        console.log( this.conversation)

      } catch (error) {
        this.response = "Error: " + error.message;
      } finally {
    // Reset loading state
    this.loading = false;
  }
    }
  }
};
</script>

<style scoped>
.chat-container {

  margin: 30px auto;
  padding: 20px;
  background: #ffffff;
  box-shadow: 0 0 10px rgba(0,0,0,0.05);
  border-radius: 12px;
}


.chat-box {
  display: flex;
  flex-direction: column;
  height: 500px;
  border: 1px solid #e0e0e0;
  border-radius: 10px;
  overflow: hidden;
  background-color: #fff;
}

.response-area {
  flex: 1;
  padding: 15px;
  overflow-y: auto;
  background-color: #f5f7fa;
  border-bottom: 1px solid #ddd;
}

.input-area {
  display: flex;
  align-items: center;
  padding: 12px;
  border-top: 1px solid #e0e0e0;
  background-color: #ffffff;
  gap: 10px;
}

textarea {
  flex: 1;
  resize: none;
  padding: 10px 12px;
  font-size: 15px;
  border-radius: 8px;
  border: 1px solid #ccc;
  font-family: 'Segoe UI', sans-serif;
  height: 50px;
}

button {
  padding: 10px 16px;
  background-color: #007acc;
  color: white;
  font-weight: bold;
  font-size: 18px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s;
}

button:hover {
  background-color: #005ea3;
}

.formatted-text {
  font-family: 'Segoe UI', sans-serif;
  font-size: 16px;
  line-height: 1.6;
  color: #333;
  white-space: pre-wrap;
}
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.logo {
  height: 50px;
  width: auto;
}

h2 {
  font-size: 18px;
  text-align: right;
  font-style: italic;
  color: #333;
}
.default-text {
  text-align: center;
  font-size: 18px;
  color: #888;
  padding-top: 30px;
  font-style: italic;
}


</style>
