# RAG Chatbot Integration in Your Book

✅ **The chatbot is now integrated into your Docusaurus book!**

## 🚀 Quick Start

The `/chat` route is now available in your book at:
- **http://localhost:3000/chat** (when running locally)

## 📁 Files Added to Your Book Project

```
docusaurus-book/
├── src/
│   ├── components/
│   │   ├── RagChat.tsx              ← Chat component (moved here)
│   │   └── RagChat.module.css       ← Styles (moved here)
│   └── pages/
│       ├── chat.tsx                 ← /chat page (new)
│       └── chat.module.css          ← Page styles (new)
└── CHATBOT_INTEGRATION.md           ← This file
```

## 🔧 What You Need to Do

### 1. Make Sure Backend is Running

```bash
cd backend
pip install -r requirements.txt
uvicorn app:app --reload
```

**The backend must run on http://localhost:8000** (default)

### 2. Run Your Docusaurus Book

```bash
cd docusaurus-book
npm install  # if not already done
npm run start
```

### 3. Open the Chat

Visit: **http://localhost:3000/chat**

You should see the chatbot chat interface!

## ✅ What's Been Done

✅ `RagChat.tsx` component copied to `docusaurus-book/src/components/`
✅ `RagChat.module.css` styles copied to `docusaurus-book/src/components/`
✅ `/chat` page created at `docusaurus-book/src/pages/chat.tsx`
✅ Chat page styles at `docusaurus-book/src/pages/chat.module.css`

## 🎯 How to Use the Chatbot

1. **Open** http://localhost:3000/chat
2. **Type** a question about the book
3. **Click** "Ask →" or press Enter
4. **See** answers with source citations
5. **Select** text on any page to query just that section
6. **Click** "Query Selection ✓" to answer about selection

## 📝 To Add a Chat Link to Your Navigation

If you want a chat link in your Docusaurus navbar:

Edit `docusaurus-book/docusaurus.config.ts` and add to the navbar items:

```typescript
{
  type: 'doc',
  docId: 'intro',
  position: 'left',
  label: 'Docs',
},
{
  href: '/chat',
  label: 'Chat',
  position: 'left',
},  // Add this
```

Or in the navbar config:
```typescript
navbar: {
  items: [
    // ... existing items ...
    {
      href: '/chat',
      label: '💬 Chat with Book',
      position: 'right',
    },
  ],
},
```

## 🔗 API Endpoint

The chat component expects the backend API at:
- **Default:** `http://localhost:8000`
- **Custom:** Set `REACT_APP_API_ENDPOINT` environment variable

## 🐛 Troubleshooting

### Chat page shows but no response from queries

```bash
# Check if backend is running
curl http://localhost:8000/health

# Should return:
# {"status":"healthy","database":true,"vector_store":true,"embeddings":true}
```

### "Cannot GET /chat"

- Make sure you have the latest Docusaurus files
- Restart: `npm run start`
- Check that `docusaurus-book/src/pages/chat.tsx` exists

### Styling looks broken

- CSS Modules might not be loading
- Try: `npm install && npm run start`
- Clear Docusaurus cache: `rm -rf .docusaurus`

### Backend connection error

Check in browser console (F12):
- If you see CORS error: Make sure `CORS_ORIGINS` in `backend/.env` includes your frontend URL
- Default: `["http://localhost:3000", "http://localhost:3001"]`

## 📚 Next Steps

1. **Ingest your book documents** so the chatbot has content:
   ```bash
   python scripts/ingest_documents.py --path docusaurus-book/docs
   ```

2. **Test with sample documents first** (optional):
   ```bash
   python scripts/ingest_documents.py --sample
   ```

3. **Navigate to** http://localhost:3000/chat and start asking questions!

## 🎨 Customizing the Chat

You can customize the chatbot by editing:

- `docusaurus-book/src/pages/chat.tsx` - Page layout and instructions
- `docusaurus-book/src/components/RagChat.tsx` - Chat component behavior
- `docusaurus-book/src/components/RagChat.module.css` - Chat styles
- `docusaurus-book/src/pages/chat.module.css` - Page styles

## 🆘 Need Help?

All documentation is in the project root:

- `QUICK_START.txt` - 5-minute setup
- `README.md` - Project overview
- `RAG_SETUP_GUIDE.md` - Detailed guide
- `API_EXAMPLES.md` - API usage

---

**Status:** ✅ Chatbot integrated and ready to use!

Open http://localhost:3000/chat now! 🎉
