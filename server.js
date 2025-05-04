// Load environment variables
require('dotenv').config();

// Imports
const express = require('express');
const path = require('path');
const multer = require('multer');
const fs = require('fs');
const { GoogleGenerativeAI } = require('@google/generative-ai');

// Check if API key is valid
if (!process.env.GEMINI_API_KEY) {
  console.error("❌ Missing GEMINI_API_KEY in .env");
  process.exit(1);
}

// Init
const app = express();
const PORT = process.env.PORT || 3000;
const upload = multer({ dest: 'uploads/' });
const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);

// Middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, 'public')));

// Routes
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.post('/get', upload.single('file'), async (req, res) => {
  const userInput = req.body.msg;
  const file = req.file;

  try {
    const model = genAI.getGenerativeModel({ model: 'gemini-1.5-flash' });
    const prompt = [userInput];

    if (file) {
      const fileData = fs.readFileSync(file.path);
      const image = {
        inlineData: {
          data: fileData.toString('base64'),
          mimeType: file.mimetype,
        },
      };
      prompt.push(image);
    }

    console.log("🚀 Prompt:", prompt);
    const result = await model.generateContent(prompt);

    const output = result.response.text();
    console.log("✅ Gemini output:", output);
    res.send(output);
  } catch (err) {
    console.error("❌ Gemini error:", err.message || err);
    res.status(500).send("An error occurred while generating the response.");
  } finally {
    if (file) fs.unlinkSync(file.path);
  }
});

// Start server
app.listen(PORT, () => {
  console.log(`✅ Server running at http://localhost:${PORT}`);
});
