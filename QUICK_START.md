# ⚡ QUICK START GUIDE

## 🚀 Start Server (30 seconds)

```bash
# Terminal 1: Run Server
cd c:\Users\AUDITORIUM\Pictures\comp_project
.\.venv\Scripts\Activate.ps1
python manage.py runserver

# Console will show:
# Starting development server at http://127.0.0.1:8000/
```

## 🌐 Access Application

Open browser: **http://127.0.0.1:8000/accounts/login/**

**Demo Credentials** (if available in database):
- Username: `student1`
- Password: (check your database or create a test user)

## ✨ Test Sidebar Toggle (30 seconds)

1. Log in successfully
2. Look at top-left corner → See menu button **☰**
3. Click **☰** → Sidebar shrinks (icons only)
4. Click **☰** → Sidebar expands (full text returns)
5. Repeat infinitely ✓

**Expected Sidebar States**:

**Expanded** (Natural)
```
🏠 Dashboard
➕ Submit Complaint  
📋 My Complaints
👤 Profile
⚙️ Settings
❓ Help & Support
```

**Collapsed** (After clicking ☰)
```
🏠
➕
📋
👤
⚙️
❓
```

## 💬 Test Chatbot (1 minute)

1. Click **Help & Support** in sidebar
2. Scroll right to see **AI Assistant** chatbot
3. Ask question 1: **"How do I submit a complaint?"**
   - Expected: Instant answer with ✓ emoji
4. Ask question 2: **"How do I reset my SR2 password?"**
   - Expected: Answer with 🔍 emoji (from Google search)
5. Ask question 3: **"What is artificial intelligence?"**
   - Expected: Web search results with sources

## 📱 Pages to Test Toggle On

All of these should have working toggle:

- ✓ Dashboard (Student/Staff/Admin)
- ✓ Submit Complaint  
- ✓ My Complaints
- ✓ Complaint Detail
- ✓ Complaint Stats
- ✓ Assign Complaints
- ✓ User Profile
- ✓ Settings
- ✓ Help & Support

## 🧪 Validation Checklist

Quick checks (2 minutes):

- [ ] Server starts without errors
- [ ] Can log in successfully
- [ ] Sidebar toggle works (☰ button shrinks/expands)
- [ ] Toggle persists after page refresh
- [ ] Can navigate pages (sidebar stays visible)
- [ ] Chatbot responds to FAQ questions (✓)
- [ ] Chatbot searches Google (🔍)
- [ ] Chat history saved after refresh
- [ ] No console errors (F12 → Console)

## 🔧 Troubleshooting (Quick Fixes)

| Problem | Solution |
|---------|----------|
| Server crashes | Restart: `python manage.py runserver` |
| Sidebar doesn't toggle | Refresh page (F5) or clear cache (Ctrl+Shift+Del) |
| Chatbot doesn't respond | Check internet, restart server |
| Page styles broken | Clear browser cache (Ctrl+Shift+Del) |
| 404 Error on /accounts/ | Make sure you're logged in first |

## 📞 Emergency Restart

If something breaks:

```bash
# Kill existing server
# (Close terminal or press Ctrl+C)

# Start fresh
cd c:\Users\AUDITORIUM\Pictures\comp_project
.\.venv\Scripts\Activate.ps1
python manage.py check
python manage.py runserver
```

## 📚 Detailed Resources

For comprehensive testing:
- **TESTING_GUIDE.md** - 14 detailed test cases
- **IMPLEMENTATION_SUMMARY.md** - Technical details
- **TESTING_GUIDE.md** - Troubleshooting section

## ✅ Status

- ✅ Sidebar Toggle: **READY**
- ✅ Chatbot Search: **READY**
- ✅ All Features: **TESTED & WORKING**
- ✅ Server: **RUNNING**

---

**Ready to test? Go to http://127.0.0.1:8000/accounts/login/ 🚀**
