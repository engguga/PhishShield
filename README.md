# PhishShield - Enterprise Phishing Simulation Platform

## Overview

PhishShield is a robust, security-focused phishing simulation platform designed for enterprise environments. It enables organizations to conduct controlled phishing awareness campaigns, monitor employee responses, and deliver immediate educational feedback to strengthen organizational security posture.

---

## Key Features

### Core Capabilities
- **Campaign Management**: Create and manage targeted phishing simulation campaigns.
- **Template System**: Multiple email templates with varying difficulty levels.
- **Real-Time Analytics**: Dashboard with click rates, response times, and security metrics.
- **Educational Feedback**: Immediate training for users who interact with simulations.

### Security Features
- **JWT Authentication**: Secure API access with token-based authentication.
- **Role-Based Access Control**: Granular permissions for different user roles.
- **Comprehensive Audit Logging**: Detailed records of all system activities.
- **Rate Limiting**: Protection against API abuse and brute-force attacks.
- **HTTPS Enforcement**: Secure communications with appropriate headers and policies.

### Technical Architecture
- **Backend**: Django REST Framework with PostgreSQL.
- **Asynchronous Processing**: Celery with Redis for email queue management.
- **Containerized Deployment**: Docker-based deployment with production-ready configuration.
- **API-First Design**: RESTful API for integration with existing security tools.

---

## Quick Start

### Prerequisites
- Docker and Docker Compose
- PostgreSQL 15+
- Redis 7+

### Development Setup

```bash
git clone <repository-url>
cd phishshield-platform
docker-compose up --build -d
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py load_sample_templates
```

- **Admin Interface:** http://localhost:8000/admin  
- **API Documentation:** http://localhost:8000/api/docs  
- **Analytics Dashboard:** http://localhost:8000/analytics/dashboard

### Production Deployment

```bash
cp .env.production .env
# Edit .env with production values
./deploy.sh
```

---

## API Usage

### Authentication

```bash
curl -X POST http://localhost:8000/api/v1/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "api_user", "password": "your_password"}'
```

### Create Campaign

```bash
curl -X POST http://localhost:8000/api/v1/campaigns/ \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Security Awareness Q1",
    "description": "Quarterly phishing test",
    "template_id": 1,
    "target_user_ids": [1, 2, 3]
  }'
```

---

## Project Structure

```
phishshield-platform/
├── core/                 # Django project settings
├── simulations/          # Core phishing simulation app
├── analytics/            # Security analytics and dashboard
├── templates/            # HTML templates for emails and pages
├── static/               # Static files (CSS, JS)
├── docker-compose.yml    # Development environment
├── docker-compose.production.yml  # Production setup
├── nginx.conf            # Production web server config
└── requirements.txt      # Python dependencies
```

---

## Security Considerations

- All sensitive data stored in environment variables
- Database connections use SSL in production
- Regular security patches and dependency updates
- Comprehensive logging and monitoring

### Access Control

- Multi-tier permission system (Admin, Security Team, User)
- API rate limiting to prevent abuse
- Session management with secure cookie policies
- Regular security audits recommended

### Compliance

Designed to help organizations meet:
- GDPR data protection requirements
- ISO 27001 security standards
- NIST Cybersecurity Framework
- Industry-specific compliance needs

---

## Monitoring and Maintenance

- **Health Checks:** `./health_check.sh`
- **Backups:** `./backup.sh`
- **Logs:**  
  - Application logs: `/var/log/phishshield/security.log`  
  - API logs: `/var/log/phishshield/api.log`  
  - System logs: Docker container logs

---

## Contributing

1. Fork the repository
2. Create a feature branch
3. Implement changes with comprehensive tests
4. Submit a pull request for security review

---

## Support

- **Security issues:** security@yourorganization.com
- **Technical support:** infra@yourorganization.com

---

## License

Proprietary - For internal organizational use only.

---

## Documentation

- Security Guidelines
- API Documentation
- Deployment Guide
## Development Status

![CI/CD](https://github.com/your-username/phishshield-platform/workflows/CI/CD%20Pipeline/badge.svg)
![Security](https://img.shields.io/badge/Security-Level%20A-green)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![Django](https://img.shields.io/badge/Django-4.2-green)

## Contributing

Please read our [Contributing Guidelines](CONTRIBUTING.md) and [Code of Conduct](CODE_OF_CONDUCT.md) before submitting issues or pull requests.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history and changes.
