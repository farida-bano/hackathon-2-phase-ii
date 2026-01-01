#!/bin/bash

echo "🔍 Testing Backend API..."
echo ""

echo "1️⃣ Health Check:"
curl -s http://localhost:8000/
echo ""
echo ""

echo "2️⃣ User Signup:"
RESPONSE=$(curl -s -X POST http://localhost:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"demo@example.com","password":"securepass123"}')
echo "$RESPONSE"
TOKEN=$(echo "$RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin).get('token', ''))")
echo ""

echo "3️⃣ Create Todo:"
curl -s -X POST http://localhost:8000/todos \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"description":"Buy groceries"}'
echo ""
echo ""

echo "4️⃣ Create Another Todo:"
TODO_RESPONSE=$(curl -s -X POST http://localhost:8000/todos \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"description":"Finish Phase II project"}')
echo "$TODO_RESPONSE"
TODO_ID=$(echo "$TODO_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['id'])")
echo ""

echo "5️⃣ List All Todos:"
curl -s -X GET "http://localhost:8000/todos" \
  -H "Authorization: Bearer $TOKEN"
echo ""
echo ""

echo "6️⃣ Toggle Todo Completion (ID: $TODO_ID):"
curl -s -X POST "http://localhost:8000/todos/$TODO_ID/toggle" \
  -H "Authorization: Bearer $TOKEN"
echo ""
echo ""

echo "7️⃣ List Completed Todos:"
curl -s -X GET "http://localhost:8000/todos?completed=true" \
  -H "Authorization: Bearer $TOKEN"
echo ""
echo ""

echo "✅ All API tests completed!"
