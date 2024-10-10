"""
Quickstart
==========

This example shows a quick and easy example of how to use atlasapprox to get and plot the expression of some gees in a specific organ of a specific organism.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import atlasapprox as aa

# Initialize the API
api = aa.API()

# Get the average expression of CD4 and CD8A in the human lung
expression = api.average(organism="h_sapiens", organ="lung", features=["CD4", "CD8A"])

# Plot the result
fig, ax = plt.subplots(figsize=(7, 4))
sns.heatmap(expression, ax=ax)
fig.tight_layout()
