import os
from openai import OpenAI

# Initialize client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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
        return f"❌ Error during AI review: {str(e)}"


if __name__ == "__main__":
    # ✅ Check diff file exists
    if not os.path.exists("diff.txt"):
        print("❌ diff.txt not found")
        exit(1)

    with open("diff.txt", "r") as f:
        diff = f.read()

    # 🔥 Limit size (IMPORTANT)
    diff = diff[:5000]

    review = review_code(diff)

    print("=== AI REVIEW ===")
    print(review)

    # ✅ Save output
    with open("review.txt", "w") as f:
        f.write(review)

    # 🚨 Fail pipeline if critical issue found
    if "critical" in review.lower():
        print("❌ Critical issue detected. Failing pipeline...")
        exit(1)