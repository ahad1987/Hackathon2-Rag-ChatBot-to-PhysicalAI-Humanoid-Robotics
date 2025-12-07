#!/bin/bash
# RAG Chatbot End-to-End Verification Script
# This script tests the complete RAG pipeline

set -e

echo "======================================================================="
echo "RAG Chatbot End-to-End Verification"
echo "======================================================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
BACKEND_URL="${BACKEND_URL:-http://localhost:8000}"
API_TIMEOUT=30

# Check functions
check_service() {
    local name=$1
    local url=$2

    echo -n "Checking $name... "
    if timeout $API_TIMEOUT curl -s "$url" > /dev/null 2>&1; then
        echo -e "${GREEN}✓ OK${NC}"
        return 0
    else
        echo -e "${RED}✗ FAILED${NC}"
        return 1
    fi
}

test_health() {
    echo ""
    echo "1. Testing Health Check Endpoint"
    echo "--------------------------------"

    response=$(curl -s "$BACKEND_URL/health")
    echo "Response: $response"

    # Check required fields
    if echo "$response" | grep -q '"status"'; then
        echo -e "${GREEN}✓ Health endpoint responds${NC}"
        return 0
    else
        echo -e "${RED}✗ Health endpoint failed${NC}"
        return 1
    fi
}

test_embedding() {
    echo ""
    echo "2. Testing Document Embedding"
    echo "------------------------------"

    # Create test document
    doc_payload=$(cat <<EOF
{
  "doc_id": "verify-test-doc",
  "title": "Test Document for Verification",
  "content": "Humanoid robotics is an exciting field. These robots combine artificial intelligence with physical systems. They can perform tasks in human environments. Vision and language models enable natural interaction. Safety is paramount in robotics. Modern robots use deep learning for perception.",
  "chapter": "Introduction",
  "lesson": "Basics"
}
EOF
)

    echo "Sending document: verify-test-doc"
    response=$(curl -s -X POST "$BACKEND_URL/embed" \
        -H "Content-Type: application/json" \
        -d "$doc_payload")

    echo "Response: $response"

    # Check response contains expected fields
    if echo "$response" | grep -q '"chunks_created"'; then
        chunks=$(echo "$response" | grep -o '"chunks_created":[0-9]*' | cut -d: -f2)
        echo -e "${GREEN}✓ Embedding successful (created $chunks chunks)${NC}"
        return 0
    else
        echo -e "${RED}✗ Embedding failed${NC}"
        return 1
    fi
}

test_query() {
    echo ""
    echo "3. Testing RAG Query"
    echo "--------------------"

    query_payload=$(cat <<EOF
{
  "query": "What is humanoid robotics?",
  "top_k": 5
}
EOF
)

    echo "Sending query: 'What is humanoid robotics?'"
    response=$(curl -s -X POST "$BACKEND_URL/query" \
        -H "Content-Type: application/json" \
        -d "$query_payload")

    echo "Response: $response"

    # Check response contains expected fields
    if echo "$response" | grep -q '"short_answer"'; then
        answer=$(echo "$response" | grep -o '"short_answer":"[^"]*' | cut -d'"' -f4 | head -c 100)
        confidence=$(echo "$response" | grep -o '"confidence_score":[0-9.]*' | cut -d: -f2)

        echo -e "${GREEN}✓ Query successful${NC}"
        echo "  Answer: $answer..."
        echo "  Confidence: $confidence"

        # Check for sources
        if echo "$response" | grep -q '"sources"'; then
            source_count=$(echo "$response" | grep -o '"chunk_id"' | wc -l)
            echo "  Sources found: $source_count"
        fi

        return 0
    else
        echo -e "${RED}✗ Query failed${NC}"
        return 1
    fi
}

test_selection_query() {
    echo ""
    echo "4. Testing Selection-Based Query"
    echo "--------------------------------"

    selection_payload=$(cat <<EOF
{
  "query": "What aspect is mentioned?",
  "selected_text": "Safety is paramount in robotics."
}
EOF
)

    echo "Sending selection query with text: 'Safety is paramount in robotics.'"
    response=$(curl -s -X POST "$BACKEND_URL/select-query" \
        -H "Content-Type: application/json" \
        -d "$selection_payload")

    echo "Response: $response"

    # Check response
    if echo "$response" | grep -q '"is_selection_mode":true'; then
        echo -e "${GREEN}✓ Selection query successful${NC}"

        if echo "$response" | grep -q '"short_answer"'; then
            answer=$(echo "$response" | grep -o '"short_answer":"[^"]*' | cut -d'"' -f4 | head -c 100)
            echo "  Answer: $answer..."
        fi

        return 0
    else
        echo -e "${RED}✗ Selection query failed${NC}"
        return 1
    fi
}

test_openapi() {
    echo ""
    echo "5. Testing OpenAPI Documentation"
    echo "--------------------------------"

    response=$(curl -s "$BACKEND_URL/openapi.json")

    if echo "$response" | grep -q '"openapi"'; then
        echo -e "${GREEN}✓ OpenAPI schema available${NC}"
        echo "  API docs: $BACKEND_URL/docs"
        return 0
    else
        echo -e "${RED}✗ OpenAPI schema not found${NC}"
        return 1
    fi
}

# Main execution
main() {
    local passed=0
    local failed=0

    echo "Backend URL: $BACKEND_URL"
    echo ""

    # Check service availability
    if ! check_service "Backend API" "$BACKEND_URL/health"; then
        echo ""
        echo -e "${RED}Backend API is not available. Start it with:${NC}"
        echo "  cd backend && pip install -r requirements.txt && uvicorn app:app --reload"
        exit 1
    fi

    # Run tests
    if test_health; then ((passed++)); else ((failed++)); fi
    if test_embedding; then ((passed++)); else ((failed++)); fi
    if test_query; then ((passed++)); else ((failed++)); fi
    if test_selection_query; then ((passed++)); else ((failed++)); fi
    if test_openapi; then ((passed++)); else ((failed++)); fi

    # Summary
    echo ""
    echo "======================================================================="
    echo "VERIFICATION SUMMARY"
    echo "======================================================================="
    echo -e "Passed: ${GREEN}$passed${NC}"
    echo -e "Failed: ${RED}$failed${NC}"
    echo ""

    if [ $failed -eq 0 ]; then
        echo -e "${GREEN}✓ All tests passed!${NC}"
        echo ""
        echo "Next steps:"
        echo "1. Test the frontend: http://localhost:3000/chat"
        echo "2. Ingest your book documents: python scripts/ingest_documents.py --path docusaurus-book/docs"
        echo "3. Run integration tests: pytest backend/tests/ -v"
        echo ""
        return 0
    else
        echo -e "${RED}✗ Some tests failed${NC}"
        echo ""
        echo "Debugging tips:"
        echo "1. Check backend logs: docker logs rag-backend"
        echo "2. Verify environment variables in .env"
        echo "3. Ensure Neon and Qdrant are accessible"
        echo ""
        return 1
    fi
}

# Run main
main
exit $?
