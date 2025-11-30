#!/bin/bash
# Quick script to commit and push all staged changes

echo "=========================================="
echo "  Git Commit and Push Script"
echo "=========================================="
echo ""

# Check if there are staged changes
if git diff --cached --quiet; then
    echo "❌ No staged changes found!"
    echo "Run 'git status' to see what needs to be staged."
    exit 1
fi

echo "📋 Staged files:"
git diff --cached --name-only | head -10
echo ""

# Get commit message
COMMIT_MSG="Add Docker simulation setup with Gazebo and RViz"

# Confirm commit
echo "Will commit with message:"
echo "  '$COMMIT_MSG'"
echo ""
read -p "Continue? (y/n) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Commit cancelled."
    exit 1
fi

# Commit
echo "📝 Committing changes..."
git commit -m "$COMMIT_MSG"

if [ $? -ne 0 ]; then
    echo "❌ Commit failed!"
    exit 1
fi

echo "✅ Commit successful!"
echo ""

# Ask about push
read -p "Push to remote? (y/n) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🚀 Pushing to remote..."
    
    # Try to detect branch name
    BRANCH=$(git branch --show-current)
    echo "Branch: $BRANCH"
    
    git push origin $BRANCH
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "✅ Push successful!"
        echo ""
        echo "🎉 Done! Now you can clone on your local machine:"
        echo "   git clone <your-repo-url> cowbot"
    else
        echo "❌ Push failed! Check your remote configuration."
        exit 1
    fi
else
    echo "⏸️  Skipping push. Run 'git push origin <branch>' manually."
fi

echo ""
echo "=========================================="
