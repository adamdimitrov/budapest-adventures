#!/bin/bash
# -------------------------------------------------------------
# BUDAPEST ADVENTURES - AUTOMATED RATINGS SYNC
# -------------------------------------------------------------

# Force path variables to ensure all executables are found in cron/agent environments
PATH=/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin

# Navigate to project directory
cd /Users/adamdimitrov/Development/budapest-adventures

echo "========================================="
echo "Starting automated ratings sync: $(date)"
echo "========================================="

# Run the python scraper
python3 update_ratings.py

# Verify ratings.json was generated and is not empty
if [ -s "ratings.json" ]; then
    echo "ratings.json updated successfully. Committing to GitHub..."
    
    # Stage, commit and push to your repository
    git add ratings.json
    git commit -m "Automated monthly ratings sync"
    git push
    
    echo "Successfully pushed latest ratings to GitHub!"
else
    echo "Error: ratings.json is empty or was not generated. Skipping git push."
fi

echo "Sync finished at: $(date)"
echo "========================================="
