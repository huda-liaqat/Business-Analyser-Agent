# Workflow Guide: How Database Storage Works

## 🎯 Simple Answer

**YES!** When you run the project, **analysis is automatically saved to the database**. You don't need to run any extra commands.

---

## 📋 Complete Workflow

### Step 1: Run the Project

```bash
streamlit run app.py
```

### Step 2: Run an Analysis

1. Enter a ticker (e.g., `AAPL`)
2. Choose analysis type (Full or Quick)
3. Click **"🚀 Start Analysis"**

### Step 3: Automatic Storage ✨

**Everything happens automatically:**
- ✅ Query is created in database
- ✅ Agent actions are logged
- ✅ Report is validated with Pydantic
- ✅ Report is saved to database
- ✅ Metadata is saved (scores, summaries)
- ✅ You see a success message: "💾 Report saved to database!"

**No extra steps needed!**

---

## 📊 Viewing Stored Data

### Option 1: In Streamlit App (Easiest) ⭐

1. Open the sidebar
2. Expand **"📊 View Stored Reports"**
3. See all your saved reports!

**Features:**
- View recent analyses
- See report previews
- Check completeness & confidence scores
- View full reports

### Option 2: Command Line (Optional)

```bash
# View all data
python view_database.py

# View specific ticker
python view_database.py --ticker AAPL

# Interactive menu
python view_database.py --interactive
```

### Option 3: SQLite Browser (Optional)

1. Download DB Browser for SQLite: https://sqlitebrowser.org/
2. Open `business_analyst.db`
3. Browse tables and data

---

## 🔄 What Gets Stored Automatically

When you run an analysis, these are saved:

| Data | Where | When |
|------|-------|------|
| **User Query** | `user_queries` table | At start |
| **Agent Actions** | `agent_logs` table | During execution |
| **Report** | `reports` table | After generation |
| **Metadata** | `analysis_metadata` table | After validation |

---

## 💡 Example Workflow

```
1. You: Run "streamlit run app.py"
2. You: Enter "AAPL" and click "Start Analysis"
3. System: Creates query in database (ID: 1)
4. System: Logs agent actions
5. System: Generates report
6. System: Validates report (Pydantic)
7. System: Saves report to database
8. System: Saves metadata (scores, summary)
9. You: See "💾 Report saved to database!"
10. You: Expand "📊 View Stored Reports" in sidebar
11. You: See your saved report!
```

---

## ❓ FAQ

### Q: Do I need to run commands after analysis?
**A:** No! Everything is automatic. Commands are only for viewing data.

### Q: Where is the database file?
**A:** `business_analyst.db` in your project root (created automatically).

### Q: Can I disable database storage?
**A:** Yes, but it's enabled by default. The crew uses `enable_db=True` by default.

### Q: What if database fails?
**A:** The analysis still works! Database errors are caught and logged, but don't block the analysis.

### Q: How do I see old reports?
**A:** Use the sidebar "View Stored Reports" expander, or run `python view_database.py`.

---

## 🎯 Quick Reference

| Action | Command/Location |
|--------|------------------|
| **Run project** | `streamlit run app.py` |
| **View in app** | Sidebar → "📊 View Stored Reports" |
| **View in terminal** | `python view_database.py` |
| **Database file** | `business_analyst.db` (auto-created) |

---

## ✅ Summary

1. **Run analysis** → Automatically saved ✅
2. **View in app** → Sidebar expander ✅
3. **View in terminal** → Optional command ✅

**No extra steps needed!** Just run the app and analyze. Everything is stored automatically! 🚀

