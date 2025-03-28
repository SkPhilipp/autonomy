#!/usr/bin/env python3
import os
import sys
import json
import subprocess
import re
from datetime import datetime
from mcp.server.fastmcp import FastMCP
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("workflow")


class Workflow:
    def __init__(self, working_dir):
        self.working_dir = working_dir

        # Check if gh CLI is installed
        if not self._command_exists("gh"):
            logger.error("GitHub CLI (gh) is not installed. Please install it first:")
            logger.error("https://cli.github.com/manual/installation")
            sys.exit(1)

        try:
            self.run(["gh", "auth", "status"])
        except subprocess.CalledProcessError:
            logger.error("Please authenticate with GitHub first using: gh auth login")
            sys.exit(1)

    def _command_exists(self, cmd):
        """Check if a command exists in the system PATH"""
        return (
            subprocess.call(
                ["which", cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            == 0
        )

    def run(self, cmd, check=True):
        """Run a command and return its output"""
        logger.info(f"Running: {' '.join(cmd)}")

        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=check,
            cwd=self.working_dir,
        )

        output_stdout = result.stdout.strip()
        output_stderr = result.stderr.strip()

        logger.info(f"Output: {output_stdout}")
        logger.info(f"Error: {output_stderr}")

        output = output_stdout + "\n" + output_stderr
        max_output_length = 50000
        if len(output) > max_output_length:
            truncated = output[:max_output_length]
            logger.info(
                f"Output truncated from {len(output)} to {max_output_length} characters"
            )
            return truncated + "\n... [output truncated]"

        return output
