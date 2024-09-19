# Auto Backup and Delete for POS Systems

## Overview

This project automates the backup and deletion process for databases used in POS (Point of Sale) systems across India(for zota healthcare, ZEELAB Pharmacy and Pradhan Mantri Bhartiya Janaushadhi Pariyojana). It ensures efficient storage management by maintaining a maximum of 15 backup files per store. Any files exceeding this limit are automatically deleted based on predefined conditions.

## Features

- Automated backup of POS system databases.
- Storage of up to 15 backup files per store.
- Automatic deletion of backup files exceeding the 15-file limit.
- Efficient storage management for large database files.

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/auto-backup-and-delete.git
   ```
2. Navigate to the project directory:
   ```sh
   cd auto-backup-and-delete
   ```
3. Run the docker compose file
   ```sh
   docker-compose up -d
   ```

## Usage

1. Configure the backup settings in the `mainprocess/.env` file.
2. Run the backup script:
   ```sh
   python main.py
   ```

## Contributing

1. Fork the repository.
2. Create a new branch:
   ```sh
   git checkout -b feature-branch
   ```
3. Make your changes and commit them:
   ```sh
   git commit -m "Description of changes"
   ```
4. Push to the branch:
   ```sh
   git push origin feature-branch
   ```
5. Create a pull request.

## Contact

For any questions or suggestions, please contact dhruv.modi2345@gmail.com.
