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

  if (!userInput) {
    return res.status(400).send("❌ Missing 'msg' parameter in the request.");
  }

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

    const output = result.response.text;  // Corrected if necessary for your actual output structure
    console.log("✅ Gemini output:", output);
    res.json({ text: output });  // Ensure response is returned in JSON format
  } catch (err) {
    console.error("❌ Gemini error:", err.message || err);
    res.status(500).send("An error occurred while generating the response.");
  } finally {
    // Ensure the file is deleted after processing, regardless of success or failure
    if (file) {
      try {
        fs.unlinkSync(file.path);
      } catch (deleteError) {
        console.error("❌ Error deleting file:", deleteError.message);
      }
    }
  }
});

// Start server
app.listen(PORT, () => {
  console.log(`✅ Server running at http://localhost:${PORT}`);
});
