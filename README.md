# Creative Blog Writer (Keyword -> GPT Blog Post)

This program takes one keyword and generates a creative blog post using the OpenAI API.

## Why this default model?
- Default model: `gpt-4.1-mini`
- Reason: strong writing quality at a lower cost than larger flagship models.
- You can switch models anytime with `--model` or `BLOG_MODEL`.

## Setup
1. Create and activate your Python environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set your API key:
   - PowerShell:
     ```powershell
     $env:OPENAI_API_KEY="your_api_key_here"
     ```

## Usage
Generate a Korean post:
```bash
python blog_writer.py "미니멀 라이프"
```

Choose model/language/creativity:
```bash
python blog_writer.py "홈카페" --model gpt-4.1-mini --language Korean --temperature 1.0
```

Save output to file:
```bash
python blog_writer.py "여행 사진" --save post.md
```

## Streamlit Web UI
Run the web app:
```bash
streamlit run streamlit_app.py
```

Features:
- Enter one keyword and click a button to generate a post.
- Set model/language/temperature in the sidebar.
- Input API key in the sidebar (or use `OPENAI_API_KEY` env).
- Download generated content as Markdown.

## Vercel Deploy (Fix 404)
This repository now includes a Vercel-ready web entry and API:
- `index.html` (root page)
- `api/generate.js` (serverless function)

Deploy steps:
1. Import this GitHub repo in Vercel.
2. In Vercel Project Settings -> Environment Variables, add:
   - `OPENAI_API_KEY=your_api_key`
3. Redeploy.

After deploy, opening the root URL should no longer show `404: NOT_FOUND`.

## Optional environment variables
- `BLOG_MODEL` (default: `gpt-4.1-mini`)
- `BLOG_LANGUAGE` (default: `Korean`)
- `BLOG_TEMPERATURE` (default: `0.9`)
