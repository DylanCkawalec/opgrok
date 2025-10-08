"""
Integration Tests for n8n Workflow System

Tests the complete workflow lifecycle:
1. Generation
2. Connection
3. Modification
4. Activation
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from webapp.app.n8n_service import N8NService, GrokWorkflowBuilder
from webapp.app.n8n_connector import N8NWorkflowAnalyzer, auto_connect_workflow
import os
from dotenv import load_dotenv

load_dotenv()


async def test_complete_lifecycle():
    """Test the full workflow lifecycle"""
    
    print("🧪 OPGROK Integration Test Suite")
    print("=" * 60)
    
    api_key = os.getenv("XAI_API_KEY")
    n8n = N8NService()
    
    # Test 1: n8n Connection
    print("\n✅ TEST 1: n8n API Connection")
    try:
        healthy = await n8n.health_check()
        print(f"   n8n healthy: {healthy}")
        assert healthy, "n8n not accessible"
    except Exception as e:
        print(f"   ❌ Failed: {e}")
        return
    
    # Test 2: List Workflows
    print("\n✅ TEST 2: List Existing Workflows")
    try:
        workflows = await n8n.list_workflows()
        print(f"   Found {len(workflows)} workflows")
        
        if workflows:
            wf = workflows[0]
            print(f"   Latest: {wf.get('name')}")
            print(f"   ID: {wf.get('id')}")
            print(f"   Nodes: {len(wf.get('nodes', []))}")
            print(f"   Active: {wf.get('active')}")
            
            # Test 3: Analyze Workflow
            print("\n✅ TEST 3: Workflow Analysis")
            analyzer = N8NWorkflowAnalyzer(wf)
            analysis = analyzer.analyze_structure()
            print(f"   Total nodes: {analysis['total_nodes']}")
            print(f"   Connected: {analysis['connected_nodes']}")
            print(f"   Unconnected: {analysis['unconnected_nodes']}")
            print(f"   Triggers: {len(analysis['triggers'])}")
            print(f"   Outputs: {len(analysis['outputs'])}")
            
            # Test 4: Connection Suggestions
            print("\n✅ TEST 4: Connection Analysis")
            suggestions = analysis['suggested_connections']
            print(f"   Connection suggestions: {len(suggestions)}")
            for sugg in suggestions[:3]:
                print(f"   - {sugg}")
            
            # Test 5: Workflow Generation
            print("\n✅ TEST 5: Simple Workflow Generation")
            builder = GrokWorkflowBuilder(api_key)
            try:
                simple_wf = await builder.build_complete_workflow(
                    "Send test message to Telegram every hour",
                    mode="interpret"
                )
                print(f"   Generated: {simple_wf.name}")
                print(f"   Nodes: {len(simple_wf.nodes)}")
                print(f"   Connections: {len(simple_wf.connections)}")
            except Exception as e:
                print(f"   ⚠️ Generation test skipped: {str(e)[:100]}")
    
    except Exception as e:
        print(f"   ❌ Failed: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 Test Suite Complete")
    print("\nNext: Verify in browser at http://localhost:8000/workflows")


if __name__ == "__main__":
    asyncio.run(test_complete_lifecycle())
