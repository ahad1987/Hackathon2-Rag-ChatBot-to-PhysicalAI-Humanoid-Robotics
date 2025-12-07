# RAG Chatbot Deployment Checklist

**Project:** Physical AI & Humanoid Robotics: Rise of the Digital Human
**Date:** December 7, 2024

---

## Pre-Deployment Validation

### Code Quality
- [ ] All tests pass: `pytest backend/tests/ -v`
- [ ] No linting errors: `pylint backend/*.py`
- [ ] Type checking passes: `mypy backend/`
- [ ] API documentation complete: `/docs` endpoint works
- [ ] No hardcoded secrets in code

### Integration Testing
- [ ] Health check passes: `curl http://localhost:8000/health`
- [ ] Sample embedding succeeds: `python scripts/ingest_documents.py --sample`
- [ ] Query returns results: `bash verify_rag.sh`
- [ ] Frontend loads without errors: `http://localhost:3000/chat`
- [ ] Selection mode works: Can select text and query

### Security Review
- [ ] CORS properly configured for production domain
- [ ] API keys stored in `.env` (not in code)
- [ ] Rate limiting enabled (60 req/min)
- [ ] Input sanitization verified
- [ ] Database credentials are strong
- [ ] HTTPS/TLS configured
- [ ] OWASP Top 10 review completed

### Performance Baseline
- [ ] Backend response time < 2 seconds
- [ ] Frontend load time < 3 seconds
- [ ] Embedding generation < 1 second per batch
- [ ] Query search < 500ms
- [ ] Database queries optimized

---

## Infrastructure Setup

### Cloud Services Configuration

#### OpenAI Account
- [ ] Account created and verified
- [ ] API key generated and stored securely
- [ ] Usage limits configured
- [ ] Billing method set up
- [ ] Organization (if applicable) configured

#### Qdrant Cloud
- [ ] Cluster created
- [ ] API key generated
- [ ] Collection configured: `book-embeddings`
- [ ] Payload indexes created:
  - [ ] `doc_id` (keyword)
  - [ ] `chapter` (keyword)
  - [ ] `lesson` (keyword)
- [ ] Backup/snapshots enabled

#### Neon PostgreSQL
- [ ] Project created
- [ ] Database `rag_chatbot` created
- [ ] User credentials set up
- [ ] Connection pooling enabled
- [ ] Backup settings configured
- [ ] SSL/TLS enforced

### Local Infrastructure (if applicable)
- [ ] Docker and Docker Compose installed
- [ ] Docker memory limits set (4GB+ for backend)
- [ ] Volume mounts configured
- [ ] Network bridges created

---

## Deployment Configuration

### Environment Variables

**Backend (.env file):**
```
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4-turbo-preview
EMBEDDING_MODEL=text-embedding-3-small
QDRANT_URL=https://...
QDRANT_API_KEY=...
QDRANT_COLLECTION_NAME=book-embeddings
NEON_DB_URL=postgresql://...
API_HOST=0.0.0.0
API_PORT=8000
ENV=production
CORS_ORIGINS=[...]
```

**Frontend (.env):**
```
REACT_APP_API_ENDPOINT=https://api.yourdomain.com
```

- [ ] All required variables present
- [ ] Values match production endpoints
- [ ] Sensitive values obfuscated in logs
- [ ] Staging and production configs differ

### Secrets Management

- [ ] Production secrets stored in platform-specific service:
  - [ ] Vercel Environment Variables (frontend)
  - [ ] Google Cloud Secret Manager (Cloud Run)
  - [ ] Heroku Config Vars (if Heroku)
  - [ ] GitHub Secrets (for CI/CD)
- [ ] No plaintext secrets in repository
- [ ] Secret rotation policy documented
- [ ] Access logs enabled for secrets

### Application Configuration

**Backend:**
- [ ] Logging level set to INFO (not DEBUG in production)
- [ ] Error reporting configured (Sentry, DataDog, etc.)
- [ ] Performance monitoring enabled
- [ ] Database connection pooling optimized:
  - Min connections: 5
  - Max connections: 20

**Frontend:**
- [ ] API endpoint points to production backend
- [ ] Error tracking configured
- [ ] Analytics enabled (Google Analytics, etc.)
- [ ] Asset paths use CDN

---

## Document Ingestion

- [ ] All book Markdown files accessible
- [ ] Frontmatter parsing tested
- [ ] Chunking parameters optimized:
  - Chunk size: 1000 tokens
  - Overlap: 200 tokens
- [ ] Full ingestion completes without errors:
  ```bash
  python scripts/ingest_documents.py --path docusaurus-book/docs
  ```
- [ ] Ingestion results logged:
  - [ ] Files processed: ___
  - [ ] Chunks created: ___
  - [ ] Vectors upserted: ___
  - [ ] Total tokens: ___
- [ ] Spot-check queries for correctness
- [ ] No data corruption detected

---

## Deployment Target Setup

### Option A: Google Cloud Run (Recommended)

- [ ] Project created in Google Cloud Console
- [ ] Service account created with permissions:
  - Cloud Run Admin
  - Container Registry Service Agent
  - Cloud SQL Client
- [ ] Docker Registry access configured
- [ ] Cloud SQL connections allowed
- [ ] Environment secrets configured in Cloud Run service
- [ ] VPC Connector set up (if using Cloud SQL)

### Option B: Heroku

- [ ] Heroku account created
- [ ] Heroku CLI installed and authenticated
- [ ] App created: `heroku create <app-name>`
- [ ] Procfile created
- [ ] Config variables set: `heroku config:set KEY=value`
- [ ] PostgreSQL addon added: `heroku addons:create heroku-postgresql`

### Option C: Docker Swarm / Kubernetes

- [ ] Cluster configured
- [ ] Persistent volume storage set up
- [ ] Secret management configured
- [ ] Ingress/Load balancer configured
- [ ] Auto-scaling policies defined

### Option D: Virtual Machine (AWS EC2, DigitalOcean, Linode)

- [ ] Instance created and secured
- [ ] SSH key pair generated and stored
- [ ] Security groups configured:
  - [ ] Allow port 80 (HTTP)
  - [ ] Allow port 443 (HTTPS)
  - [ ] Allow port 5432 (PostgreSQL, if internal)
  - [ ] Restrict other ports
- [ ] Database port accessible from app only
- [ ] Firewall configured
- [ ] DDoS protection enabled (if available)

---

## Frontend Deployment

### Vercel (Recommended for Next.js/React)

- [ ] GitHub repository connected
- [ ] Environment variables configured in Vercel dashboard
- [ ] Build command verified: `npm run build`
- [ ] Output directory: `build/`
- [ ] Serverless functions configured (if needed)
- [ ] Preview deployments enabled
- [ ] Analytics dashboard set up

### Netlify

- [ ] GitHub repository connected
- [ ] Build command: `npm run build`
- [ ] Publish directory: `build/`
- [ ] Environment variables configured
- [ ] Function settings configured
- [ ] Redirect rules for SPA configured
- [ ] Domain custom DNS updated

### Traditional Web Server (Apache/Nginx)

- [ ] Server provisioned
- [ ] SSL certificate installed (Let's Encrypt)
- [ ] Reverse proxy configured for `/api/*` routes
- [ ] Static file caching headers set
- [ ] Gzip compression enabled
- [ ] Security headers configured:
  - [ ] X-Content-Type-Options: nosniff
  - [ ] X-Frame-Options: DENY
  - [ ] Strict-Transport-Security

---

## Monitoring & Observability

### Application Monitoring

- [ ] Error tracking enabled (Sentry, Rollbar, etc.)
- [ ] Performance monitoring enabled (NewRelic, DataDog, etc.)
- [ ] Health check endpoint monitored
- [ ] Alert thresholds defined:
  - [ ] Error rate > 1%
  - [ ] Response time > 5s
  - [ ] Database connection failures
  - [ ] API quota exhaustion

### Infrastructure Monitoring

- [ ] CPU usage monitoring
- [ ] Memory usage monitoring
- [ ] Disk space monitoring
- [ ] Network throughput monitoring
- [ ] Database performance monitoring
- [ ] Alerts configured for:
  - [ ] High resource usage
  - [ ] Service outages
  - [ ] Slow queries

### Logging

- [ ] Centralized logging enabled (ELK, CloudWatch, Stackdriver)
- [ ] Log retention policies set
- [ ] Error logs captured and searchable
- [ ] Query logs captured for analysis
- [ ] Audit logs for API access

### Analytics

- [ ] User query analytics enabled
- [ ] Common questions tracked
- [ ] Response quality metrics collected
- [ ] User satisfaction surveys configured

---

## Database Backups

### Neon Backups
- [ ] Automatic daily backups enabled
- [ ] Backup retention: minimum 7 days
- [ ] Test restore procedure documented
- [ ] Backup size monitoring enabled

### Qdrant Backups
- [ ] Snapshot strategy documented
- [ ] Snapshots scheduled (daily or weekly)
- [ ] Snapshot storage location verified
- [ ] Recovery procedure tested

### Restore Procedure
- [ ] Documented in runbook
- [ ] Tested with sample data
- [ ] Recovery time objective (RTO) defined
- [ ] Recovery point objective (RPO) defined

---

## Security Hardening

### API Security
- [ ] CORS headers configured correctly
- [ ] Rate limiting enabled
- [ ] Input validation on all endpoints
- [ ] SQL injection prevention verified
- [ ] XSS protection verified
- [ ] CSRF tokens if applicable
- [ ] API authentication configured (if needed)

### Data Security
- [ ] Data in transit encrypted (HTTPS/TLS)
- [ ] Data at rest encrypted (database encryption)
- [ ] PII handling policy documented
- [ ] Data retention policy enforced
- [ ] GDPR/CCPA compliance reviewed

### Access Control
- [ ] Admin console protected
- [ ] Database access restricted
- [ ] CI/CD secrets secured
- [ ] Key rotation policy documented

---

## Performance Optimization

- [ ] Database connection pooling optimized
- [ ] Query caching enabled where applicable
- [ ] Vector search indexes optimized
- [ ] Frontend assets minified and compressed
- [ ] CDN configured for static assets
- [ ] API response time profiled and optimized
- [ ] Load testing completed

---

## Testing in Production

### Smoke Tests
```bash
# Health check
curl https://yourdomain.com/api/health

# Sample query
curl -X POST https://yourdomain.com/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is in the book?"}'
```

- [ ] Passed

### User Acceptance Testing
- [ ] Chat interface works
- [ ] Text selection mode works
- [ ] Source citations display correctly
- [ ] Performance is acceptable
- [ ] No console errors
- [ ] Mobile responsive

---

## Documentation

- [ ] README.md updated with production URL
- [ ] API documentation current
- [ ] Deployment guide documented
- [ ] Runbook for common issues created
- [ ] Architecture diagrams up to date
- [ ] Development guide updated

---

## Post-Deployment

- [ ] Monitor error rates for 24 hours
- [ ] Check API usage metrics
- [ ] Verify database performance
- [ ] Collect user feedback
- [ ] Document lessons learned
- [ ] Update runbooks with new knowledge

---

## Rollback Plan

**Trigger Conditions:**
- [ ] Error rate > 5%
- [ ] Response time > 10s
- [ ] Database unavailable > 10 minutes
- [ ] Multiple critical errors reported

**Rollback Procedure:**
1. [ ] Identify last known good version
2. [ ] Stop current deployment
3. [ ] Revert to previous version:
   - Backend: `git revert <commit>`
   - Frontend: Redeploy from previous tag
4. [ ] Verify health checks pass
5. [ ] Monitor for 1 hour
6. [ ] Document incident and root cause

---

## Sign-Off

- [ ] Development Lead: _____________________ Date: _____
- [ ] QA Lead: _____________________ Date: _____
- [ ] Operations Lead: _____________________ Date: _____
- [ ] Project Owner: _____________________ Date: _____

---

**Deployment Date:** _______________

**Deployed By:** _______________________________

**Notes:**

