#!/bin/bash
python3 <<EOF
import os
import requests
import datetime
import subprocess
from xml.etree import ElementTree as ET

# Nexus configurations
nexus_url = "http://18.61.157.144:8081/repository/billing-releases-timestamp/com/drucare/billing/"
artifact_id = "billing"

# Fetch the current version from pom.xml
tree = ET.parse("pom.xml")
root = tree.getroot()
namespace = {"m": "http://maven.apache.org/POM/4.0.0"}

# Extract groupId, artifactId, and version from pom.xml
group_id = root.find("m:groupId", namespace).text
artifact_id = root.find("m:artifactId", namespace).text
base_version = root.find("m:version", namespace).text

# Generate a new version with timestamp for each build
timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M")
new_version = f"{base_version}-{timestamp}"

# Temporarily set the new timestamped version with Maven
subprocess.run(["mvn", "versions:set", f"-DnewVersion={new_version}"], check=True)

# Deploy the artifact to Nexus using Maven
deploy_result = subprocess.run(["mvn", "clean", "deploy"], check=True)

# Revert the version in pom.xml back to the original version after deployment
subprocess.run(["mvn", "versions:revert"], check=True)

# Final message based on the deployment result
if deploy_result.returncode == 0:
    print(f"Successfully deployed version {new_version} to Nexus")
else:
    print("Failed to deploy to Nexus")
EOF
