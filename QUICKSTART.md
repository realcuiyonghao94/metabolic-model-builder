# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### 1. Clone the Repository

```bash
git clone https://github.com/realcuiyonghao94/metabolic-model-builder.git
cd metabolic-model-builder
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Download CarveMe Database (Optional)

For full genome reconstruction capability:

```bash
carveme download -d bigg
```

### 4. Run the App

```bash
streamlit run metabolic_model_app.py
```

The app will open in your browser at `http://localhost:8501`

---

## 📖 Usage Tutorial

### Building Your First Model

1. **Open the App** → Browser shows interactive interface
2. **Select Organism** → Choose from E. coli, C. glutamicum, or Custom
3. **Configure Options** → Set organism name, ID, and parameters
4. **Build Model** → Click "Build Model" button
5. **Download** → Export SBML XML file

### Advanced Usage

#### Custom Organism Model

```python
from cobra import Model, Reaction, Metabolite
from cobra.io import write_sbml_model

# Create model
model = Model('my_organism')

# Add metabolites and reactions
glucose = Metabolite('glc__D_c', compartment='c')
# ... add reactions ...

# Save
write_sbml_model(model, 'my_model.xml')
```

#### Load and Analyze Model

```python
from cobra import io

# Load model
model = io.read_sbml_model('model.xml')

# Run FBA
solution = model.optimize()
print(f"Growth: {solution.objective_value}")

# Change objective
model.objective = 'EX_product'
solution = model.optimize()
```

---

## 🎯 Common Tasks

### View Model Statistics

```python
model = io.read_sbml_model('model.xml')
print(f"Reactions: {len(model.reactions)}")
print(f"Metabolites: {len(model.metabolites)}")
print(f"Genes: {len(model.genes)}")
```

### Export Model to Different Formats

```python
from cobra.io import write_sbml_model, write_json_model

# SBML (standard)
write_sbml_model(model, 'model.xml')

# JSON (lightweight)
write_json_model(model, 'model.json')
```

### Perform Sensitivity Analysis

```python
from cobra.flux_analysis import sensitivity_analysis

# Knockout sensitivity
sensitivities = sensitivity_analysis(model, 'knockouts')
```

---

## 🔗 Repository Links

- **GitHub**: https://github.com/realcuiyonghao94/metabolic-model-builder
- **Streamlit Cloud**: https://share.streamlit.io/realcuiyonghao94/metabolic-model-builder
- **Issues**: https://github.com/realcuiyonghao94/metabolic-model-builder/issues

---

## 💡 Tips & Tricks

1. **Save models regularly** - Download after each build
2. **Use template models** - Start with iML1515 or iAF1260
3. **Validate models** - Check for blocked reactions
4. **Export for visualization** - Load in Escher or other tools

---

## 🆘 Troubleshooting

### App Won't Start
```bash
# Verify installation
pip list | grep streamlit

# Reinstall if needed
pip install --upgrade streamlit
```

### CarveMe Not Found
```bash
# Install CarveMe
pip install carveme

# Verify installation
python -c "import carveme; print(carveme.__version__)"
```

### Permission Denied (Windows)
```powershell
# Run PowerShell as Administrator
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 📚 Learning Resources

- [COBRApy Documentation](https://cobrapy.readthedocs.io/)
- [CarveMe Paper](https://www.microbiologyresearch.org/content/journal/mgen/10.1099/mgen.0.000155)
- [SBML Format](http://sbml.org/)
- [Metabolic Engineering](https://en.wikipedia.org/wiki/Metabolic_engineering)

---

## 💬 Need Help?

1. Check the [README.md](README.md)
2. Review [DEPLOYMENT.md](DEPLOYMENT.md)
3. Open an issue on GitHub
4. Send an email to realcuiyonghao94@github.com

---

**Happy modeling! 🧬**
