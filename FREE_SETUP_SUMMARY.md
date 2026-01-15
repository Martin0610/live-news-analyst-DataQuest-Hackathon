# 🆓 100% FREE Setup - No Credit Card Needed!

## ✅ Everything is FREE!

Your entire hackathon project costs **$0/month**:

- ✅ **Gemini API**: FREE (1,500 requests/day)
- ✅ **GNews API**: FREE (100 requests/day)  
- ✅ **Render Hosting**: FREE (512MB RAM)
- ✅ **Total Cost**: **$0/month** 🎉

**No credit card required for any service!**

---

## 🚀 5-Minute FREE Setup

### Step 1: Get Gemini API Key (2 minutes) - FREE!

1. Go to: https://aistudio.google.com/app/apikey
2. Sign in with any Google account
3. Click "Create API Key"
4. Copy your key (starts with `AIza...`)

**No credit card needed!** ✅

### Step 2: Get GNews API Key (2 minutes) - FREE!

1. Go to: https://gnews.io/register
2. Sign up with email
3. Verify email
4. Copy API key from dashboard

**Free tier: 100 requests/day** ✅

### Step 3: Add Keys to Project (1 minute)

```bash
copy .env.example .env  # Windows
# or
cp .env.example .env    # Mac/Linux
```

Edit `.env`:
```env
GEMINI_API_KEY=AIza...your-key-here
GNEWS_API_KEY=...your-key-here
```

**Done! Total time: 5 minutes** ⚡

---

## 💡 Why This is Perfect for Hackathons

### Gemini Free Tier
- **60 requests per minute**
- **1,500 requests per day**
- **No expiration** - free forever!
- **No credit card** required
- **High quality** - Gemini 1.5 Flash

### GNews Free Tier
- **100 requests per day**
- **10 articles per request**
- **No credit card** required
- **Perfect for demos**

### Render Free Tier
- **512MB RAM**
- **Automatic deploys**
- **HTTPS included**
- **No credit card** for free tier

---

## 📊 Is Free Tier Enough?

**YES!** Here's the math:

### Our App Usage
- News polling: 1 request/minute = **1,440/day**
- Gemini embeddings: ~10/minute = **~100/day**
- Gemini chat: ~5 queries/hour = **~50/day**
- **Total Gemini: ~150/day** (well under 1,500 limit!)

### For Demo/Hackathon
- Run for 3 days
- ~50 test queries
- ~500 news articles ingested
- **All within free limits!** ✅

---

## 🆚 Comparison: Free vs Paid

| Feature | Gemini (FREE) | OpenAI (Paid) |
|---------|---------------|---------------|
| **Setup Cost** | $0 | $5 minimum |
| **Monthly Cost** | $0 | $5-10 |
| **Credit Card** | Not needed | Required |
| **Daily Limit** | 1,500 requests | Pay per use |
| **Quality** | Excellent | Excellent |
| **Speed** | Very fast | Fast |
| **Best For** | Hackathons! | Production |

**For hackathons: Gemini wins!** 🏆

---

## 🎯 Quick Links

### Get Your FREE Keys
- **Gemini**: https://aistudio.google.com/app/apikey
- **GNews**: https://gnews.io/register

### Documentation
- **Detailed Setup**: [GEMINI_SETUP.md](GEMINI_SETUP.md)
- **Quick Start**: [QUICKSTART.md](QUICKSTART.md)
- **Deployment**: [DEPLOYMENT.md](DEPLOYMENT.md)

### Dashboards
- **Gemini Usage**: https://aistudio.google.com/
- **GNews Usage**: https://gnews.io/dashboard
- **Render Logs**: https://dashboard.render.com/

---

## ✅ Verification Checklist

Before deploying, verify:

- [ ] Gemini key starts with `AIza`
- [ ] GNews key is from dashboard
- [ ] Both keys in `.env` file
- [ ] No extra spaces in `.env`
- [ ] `.env` is in `.gitignore` (don't commit keys!)

Test locally:
```bash
python app.py
# In another terminal:
python test_api.py
```

---

## 🚀 Deploy to Render (Also FREE!)

1. Push code to GitHub
2. Go to https://dashboard.render.com/
3. New Web Service → Connect repo
4. Add environment variables:
   - `GEMINI_API_KEY` = `AIza...`
   - `GNEWS_API_KEY` = `...`
5. Deploy!

**Render free tier: No credit card needed!** ✅

---

## 💪 You're All Set!

You now have:
- ✅ FREE Gemini API (1,500 req/day)
- ✅ FREE GNews API (100 req/day)
- ✅ FREE Render hosting
- ✅ **Total cost: $0/month**

**Perfect for hackathons!** 🎉

---

## 🆘 Troubleshooting

### "Invalid Gemini API key"
- Check key starts with `AIza`
- Get new key from https://aistudio.google.com/app/apikey
- No spaces in `.env`

### "Rate limit exceeded" (Gemini)
- Free tier: 60/min, 1,500/day
- Wait a minute and retry
- Check usage: https://aistudio.google.com/

### "Rate limit exceeded" (GNews)
- Free tier: 100/day
- Increase `POLLING_INTERVAL=300` (5 minutes)
- Check usage: https://gnews.io/dashboard

### "Module not found: google.generativeai"
```bash
pip install -r requirements.txt
```

---

## 🎓 Pro Tips

1. **Monitor Usage**: Check dashboards daily during hackathon
2. **Optimize Polling**: Increase interval if hitting limits
3. **Cache Responses**: Reduce duplicate queries
4. **Test Early**: Verify keys work before demo day
5. **Have Backup**: Keep old keys in case of issues

---

## 📞 Support

- **Gemini Docs**: https://ai.google.dev/docs
- **GNews Docs**: https://gnews.io/docs
- **Our Troubleshooting**: [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

---

## 🎉 Ready to Win!

You have a **100% FREE** solution that:
- Costs $0/month
- Requires no credit card
- Has generous free limits
- Is production-ready
- Works perfectly for hackathons

**Now go deploy and win!** 🚀

---

**Built for Inter IIT Hackathon 2026**

*Keeping it free for students!* 💚
