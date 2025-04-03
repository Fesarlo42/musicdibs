#!/bin/bash
# init_db.sh - Database initialization script

set -e  # Exit on error

# Load environment variables
if [ -f "$(dirname "$0")/.env" ]; then
    export $(grep -v '^#' "$(dirname "$0")/.env" | xargs)
else
    echo "⚠️ .env file not found! Make sure it exists in the script directory."
    exit 1
fi

echo "=== Starting database initialization ==="

# Check if MySQL client is installed
if ! command -v mysql &> /dev/null; then
    echo "❌ MySQL client not found. Please install it before running this script."
    exit 1
fi

# Prompt for MySQL root password
read -sp "Enter MySQL root password: " ROOT_PASSWORD
echo

# Run schema.sql to create database & tables
echo "📌 Creating database schema..."
envsubst < "$(dirname "$0")/schema.sql" | mysql -u$MYSQL_USER -p$ROOT_PASSWORD

# Run users.sql to create users & set permissions
echo "🔑 Setting up database users and permissions..."
envsubst < "$(dirname "$0")/users.sql" | mysql -u$MYSQL_USER -p$ROOT_PASSWORD

# Load seed data if user confirms
read -p "Do you want to load development seed data? (y/n): " LOAD_SEEDS
if [[ $LOAD_SEEDS == "y" || $LOAD_SEEDS == "Y" ]]; then
    echo "🌱 Loading seed data..."
    envsubst < "$(dirname "$0")/../seeds/dev_data.sql" | mysql -u$MYSQL_USER -p$ROOT_PASSWORD
    echo "✅ Seed data loaded successfully!"
fi

echo "🎉 Database initialization completed successfully!"
