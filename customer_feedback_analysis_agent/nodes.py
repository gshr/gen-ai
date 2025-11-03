from state import CustomerFeedbackAnalysisState
import boto3
import json
from botocore.exceptions import ClientError


client = boto3.client("bedrock-runtime", region_name="us-east-1")
MODEL_ID = "anthropic.claude-3-haiku-20240307-v1:0"


def analyse_sentiment(state: CustomerFeedbackAnalysisState):
    instruction = (
        "You are an expert AI sentiment analyst. "
        "Classify the sentiment as Positive, Negative, or Neutral and give a brief explanation. "
        "Return only valid JSON with keys: Sentiment, Explanation."
    )

    user_prompt = f"""{instruction}

    Customer Message:
    {state["input_text"]}
    """

    native_request = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 300,
        "temperature": 0.3,
        "messages": [
            {
                "role": "user",
                "content": [{"type": "text", "text": user_prompt}],
            }
        ],
    }
    request = json.dumps(native_request)

    try:
        response = client.invoke_model(modelId=MODEL_ID, body=request)
    except (ClientError, Exception) as e:
        print(f"ERROR: Can't invoke '{MODEL_ID}'. Reason: {e}")
        raise
    model_response = json.loads(response["body"].read())
    response_text = json.loads(model_response["content"][0]["text"])
    state["sentiment"] = response_text["Sentiment"]
    state["explanation"] = response_text["Explanation"]
    return state


def router(state: CustomerFeedbackAnalysisState) -> str:
    print(state)
    return "analyze_issue" if state.get("sentiment") == "Negative" else "END"


def analyze_issue(
    state: CustomerFeedbackAnalysisState,
) -> CustomerFeedbackAnalysisState:
    instruction = (
        "You are a customer feedback triage assistant.\n"
        "Task 1: Classify the PRIMARY issue category as one of: delivery, product_defect, customer_service, other.\n"
        "Task 2: Provide a single actionable rectification step the business can take.\n"
        "Respond ONLY in valid JSON with keys: Issue, Rectification.\n"
        "Definitions:\n"
        "- delivery: delays, courier problems, damaged-in-transit, packaging issues\n"
        "- product_defect: broken, faulty, not working, quality/performance problems\n"
        "- customer_service: rude/slow/unhelpful support, refund/return hassles, poor communication\n"
        "- other: anything else\n"
    )

    user_prompt = f"""{instruction}

Customer Message:
{state["input_text"]}
"""

    native_request = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 300,
        "temperature": 0.2,
        "messages": [
            {
                "role": "user",
                "content": [{"type": "text", "text": user_prompt}],
            }
        ],
    }

    try:
        response = client.invoke_model(
            modelId=MODEL_ID, body=json.dumps(native_request)
        )
    except (ClientError, Exception) as exc:
        raise exc

    model_response = json.loads(response["body"].read())
    raw_text = model_response["content"][0]["text"]
    parsed = json.loads(raw_text)
    state["issue_type"] = parsed.get("Issue", "other")
    state["rectification_suggestion"] = (
        parsed.get(
            "Rectification", "Review case and contact customer with resolution."
        ),
    )
    return state
