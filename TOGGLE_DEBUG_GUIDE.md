# Sidebar Toggle - Debug & Testing Guide

## Quick Testing (5 seconds)

1. **Go to any dashboard** (admin, staff, or student)
2. **Click the ☰ (hamburger) button** in the top-left header
3. **Observe:**
   - Sidebar should shrink from 280px to 70px width
   - Main content should shift right smoothly
   - Navigation text should fade out

## Detailed Verification Steps

### Step 1: Visual Inspection
```
✓ Sidebar collapses when clicking ☰
✓ Main content area expands smoothly
✓ Text in sidebar is hidden when collapsed
✓ Icons remain visible in collapsed state
✓ Smooth animation (not instant)
```

### Step 2: Console Debug (Press F12)
Open Developer Tools → Console tab and look for these messages:

**On Page Load:**
```
[SIDEBAR INIT] Starting initialization
[SIDEBAR INIT] Saved state: false (or true)
[SIDEBAR INIT] Applied expanded state: margin-left=280px (or collapsed state: margin-left=70px)
```

**After Clicking ☰:**
```
Sidebar toggled. Collapsed: true (or false)
Sidebar classes: collapsed (or empty)
Main-Content marginLeft: 70px (or 280px)
```

### Step 3: State Persistence
1. Open dashboard
2. Click ☰ to collapse sidebar
3. Refresh page (F5)
4. **Result:** Sidebar should still be collapsed

### Step 4: Keyboard Shortcut (Developer Mode)
While on any dashboard:
- Press **Ctrl + Shift + T** to toggle sidebar
- Check console for debug message:
  ```
  [DEBUG] Manual toggle triggered via Ctrl+Shift+T
  ```

## Common Issues & Solutions

### Issue: Toggle button doesn't work
**Solution:**
1. Open Console (F12)
2. Type: `toggleSidebar()` and press Enter
3. If nothing happens, check:
   - Is `/static/dashboard.js` loaded? (Network tab)
   - Are there JavaScript errors? (Console tab shows red errors)

### Issue: Sidebar doesn't shrink
**Solution:**
1. Check Console for errors
2. Verify sidebar element exists:
   - Type in Console: `document.getElementById('sidebar')` 
   - Should return the sidebar element (not null)
3. Check CSS is loaded:
   - Type in Console: `window.getComputedStyle(document.getElementById('sidebar')).width`
   - Should return "280px" initially

### Issue: Content doesn't shift
**Solution:**
1. Check main-content element exists:
   - Type in Console: `document.querySelector('.main-content')`
   - Should return the element
2. Check initial margin:
   - Type in Console: `window.getComputedStyle(document.querySelector('.main-content')).marginLeft`
   - Should return "280px"

### Issue: State doesn't persist on reload
**Solution:**
1. Check localStorage is working:
   - Type in Console: `localStorage.getItem('sidebarCollapsed')`
   - Should return "true" or "false" (or null if never set)
2. Clear and retry:
   - `localStorage.clear()` then refresh

## Console Commands for Testing

```javascript
// Check if elements exist
document.getElementById('sidebar')
document.querySelector('.main-content')

// Check current computed styles
window.getComputedStyle(document.getElementById('sidebar')).width
window.getComputedStyle(document.querySelector('.main-content')).marginLeft

// Check localStorage state
localStorage.getItem('sidebarCollapsed')

// Manually trigger toggle
toggleSidebar()

// Check if function exists
typeof toggleSidebar === 'function'

// View all sidebar classes
document.getElementById('sidebar').className

// View body classes
document.body.className

// Check transition property
window.getComputedStyle(document.getElementById('sidebar')).transition
window.getComputedStyle(document.querySelector('.main-content')).transition
```

## Testing Checklist

### Windows/Mac
- [ ] Click hamburger → sidebar collapses
- [ ] Click again → sidebar expands
- [ ] Refresh page → state persists
- [ ] Check console logs appear
- [ ] Test on Chrome/Firefox/Edge

### Mobile (if responsive)
- [ ] Test touch on hamburger button
- [ ] Verify sidebar collapse works on small screen
- [ ] Check content is readable when collapsed

## Files Involved (If You Need to Edit)

- `/templates/base_dashboard.html` - HTML structure + inline init script
- `/static/dashboard.js` - JavaScript toggle & restoration logic
- `/static/dashboard.css` - Animations & transitions

## Key Changes Made

1. **JavaScript now directly sets margin-left** instead of relying on CSS selectors
2. **Inline IIFE runs immediately** when page loads to prevent visual jump
3. **localStorage persists state** across page reloads
4. **Smooth CSS transitions** animate both sidebar width and content margin

---

**If toggle STILL doesn't work:**
1. ✓ Check all console messages (F12 → Console)
2. ✓ Try keyboard shortcut (Ctrl+Shift+T)
3. ✓ Try manual console command: `toggleSidebar()`
4. ✓ Check browser cache (Ctrl+Shift+Delete → clear cache)
5. ✓ Try different browser/incognito window
6. ✓ Share console errors for further debugging
