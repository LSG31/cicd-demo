#!/usr/bin/env bash
set -euo pipefail

IMAGE="${IMAGE:?IMAGE is required, e.g. ghcr.io/OWNER/REPO:TAG}"
ENVIRONMENT="${ENVIRONMENT:-production}"
PORT="${PORT:-8000}"

CONTAINER_NAME="cicd-demo-${ENVIRONMENT}"

echo "Deploying ${IMAGE} to ${ENVIRONMENT}..."
docker pull "${IMAGE}"
docker rm -f "${CONTAINER_NAME}" 2>/dev/null || true
docker run -d \
  --name "${CONTAINER_NAME}" \
  --restart unless-stopped \
  -p "${PORT}:8000" \
  -e APP_ENV="${ENVIRONMENT}" \
  -e APP_VERSION="${IMAGE##*:}" \
  -e LOG_LEVEL="INFO" \
  "${IMAGE}"

echo "Waiting for health check..."
for i in {1..20}; do
  if curl -fsS "http://127.0.0.1:${PORT}/health" >/dev/null; then
    echo "Deployment healthy."
    docker ps --filter "name=${CONTAINER_NAME}"
    exit 0
  fi
  sleep 2
done

echo "Deployment failed health check. Logs:"
docker logs --tail 100 "${CONTAINER_NAME}"
exit 1
