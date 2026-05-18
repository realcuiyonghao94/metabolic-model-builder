"""
CarveMe Demonstration - Genome-scale Metabolic Model Reconstruction
"""
import carveme
from reframed import CBModel
import cobra

print("=" * 60)
print("CarveMe Demo - Metabolic Model Reconstruction")
print("=" * 60)

print(f"\nCarveMe version: {carveme.__version__}")
print("\n✓ CarveMe is successfully installed!")
print("✓ Reframed (dependency) is available")
print("✓ COBRApy (dependency) is available")

print("\n" + "=" * 60)
print("CarveMe Capabilities:")
print("=" * 60)

capabilities = [
    "1. Reconstruct genome-scale metabolic models from FASTA sequences",
    "2. Automatic gene annotation and pathway reconstruction",
    "3. Integration with BiGG database for metabolic reactions",
    "4. Export models in SBML format",
    "5. Compatible with COBRApy for constraint-based FBA",
    "6. Gene-to-protein-to-reaction (GPR) association"
]

for cap in capabilities:
    print(f"  {cap}")

print("\n" + "=" * 60)
print("Next Steps:")
print("=" * 60)

steps = [
    "1. Prepare your genome in FASTA format",
    "2. Download BiGG database: carveme download -d bigg",
    "3. Build model: carveme build -g genome.fasta -o model.xml",
    "4. Analyze model using COBRApy or reframed",
    "5. Perform FBA, FVA, or pathway analysis"
]

for step in steps:
    print(f"  {step}")

print("\n" + "=" * 60)
print("Example Python Usage:")
print("=" * 60)

example_code = """
# Import necessary modules
from cobra import Model, Reaction, Metabolite
from reframed import CBModel

# Create a simple metabolic model
model = Model('example_model')

# Add reactions and metabolites
atp = Metabolite('atp_c', compartment='c')
adp = Metabolite('adp_c', compartment='c')
pi = Metabolite('pi_c', compartment='c')

reaction = Reaction('ATP_hydrolysis')
reaction.add_metabolites({atp: -1, adp: 1, pi: 1})
model.add_reactions([reaction])

# Export model
cobra.io.write_sbml_model(model, 'example.xml')
"""

print(example_code)

print("\n✓ Demo completed successfully!")
