# 🧪 TESTING GUIDE: Sidebar Toggle & Smart Chatbot

## ✅ System Status
- ✅ Django Configuration: Valid (no issues)
- ✅ All Required Packages: Installed (requests, beautifulsoup4)
- ✅ Backend API: Ready (/accounts/api/chatbot-search/)
- ✅ Frontend Components: Integrated on all 11+ pages
- ✅ Database: Connected

---

## 🚀 HOW TO START THE SERVER

```bash
# Navigate to project directory
cd c:\Users\AUDITORIUM\Pictures\comp_project

# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Run development server
python manage.py runserver
```

The server will start at: **http://127.0.0.1:8000**

---

## 📋 FEATURE 1: SIDEBAR TOGGLE (ENHANCED)

### What It Does:
- Click hamburger menu (☰) → Sidebar **shrinks to 70px** (icons only)
- Text labels like "Help & Support", "Dashboard", etc. **disappear**
- Click again → Sidebar **expands to 280px** (icons + text)
- **Repeats infinitely** on every click
- **State persists** - remembers your choice after refresh

### Test Steps:

#### Test 1.1: Basic Toggle on One Page
1. Log in to the system
2. Navigate to any page (e.g., "My Complaints")
3. Look at the sidebar on the left - you should see:
   ```
   🏠 Dashboard
   ➕ Submit Complaint
   📋 My Complaints
   ```
4. Click the hamburger menu ☰ in top-left corner
5. **Expected**: Sidebar shrinks - now you see **only icons**, text disappears
6. Click the ☰ button again
7. **Expected**: Sidebar expands - text labels reappear

#### Test 1.2: Toggle Across Multiple Pages
1. Start with sidebar expanded
2. Click ☰ to collapse it (icons only)
3. Click "My Complaints" from sidebar
4. **Expected**: Page loads with sidebar **still collapsed** (icons only)
5. Expand sidebar by clicking ☰ again
6. Click "Profile" from sidebar
7. **Expected**: Sidebar **remains expanded** as you navigate

#### Test 1.3: State Persistence
1. Collapse the sidebar (click ☰)
2. Navigate to different pages
3. **Close and reopen the browser** (or refresh page)
4. **Expected**: Sidebar is **still collapsed** (remembers your choice)
5. Expand sidebar
6. Refresh browser again
7. **Expected**: Sidebar is **still expanded**

#### Test 1.4: Pages to Test Toggle On
Test the toggle works on **all these pages**:

| Page | URL/Location |
|------|--------------|
| Student Dashboard | Dashboard (Students) |
| Staff Dashboard | Dashboard (Staff) |
| Admin Dashboard | Dashboard (Admin) |
| Submit Complaint | Sidebar → Submit Complaint |
| My Complaints | Sidebar → My Complaints |
| Complaint Stats | Sidebar → (if available) |
| Assign Complaints | Sidebar → (if available) |
| Complaint Detail | Click on any complaint |
| User Profile | Sidebar → Account → Profile |
| Settings | Sidebar → Account → Settings |
| Help & Support | Sidebar → Account → Help & Support |

---

## 💬 FEATURE 2: SMART CHATBOT WITH GOOGLE SEARCH

### What It Does:
The chatbot in Help & Support now has **two levels of intelligence**:
1. **FAQ Database** - Quick answers for complaint system questions
2. **Google Search** - Searches the web (including UDOM) for any question

### Test Steps:

#### Test 2.1: FAQ Questions (Built-in Answers)
Navigate to **Help & Support** page:

1. **Question**: "How do I submit a complaint?"
   - **Expected**: Bot responds with FAQ answer about complaint submission
   - **Indicator**: Message starts with ✓ (checkmark)

2. **Question**: "How long does resolution take?"
   - **Expected**: Bot responds with FAQ answer about resolution timeline
   - **Indicator**: Message starts with ✓

3. **Question**: "Is my complaint confidential?"
   - **Expected**: Bot responds with FAQ answer about privacy
   - **Indicator**: Message starts with ✓

#### Test 2.2: UDOM-Related Questions (Google Search)
**These should trigger Google search with UDOM priority:**

1. **Question**: "How do I reset my SR2 password?"
   - **Expected**: Bot searches for UDOM SR2 password reset info
   - **Expected Output**: Step-by-step instructions or IT Support contact
   - **Indicator**: Message starts with 🔍 (Search Result)

2. **Question**: "How to register for courses UDOM?"
   - **Expected**: Bot finds course registration instructions from UDOM portal
   - **Indicator**: Message starts with 🔍

3. **Question**: "What are exam marks UDOM?"
   - **Expected**: Bot finds academic records information
   - **Indicator**: Message starts with 🔍

#### Test 2.3: General Knowledge Questions (Google Search)
**These should perform general web search:**

1. **Question**: "What is machine learning?"
   - **Expected**: Bot searches the web and provides a general answer
   - **Indicator**: Message starts with 🔍

2. **Question**: "How to fix computer performance?"
   - **Expected**: Bot searches and provides troubleshooting steps
   - **Indicator**: Message starts with 🔍

3. **Question**: "Best practices for web design?"
   - **Expected**: Bot searches and provides best practices
   - **Indicator**: Message starts with 🔍

#### Test 2.4: Chat History Persistence
1. Ask a question: "How do I submit a complaint?"
2. Type another question: "How long does resolution take?"
3. **Refresh the browser page** (F5 or Ctrl+R)
4. **Expected**: **Both questions and answers are still visible** in chat
5. Close and reopen the Help & Support page
6. **Expected**: Chat history is **still there** (persisted in browser)

#### Test 2.5: Message Flow Visualization
Each message should look like this:

```
User Message (right-aligned, blue background):
   "How do I submit a complaint?"

Bot Response (left-aligned, white background):
   ✓ To submit a complaint, navigate to the "Submit Complaint" section...
   [or]
   🔍 Search Result:
   Based on search results: [answer from Google]
   
   📚 Sources:
   1. Title of Source 1
   2. Title of Source 2
   3. Title of Source 3
```

#### Test 2.6: Error Handling
1. Type a very short question: "Hi"
2. **Expected**: Bot says "Please provide a longer search query"
3. Wait a few seconds to see typing indicator (three dots animation)
4. Bot should respond with answer

---

## 🔍 TECHNICAL VALIDATION

### Frontend Check (Browser Console)
To verify the toggle is working, open browser developer tools (F12):

```javascript
// In Console, run:
const sidebar = document.getElementById('sidebar');
console.log('Sidebar collapsed?', sidebar.classList.contains('collapsed'));
console.log('Sidebar width:', window.getComputedStyle(sidebar).width);
```

**Expected Output (Collapsed)**:
```
Sidebar collapsed? true
Sidebar width: 70px
```

**Expected Output (Expanded)**:
```
Sidebar collapsed? false
Sidebar width: 280px
```

### API Endpoint Test
To verify the chatbot API is working:

```bash
# Open terminal and run:
# Make sure server is running first

curl -X POST http://127.0.0.1:8000/accounts/api/chatbot-search/ \
  -H "Content-Type: application/json" \
  -d "{\"query\": \"How to reset password\"}"

# Should return JSON response with answer and sources
```

---

## ⚙️ CONFIGURATION DETAILS

### Sidebar CSS Properties
```css
/* Expanded (Default) */
.sidebar {
    width: 280px;
}

/* Collapsed */
.sidebar.collapsed {
    width: 70px;
}

/* Smooth Animation */
transition: width 0.4s ease;
```

### Backend API Configuration
```python
# Endpoint: /accounts/api/chatbot-search/
# Method: POST
# Authentication: Required (login_required)

Request JSON:
{
    "query": "user question here"
}

Response JSON:
{
    "success": true,
    "answer": "answer text",
    "sources": [
        {"title": "Source Title", "link": "https://..."},
        ...
    ]
}
```

### Chatbot Keywords for UDOM Search
The chatbot prioritizes UDOM search for:
- `password` / `reset`
- `sr2`
- `registration`
- `academic`
- `exam`

---

## 🐛 TROUBLESHOOTING

### Issue: Sidebar not toggling
- **Solution 1**: Refresh page (F5)
- **Solution 2**: Clear browser localStorage:
  - Open DevTools (F12) → Application → LocalStorage → Clear
  - Refresh page

### Issue: Toggle doesn't stay collapsed after refresh
- **Solution**: Check if localStorage is enabled in browser
  - Settings → Privacy → Allow sites to save and read cookie data

### Issue: Chatbot API error
- **Solution 1**: Ensure venv is activated: `.\.venv\Scripts\Activate.ps1`
- **Solution 2**: Check packages installed: `pip list` (should show requests, beautifulsoup4)
- **Solution 3**: Check server logs for errors

### Issue: Google search results not appearing
- **Solution 1**: Check internet connection
- **Solution 2**: Try a different search query
- **Solution 3**: Check Django server logs for API errors

---

## ✅ SIGN-OFF CHECKLIST

When testing, verify these items:

- [ ] Sidebar toggle works on all 11+ pages
- [ ] Toggle collapses to icons only (no text)
- [ ] Toggle expands to show text again
- [ ] Toggle repeats infinitely
- [ ] Sidebar state persists after page refresh
- [ ] Sidebar state persists after browser close/reopen
- [ ] Navigation works while sidebar is collapsed
- [ ] Navigation works while sidebar is expanded
- [ ] FAQ questions show ✓ indicator
- [ ] Google search questions show 🔍 indicator
- [ ] Chat history persists after page refresh
- [ ] Chat history shows correct source citations
- [ ] UDOM questions prioritize UDOM results
- [ ] General questions perform web search
- [ ] All pages maintain consistent styling
- [ ] No console errors (F12 → Console tab)

---

## 📞 SUPPORT

If you encounter any issues:
1. Check this testing guide
2. Look at browser console (F12) for error messages
3. Check Django server terminal for errors
4. Verify virtual environment is activated
5. Verify required packages are installed

**Happy Testing! 🎉**
