const express = require('express');
const app = express();
const port = 3001; // Or any port you prefer

app.use(express.json());

app.get('/', (req, res) => {
  res.send('Backend is running!');
});

app.post('/api/login', (req, res) => {
  const { username, password } = req.body;
  // TODO: Implement actual authentication logic here
  if (username && password) {
    // For now, let's just simulate a successful login
    res.json({ success: true, message: 'Login successful (simulated)', token: 'fake-jwt-token' });
  } else {
    res.status(400).json({ success: false, message: 'Username and password are required' });
  }
});

app.listen(port, () => {
  console.log(\`Server listening at http://localhost:\${port}\`);
}); 
