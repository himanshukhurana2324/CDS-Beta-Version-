const chatbotToggler = document.querySelector(".chatbot-toggler");
const closeBtn = document.querySelector(".close-btn");
const chatbox = document.querySelector(".chatbox");
const chatInput = document.querySelector(".chat-input textarea");
const sendChatBtn = document.querySelector(".chat-input span");

let userMessage = null; // Variable to store user's message
const API_KEY = "PASTE-YOUR-API-KEY"; // Paste your API key here
const inputInitHeight = chatInput.scrollHeight;

const createChatLi = (message, className) => {
  // Create a chat <li> element with passed message and className
  const chatLi = document.createElement("li");
  chatLi.classList.add("chat", `${className}`);
  let chatContent =
    className === "outgoing"
      ? `<p></p>`
      : `<span class="material-symbols-outlined">smart_toy</span><p></p>`;
  chatLi.innerHTML = chatContent;
  chatLi.querySelector("p").textContent = message;
  return chatLi; // return chat <li> element
};

const generateResponse = async (message, chatElement) => {
  try {
    // Fetch your API_KEY
    const API_KEY = "AIzaSyBAxmvFXyWMxAehZ5GL-q4HlsxN6gqAwV0";

    // Access your API key
    const genAI = new GoogleGenerativeAI(API_KEY);

    // For text-only input, use the gemini-pro model
    const model = genAI.getGenerativeModel({ model: "gemini-pro" });

    // Generate content based on the message
    const result = await model.generateContent(message);
    const response = await result.response;
    const text = await response.text();

    // Update the chat element with the response data
    const messageElement = chatElement.querySelector("p");
    messageElement.textContent = text.trim();
  } catch (error) {
    // Handle errors
    const messageElement = chatElement.querySelector("p");
    // Add an error class to the chat element
    messageElement.classList.add("error");
    // Display an error message
    messageElement.textContent =
      "Oops! Something went wrong. Please try again.";
    // Log the error to the console for debugging
    console.error("Error fetching data:", error);
  } finally {
    // Scroll to the bottom of the chatbox
    chatbox.scrollTo(0, chatbox.scrollHeight);
  }
};

const handleChat = () => {
  userMessage = chatInput.value.trim(); // Get user entered message and remove extra whitespace
  if (!userMessage) return;

  // Clear the input textarea and set its height to default
  chatInput.value = "";
  chatInput.style.height = `${inputInitHeight}px`;

  // Append the user's message to the chatbox
  chatbox.appendChild(createChatLi(userMessage, "outgoing"));
  chatbox.scrollTo(0, chatbox.scrollHeight);

  setTimeout(() => {
    // Display "Thinking..." message while waiting for the response
    const incomingChatLi = createChatLi("Thinking...", "incoming");
    chatbox.appendChild(incomingChatLi);
    chatbox.scrollTo(0, chatbox.scrollHeight);
    generateResponse(userMessage, incomingChatLi);
  }, 600);
};

chatInput.addEventListener("input", () => {
  // Adjust the height of the input textarea based on its content
  chatInput.style.height = `${inputInitHeight}px`;
  chatInput.style.height = `${chatInput.scrollHeight}px`;
});

chatInput.addEventListener("keydown", (e) => {
  // If Enter key is pressed without Shift key and the window
  // width is greater than 800px, handle the chat
  if (e.key === "Enter" && !e.shiftKey && window.innerWidth > 800) {
    e.preventDefault();
    handleChat();
  }
});

sendChatBtn.addEventListener("click", handleChat);
closeBtn.addEventListener("click", () =>
  document.body.classList.remove("show-chatbot")
);
chatbotToggler.addEventListener("click", () =>
  document.body.classList.toggle("show-chatbot")
);
