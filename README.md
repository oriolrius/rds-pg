# RDS PostgreSQL CloudFormation Stack

This CloudFormation template deploys a PostgreSQL RDS instance with all required networking infrastructure.

## What Gets Created

- **VPC** with CIDR `10.0.0.0/16`
- **4 Subnets** across 2 Availability Zones (2 public, 2 private)
- **Internet Gateway** with routing for public subnets
- **Security Groups** for database and application access
- **RDS PostgreSQL 15.15** instance (`db.m5.xlarge`, 20GB encrypted storage)

## Prerequisites

- AWS CLI configured with appropriate credentials
- Sufficient IAM permissions to create VPC, RDS, and EC2 resources

## Usage

### Create the Stack

```bash
aws cloudformation create-stack \
  --stack-name my-postgres-stack \
  --template-body file://rds-postgresql.yaml \
  --parameters \
    ParameterKey=DBUsername,ParameterValue=postgres \
    ParameterKey=DBPassword,ParameterValue=YourSecurePassword123
```

### Wait for Stack Creation

```bash
aws cloudformation wait stack-create-complete \
  --stack-name my-postgres-stack
```

### Check Stack Status

```bash
aws cloudformation describe-stacks \
  --stack-name my-postgres-stack \
  --query 'Stacks[0].StackStatus' \
  --output text
```

### View Stack Events (Progress)

```bash
aws cloudformation describe-stack-events \
  --stack-name my-postgres-stack \
  --query 'StackEvents[*].[Timestamp,ResourceStatus,ResourceType,LogicalResourceId]' \
  --output table
```

### Get Database Endpoint

```bash
aws cloudformation describe-stacks \
  --stack-name my-postgres-stack \
  --query 'Stacks[0].Outputs[?OutputKey==`DBEndpoint`].OutputValue' \
  --output text
```

### Destroy the Stack

```bash
aws cloudformation delete-stack \
  --stack-name my-postgres-stack
```

### Wait for Stack Deletion

```bash
aws cloudformation wait stack-delete-complete \
  --stack-name my-postgres-stack
```

## Connecting to the Database

Once the stack is created, connect using:

```bash
psql -h <DBEndpoint> -U postgres -d mydb
```

Note: Your client must be in a security group that is allowed by the `AppSecurityGroup`, or you need to modify the `DatabaseSecurityGroup` to allow your IP address.

## Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| DBUsername | postgres | Master database username |
| DBPassword | (required) | Master password (min 8 characters) |

## Database Specifications

| Property | Value |
|----------|-------|
| Engine | PostgreSQL 15.15 |
| Instance Class | db.m5.xlarge |
| Storage | 20GB gp2 (encrypted) |
| Multi-AZ | No |
| Backup Retention | 7 days |
| Publicly Accessible | Yes |
