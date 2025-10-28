@echo off
echo 🧪 Running Nutrition Intelligence Test Suite
echo ===============================================

echo.
echo 🐍 Testing Backend API...
cd backend
python run_tests.py

echo.
echo 🔄 Testing Frontend Build...
cd ..\frontend
npm run build

echo.
echo ✅ All tests completed!
pause