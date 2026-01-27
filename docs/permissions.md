# CloudFormation Deployment Permissions

## Required AWS Permissions for RDS PostgreSQL + Jupyter Stack

### Core CloudFormation Permissions
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "cloudformation:CreateStack",
        "cloudformation:UpdateStack",
        "cloudformation:DeleteStack",
        "cloudformation:DescribeStacks",
        "cloudformation:DescribeStackEvents",
        "cloudformation:DescribeStackResources",
        "cloudformation:GetTemplate"
      ],
      "Resource": "*"
    }
  ]
}
```

### Resource-Specific Permissions

#### RDS Permissions
- `rds:CreateDBInstance`
- `rds:CreateDBSubnetGroup`
- `rds:DescribeDBInstances`
- `rds:DescribeDBSubnetGroups`
- `rds:DeleteDBInstance`
- `rds:DeleteDBSubnetGroup`

#### EC2/VPC Permissions
- `ec2:CreateVpc`
- `ec2:CreateSubnet`
- `ec2:CreateSecurityGroup`
- `ec2:CreateInternetGateway`
- `ec2:CreateRouteTable`
- `ec2:RunInstances`
- `ec2:DescribeInstances`
- `ec2:DescribeVpcs`
- `ec2:DescribeSubnets`
- `ec2:DescribeSecurityGroups`
- `ec2:AuthorizeSecurityGroupIngress`

#### IAM Permissions
- `iam:CreateRole`
- `iam:CreateInstanceProfile`
- `iam:AttachRolePolicy`
- `iam:PassRole`

## Current Role Analysis

### Manager Role: `AWSReservedSSO_esadeis_IsbManagersPS_24a80825ae348853`
**Status**: ✅ **COMPLETE**
- Has `AdministratorAccess` policy
- Can deploy CloudFormation stack without issues

### User Role: `AWSReservedSSO_esadeis_IsbUsersPS_7960644547b612a3`
**Status**: ❌ **MISSING CloudFormation permissions**

**Current Permissions**:
- `rds:*` ✅
- `ec2:*` ✅
- `iam:*` ✅
- `s3:*` ✅
- `lambda:*` ✅
- `dynamodb:*` ✅

**Missing Permissions**:
- `cloudformation:*` ❌

## Missing Permissions for IsbUser Role

The IsbUser role needs the following additional permissions to deploy CloudFormation stacks:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "cloudformation:*"
      ],
      "Resource": "*"
    }
  ]
}
```

## Recommendation

Add CloudFormation permissions to the IsbUser role inline policy or attach the AWS managed policy:
- `arn:aws:iam::aws:policy/AWSCloudFormationFullAccess`
