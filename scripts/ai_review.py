import os
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

    except Exception as e:
        print(f"❌ Error during AI review: {str(e)}")
        with open("review.txt", "w") as f:
            f.write(f"Error: {str(e)}")
        exit(1)


if __name__ == "__main__":

    # ✅ Check diff file exists
    if not os.path.exists("diff.txt"):
        print("❌ diff.txt not found")
        exit(1)

    with open("diff.txt", "r") as f:
        diff = f.read()

    # ✅ Handle empty diff
    if not diff.strip():
        print("⚠️ No changes found in diff")
        exit(0)

    # ✅ Limit size safely
    MAX_LENGTH = 5000
    if len(diff) > MAX_LENGTH:
        diff = diff[:MAX_LENGTH] + "\n... (truncated)"

    review = review_code(diff)

    print("=== AI REVIEW ===")
    print(review)

    # ✅ Save output
    with open("review.txt", "w") as f:
        f.write(review)

    # 🚨 Better severity detection
    if any(word in review.lower() for word in ["critical", "high severity", "severe"]):
        print("❌ Critical issue detected. Failing pipeline...")
        exit(1)