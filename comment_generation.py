import pandas as pd
import ast
import ollama
import re


def generate_human_like_comment(df):
    """
    Takes already-loaded dataframe and generates comment from it
    """

    if df is None or df.empty:
        return "", {"error": "No data loaded"}

    # ✅ Select ONE blog from existing CSV (e.g. most comments)
    blog = df.sort_values(by="comment_count", ascending=False).iloc[0]

    summary = blog["summary"]
    raw_comments = blog.get("comments", "")

    try:
        existing_discussion = ast.literal_eval(raw_comments) if pd.notna(raw_comments) else []
    except:
        existing_discussion = []

    discussion_snippet = "\n".join(str(c)[:200] for c in existing_discussion[:5])

    prompt = f"""
Write a short casual comment.

SUMMARY: {summary}

COMMENTS:
{discussion_snippet if discussion_snippet else "None"}

Rules:
- 40 words max
- informal
- like a real person
- no labels
"""

    try:
        res = ollama.chat(
            model="mistral",
            messages=[{"role": "user", "content": prompt}]
        )

        comment = res["message"]["content"].strip()
        comment = re.sub(r'^(Comment|Response):\s*', '', comment)

        meta = {
            "title": blog["title"],
            "url": blog["url"]
        }

        return comment, meta

    except Exception as e:
        return "", {"error": str(e)}