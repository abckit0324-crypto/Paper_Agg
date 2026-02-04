# Deployment Guide: Paper Aggregator

This guide walks you through deploying the Paper Aggregator as a **free demo** on cloud platforms.

---

## 🎯 Recommended Platform: **Render.com** (FREE)

**Why Render?**
- ✅ Generous free tier (750 hours/month)
- ✅ Automatic deploys from GitHub
- ✅ Built-in PostgreSQL database (free for 90 days, renewable)
- ✅ Zero DevOps - just push to GitHub
- ✅ Free SSL certificates

---

## 📋 Deployment Steps for Render

### 1. **Push Your Code to GitHub**

If you haven't already, push your code to a GitHub repository:

```bash
cd /home/runw/Project/Paper_Agg
git add .
git commit -m "Add deployment configuration"
git push origin main
```

> **Note:** If you need help setting up git, use the `/push-to-git` workflow.

### 2. **Sign Up for Render**

1. Go to [render.com](https://render.com)
2. Sign up using your GitHub account (recommended for easy integration)

### 3. **Create a New Web Service**

1. In Render dashboard, click **"New +"** → **"Blueprint"**
2. Connect your GitHub repository (`Paper_Agg`)
3. Render will automatically detect the `render.yaml` file
4. Click **"Apply"**

Render will:
- Create a PostgreSQL database
- Deploy your web service
- Provide a public URL (e.g., `https://paper-aggregator.onrender.com`)

### 4. **Initial Setup**

**Important:** The free tier services "spin down" after 15 minutes of inactivity. The first request after spin-down may take 30-60 seconds to wake up.

On first deploy:
- The database will be initialized automatically
- The scraper will run on first startup (may take 5-10 minutes)
- Monitor logs in Render dashboard

### 5. **Access Your Demo**

Once deployed, access at: `https://your-app-name.onrender.com`

---

## 🔄 Alternative Free Platforms

### **Railway.app**
- **Free tier:** $5/month credit (enough for small demos)
- **Pros:** Very user-friendly, similar to Render
- **Cons:** Credit-based (not unlimited free)

**Deploy to Railway:**
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Deploy
railway up
```

### **Fly.io**
- **Free tier:** 3 VMs, 3GB storage
- **Pros:** Good for apps needing more control
- **Cons:** More technical setup

**Deploy to Fly.io:**
```bash
# Install Fly CLI
curl -L https://fly.io/install.sh | sh

# Login
fly auth login

# Create app
fly launch

# Deploy
fly deploy
```

---

## ⚠️ Why NOT AWS Free Tier?

While AWS offers a free tier, it's **not recommended** for this use case:

| Issue | Description |
|-------|-------------|
| ❌ **Complexity** | Requires manual setup of EC2, RDS, VPC, Security Groups, Load Balancers |
| ❌ **Time-limited** | Free tier expires after 12 months |
| ❌ **Billing Risks** | Easy to accidentally incur charges (data transfer, storage, etc.) |
| ❌ **Maintenance** | Requires manual updates, security patches, scaling |

**Verdict:** Use Render/Railway for demos. Use AWS only for production with proper DevOps support.

---

## 🛠️ Configuration Details

### Environment Variables

The app automatically uses these on Render:
- `DATABASE_URL` - PostgreSQL connection (auto-provided by Render)
- `PORT` - Web service port (auto-provided)
- `PYTHON_VERSION` - Set to 3.9.0

### Database

- **Local development:** SQLite (`database/papers.db`)
- **Production (Render):** PostgreSQL (automatically configured)

The code automatically switches based on the `DATABASE_URL` environment variable.

### Limitations of Free Tier and Solutions

**Understanding "750 Hours/Month":**
- 750 hours = **31.25 days** worth of runtime
- A month has ~720-744 hours, so **750 hours IS ENOUGH for 24/7 operation**
- The limit is NOT the issue for persistent deployment

**The REAL Limitation: Auto Spin-Down**
- ⚠️ Free tier services **spin down after 15 minutes of inactivity**
- First request after spin-down takes **30-60 seconds** to wake up
- This affects user experience, not total runtime

**Solutions for Persistent (Always-On) Deployment:**

#### Option 1️⃣: Free Uptime Monitoring (RECOMMENDED for demos)
Use a service to ping your app every 14 minutes to prevent spin-down:

**Free Options:**
- **[UptimeRobot](https://uptimerobot.com/)** - 50 monitors free, 5-min intervals
- **[Cron-Job.org](https://cron-job.org/)** - Free HTTP pings
- **[Better Uptime](https://betteruptime.com/)** - Free tier available

**Setup:**
1. Sign up for UptimeRobot (free)
2. Add a new "HTTP(s)" monitor
3. URL: `https://your-app-name.onrender.com/`
4. Interval: **Every 5 minutes** (stays within free tier)
5. Done! Your app stays warm 24/7 for FREE

#### Option 2️⃣: Upgrade to Render Paid Tier
- **Cost:** $7/month (web service) + $7/month (database) = **$14/month**
- **Benefits:** No spin-down, always warm, faster response times
- **When to use:** Production apps, serious demos

#### Option 3️⃣: Use Railway.app Instead
- **Free tier:** $5/month **credit** (usually enough for small apps to run 24/7)
- **No auto spin-down** on free tier (as of 2026)
- **Deployment:** Similar ease to Render

#### Option 4️⃣: Self-Host on Always-Free Cloud VMs
Platforms with truly free, always-on VMs:
- **Oracle Cloud:** 2 free VMs forever (ARM-based, 24GB RAM!)
- **Google Cloud:** 1 free e2-micro VM forever
- **Requires:** More setup (Docker, Nginx, manual deployment)

**Bottom Line:**
- **For demos:** Use Render + UptimeRobot (FREE, 5 min setup)
- **For production:** Upgrade to Render paid ($14/month) or Railway
- **For learning/personal:** Oracle Cloud free tier (more complex setup)

---

## 🔍 Monitoring

### View Logs on Render
1. Go to your web service in Render dashboard
2. Click **"Logs"** tab
3. Real-time logs will show scraping progress, errors, etc.

### Check Database
Render provides a PostgreSQL shell:
1. Go to your database in Render dashboard
2. Click **"Shell"** tab
3. Run SQL queries to inspect data

---

## 🚀 Next Steps

After deploying:

1. **Test the scraper:** Click "Refresh Data" in the UI
2. **Monitor logs:** Check Render dashboard for any errors
3. **Share the demo:** Send the public URL to collaborators
4. **Add custom domain** (optional): Render supports free custom domains

---

## 📞 Troubleshooting

### Issue: "Application failed to respond"
- **Cause:** Scraper is still running on startup
- **Solution:** Wait 5-10 minutes for initial scraping to complete

### Issue: Database connection errors
- **Cause:** PostgreSQL not properly configured
- **Solution:** Check that `DATABASE_URL` environment variable is set in Render

### Issue: Slow response times
- **Cause:** Free tier services spin down after inactivity
- **Solution:** Use uptime monitoring or upgrade to paid tier

### Issue: Scraper not finding papers
- **Cause:** Conference websites may have changed structure
- **Solution:** Check logs, update scrapers in `scrapers/` directory

---

## 💡 Tips for Demo Success

1. **Pre-populate database:** Run scrapers locally first, then deploy with data
2. **Set expectations:** Warn users about 30-60s cold start times on free tier
3. **Monitor usage:** Check Render dashboard to track hours used
4. **Document features:** Add a "Features" or "About" page to your UI

---

## 📚 Resources

- [Render Documentation](https://render.com/docs)
- [Railway Documentation](https://docs.railway.app)
- [Fly.io Documentation](https://fly.io/docs)
- [FastAPI Deployment Guide](https://fastapi.tiangolo.com/deployment/)

---

**Questions?** Open an issue on GitHub or check the main [README.md](README.md).
