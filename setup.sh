#!/bin/bash
set -e

# Step 1: Create a virtual environment
echo "Creating virtual environment 'myenv'..."
python -m venv myenv

# Step 2: Activate the virtual environment within the script (for setup only)
echo "Activating virtual environment for setup..."
source myenv/bin/activate

# Navigate to the project directory
cd Voice-assistant-kb

# Step 3: Install requirements
if [ -f "requirements.txt" ]; then
    echo "Installing requirements from requirements.txt..."
    pip install -r requirements.txt
else
    echo "Error: requirements.txt not found!"
    deactivate
    exit 1
fi

# Deactivate the environment (to ensure script cleanliness)
deactivate

echo "Virtual environment setup complete and requirements installed!"

# Check if .gitignore exists
if [ ! -f .gitignore ]; then
    echo "Creating .gitignore file..."
    touch .gitignore
else
    echo ".gitignore already exists."
fi

# Add 'myenv' and 'setup_env.sh' to .gitignore if not already added
if ! grep -q '^myenv$' .gitignore; then
    echo "Adding 'myenv' to .gitignore..."
    echo "myenv" >> .gitignore
fi

if ! grep -q '^setup_env.sh$' .gitignore; then
    echo "Adding 'setup_env.sh' to .gitignore..."
    echo "setup_env.sh" >> .gitignore
fi

echo ".gitignore updated successfully!"

touch .env
echo ".env" >> .gitignore