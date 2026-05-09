#!/bin/bash
# deploy.sh — build, push e deploy no Cloud Run Jobs
# Uso: bash deploy.sh
 
set -e
 
PROJECT_ID="job-hunter-494620"
REGION="us-central1"
IMAGE="gcr.io/${PROJECT_ID}/job-hunter"
JOB_NAME="job-hunter"
 
echo "=== Build e push da imagem ==="
gcloud builds submit \
  --tag "${IMAGE}" \
  --project "${PROJECT_ID}"
 
echo "=== Deploy no Cloud Run Jobs ==="
gcloud run jobs deploy "${JOB_NAME}" \
  --image "${IMAGE}" \
  --region "${REGION}" \
  --project "${PROJECT_ID}" \
  --set-secrets "OPENAI_API_KEY=OPENAI_API_KEY:latest" \
  --memory 512Mi \
  --task-timeout 600 \
  --max-retries 1
 
echo "=== Criando schedule (8h seg-sex, horário de Brasília) ==="
gcloud scheduler jobs create http "${JOB_NAME}-schedule" \
  --schedule "0 8 * * 1-5" \
  --time-zone "America/Sao_Paulo" \
  --uri "https://${REGION}-run.googleapis.com/apis/run.googleapis.com/v1/namespaces/${PROJECT_ID}/jobs/${JOB_NAME}:run" \
  --oauth-service-account-email "${PROJECT_ID}@appspot.gserviceaccount.com" \
  --location "${REGION}" \
  --project "${PROJECT_ID}" \
  2>/dev/null || echo "Schedule já existe — atualizando..." && \
gcloud scheduler jobs update http "${JOB_NAME}-schedule" \
  --schedule "0 8 * * 1-5" \
  --time-zone "America/Sao_Paulo" \
  --location "${REGION}" \
  --project "${PROJECT_ID}"
 
echo ""
echo "Deploy concluído!"
echo "Para executar manualmente: gcloud run jobs execute ${JOB_NAME} --region ${REGION}"