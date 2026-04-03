export default async function handler(req, res) {
  if (req.method !== "POST") {
    return res.status(405).json({ error: "Method not allowed" });
  }

  try {
    const {
      keyword,
      model = "gpt-4.1-mini",
      language = "Korean",
      temperature = 0.9,
      style = "친근하게",
    } = req.body || {};

    if (!keyword || !String(keyword).trim()) {
      return res.status(400).json({ error: "keyword is required" });
    }

    const apiKey = process.env.OPENAI_API_KEY;
    if (!apiKey) {
      return res.status(500).json({ error: "OPENAI_API_KEY is not configured" });
    }

    const toneByStyle = {
      친근하게: "friendly, warm, conversational",
      진지하게: "serious, authoritative, analytical",
    };
    const tone = toneByStyle[style] || toneByStyle["친근하게"];

    const prompt = `Write a highly creative, SEO-friendly blog post about '${String(keyword).trim()}' in ${language}. Use a unique angle, memorable storytelling, and practical takeaways. Include:\n1) A strong title\n2) An engaging introduction\n3) 3-5 section headings with useful details\n4) A concise summary\n5) 5 relevant hashtags\nStyle: ${style}\nTone: ${tone}. Avoid fluff and repetition.`;

    const response = await fetch("https://api.openai.com/v1/responses", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${apiKey}`,
      },
      body: JSON.stringify({
        model,
        temperature,
        input: [
          {
            role: "system",
            content:
              "You are a skilled blog writer. Produce original, useful, and well-structured posts. Do not copy existing copyrighted text.",
          },
          {
            role: "user",
            content: prompt,
          },
        ],
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      const message = data?.error?.message || "OpenAI request failed";
      return res.status(response.status).json({ error: message });
    }

    const outputText = data?.output_text || "";
    return res.status(200).json({ text: outputText });
  } catch (error) {
    return res.status(500).json({ error: error?.message || "Unknown server error" });
  }
}
