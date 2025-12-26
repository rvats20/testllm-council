"""
Test script for LLM Council
Run this to verify the setup works correctly
"""
from council import LLMCouncil
import json


def test_council():
    """Test the council with various queries"""
    
    print("="*60)
    print("LLM COUNCIL TEST SUITE")
    print("="*60)
    
    test_queries = [
        "What are the security implications of using JWT tokens?",
        "Explain quantum computing in simple terms",
        "How do I optimize database queries for performance?"
    ]
    
    # Initialize council
    print("\n1. Initializing council...")
    try:
        council = LLMCouncil()
        print("✅ Council initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize: {e}")
        print("\nMake sure you have set ANTHROPIC_API_KEY:")
        print("export ANTHROPIC_API_KEY='sk-ant-...'")
        return
    
    # Test with first query
    print(f"\n2. Testing with query: '{test_queries[0]}'")
    try:
        decision = council.run_council(test_queries[0])
        print("✅ Council completed successfully")
        
        # Verify decision object
        print("\n3. Verifying decision object...")
        assert decision.winner in ["agent_analytical", "agent_creative", "agent_practical"]
        assert 0 <= decision.confidence <= 1
        assert decision.safety_gate_status in ["APPROVED", "REQUIRES_APPROVAL", "BLOCKED"]
        assert len(decision.agent_responses) == 3
        assert len(decision.judge_scores) == 2
        print("✅ Decision object structure valid")
        
        # Save outputs
        print("\n4. Saving outputs...")
        council.save_decision(decision, "test_decision.json")
        council.save_audit_log("test_audit_log.json")
        print("✅ Outputs saved successfully")
        
        # Load and verify saved files
        print("\n5. Verifying saved files...")
        with open("test_decision.json", 'r') as f:
            saved_decision = json.load(f)
        with open("test_audit_log.json", 'r') as f:
            saved_audit = json.load(f)
        
        assert saved_decision["winner"] == decision.winner
        assert len(saved_audit) > 0
        print("✅ Saved files verified")
        
        # Print summary
        print("\n" + "="*60)
        print("TEST RESULTS")
        print("="*60)
        print(f"Winner: {decision.winner}")
        print(f"Confidence: {decision.confidence:.2%}")
        print(f"Safety Gate: {decision.safety_gate_status}")
        print(f"Risks: {len(decision.risks)}")
        print(f"Audit Log Entries: {len(saved_audit)}")
        print("="*60)
        print("\n✅ ALL TESTS PASSED")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()


def test_safety_gate():
    """Test safety gate logic"""
    print("\n" + "="*60)
    print("TESTING SAFETY GATE")
    print("="*60)
    
    council = LLMCouncil()
    
    # Test cases
    test_cases = [
        {"confidence": 0.9, "risks": [], "avg_safety": 9, "expected": "APPROVED"},
        {"confidence": 0.4, "risks": ["Low confidence"], "avg_safety": 7, "expected": "REQUIRES_APPROVAL"},
        {"confidence": 0.8, "risks": [], "avg_safety": 5, "expected": "BLOCKED"},
    ]
    
    for i, case in enumerate(test_cases):
        result = council.safety_gate(case["confidence"], case["risks"], case["avg_safety"])
        status = "✅" if result == case["expected"] else "❌"
        print(f"\nTest {i+1}: {status}")
        print(f"  Confidence: {case['confidence']}, Safety: {case['avg_safety']}, Risks: {len(case['risks'])}")
        print(f"  Expected: {case['expected']}, Got: {result}")
    
    print("\n" + "="*60)


if __name__ == "__main__":
    test_council()
    test_safety_gate()
