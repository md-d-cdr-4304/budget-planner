# MongoDB Dockerfile (Optional - using official image)
# This file is provided for reference but we'll use the official MongoDB image

FROM mongo:7.0

# Create a custom initialization script if needed
COPY init-mongo.js /docker-entrypoint-initdb.d/

# Set environment variables
ENV MONGO_INITDB_ROOT_USERNAME=admin
ENV MONGO_INITDB_ROOT_PASSWORD=password123
ENV MONGO_INITDB_DATABASE=budget_planner

# Expose MongoDB port
EXPOSE 27017

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD mongosh --eval "db.adminCommand('ping')" || exit 1


