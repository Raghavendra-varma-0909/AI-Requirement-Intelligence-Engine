# 🧠 AI Requirement Intelligence Engine (Frontend)

This directory contains the React (Vite) frontend for the **AI Requirement Intelligence Engine**.

🌐 **Live Demo:** [ai-requirement-intelligence-engine.vercel.app](https://ai-requirement-intelligence-engine.vercel.app)

## Production Deployment

This project is specifically configured to be seamlessly deployed on **Vercel**. 
- It uses the standard Vite build command (`npm run build`) via the Vite build pipeline.
- Custom routing is managed explicitly through `vercel.json` on deployment.
- It connects to the AI backend dynamically. Ensure the `VITE_API_URL` environment variable is set in the Vercel dashboard to point to your live Render API (e.g., `https://ai-req-engine-api.onrender.com`).

## Tech Stack
- **React** (via Vite for hot module replacement)
- **Vanilla CSS3** (Custom Aurora Theme, glassmorphism)
- **Deployment:** Vercel

*For full architectural documentation and logic breakdown, please see the `README.md` located in the root of the repository.*
