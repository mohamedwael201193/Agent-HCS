#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

echo "--- Starting Custom Build Process ---"

# Step 1: Install the 'install-jdk' utility.
# This is a prerequisite for our Java installation script.
echo "Installing 'install-jdk' library..."
pip install install-jdk

# Step 2: Run the Python script to install the JDK and capture its output.
# The Python script will print the JAVA_HOME path to stdout.
echo "Running JDK installation script..."
JAVA_HOME_PATH=$(python build/setup_java.py)

# Step 3: Export the necessary environment variables.
# These variables are required by pyjnius to find the JVM and JDK tools.
# The 'export' command makes them available to all subsequent commands in this script.
echo "Exporting JAVA_HOME and updating PATH..."
export JAVA_HOME=$JAVA_HOME_PATH
export PATH="$JAVA_HOME/bin:$PATH"

# Step 4: Verify the Java installation (optional but recommended for debugging).
echo "Verifying Java installation..."
java -version

# Step 5: Install the project's Python dependencies.
# Now that the environment is correctly configured with a JDK,
# 'pip install' will be able to successfully build the 'pyjnius' package.
echo "Installing Python dependencies from requirements.txt..."
pip install -r requirements.txt

echo "--- Custom Build Process Finished Successfully ---"


