# Phase 1: Quick Start Setup Guide

**Date**: 2025-12-06
**Feature**: Physical AI & Humanoid Robotics Book (Docusaurus)
**Audience**: Developers implementing the book
**Time to Complete**: 30–45 minutes

---

## Overview

This guide walks you through setting up a Docusaurus project for the book "Physical AI & Humanoid Robotics: The Rise of the Digital Human." Follow these steps sequentially; each step builds on the previous one.

**Prerequisites**:
- macOS, Linux, or Windows (with WSL2)
- Administrator access to install software
- Basic terminal/command-line comfort
- Git installed and configured

---

## Step 1: Check Node.js Installation (2 minutes)

### Verify Node.js and npm

```bash
# Check Node.js version (need 18.0 or higher)
node --version
# Expected output: v18.x.x or higher

# Check npm version (need 9 or higher)
npm --version
# Expected output: 9.x.x or higher
```

### If Not Installed

Visit https://nodejs.org/ and download the **LTS (Long Term Support)** version. Follow the installer; it includes npm.

After installation, verify again:
```bash
node --version
npm --version
```

---

## Step 2: Create Docusaurus Project (5 minutes)

### Create Project Directory

```bash
# Navigate to your workspace
cd ~/projects  # or your preferred location

# Create a new Docusaurus project
npx create-docusaurus@latest docusaurus-book classic

# When prompted:
# ✔ Do you want to install dependencies? › Yes
# This may take 2–3 minutes
```

### Verify Installation

```bash
cd docusaurus-book

# Start development server
npm run start

# Expected: Docusaurus opens in browser at http://localhost:3000
# Press Ctrl+C to stop the server
```

---

## Step 3: Configure docusaurus.config.js (10 minutes)

This file controls the site's basic settings.

### Edit Configuration

**File**: `docusaurus-book/docusaurus.config.js`

Find and update these sections:

#### 3a: Site Identity

```javascript
module.exports = {
  title: 'Physical AI & Humanoid Robotics',
  tagline: 'The Rise of the Digital Human',
  url: 'https://yourusername.github.io',  // Update to your GitHub Pages URL
  baseUrl: '/book-repo-name/',             // Update to your repository name

  // ... rest of config
};
```

#### 3b: Theme Configuration (Navbar & Footer)

```javascript
themeConfig: {
  navbar: {
    title: 'Physical AI & Humanoid Robotics',
    items: [
      {
        type: 'doc',
        docId: 'index',
        position: 'left',
        label: 'Book',
      },
      {
        href: 'https://github.com/yourusername/repo-name',  // Your GitHub repo
        label: 'GitHub',
        position: 'right',
      },
    ],
  },
  footer: {
    copyright: `Copyright © 2025 Abdul Ahad Javaid. All rights reserved.`,
  },
},
```

#### 3c: Enable Blog (Set to false)

```javascript
presets: [
  [
    '@docusaurus/preset-classic',
    {
      docs: {
        sidebarPath: require.resolve('./sidebars.js'),
      },
      blog: false,  // ← No blog, just documentation
      theme: {
        customCss: require.resolve('./src/css/custom.css'),
      },
    },
  ],
],
```

---

## Step 4: Configure sidebars.js (10 minutes)

This file controls the navigation structure.

**File**: `docusaurus-book/sidebars.js`

Replace the entire content with:

```javascript
module.exports = {
  docs: [
    {
      type: 'doc',
      id: 'index',
      label: 'Home',
    },
    {
      type: 'category',
      label: 'Introduction',
      items: [
        'introduction/what-is-physical-ai',
        'introduction/evolution-of-systems',
        'introduction/why-this-matters',
      ],
    },
    {
      type: 'category',
      label: 'Foundations',
      items: [
        'foundations/ai-robotics-connection',
        'foundations/hardware-overview',
        'foundations/software-overview',
      ],
    },
    {
      type: 'category',
      label: 'How to Learn',
      items: [
        'approach/hands-on-philosophy',
        'approach/prerequisites',
        'approach/how-to-use-this-book',
      ],
    },
    {
      type: 'category',
      label: 'Real-World Applications',
      items: [
        'applications/use-cases',
      ],
    },
    {
      type: 'category',
      label: 'Module 1: ROS 2',
      items: [
        'module1/index',
        'module1/chapter-1-middleware',
        'module1/chapter-2-nodes-topics',
        'module1/chapter-3-python-agents',
        'module1/chapter-4-urdf',
      ],
      collapsed: false,  // Keep expanded by default
    },
    {
      type: 'category',
      label: 'Ethics & Future',
      items: [
        'ethics/responsible-ai',
        'ethics/future-directions',
      ],
    },
    {
      type: 'doc',
      id: 'glossary',
      label: 'Glossary',
    },
  ],
};
```

---

## Step 5: Create Folder Structure (5 minutes)

Create all necessary folders and placeholder files.

### Create Folders

```bash
# From docusaurus-book/ root:

mkdir -p docs/introduction
mkdir -p docs/foundations
mkdir -p docs/approach
mkdir -p docs/applications
mkdir -p docs/module1
mkdir -p docs/ethics
mkdir -p docs/img
```

### Create Empty Placeholder Files

```bash
# Homepage and special pages
touch docs/index.md
touch docs/title-page.md

# Introduction section
touch docs/introduction/what-is-physical-ai.md
touch docs/introduction/evolution-of-systems.md
touch docs/introduction/why-this-matters.md

# Foundations section
touch docs/foundations/ai-robotics-connection.md
touch docs/foundations/hardware-overview.md
touch docs/foundations/software-overview.md

# Approach section
touch docs/approach/hands-on-philosophy.md
touch docs/approach/prerequisites.md
touch docs/approach/how-to-use-this-book.md

# Applications section
touch docs/applications/use-cases.md

# Module 1 section
touch docs/module1/index.md
touch docs/module1/chapter-1-middleware.md
touch docs/module1/chapter-2-nodes-topics.md
touch docs/module1/chapter-3-python-agents.md
touch docs/module1/chapter-4-urdf.md

# Ethics section
touch docs/ethics/responsible-ai.md
touch docs/ethics/future-directions.md

# Special pages
touch docs/glossary.md
touch docs/writing-guidelines.md
```

---

## Step 6: Create Initial Homepage Content (5 minutes)

**File**: `docs/index.md`

```markdown
---
title: Home
slug: /
sidebar_position: 0
---

# Physical AI & Humanoid Robotics

## The Rise of the Digital Human

Welcome to a beginner's guide to Physical AI and Humanoid Robotics.

This book introduces you to how artificial intelligence combines with robotics to create machines that think AND act in the physical world.

### What You'll Learn

- What Physical AI really is
- How robots and AI work together
- How to control robots with ROS 2
- Real-world applications in healthcare, manufacturing, and research
- The future of humanoid robots

### The Modules

**Module 1: The Robotic Nervous System (ROS 2)**

Master the communication framework used by robots worldwide. Learn to write Python code that controls real robots.

### Who This Is For

- Beginners curious about AI and robotics
- No prior technical knowledge assumed
- Hands-on, practical learning approach
- Progressive chapters that build on each other

### Getting Started

Start with the [Introduction](./introduction/what-is-physical-ai.md), then progress through the book in order.

---

**Ready?** [Begin with Introduction](./introduction/what-is-physical-ai.md)
```

---

## Step 7: Create Glossary Placeholder (3 minutes)

**File**: `docs/glossary.md`

```markdown
---
title: Glossary
description: Complete glossary of terms used in the book.
slug: /glossary
sidebar_position: 99
---

# Glossary

This glossary defines all technical terms used in the book. Terms are introduced in the chapters where they're first used; refer here anytime for clarification.

## A

**Actuator**: A device that moves or controls something in the physical world. Example: a motor that rotates a robot's arm.

**Artificial Intelligence (AI)**: Software systems that learn patterns from data and make decisions.

**Autonomy**: The ability to make decisions and act without human control.

## H

**Hardware**: Physical equipment (processors, motors, sensors) that forms a robot.

**Humanoid Robotics**: Robots designed with a human-like form and behavior.

## M

**Machine Learning**: A type of AI where systems improve performance by learning from examples.

**Middleware**: Software framework that enables communication between software components.

## N

**Node**: A computational unit in ROS 2; each node performs one task.

## R

**Robot**: A machine designed to sense, think, and act in the physical world.

**Robotics**: Engineering discipline of building machines that sense, think, and act.

**ROS 2 (Robot Operating System 2)**: Middleware framework for robot communication and control.

**rclpy**: Python client library for ROS 2.

## S

**Sensor**: A device that perceives the environment (camera, lidar, pressure sensor, etc.).

**Services**: ROS 2 communication pattern for request/reply (client/server).

**Software**: Programs and algorithms that run on robot processors.

## T

**Topics**: Named channels for publishing and subscribing to messages (pub/sub pattern).

## U

**URDF (Unified Robot Description Format)**: XML format for describing robot structure.

---

**Note**: This glossary is updated as new terms are introduced in each chapter.
```

---

## Step 8: Verify Build (5 minutes)

### Build Locally

```bash
# From docusaurus-book/ root:

# Install dependencies (if not done)
npm install

# Build the site
npm run build

# Expected output:
# [INFO] [build] Site built successfully in [time]
# docusaurus-book/build/ folder is created
```

### Preview Locally

```bash
# Serve the build locally
npm run serve

# Expected: Opens browser to http://localhost:3000
# Verify:
#  - Homepage displays
#  - Sidebar navigation appears
#  - Navigation links work (even though pages are empty)
# Press Ctrl+C to stop
```

---

## Step 9: Initialize Git Repository (3 minutes)

```bash
# From docusaurus-book/ root:

# Initialize Git
git init

# Add all files
git add .

# Create initial commit
git config user.email "your-email@example.com"
git config user.name "Your Name"
git commit -m "Initial Docusaurus setup for Physical AI book"

# Verify
git log --oneline
# Should show: Initial Docusaurus setup for Physical AI book
```

---

## Step 10: (Optional) Create GitHub Repository (5 minutes)

Skip if not deploying to GitHub Pages.

### On GitHub

1. Create new repository: https://github.com/new
2. Name: `physical-ai-book` (or your choice)
3. Set to public
4. Do NOT initialize README
5. Click "Create repository"

### Connect Local to GitHub

```bash
# From docusaurus-book/ root:

# Add GitHub remote
git remote add origin https://github.com/yourusername/physical-ai-book.git

# Push to GitHub
git branch -M main
git push -u origin main

# Verify on GitHub: your repository should appear with files
```

---

## Common Issues & Fixes

| Issue | Solution |
|-------|----------|
| `npm: command not found` | Node.js not installed; visit https://nodejs.org/ |
| `Error: ENOENT: no such file or directory` | Create folders manually using `mkdir -p` command |
| Build fails with "Missing sidebars.js" | Ensure `sidebars.js` exists in project root |
| Port 3000 already in use | Change port: `npm run start -- --port 3001` |
| Git push fails | Check authentication; use personal access token if needed |
| Images not loading | Ensure images are in `docs/img/` folder |
| Links broken | Use relative paths: `./chapter-2.md` not `/docs/chapter-2.md` |

---

## Next Steps After Setup

1. **Write Content**: Follow writing guidelines from plan.md to write chapter content
2. **Test Locally**: Run `npm run start` after each chapter to verify formatting
3. **Validate Links**: Ensure all internal links work
4. **Build & Test**: Run `npm run build` before deployment
5. **Deploy**: Push to GitHub or Vercel for live hosting

---

## Development Workflow During Content Writing

```bash
# Daily workflow:

# 1. Start development server
npm run start

# 2. Edit markdown files in docs/

# 3. Changes auto-reload in browser

# 4. When done, commit
git add .
git commit -m "Write Chapter 1 content"
git push

# 5. Build before major milestones
npm run build

# 6. When ready to deploy
npm run deploy  # (for GitHub Pages)
```

---

## Deployment to GitHub Pages

```bash
# Ensure docusaurus.config.js has correct URLs:
# - url: https://yourusername.github.io
# - baseUrl: /physical-ai-book/

# Build for production
npm run build

# Deploy
npm run deploy

# Verify: Visit https://yourusername.github.io/physical-ai-book/
```

---

## Useful Commands Reference

| Command | Purpose |
|---------|---------|
| `npm run start` | Start development server (hot reload) |
| `npm run build` | Build static site for deployment |
| `npm run serve` | Serve built site locally |
| `npm run deploy` | Deploy to GitHub Pages |
| `git status` | Check file status |
| `git add .` | Stage all changes |
| `git commit -m "msg"` | Commit with message |
| `git push` | Push to GitHub |
| `git log --oneline` | View commit history |

---

## Checklist: You're Ready When...

- [x] Node.js 18+ installed and verified
- [x] Docusaurus project created successfully
- [x] docusaurus.config.js updated with your info
- [x] sidebars.js configured with book structure
- [x] All folders created (`introduction/`, `module1/`, etc.)
- [x] Placeholder files created for all chapters
- [x] `npm run build` succeeds
- [x] Local preview works (`npm run serve`)
- [x] Git repository initialized
- [x] (Optional) GitHub repository created and connected

---

**Status**: ✅ **QUICKSTART SETUP COMPLETE**

**Next Steps**:
1. Begin writing content following guidelines in plan.md
2. Use writing standards (simple English, max 2 code examples per chapter)
3. Test frequently with `npm run start`
4. Deploy when all content is ready

---

**Need Help?**

Refer to:
- Docusaurus Docs: https://docusaurus.io/docs
- ROS 2 Docs: https://docs.ros.org/en/humble/
- Python rclpy: https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Py-Publisher-And-Subscriber.html

Good luck! 🚀
