#!/bin/bash

# GitHub Pages Deployment Script for CV Portfolio
echo "🚀 GitHub Pages CV Portfolio Setup Script"
echo "==========================================="

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📂 Initializing Git repository..."
    git init
    echo "✅ Git repository initialized"
else
    echo "📂 Git repository already exists"
fi

# Add all files
echo "📁 Adding files to Git..."
git add .

# Commit changes
echo "💬 Enter commit message (or press Enter for default):"
read commit_message
if [ -z "$commit_message" ]; then
    commit_message="Add CV portfolio files for GitHub Pages"
fi

git commit -m "$commit_message"
echo "✅ Files committed: $commit_message"

# Check if remote exists
if git remote get-url origin &>/dev/null; then
    echo "🔗 Remote origin already exists"
    echo "📤 Pushing to existing repository..."
    git push origin main
else
    echo "🔗 No remote repository found"
    echo "Please set up your GitHub repository first:"
    echo ""
    echo "1. Create a new repository on GitHub"
    echo "2. Copy the repository URL"
    echo "3. Run: git remote add origin <your-repo-url>"
    echo "4. Run: git push -u origin main"
    echo ""
    echo "📋 Example commands:"
    echo "git remote add origin https://github.com/yourusername/cv-portfolio.git"
    echo "git branch -M main"
    echo "git push -u origin main"
fi

echo ""
echo "🌐 After pushing to GitHub:"
echo "1. Go to your repository settings"
echo "2. Navigate to 'Pages' section"
echo "3. Set source to 'Deploy from a branch'"
echo "4. Select 'main' branch and '/ (root)' folder"
echo "5. Your site will be available at: https://yourusername.github.io/repository-name/"
echo ""
echo "✅ Setup complete! Your CV portfolio is ready for GitHub Pages."
