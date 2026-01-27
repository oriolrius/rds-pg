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
- IAM permissions to create VPC, RDS, and EC2 resources
- Docker (for connect.sh)
- [uv](https://docs.astral.sh/uv/) (for demo notebook)

## Usage

### Create the Stack

```bash
source .env && aws cloudformation create-stack \
  --stack-name my-postgres-stack \
  --template-body file://cloudformation/rds-postgresql.yaml \
  --parameters \
    ParameterKey=DBUsername,ParameterValue=$DB_USER \
    ParameterKey=DBPassword,ParameterValue=$DB_PASSWORD \
    ParameterKey=MyIP,ParameterValue=$MY_IP
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

Create a `.env` file (get your IP from `curl -s https://ip.joor.net`):

```
MY_IP=X.X.X.X
DB_HOST=<DBEndpoint>
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=YourSecurePassword123
DB_NAME=mydb
```

Then run:

```bash
./connect.sh
```

## SQL Practice Notebook

Interactive Jupyter notebook for SQL practice:

```bash
uv run jupyter lab --ip 0.0.0.0 --port 47500 sql_practice.ipynb
```

Opens at http://localhost:47500

Students can write SQL directly using `%%sql` magic:

```sql
%%sql
SELECT * FROM users WHERE city = 'Barcelona';
```

### SQL Explorer Setup

The JupyterLab SQL Explorer extension requires a separate config file. Create it from your `.env`:

```bash
mkdir -p ~/work/.database
cat > ~/work/.database/db_conf.json << EOF
{
    "rds": {
        "name": "rds",
        "db_type": "2",
        "db_id": "rds",
        "db_host": "$DB_HOST",
        "db_port": "$DB_PORT",
        "db_user": "$DB_USER",
        "db_pass": "$DB_PASSWORD",
        "db_name": "$DB_NAME"
    }
}
EOF
```

Or run this one-liner after sourcing `.env`:

```bash
source .env && mkdir -p ~/work/.database && echo "{\"rds\":{\"name\":\"rds\",\"db_type\":\"2\",\"db_id\":\"rds\",\"db_host\":\"$DB_HOST\",\"db_port\":\"$DB_PORT\",\"db_user\":\"$DB_USER\",\"db_pass\":\"$DB_PASSWORD\",\"db_name\":\"$DB_NAME\"}}" > ~/work/.database/db_conf.json
```

**Note:** `db_type` values: `1`=MySQL, `2`=PostgreSQL, `3`=Oracle, `6`=SQLite

## Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| DBUsername | postgres | Master database username |
| DBPassword | (required) | Master password (min 8 characters) |
| MyIP | (required) | Your IP address for database access |

## Database Specifications

| Property | Value |
|----------|-------|
| Engine | PostgreSQL 15.15 |
| Instance Class | db.m5.xlarge |
| Storage | 20GB gp2 (encrypted) |
| Multi-AZ | No |
| Backup Retention | 7 days |
| Publicly Accessible | Yes |
