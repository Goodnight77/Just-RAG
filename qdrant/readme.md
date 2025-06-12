# Qdrant Vector Search Project

This project demonstrates the capabilities of Qdrant, a powerful vector similarity search engine. It processes textual data to create vector embeddings and enables efficient similarity searches.

## Project Structure

The core components of this project are organized as follows:

* `qdrant/`: This directory contains all the project files, including:
   * `Qdrant_talk.ipynb`: The Jupyter Notebook containing the main code, explanations, and instructions for running the project.
   * `ains3_0.txt`: The primary dataset used for vectorization and search operations.

## Data

The project utilizes the `ains3_0.txt` file as its source data. This file should be placed within the `qdrant` folder alongside the notebook.

## Requirements & Setup

All necessary Python libraries and dependencies are listed and installed within the `Qdrant_talk.ipynb` notebook.

To set up your environment:

1. **Clone or download** this project to your local machine.
2. Ensure `ains3_0.txt` is located in the `qdrant` folder.
3. Open `Qdrant_talk.ipynb` using Jupyter Notebook, JupyterLab, or **Google Colab**.

## Getting Started

You have a few options to run this project:

### Option 1: Local Environment (Jupyter Notebook/Lab)

1. Navigate to the `qdrant` directory.
2. Launch Jupyter Notebook/Lab:

```bash
jupyter notebook
# or
jupyter lab
```

3. Open `Qdrant_talk.ipynb`.
4. Execute each cell in the notebook. This will guide you through:
   * Setting up the Qdrant client.
   * Loading and processing the `ains3_0.txt` data.
   * Creating vector embeddings.
   * Populating a Qdrant collection.
   * Performing vector similarity searches.

### Option 2: Google Colab

You can also run this notebook directly in Google Colab, which provides a free, cloud-based Jupyter environment.

1. Open the notebook directly in Colab using this link: https://colab.research.google.com/drive/1TeZfj600xamgkM91B9mJphPAZ47F6mzC?usp=sharing
2. Once opened in Colab, you may need to upload the `ains3_0.txt` file manually to the Colab environment's file system or adjust the path in the notebook to fetch it from a public source (e.g., GitHub) if it's hosted there.
3. Execute each cell in the notebook. Colab will handle the installation of required packages automatically.

**Enjoy exploring Qdrant!**