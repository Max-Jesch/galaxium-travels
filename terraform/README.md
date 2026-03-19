# Galaxium Booking System - Terraform Infrastructure

This directory contains the complete Infrastructure as Code (IaC) configuration for deploying the Galaxium Booking System to AWS.

## Architecture Overview

- **VPC**: Custom VPC with public and private subnets across 2 availability zones
- **NAT Gateway**: Single NAT Gateway for cost optimization (configurable)
- **RDS**: PostgreSQL 14.10 database in private subnets
- **ECS Fargate**: Containerized backend and frontend services
- **ALB**: Application Load Balancer for routing traffic
- **ECR**: Container image repositories
- **CloudWatch**: Centralized logging
- **Secrets Manager**: Secure database credential storage

## Prerequisites

1. **AWS CLI** configured with appropriate credentials
2. **Terraform** >= 1.0 installed
3. **Docker images** built and ready to push to ECR (see Phase 2)

## Quick Start

### 1. Initialize Terraform

```bash
cd terraform
terraform init
```

### 2. Configure Variables

```bash
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars with your specific values
```

### 3. Validate Configuration

```bash
terraform validate
terraform fmt -recursive
```

### 4. Plan Deployment

```bash
terraform plan -out=tfplan
```

Review the plan carefully to understand what resources will be created.

### 5. Apply Configuration

```bash
terraform apply tfplan
```

This will create all AWS resources. The process takes approximately 10-15 minutes.

### 6. Save Outputs

```bash
terraform output > outputs.txt
terraform output -json > outputs.json
```

## Important Outputs

After deployment, you'll receive:

- `alb_url`: The public URL to access your application
- `ecr_backend_repository_url`: ECR repository for backend images
- `ecr_frontend_repository_url`: ECR repository for frontend images
- `ecs_cluster_name`: ECS cluster name for deployments
- `db_credentials_secret_arn`: Secrets Manager ARN for database credentials

## Configuration Files

- `main.tf`: Provider and Terraform configuration
- `variables.tf`: Input variable definitions
- `vpc.tf`: VPC, subnets, NAT Gateway, routing
- `security_groups.tf`: Security group rules
- `rds.tf`: PostgreSQL database configuration
- `ecr.tf`: Container registries
- `ecs.tf`: ECS cluster, task definitions, services
- `alb.tf`: Application Load Balancer and routing
- `cloudwatch.tf`: Log groups
- `iam.tf`: IAM roles and policies
- `outputs.tf`: Output values

## Cost Optimization

For development environments:

- Single NAT Gateway (~$32/month)
- db.t3.micro RDS instance
- 256 CPU / 512 MB memory for ECS tasks
- 7-day CloudWatch log retention

For production:

- Multi-AZ NAT Gateways
- Larger RDS instance
- Increased ECS task resources
- 30-day log retention
- Multi-AZ RDS deployment

## Cleanup

To destroy all resources:

```bash
terraform destroy
```

**Warning**: This will delete all resources including the database. Make sure to backup any important data first.

## Security Notes

- Database credentials are automatically generated and stored in AWS Secrets Manager
- RDS is deployed in private subnets with no public access
- Security groups follow the principle of least privilege
- All data at rest is encrypted

## Troubleshooting

### NAT Gateway Issues

If ECS tasks can't pull images from ECR, verify:
- NAT Gateway is created and associated with private subnets
- Route tables are correctly configured
- Security groups allow outbound traffic

### RDS Connection Issues

- Verify security group allows traffic from ECS tasks
- Check that DATABASE_URL secret is correctly formatted
- Ensure RDS is in the same VPC as ECS tasks

### ECS Task Failures

Check CloudWatch logs:
```bash
aws logs tail /ecs/galaxium-booking-backend --follow
aws logs tail /ecs/galaxium-booking-frontend --follow
```

## Next Steps

After infrastructure is deployed:
1. Push Docker images to ECR repositories
2. Update ECS services to use new images
3. Run database migrations
4. Test the application via the ALB URL

See `bob_artifacts/phase4-deployment-testing.md` for detailed deployment instructions.