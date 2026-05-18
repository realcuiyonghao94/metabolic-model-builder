# GitHub Deployment Guide

## 📦 Deploying Metabolic Model Builder to GitHub

### Prerequisites
- Git installed on your machine
- GitHub account (realcuiyonghao94)
- GitHub CLI (optional but recommended)

---

## 🚀 Step-by-Step Deployment

### Option 1: Using GitHub CLI (Recommended)

```bash
# 1. Navigate to project directory
cd c:\Users\YHC\myvscode\CarveMe

# 2. Initialize git repository
git init

# 3. Add all files
git add .

# 4. Create initial commit
git commit -m "Initial commit: Metabolic Model Builder with CarveMe integration"

# 5. Create repository on GitHub (using GitHub CLI)
gh repo create metabolic-model-builder --public --source=. --remote=origin --push

# 6. Verify
git remote -v
```

### Option 2: Using GitHub Web Interface + Git

```bash
# 1. Create new repository on GitHub:
#    - Go to https://github.com/new
#    - Name: metabolic-model-builder
#    - Description: Interactive app for genome-scale metabolic model reconstruction
#    - Public repository
#    - Click "Create repository"

# 2. Local setup
cd c:\Users\YHC\myvscode\CarveMe

# 3. Initialize git
git init
git add .
git commit -m "Initial commit: Metabolic Model Builder"

# 4. Add remote and push
git remote add origin https://github.com/realcuiyonghao94/metabolic-model-builder.git
git branch -M main
git push -u origin main
```

---

## 🌐 Deploy to Streamlit Cloud

### 1. Connect GitHub to Streamlit

- Go to https://streamlit.io/cloud
- Sign in with GitHub
- Click "New app"
- Select repository: `realcuiyonghao94/metabolic-model-builder`
- Select branch: `main`
- Set main file path: `metabolic_model_app.py`
- Click "Deploy"

### 2. Environment Configuration

Create `~/.streamlit/secrets.toml` (don't commit this):

```toml
# Add any API keys or secrets here
# For example:
# api_key = "your-api-key"
```

---

## 📝 Project File Checklist

Before pushing to GitHub, ensure these files are present:

```
✓ metabolic_model_app.py           # Main app
✓ build_ecoli_model.py             # E. coli model
✓ build_cglutamicum_model.py       # C. glutamicum model
✓ carveme_example.py               # CarveMe demo
✓ README.md                        # Documentation
✓ requirements.txt                 # Dependencies
✓ .gitignore                       # Git ignore file
✓ .streamlit/config.toml           # Streamlit config
✓ DEPLOYMENT.md                    # This file
✓ LICENSE                          # MIT License (optional)
```

---

## 🔧 Common Issues & Solutions

### Issue 1: Git not recognized
**Solution**: Install Git from https://git-scm.com/download/win

### Issue 2: Authentication failed
**Solution**: 
```bash
# Use GitHub Personal Access Token instead of password
# Generate token at: https://github.com/settings/tokens
git remote set-url origin https://<token>@github.com/realcuiyonghao94/metabolic-model-builder.git
```

### Issue 3: Large file warning
**Solution**: Files in `.gitignore` will not be tracked

### Issue 4: Streamlit deployment fails
**Solution**:
- Check `requirements.txt` includes all dependencies
- Verify Python version compatibility
- Check logs at https://share.streamlit.io

---

## 📊 Repository Structure

```
metabolic-model-builder/
├── .github/
│   └── workflows/              # GitHub Actions (optional)
├── .streamlit/
│   └── config.toml
├── models/                     # Generated models (in .gitignore)
├── genomes/                    # Reference genomes (in .gitignore)
├── metabolic_model_app.py      # Main Streamlit app
├── build_ecoli_model.py        # E. coli builder
├── build_cglutamicum_model.py  # C. glutamicum builder
├── carveme_example.py          # CarveMe demo
├── requirements.txt            # Dependencies
├── README.md                   # Main documentation
├── DEPLOYMENT.md               # This file
├── .gitignore                  # Git ignore rules
└── LICENSE                     # MIT License
```

---

## 🔄 Updating Repository

After initial deployment, update with:

```bash
# 1. Make changes to files
# 2. Stage changes
git add .

# 3. Commit with message
git commit -m "Description of changes"

# 4. Push to GitHub
git push origin main

# 5. Streamlit will auto-deploy if connected to Streamlit Cloud
```

---

## 🐛 Debugging

### Check git status
```bash
git status
```

### View commit history
```bash
git log --oneline
```

### View remote repository
```bash
git remote -v
```

### Reset changes
```bash
# Discard local changes
git reset --hard HEAD

# Undo last commit (keep changes)
git reset --soft HEAD~1
```

---

## 📚 Resources

- Git Documentation: https://git-scm.com/doc
- GitHub Guides: https://guides.github.com/
- Streamlit Deployment: https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app
- GitHub Actions: https://docs.github.com/en/actions

---

## ✅ Verification Checklist

After deployment, verify:

- [ ] Repository visible on GitHub
- [ ] All files uploaded (check file count)
- [ ] README.md displays correctly
- [ ] requirements.txt readable
- [ ] .gitignore working (large files not shown)
- [ ] Streamlit Cloud deployment successful
- [ ] App runs without errors at https://share.streamlit.io/...

---

## 🎉 Success!

Your Metabolic Model Builder app is now live on GitHub and ready for:
- Sharing with collaborators
- Contributing to the project
- Deploying to Streamlit Cloud
- Tracking changes and versions
