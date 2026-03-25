import os
import traceback
from openai import OpenAI

# ✅ Validate API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("❌ OPENAI_API_KEY not set")
    exit(1)

client = OpenAI(api_key=api_key)


def review_code(diff):
    prompt = f"""
You are a senior DevOps engineer.

Review the following code diff and provide output in this format:

### 🔍 Issues Found
- ...

### ⚠️ Security Risks
- ...

### 💡 Suggestions
- ...

### 🚨 Severity
(Critical / Warning / Info)

Code:
{diff}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Expert DevOps reviewer"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )

        return response.choices[0].message.content

    except Exception:
        print("❌ Error during AI review:")
        traceback.print_exc()

        with open("review.txt", "w") as f:
            f.write("Error occurred during AI review")

        exit(1)


if __name__ == "__main__":

    if not os.path.exists("diff.txt"):
        print("❌ diff.txt not found")
        exit(1)

    with open("diff.txt", "r") as f:
        diff = f.read()

    if not diff.strip():
        print("⚠️ No changes found in diff")
        exit(0)

    print(f"Diff size: {len(diff)} characters")

    MAX_LENGTH = 5000
    if len(diff) > MAX_LENGTH:
        diff = diff[:MAX_LENGTH] + "\n... (truncated)"

    review = review_code(diff)

    print("\n===== AI REVIEW START =====\n")
    print(review)
    print("\n===== AI REVIEW END =====\n")

    with open("review.txt", "w") as f:
        f.write(review)

    if any(word in review.lower() for word in ["critical", "high severity", "severe"]):
        print("❌ Critical issue detected. Failing pipeline...")
        exit(1)
        # final done