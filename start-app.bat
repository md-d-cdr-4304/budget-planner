@echo off
echo Starting Budget Planner Application...
echo.

echo Pulling latest images...
docker-compose pull

echo.
echo Starting services...
docker-compose up -d

echo.
echo Waiting for services to start...
timeout /t 10

echo.
echo Checking service status...
docker-compose ps

echo.
echo ========================================
echo Budget Planner Application Started!
echo ========================================
echo.
echo Access URLs:
echo Frontend: http://localhost:5000
echo Auth API: http://localhost:5001
echo MongoDB: localhost:27017
echo.
echo To view logs: docker-compose logs -f
echo To stop: docker-compose down
echo.
pause

