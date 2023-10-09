# 🔥 `twspace-crawler` Installation & Setup Guide 🔥

Yo fam! 🤙 If you're trying to get the 411 on how to set up `twspace-crawler` to monitor and download Twitter Spaces, you've come to the right spot! Let's get this bread! 🍞🚀

## 🛠️ Installation

### 1. **Command-line Installation** 🖥️
```bash
npm install --global twspace-crawler
```

### 2. **Module Installation** (for the nerdy devs out there) 🤓
```bash
npm install twspace-crawler
```

## 📝 Config Setup

### 1. **Create a `config.json`** 📄

Here's a sample for you to copy & vibe with:

```json
{
  "interval": 30000,
  "users": [
    {
      "username": "username"
    },
    "username_1",
    "username_2",
    "username_3",
    "username_4"
  ],  
  "webhooks": {
    "discord": [
      {
        "active": true,
        "urls": [
          "https://discord.com/api/webhooks/PLACEHOLDER_DISCORD_WEBHOOK_URLS_HERE"
        ],
        "usernames": [
          "<all>"
        ],
        "mentions": {
          "roleIds": [],
          "userIds": []
        }
      }
    ]
  }
}
```

**Note**: Replace the placeholders with the actual data, but keep it on the DL! Don't share sensitive info! 🙊

### 2. **Setup `.env` File** 🌍

This is where you keep those secret keys. Make sure to name it `.env` and keep it in the current working folder.

```env
TWITTER_AUTHORIZATION=PLACEHOLDER_YOUR_AUTHORIZATION_HERE
TWITTER_AUTH_TOKEN=PLACEHOLDER_YOUR_AUTH_TOKEN_HERE
TWITTER_CSRF_TOKEN=PLACEHOLDER_YOUR_CSRF_TOKEN_HERE
```

Again, fam, don't share those placeholder values! 🤫 Replace them with the real ones.

## 🚀 Usage

To monitor some dope users and save their Spaces when they're done:

```bash
twspace-crawler --user user1,user2,... --env ./.env --config ./config.json
```

## 🤘 Wrapping Up

That's it! You're all set to roll with `twspace-crawler`! Keep it groovy, and if you run into any issues, just remember... "The code is strong with this one!" 😎✌️

Stay vibey! 🌈🎉
