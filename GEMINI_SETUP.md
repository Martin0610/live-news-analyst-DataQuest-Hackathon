# 🆓 FREE Gemini API Setup

## Why Gemini?

**100% FREE for hackathons!**

- ✅ **Gemini API**: FREE (60 requests/min, 1500/day)
- ✅ **GNews API**: FREE (100 requests/day)
- ✅ **Total Cost**: $0/month 🎉

Compare to OpenAI: ~$5-10/month minimum

---

## Get Your FREE Gemini API Key (2 minutes)

### Step 1: Go to Google AI Studio
Visit: https://aistudio.google.com/app/apikey

### Step 2: Sign in with Google
Use any Google account (Gmail, etc.)

### Step 3: Create API Key
1. Click "Create API Key"
2. Select "Create API key in new project" (or use existing)
3. Copy your API key (starts with `AIza...`)

**That's it! No credit card required!** 🎉

---

## Get Your FREE GNews API Key (2 minutes)

### Step 1: Go to GNews
Visit: https://gnews.io/register

### Step 2: Sign Up
1. Enter email and password
2. Verify email
3. Login to dashboard

### Step 3: Copy API Key
Your API key is shown on the dashboard

**Free tier: 100 requests/day** (perfect for hackathons!)

---

## Add Keys to Your Project

### Option 1: Local Development

Create `.env` file:
```bash
copy .env.example .env  # Windows
cp .env.example .env    # Mac/Linux
```

Edit `.env`:
```env
GEMINI_API_KEY=AIza...your-key-here
GNEWS_API_KEY=...your-key-here
```

### Option 2: Render Deployment

In Render dashboard:
1. Go to your service → Environment
2. Add variables:
   - `GEMINI_API_KEY` = `AIza...`
   - `GNEWS_API_KEY` = `...`
3. Save changes

---

## Gemini Free Tier Limits

### What You Get (FREE Forever!)
- **60 requests per minute**
- **1,500 requests per day**
- **Gemini 1.5 Flash** - Fast and smart
- **Gemini Embedding** - High quality embeddings

### Is This Enough?
**YES!** For our app:
- News polling: 1 request/minute = 1,440/day
- User queries: ~50-100/day typical
- **Total: Well within limits** ✅

### If You Need More
Gemini Pro is still very cheap:
- $0.00025 per 1K characters (input)
- $0.0005 per 1K characters (output)
- **~$1-2/month for heavy use**

---

## Why Gemini vs OpenAI?

| Feature | Gemini (FREE) | OpenAI (Paid) |
|---------|---------------|---------------|
| **Cost** | $0/month | ~$5-10/month |
| **Speed** | Very fast | Fast |
| **Quality** | Excellent | Excellent |
| **Free Tier** | 1,500 req/day | None |
| **Setup** | 2 minutes | 5 minutes + billing |

**For hackathons: Gemini is perfect!** 🎯

---

## Testing Your Keys

### Test Gemini Key
```bash
python -c "import google.generativeai as genai; genai.configure(api_key='YOUR_KEY'); print('✅ Gemini key works!')"
```

### Test GNews Key
```bash
curl "https://gnews.io/api/v4/top-headlines?apikey=YOUR_KEY&topic=technology&lang=en"
```

### Test Full App
```bash
python app.py
# In another terminal:
python test_api.py
```

---

## Troubleshooting

### "Invalid API key" for Gemini
- Check key starts with `AIza`
- No extra spaces in `.env`
- Key is from https://aistudio.google.com/app/apikey

### "Rate limit exceeded" for Gemini
- Free tier: 60 req/min, 1500/day
- Wait a minute and retry
- Or upgrade to paid (still very cheap)

### "Invalid API key" for GNews
- Check key from https://gnews.io/dashboard
- Verify email is confirmed
- Free tier: 100 requests/day

### "Module not found: google.generativeai"
```bash
pip install google-generativeai
```

---

## Cost Comparison

### Our App (Gemini - FREE)
- Gemini API: $0/month
- GNews API: $0/month
- Render hosting: $0/month
- **Total: $0/month** 🎉

### Same App (OpenAI - Paid)
- OpenAI API: ~$5-10/month
- GNews API: $0/month
- Render hosting: $0/month
- **Total: $5-10/month**

**Savings: 100%!** 💰

---

## Gemini Models Available

### For Embeddings
- `gemini-embedding-001` (default) - Best quality
- Free tier: 1,500 requests/day

### For Chat/Generation
- `gemini-1.5-flash` (default) - Fast, smart, FREE
- `gemini-1.5-pro` - More capable, still cheap
- `gemini-1.0-pro` - Older, still good

**We use Flash - perfect balance!**

---

## Quick Start Checklist

- [ ] Get Gemini key: https://aistudio.google.com/app/apikey
- [ ] Get GNews key: https://gnews.io/register
- [ ] Create `.env` file
- [ ] Add both keys
- [ ] Run `pip install -r requirements.txt`
- [ ] Run `python app.py`
- [ ] Test with `python test_api.py`

**Total time: 5 minutes** ⚡

---

## Links

- **Gemini API Keys**: https://aistudio.google.com/app/apikey
- **Gemini Docs**: https://ai.google.dev/docs
- **GNews Register**: https://gnews.io/register
- **GNews Dashboard**: https://gnews.io/dashboard

---

## 🎉 You're All Set!

Both APIs are **100% FREE** for hackathons. No credit card needed!

**Next steps:**
1. Get your keys (5 minutes)
2. Add to `.env` or Render
3. Deploy and demo!

**Total cost: $0** 🚀

---

**Built for Inter IIT Hackathon 2026**

*Keeping it free for students!* 💚
