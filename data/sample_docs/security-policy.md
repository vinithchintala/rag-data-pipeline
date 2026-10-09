# Flowstack Security Policy

Security is foundational to how Flowstack is built and operated. This page summarizes our certifications, encryption practices, data handling, and incident response. For the full trust center, visit trust.flowstack.example.

## Certifications & Audits

Flowstack is **SOC 2 Type II certified**, audited annually against the Trust Services Criteria for security, availability, and confidentiality. We are also **ISO/IEC 27001:2022 certified** and GDPR and CCPA compliant. Penetration tests are performed twice per year by independent third parties, and findings are remediated within SLA windows based on severity. Customers under NDA can request our latest audit reports from the trust center.

## Encryption

All data is encrypted **in transit with TLS 1.3** and **at rest with AES-256**. Database volumes, backups, and file storage are all encrypted. Encryption keys are managed in a dedicated key management service with automatic rotation every 90 days, and no Flowstack engineer can access customer data without going through audited break-glass procedures.

## Data Retention & Deletion

Workflow run history is retained for 13 months on Growth plans and configurable up to 7 years on Enterprise. If you cancel your subscription, your workspace enters a 30-day grace period during which you can reactivate or export everything. **After the grace period, all customer data is permanently deleted within 90 days**, including backups. You may request earlier deletion at any time by contacting privacy@flowstack.example; verified requests are completed within 30 days.

## Subprocessors

We use a small set of vetted subprocessors for hosting, email delivery, and analytics. The current list is published in our Data Processing Agreement and updated with 30 days notice before any change. All subprocessors are bound by contracts requiring equivalent security protections.

## Incident Response

Our incident response plan defines severity levels, on-call rotations, and communication SLAs. In the event of a confirmed security incident affecting customer data, we notify impacted workspace owners within **72 hours** of confirmation, in line with GDPR breach notification requirements, and publish a post-incident report with root cause and remediation steps.
