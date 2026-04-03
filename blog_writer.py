import argparse
import os
import sys
from typing import Optional

from openai import OpenAI


STYLE_TONE = {
    "친근하게": "friendly, warm, conversational",
    "진지하게": "serious, authoritative, analytical",
}


def build_prompt(keyword: str, language: str, style: str) -> str:
    tone = STYLE_TONE.get(style, STYLE_TONE["친근하게"])
    return (
        f"Write a highly creative, SEO-friendly blog post about '{keyword}' in {language}. "
        "Use a unique angle, memorable storytelling, and practical takeaways. "
        "Include: \n"
        "1) A strong title\n"
        "2) An engaging introduction\n"
        "3) 3-5 section headings with useful details\n"
        "4) A concise summary\n"
        "5) 5 relevant hashtags\n"
        f"Style: {style}. "
        f"Tone: {tone}. Avoid fluff and repetition."
    )


def create_blog_post(
    keyword: str,
    model: str = "gpt-4.1-mini",
    language: str = "Korean",
    temperature: float = 0.9,
    style: str = "친근하게",
    api_key: Optional[str] = None,
) -> str:
    resolved_api_key = api_key or os.getenv("OPENAI_API_KEY")
    if not resolved_api_key:
        raise RuntimeError("OPENAI_API_KEY is not set.")

    client = OpenAI(api_key=resolved_api_key)

    response = client.responses.create(
        model=model,
        temperature=temperature,
        input=[
            {
                "role": "system",
                "content": (
                    "You are a skilled blog writer. Produce original, useful, and well-structured posts. "
                    "Do not copy existing copyrighted text."
                ),
            },
            {"role": "user", "content": build_prompt(keyword, language, style)},
        ],
    )

    output_text: Optional[str] = getattr(response, "output_text", None)
    if output_text:
        return output_text.strip()

    # Fallback extraction for compatibility with SDK response shapes.
    parts = []
    for item in getattr(response, "output", []):
        for content in getattr(item, "content", []):
            text = getattr(content, "text", None)
            if text:
                parts.append(text)

    return "\n".join(parts).strip()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a creative blog post from a single keyword using the OpenAI API."
    )
    parser.add_argument("keyword", help="One keyword/topic for the blog post")
    parser.add_argument(
        "--model",
        default=os.getenv("BLOG_MODEL", "gpt-4.1-mini"),
        help="Model name (default: BLOG_MODEL env or gpt-4.1-mini)",
    )
    parser.add_argument(
        "--language",
        default=os.getenv("BLOG_LANGUAGE", "Korean"),
        help="Output language (default: BLOG_LANGUAGE env or Korean)",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=float(os.getenv("BLOG_TEMPERATURE", "0.9")),
        help="Creativity level between 0.0 and 2.0 (default: 0.9)",
    )
    parser.add_argument(
        "--style",
        default=os.getenv("BLOG_STYLE", "친근하게"),
        choices=["친근하게", "진지하게"],
        help="Writing style: 친근하게 or 진지하게 (default: 친근하게)",
    )
    parser.add_argument(
        "--save",
        default=None,
        help="Optional output file path (e.g., post.md)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    try:
        post = create_blog_post(
            keyword=args.keyword,
            model=args.model,
            language=args.language,
            temperature=args.temperature,
            style=args.style,
        )
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    if not post:
        print("Error: empty response from API", file=sys.stderr)
        return 1

    if args.save:
        with open(args.save, "w", encoding="utf-8") as f:
            f.write(post)
        print(f"Blog post saved to: {args.save}")
    else:
        print(post)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
