import jdk
import os
import sys

# Install OpenJDK 17, a common Long-Term Support (LTS) version.
# The install() function returns the path to the JAVA_HOME directory.
print("Installing OpenJDK 17...")
java_home = jdk.install("17")
print(f"OpenJDK 17 installed at: {java_home}")

# Print the JAVA_HOME path to standard output so it can be captured by the shell script.
# This is the critical output that connects this script to the build process.
sys.stdout.write(java_home)


