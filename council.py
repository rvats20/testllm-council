"""
LLM Council: Multi-agent decision system with safety gating
"""
import os
import json
import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
import anthropic


@dataclass
class AgentResponse:
    """Response from a single agent"""
    agent_id: str
    response: str
    timestamp: str


@dataclass
class JudgeScore:
    """Score from a judge agent"""
    judge_id: str
    winner: str
    confidence: float
    reasoning: str
    accuracy_score: float
    safety_score: float
    completeness_score: float


@dataclass
class DecisionObject:
    """Final decision output"""
    winner: str
    confidence: float
    risks: List[str]
    citations: List[str]
    agent_responses: List[Dict]
    judge_scores: List[Dict]
    safety_gate_status: str
    timestamp: str


class LLMCouncil:
    """Main council orchestrator"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "claude-sonnet-4-20250514"):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.model = model
        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.audit_log = []
        
    def _call_llm(self, prompt: str, system_prompt: str = "") -> str:
        """Make LLM API call"""
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=1000,
                system=system_prompt if system_prompt else "You are a helpful AI assistant.",
                messages=[{"role": "user", "content": prompt}]
            )
            return message.content[0].text
        except Exception as e:
            return f"Error: {str(e)}"
    
    def generate_agent_responses(self, query: str) -> List[AgentResponse]:
        """Generate responses from 3 different agents with different perspectives"""
        agents = [
            {
                "id": "agent_analytical",
                "system": "You are an analytical agent focused on logical reasoning and factual accuracy. Provide detailed, evidence-based responses."
            },
            {
                "id": "agent_creative",
                "system": "You are a creative agent focused on innovative solutions and alternative perspectives. Think outside the box."
            },
            {
                "id": "agent_practical",
                "system": "You are a practical agent focused on real-world applicability and actionable advice. Be concise and solution-oriented."
            }
        ]
        
        responses = []
        for agent in agents:
            response_text = self._call_llm(query, agent["system"])
            response = AgentResponse(
                agent_id=agent["id"],
                response=response_text,
                timestamp=datetime.datetime.now().isoformat()
            )
            responses.append(response)
            self.audit_log.append({
                "type": "agent_response",
                "data": asdict(response)
            })
        
        return responses
    
    def judge_responses(self, query: str, responses: List[AgentResponse]) -> List[JudgeScore]:
        """Have 2 judges evaluate and score the responses"""
        
        # Prepare responses for judging
        responses_text = "\n\n".join([
            f"**{r.agent_id}**:\n{r.response}" for r in responses
        ])
        
        judge_prompt = f"""You are an expert judge evaluating multiple AI responses to a query.

QUERY: {query}

RESPONSES:
{responses_text}

Evaluate each response on these criteria (0-10 scale):
1. Accuracy: Factual correctness and logical soundness
2. Safety: Absence of harmful, biased, or problematic content
3. Completeness: Thoroughness in addressing the query

Respond in this EXACT JSON format:
{{
    "winner": "agent_id_of_best_response",
    "confidence": 0.85,
    "reasoning": "brief explanation",
    "scores": {{
        "agent_analytical": {{"accuracy": 8, "safety": 9, "completeness": 7}},
        "agent_creative": {{"accuracy": 7, "safety": 8, "completeness": 8}},
        "agent_practical": {{"accuracy": 9, "safety": 9, "completeness": 6}}
    }}
}}"""
        
        judges = [
            {"id": "judge_primary", "system": "You are a primary judge focused on overall quality and safety."},
            {"id": "judge_secondary", "system": "You are a secondary judge focused on identifying risks and edge cases."}
        ]
        
        scores = []
        for judge in judges:
            judge_response = self._call_llm(judge_prompt, judge["system"])
            
            # Parse JSON response
            try:
                judge_data = json.loads(judge_response)
                winner_id = judge_data["winner"]
                winner_scores = judge_data["scores"][winner_id]
                
                score = JudgeScore(
                    judge_id=judge["id"],
                    winner=winner_id,
                    confidence=judge_data["confidence"],
                    reasoning=judge_data["reasoning"],
                    accuracy_score=winner_scores["accuracy"],
                    safety_score=winner_scores["safety"],
                    completeness_score=winner_scores["completeness"]
                )
            except (json.JSONDecodeError, KeyError) as e:
                # Fallback if JSON parsing fails
                score = JudgeScore(
                    judge_id=judge["id"],
                    winner="agent_analytical",
                    confidence=0.5,
                    reasoning=f"Parse error: {str(e)}",
                    accuracy_score=5.0,
                    safety_score=5.0,
                    completeness_score=5.0
                )
            
            scores.append(score)
            self.audit_log.append({
                "type": "judge_score",
                "data": asdict(score)
            })
        
        return scores
    
    def determine_winner(self, scores: List[JudgeScore]) -> tuple[str, float, List[str]]:
        """Determine final winner from judge scores"""
        # Count votes
        votes = {}
        confidence_sum = 0
        risks = []
        
        for score in scores:
            votes[score.winner] = votes.get(score.winner, 0) + 1
            confidence_sum += score.confidence
            
            # Identify risks
            if score.safety_score < 7:
                risks.append(f"Low safety score ({score.safety_score}) from {score.judge_id}")
            if score.confidence < 0.6:
                risks.append(f"Low confidence ({score.confidence}) from {score.judge_id}")
        
        # Winner is agent with most votes
        winner = max(votes.items(), key=lambda x: x[1])[0]
        avg_confidence = confidence_sum / len(scores)
        
        return winner, avg_confidence, risks
    
    def safety_gate(self, confidence: float, risks: List[str], avg_safety: float) -> str:
        """Determine if output should be blocked or requires approval"""
        if avg_safety < 6:
            return "BLOCKED"
        elif confidence < 0.5 or len(risks) > 2:
            return "REQUIRES_APPROVAL"
        else:
            return "APPROVED"
    
    def extract_citations(self, responses: List[AgentResponse]) -> List[str]:
        """Extract any citations or sources from responses"""
        citations = []
        for response in responses:
            # Simple heuristic: look for URLs or reference patterns
            text = response.response
            if "http" in text or "source:" in text.lower() or "reference:" in text.lower():
                citations.append(f"{response.agent_id}: Contains citations")
        return citations if citations else ["No explicit citations found"]
    
    def run_council(self, query: str) -> DecisionObject:
        """Run full council process"""
        print(f"\n🏛️  Running LLM Council on query: {query}\n")
        
        # Step 1: Generate agent responses
        print("📝 Generating agent responses...")
        responses = self.generate_agent_responses(query)
        
        # Step 2: Judge responses
        print("⚖️  Judging responses...")
        scores = self.judge_responses(query, responses)
        
        # Step 3: Determine winner
        print("🏆 Determining winner...")
        winner, confidence, risks = self.determine_winner(scores)
        
        # Step 4: Safety gate
        avg_safety = sum(s.safety_score for s in scores) / len(scores)
        gate_status = self.safety_gate(confidence, risks, avg_safety)
        
        # Step 5: Extract citations
        citations = self.extract_citations(responses)
        
        # Create decision object
        decision = DecisionObject(
            winner=winner,
            confidence=confidence,
            risks=risks,
            citations=citations,
            agent_responses=[asdict(r) for r in responses],
            judge_scores=[asdict(s) for s in scores],
            safety_gate_status=gate_status,
            timestamp=datetime.datetime.now().isoformat()
        )
        
        # Log decision
        self.audit_log.append({
            "type": "final_decision",
            "data": asdict(decision)
        })
        
        print(f"✅ Decision: {winner} (confidence: {confidence:.2f})")
        print(f"🚦 Safety gate: {gate_status}\n")
        
        return decision
    
    def save_audit_log(self, filename: str = "audit_log.json"):
        """Save audit log to disk"""
        with open(filename, 'w') as f:
            json.dump(self.audit_log, f, indent=2)
        print(f"📋 Audit log saved to {filename}")
    
    def save_decision(self, decision: DecisionObject, filename: str = "decision.json"):
        """Save decision object to disk"""
        with open(filename, 'w') as f:
            json.dump(asdict(decision), f, indent=2)
        print(f"💾 Decision saved to {filename}")


def main():
    """Example usage"""
    # Initialize council
    council = LLMCouncil()
    
    # Example query
    query = "What are the best practices for implementing secure authentication in a web application?"
    
    # Run council
    decision = council.run_council(query)
    
    # Save outputs
    council.save_decision(decision, "decision.json")
    council.save_audit_log("audit_log.json")
    
    # Print summary
    print("\n" + "="*60)
    print("DECISION SUMMARY")
    print("="*60)
    print(f"Winner: {decision.winner}")
    print(f"Confidence: {decision.confidence:.2%}")
    print(f"Safety Gate: {decision.safety_gate_status}")
    print(f"Risks: {', '.join(decision.risks) if decision.risks else 'None identified'}")
    print(f"Citations: {len(decision.citations)}")
    print("="*60)


if __name__ == "__main__":
    main()
