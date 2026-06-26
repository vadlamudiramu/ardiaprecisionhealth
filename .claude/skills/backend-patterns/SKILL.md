---
name: backend-patterns
description: Healthcare API architecture patterns for ARDIA PRECISION HEALTH. Reference when building FastAPI/Next.js API routes, database queries, caching, or background jobs. All patterns include HIPAA compliance considerations.
---

# Healthcare Backend Patterns

## API Design — Clinical Resource Structure

```python
# RESTful clinical resources
GET    /api/v1/patients                    # List (filtered, paginated)
GET    /api/v1/patients/{id}               # Get single patient
POST   /api/v1/patients                    # Create (requires write permission)
PATCH  /api/v1/patients/{id}              # Update
DELETE /api/v1/patients/{id}              # Soft delete only (HIPAA audit trail)

GET    /api/v1/patients/{id}/records       # Patient's clinical records
POST   /api/v1/patients/{id}/records       # Add record
GET    /api/v1/analysis/rcm                # RCM analysis
POST   /api/v1/inference/clinical          # AI clinical decision support
```

## Repository Pattern (with PHI audit)

```python
from dataclasses import dataclass
from datetime import datetime

@dataclass
class AuditContext:
    user_id: str
    purpose: str  # HIPAA minimum necessary: why is this data needed?
    ip_address: str

class PatientRepository:
    async def find_by_id(self, patient_id: str, audit: AuditContext):
        # Log PHI access BEFORE retrieving (non-repudiation)
        await self.audit_log.record(
            user_id=audit.user_id,
            record_id=patient_id,
            action="read",
            purpose=audit.purpose,
            ip=audit.ip_address,
            timestamp=datetime.utcnow()
        )
        return await self.db.fetchrow(
            "SELECT id, name, dob FROM patients WHERE id = $1",
            patient_id
        )
```

## Service Layer — AI Inference

```python
class ClinicalInferenceService:
    def __init__(self, patient_repo: PatientRepository, claude_client):
        self.patient_repo = patient_repo
        self.claude = claude_client

    async def analyze_rcm_opportunity(
        self,
        patient_id: str,
        audit: AuditContext
    ) -> dict:
        patient = await self.patient_repo.find_by_id(patient_id, audit)

        # De-identify before sending to AI model
        de_identified = self._deidentify(patient)

        response = await self.claude.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            messages=[{
                "role": "user",
                "content": f"Analyze RCM opportunity for: {de_identified}"
            }]
        )

        return {"analysis": response.content[0].text}

    def _deidentify(self, patient: dict) -> dict:
        """Remove direct PHI identifiers before AI processing."""
        return {
            "age_group": self._age_bucket(patient["dob"]),
            "conditions": patient["conditions"],
            "payer_type": patient["payer_type"]
        }
```

## Database — PHI Encryption

```sql
-- Enable pgcrypto for column-level encryption
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- PHI table with encrypted columns
CREATE TABLE patients (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    -- Encrypted PHI columns
    name_encrypted BYTEA,  -- AES-256 encrypted
    ssn_encrypted BYTEA,
    dob_encrypted BYTEA,
    -- Non-PHI columns (unencrypted, indexable)
    payer_type VARCHAR(50),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Audit log (never encrypted — must be readable for compliance)
CREATE TABLE phi_access_log (
    id BIGSERIAL PRIMARY KEY,
    user_id UUID NOT NULL,
    record_id UUID NOT NULL,
    action VARCHAR(20) NOT NULL,
    purpose TEXT NOT NULL,
    ip_address INET,
    accessed_at TIMESTAMPTZ DEFAULT NOW()
);

-- Row Level Security
ALTER TABLE patients ENABLE ROW LEVEL SECURITY;

CREATE POLICY "clinicians_see_assigned_patients"
    ON patients FOR SELECT
    USING (
        EXISTS (
            SELECT 1 FROM patient_assignments
            WHERE patient_id = patients.id
            AND clinician_id = auth.uid()
        )
    );
```

## Caching — Clinical Data (Short TTL)

```python
import redis.asyncio as redis
import json
from datetime import timedelta

class ClinicalCache:
    def __init__(self, redis_client):
        self.redis = redis_client
        # Clinical data has short TTL — accuracy is critical
        self.PHI_TTL = timedelta(minutes=5)
        self.ANALYTICS_TTL = timedelta(hours=1)

    async def get_patient_summary(self, patient_id: str) -> dict | None:
        cached = await self.redis.get(f"patient:summary:{patient_id}")
        return json.loads(cached) if cached else None

    async def set_patient_summary(self, patient_id: str, summary: dict):
        await self.redis.setex(
            f"patient:summary:{patient_id}",
            int(self.PHI_TTL.total_seconds()),
            json.dumps(summary)
        )

    async def invalidate_patient(self, patient_id: str):
        await self.redis.delete(f"patient:summary:{patient_id}")
```

## Error Handling — HIPAA-Safe Responses

```python
class HIPAAError(Exception):
    def __init__(self, internal_msg: str, public_msg: str, status_code: int):
        self.internal_msg = internal_msg  # For server logs only
        self.public_msg = public_msg      # Safe to return to client
        self.status_code = status_code

async def hipaa_error_handler(request, exc: HIPAAError):
    # Log full details server-side (never sent to client)
    logger.error("HIPAA_ERROR", extra={
        "internal": exc.internal_msg,
        "path": request.url.path,
        "user_id": getattr(request.state, "user_id", None)
    })

    # Return only safe generic message to client
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.public_msg}
    )
```

## Background Jobs — Clinical Data Processing

```python
from celery import Celery

app = Celery("ardia", broker="redis://localhost:6379/0")

@app.task(
    bind=True,
    max_retries=3,
    default_retry_delay=60,
    acks_late=True  # Don't ack until task completes (ensures audit trail)
)
def process_lab_results(self, patient_id: str, lab_data: dict, user_id: str):
    try:
        # Audit the background job access
        record_phi_access(user_id, patient_id, "background_lab_processing")
        # Process ...
    except Exception as exc:
        raise self.retry(exc=exc)
```

## Rate Limiting — Clinical API

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

# General endpoints: 100/min
# PHI endpoints: 20/min (prevent data harvesting)
# AI inference: 10/min (cost control)

@app.get("/api/v1/patients/{id}")
@limiter.limit("20/minute")
async def get_patient(id: str, request: Request):
    ...

@app.post("/api/v1/inference/clinical")
@limiter.limit("10/minute")
async def clinical_inference(request: Request):
    ...
```

**Remember**: In healthcare, correctness and compliance are more important than performance. Never sacrifice data integrity or audit trails for speed.
