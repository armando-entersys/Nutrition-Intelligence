#!/bin/bash
# Health Check Script for Nutrition Intelligence
# Checks all critical services and reports status

set -e

echo "================================"
echo "🏥 Nutrition Intelligence Health Check"
echo "================================"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check backend
echo "Checking Backend..."
if curl -s -f http://localhost:8000/health > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Backend is healthy${NC}"
else
    echo -e "${RED}✗ Backend is down${NC}"
    exit 1
fi

# Check RAG system
echo "Checking RAG System..."
if curl -s -f http://localhost:8000/api/v1/rag/health > /dev/null 2>&1; then
    echo -e "${GREEN}✓ RAG system is healthy${NC}"
else
    echo -e "${RED}✗ RAG system is down${NC}"
    exit 1
fi

# Check Nutritionist Chat
echo "Checking Nutritionist Chat..."
if curl -s -f http://localhost:8000/api/v1/nutritionist-chat/health > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Nutritionist Chat is healthy${NC}"
else
    echo -e "${YELLOW}⚠ Nutritionist Chat may have issues${NC}"
fi

# Check database
echo "Checking Database..."
if docker exec nutrition-intelligence-db pg_isready -U nutrition_user -d nutrition_intelligence > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Database is healthy${NC}"
else
    echo -e "${RED}✗ Database is down${NC}"
    exit 1
fi

# Check Redis
echo "Checking Redis..."
if docker exec nutrition-intelligence-redis redis-cli ping > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Redis is healthy${NC}"
else
    echo -e "${RED}✗ Redis is down${NC}"
    exit 1
fi

# Check frontend
echo "Checking Frontend..."
if curl -s -f http://localhost:3003 > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Frontend is serving${NC}"
else
    echo -e "${RED}✗ Frontend is down${NC}"
    exit 1
fi

# Check disk space
echo ""
echo "Checking Disk Space..."
DISK_USAGE=$(df -h / | awk 'NR==2 {print $5}' | sed 's/%//')
if [ "$DISK_USAGE" -lt 80 ]; then
    echo -e "${GREEN}✓ Disk usage: ${DISK_USAGE}%${NC}"
elif [ "$DISK_USAGE" -lt 90 ]; then
    echo -e "${YELLOW}⚠ Disk usage: ${DISK_USAGE}% (getting high)${NC}"
else
    echo -e "${RED}✗ Disk usage: ${DISK_USAGE}% (critical!)${NC}"
fi

# Check memory
echo "Checking Memory Usage..."
MEM_USAGE=$(free | grep Mem | awk '{printf "%.0f", $3/$2 * 100.0}')
if [ "$MEM_USAGE" -lt 80 ]; then
    echo -e "${GREEN}✓ Memory usage: ${MEM_USAGE}%${NC}"
elif [ "$MEM_USAGE" -lt 90 ]; then
    echo -e "${YELLOW}⚠ Memory usage: ${MEM_USAGE}% (getting high)${NC}"
else
    echo -e "${RED}✗ Memory usage: ${MEM_USAGE}% (critical!)${NC}"
fi

# Check data counts
echo ""
echo "Checking Data Integrity..."
PRODUCTS=$(docker exec nutrition-intelligence-db psql -U nutrition_user -d nutrition_intelligence -t -c "SELECT COUNT(*) FROM productos_nom051;")
FOODS=$(docker exec nutrition-intelligence-db psql -U nutrition_user -d nutrition_intelligence -t -c "SELECT COUNT(*) FROM alimentos_smae;")
echo -e "${GREEN}✓ Products in DB: ${PRODUCTS}${NC}"
echo -e "${GREEN}✓ Foods in DB: ${FOODS}${NC}"

echo ""
echo "================================"
echo -e "${GREEN}✅ All systems operational!${NC}"
echo "================================"
