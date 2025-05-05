// === server.js ===
const express = require('express');
const fs = require('fs');
const cors = require('cors');
const app = express();
const PORT = 3000;

app.use(cors());
app.use(express.json());

const DB_FILE = './db.json';

// Load DB or initialize
let db = { users: {} };
if (fs.existsSync(DB_FILE)) {
  db = JSON.parse(fs.readFileSync(DB_FILE, 'utf-8'));
}

function saveDB() {
  fs.writeFileSync(DB_FILE, JSON.stringify(db, null, 2));
}

// Routes
app.post('/login', (req, res) => {
  const { username, referrer } = req.body;
  if (!db.users[username]) {
    db.users[username] = {
      earnings: 0,
      tasks: {},
      referrer: referrer || null,
      referrals: []
    };
    // Reward referrer
    if (referrer && db.users[referrer]) {
      db.users[referrer].earnings += 10;
      db.users[referrer].referrals.push(username);
    }
    saveDB();
  }
  res.json(db.users[username]);
});

app.get('/user/:username', (req, res) => {
  const user = db.users[req.params.username];
  if (!user) return res.status(404).json({ error: 'User not found' });
  res.json(user);
});

app.post('/task/complete', (req, res) => {
  const { username, taskId, amount } = req.body;
  const user = db.users[username];
  if (!user) return res.status(404).json({ error: 'User not found' });
  if (user.tasks[taskId]) return res.status(400).json({ error: 'Task already completed' });

  user.tasks[taskId] = true;
  user.earnings += amount;
  saveDB();
  res.json(user);
});

app.listen(PORT, () => console.log(`Server running on http://localhost:${PORT}`));
