"""
Gradio UI for LLM Council
"""
import gradio as gr
import json
from council import LLMCouncil


def run_council_ui(query: str, api_key: str) -> tuple[str, str, str]:
    """Run council and return formatted outputs"""
    try:
        # Initialize council
        council = LLMCouncil(api_key=api_key)
        
        # Run council
        decision = council.run_council(query)
        
        # Save outputs
        council.save_decision(decision, "decision.json")
        council.save_audit_log("audit_log.json")
        
        # Format decision summary
        summary = f"""## 🏆 Winner: {decision.winner}

**Confidence:** {decision.confidence:.2%}  
**Safety Gate:** {decision.safety_gate_status}

### ⚠️ Risks
{chr(10).join(f"- {risk}" for risk in decision.risks) if decision.risks else "✅ No risks identified"}

### 📚 Citations
{chr(10).join(f"- {cite}" for cite in decision.citations)}
"""
        
        # Format agent responses
        responses_md = "## 📝 Agent Responses\n\n"
        for resp in decision.agent_responses:
            responses_md += f"### {resp['agent_id']}\n{resp['response']}\n\n---\n\n"
        
        # Format judge scores
        scores_md = "## ⚖️ Judge Evaluations\n\n"
        for score in decision.judge_scores:
            scores_md += f"""### {score['judge_id']}
- **Winner:** {score['winner']}
- **Confidence:** {score['confidence']:.2%}
- **Reasoning:** {score['reasoning']}
- **Scores:** Accuracy={score['accuracy_score']}, Safety={score['safety_score']}, Completeness={score['completeness_score']}

---

"""
        
        return summary, responses_md, scores_md
        
    except Exception as e:
        error_msg = f"❌ Error: {str(e)}"
        return error_msg, error_msg, error_msg


# Create Gradio interface
with gr.Blocks(title="LLM Council", theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # 🏛️ LLM Council
    
    Multi-agent decision system with safety gating. Three agents generate responses, two judges evaluate them, 
    and a final decision is made with confidence scoring and risk assessment.
    """)
    
    with gr.Row():
        with gr.Column():
            api_key_input = gr.Textbox(
                label="Anthropic API Key",
                placeholder="sk-ant-...",
                type="password",
                info="Your API key is not stored and only used for this session"
            )
            query_input = gr.Textbox(
                label="Query",
                placeholder="Enter your question or prompt...",
                lines=3
            )
            submit_btn = gr.Button("🚀 Run Council", variant="primary")
            
            gr.Markdown("""
            ### Example Queries
            - What are the security implications of using JWT tokens?
            - How should I structure a microservices architecture?
            - What are the trade-offs between SQL and NoSQL databases?
            """)
    
    with gr.Column():
        with gr.Tab("📊 Decision"):
            decision_output = gr.Markdown()
        
        with gr.Tab("💬 Agent Responses"):
            responses_output = gr.Markdown()
        
        with gr.Tab("⚖️ Judge Scores"):
            scores_output = gr.Markdown()
    
    submit_btn.click(
        fn=run_council_ui,
        inputs=[query_input, api_key_input],
        outputs=[decision_output, responses_output, scores_output]
    )
    
    gr.Markdown("""
    ---
    ### 🔒 Safety Features
    - **Confidence scoring**: Low confidence triggers approval requirement
    - **Risk assessment**: Identifies potential issues in responses
    - **Safety gating**: Blocks unsafe content automatically
    - **Audit logging**: All decisions and scores are logged
    
    ### 📋 Output Files
    After running, check for:
    - `decision.json` - Final decision object
    - `audit_log.json` - Complete audit trail
    """)


if __name__ == "__main__":
    demo.launch()
