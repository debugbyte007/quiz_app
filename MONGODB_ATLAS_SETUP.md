# MongoDB Atlas Migration Guide

## Step 1: Create MongoDB Atlas Account & Cluster

1. Go to https://www.mongodb.com/cloud/atlas
2. Sign up or sign in
3. Click "Create a Deployment"
4. Select the **M0 (Free)** tier
5. Choose your region (closest to your users)
6. Give your cluster a name (e.g., "quiz-app-cluster")
7. Click "Create Deployment" and wait 5-10 minutes

## Step 2: Create Database User

1. In MongoDB Atlas, go to **Database Access**
2. Click **"Add New Database User"**
3. Set username: `quiz_user`
4. Set a strong password (save it!)
5. Set Database User Privileges: **Read and Write to Any Database**
6. Click **"Add User"**

## Step 3: Allow Network Access

1. Go to **Network Access**
2. Click **"Add IP Address"**
3. Choose **"Allow access from anywhere"** (or enter your IP for security)
4. Click **"Confirm"**

## Step 4: Get Connection String

1. Click **"Connect"** on your cluster
2. Select **"Drivers"** and choose **Python 3.6 or later**
3. Copy the connection string:
   ```
   mongodb+srv://quiz_user:<password>@<cluster-name>.mongodb.net/quiz_app?retryWrites=true&w=majority
   ```
4. Replace `<password>` with your actual password

## Step 5: Migrate Local Data to Atlas

From your terminal in the backend folder:

```bash
# Install dependencies if not already installed
pip install pymongo

# Run the migration script
python migrate_to_atlas.py
```

When prompted, paste your complete MongoDB Atlas connection string.

Expected output:
```
✓ Successfully connected to MongoDB Atlas!
✓ Inserted 2 users
✓ Inserted 1 quizzes
✓ Inserted 2 results
✓ Created indexes
✅ Migration complete! All data is now in MongoDB Atlas.
```

## Step 6: Update Backend Configuration

### Option A: Using Environment Variables (Recommended)

Create a `.env` file in the backend folder:
```
MONGO_URI=mongodb+srv://quiz_user:YOUR_PASSWORD@YOUR_CLUSTER.mongodb.net/quiz_app?retryWrites=true&w=majority
SECRET_KEY=your-secret-key-here
```

### Option B: For Render/Heroku Deployment

1. Go to your hosting platform's environment variables settings
2. Add: `MONGO_URI=mongodb+srv://quiz_user:YOUR_PASSWORD@YOUR_CLUSTER.mongodb.net/quiz_app?retryWrites=true&w=majority`

## Verification

1. The backend is configured to read `MONGO_URI` from environment variables
2. If `MONGO_URI` is not set, it defaults to localhost (for local development)
3. To switch between local and Atlas, simply set/unset the `MONGO_URI` environment variable

## Troubleshooting

### Connection Issues
- **"Authentication failed"**: Check username/password in connection string
- **"IP address not whitelisted"**: Go to Network Access and add your IP
- **"Host name is not valid"**: Make sure you copied the full connection string

### Data Not Appearing
- Run the migration script again
- Check that you're querying the correct database name: `quiz_app`

### Local Development
- To keep using localhost, simply don't set the `MONGO_URI` environment variable
- The code will default to `mongodb://localhost:27017/`
