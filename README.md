# AWS Automation Toolkit

A command-line tool built with Python to streamline common AWS management tasks, supported by a fully automated CI/CD pipeline.

## Overview

- **EC2 Operations**: List, start, and stop instances directly from the CLI
- **S3 Utilities**: Create buckets, upload files, and remove resources with built-in safeguards
- **Continuous Deployment**: Any push to `main` triggers a GitHub Actions workflow that tests the project and deploys updates to a live EC2 instance

## Tech Stack

| Component | Technology |
|-----------|-----------|
| **Language** | Python 3.9+ |
| **AWS SDK** | Boto3 |
| **Services** | EC2 (Linux), S3, IAM |
| **DevOps** | GitHub Actions, Bash, SSH |

## Project Structure

```
.
├── toolkit/
│   ├── __init__.py         # Package initialization
│   ├── ec2_tool.py         # EC2 management logic
│   └── s3_tool.py          # S3 operations
├── deploy/
│   └── deploy.sh           # Remote deployment script
├── .github/workflows/
│   └── ci-cd.yml           # CI/CD workflow definition
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

## Getting Started

### Prerequisites

- Python 3.9 or higher
- AWS account with appropriate credentials
- AWS CLI configured on your system

### Installation

1. **Clone and navigate to the repository**
   ```bash
   git clone https://github.com/Paffy-12/aws-automation-toolkit.git
   cd aws-automation-toolkit
   ```

2. **Create and activate a virtual environment**
   ```bash
   # macOS/Linux
   python -m venv venv
   source venv/bin/activate
   
   # Windows
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure AWS credentials**
   ```bash
   aws configure
   ```
   You'll be prompted to enter:
   - AWS Access Key ID
   - AWS Secret Access Key
   - Default region
   - Default output format (optional)

## Usage

### S3 Operations

```bash
# Create a new bucket
python -m toolkit.s3_tool create my-unique-bucket

# Upload a file
python -m toolkit.s3_tool upload my-unique-bucket --file_name data.txt

# Remove a bucket
python -m toolkit.s3_tool delete my-unique-bucket
```

### EC2 Operations

```bash
# List all instances
python -m toolkit.ec2_tool list

# Start an instance
python -m toolkit.ec2_tool start --instance_id i-1234567890abcdef0

# Stop an instance
python -m toolkit.ec2_tool stop --instance_id i-1234567890abcdef0
```

For detailed command options, run any tool with the `--help` flag:
```bash
python -m toolkit.ec2_tool --help
python -m toolkit.s3_tool --help
```

## CI/CD Pipeline

This project uses **GitHub Actions** for automated testing and deployment:

1. **Trigger**: Commits pushed to the `main` branch automatically trigger the pipeline
2. **Authentication**: The GitHub runner authenticates with the EC2 instance using stored secrets
3. **Deployment**: The `deploy/deploy.sh` script transfers the latest build and refreshes the remote environment
4. **Workflow**: See `.github/workflows/ci-cd.yml` for complete pipeline configuration

### Environment Secrets

To enable CI/CD, configure the following secrets in your GitHub repository settings:

- `EC2_HOST`: The full SSH connection string (Format: `user@ip_address`, e.g., `ec2-user@3.110.179.201`)
- `SSH_PRIVATE_KEY`: The content of your `.pem` private key file (Copy the entire content including `BEGIN` and `END` lines)

*(Note: AWS Credentials are not required in GitHub Secrets for this pipeline, as they are configured directly on the EC2 instance.)*

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support & Contact

For questions, issues, or feedback, please [open an issue](https://github.com/Paffy-12/aws-automation-toolkit/issues) on GitHub.

---

**Author**: [Prateek Nayyar](https://github.com/Paffy-12)