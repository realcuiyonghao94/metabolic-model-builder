"""
Interactive Metabolic Model Builder - Streamlit Web App
Build customized genome-scale metabolic models with a user-friendly interface
"""

import streamlit as st
import pandas as pd
from pathlib import Path
from cobra import Model, Reaction, Metabolite
from cobra.io import write_sbml_model, read_sbml_model
import tempfile
import os

# Page configuration
st.set_page_config(
    page_title="CarveMe Model Builder",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding-top: 0rem;
    }
    .title-text {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2ca02c;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

# Title
st.markdown('<p class="title-text">🧬 CarveMe Metabolic Model Builder</p>', unsafe_allow_html=True)
st.markdown("Build customized genome-scale metabolic models interactively")
st.divider()

# Initialize session state
if 'model' not in st.session_state:
    st.session_state.model = None
if 'reactions_list' not in st.session_state:
    st.session_state.reactions_list = []

# Sidebar
with st.sidebar:
    st.markdown("### 🔧 Configuration")
    
    # Step 1: Organism Information
    st.markdown("#### Step 1: Organism Information")
    organism_name = st.text_input(
        "Organism Name",
        value="My_Organism",
        help="Enter the organism name (e.g., E_coli_MG1655)"
    )
    
    organism_description = st.text_area(
        "Description (Optional)",
        help="Add notes about the organism"
    )
    
    # Step 2: Model Composition
    st.markdown("#### Step 2: Select Pathways")
    
    central_carbon = st.multiselect(
        "Central Carbon Metabolism",
        options=["Glycolysis", "Pentose Phosphate Pathway", "TCA Cycle"],
        default=["Glycolysis", "Pentose Phosphate Pathway", "TCA Cycle"],
        help="Select metabolic pathways"
    )
    
    secondary_metabolism = st.multiselect(
        "Secondary Metabolism",
        options=["Amino Acid Biosynthesis", "Fatty Acid Synthesis", "Nucleotide Synthesis"],
        default=["Amino Acid Biosynthesis"],
        help="Select secondary pathways"
    )
    
    # Step 3: Objective Function
    st.markdown("#### Step 3: Objective Function")
    objective_options = {
        "Biomass": "BIOMASS",
        "Growth": "GROWTH",
        "Glutamate Production": "EX_glu__L",
        "Lysine Production": "EX_lys__L",
        "Ethanol Production": "EX_etoh",
        "ATP Synthesis": "ATPM"
    }
    
    objective_choice = st.selectbox(
        "Select Objective",
        options=list(objective_options.keys()),
        help="Choose the metabolic objective to optimize"
    )
    
    objective_direction = st.radio(
        "Optimization Direction",
        options=["Maximize", "Minimize"],
        help="Choose optimization direction"
    )

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<p class="section-header">📋 Model Setup</p>', unsafe_allow_html=True)
    
    # Input method selection
    input_method = st.radio(
        "Choose Input Method",
        options=["Build from Presets", "Upload Genome FASTA", "Custom Define"],
        horizontal=True
    )
    
    if input_method == "Build from Presets":
        st.markdown("##### Predefined Organisms")
        
        preset_organisms = {
            "E. coli MG1655": {
                "model_id": "E_coli_MG1655",
                "description": "Escherichia coli K-12 substr. MG1655",
                "genome_size": "4.6 Mb",
                "genes": "~4300"
            },
            "C. glutamicum ATCC 13032": {
                "model_id": "C_glutamicum_ATCC13032",
                "description": "Corynebacterium glutamicum ATCC 13032",
                "genome_size": "3.3 Mb",
                "genes": "~3000"
            },
            "B. subtilis 168": {
                "model_id": "B_subtilis_168",
                "description": "Bacillus subtilis subsp. subtilis str. 168",
                "genome_size": "4.2 Mb",
                "genes": "~4100"
            },
            "S. cerevisiae S288C": {
                "model_id": "S_cerevisiae_S288C",
                "description": "Saccharomyces cerevisiae S288C",
                "genome_size": "12.1 Mb",
                "genes": "~6000"
            }
        }
        
        selected_preset = st.selectbox(
            "Select Organism",
            options=list(preset_organisms.keys())
        )
        
        preset_info = preset_organisms[selected_preset]
        col_a, col_b = st.columns(2)
        
        with col_a:
            st.info(f"**Model ID:** {preset_info['model_id']}\n\n**Genome Size:** {preset_info['genome_size']}")
        
        with col_b:
            st.info(f"**Description:** {preset_info['description']}\n\n**Genes:** {preset_info['genes']}")
        
        organism_name = preset_info['model_id']
    
    elif input_method == "Upload Genome FASTA":
        st.markdown("##### Upload Genome Sequence")
        uploaded_file = st.file_uploader("Choose a FASTA file", type=['fasta', 'fa', 'fna', 'txt'])
        
        if uploaded_file is not None:
            st.success(f"✓ File uploaded: {uploaded_file.name}")
            st.info(f"File size: {uploaded_file.size / 1024:.2f} KB")
    
    else:  # Custom Define
        st.markdown("##### Define Model Manually")
        custom_reactions = st.number_input(
            "Number of Reactions to Add",
            min_value=1,
            max_value=20,
            value=5
        )

with col2:
    st.markdown('<p class="section-header">📊 Summary</p>', unsafe_allow_html=True)
    
    summary_data = {
        "Parameter": [
            "Organism",
            "Central Carbon",
            "Secondary Metabolism",
            "Objective",
            "Direction"
        ],
        "Value": [
            organism_name,
            ", ".join(central_carbon) if central_carbon else "None",
            ", ".join(secondary_metabolism) if secondary_metabolism else "None",
            objective_choice,
            objective_direction
        ]
    }
    
    summary_df = pd.DataFrame(summary_data)
    st.dataframe(summary_df, use_container_width=True, hide_index=True)

# Build Model Section
st.divider()
st.markdown('<p class="section-header">🔨 Model Builder</p>', unsafe_allow_html=True)

col_build_left, col_build_right = st.columns([1, 1])

with col_build_left:
    if st.button("🚀 Build Model", use_container_width=True):
        with st.spinner("Building metabolic model..."):
            try:
                # Create model
                model = Model(organism_name)
                
                # Define basic metabolites
                metabolites_dict = {
                    'glucose': Metabolite('glc__D_c', compartment='c'),
                    'pyruvate': Metabolite('pyr_c', compartment='c'),
                    'atp': Metabolite('atp_c', compartment='c'),
                    'adp': Metabolite('adp_c', compartment='c'),
                    'nadh': Metabolite('nadh_c', compartment='c'),
                    'nad': Metabolite('nad_c', compartment='c'),
                    'nadph': Metabolite('nadph_c', compartment='c'),
                    'nadp': Metabolite('nadp_c', compartment='c'),
                    'glutamate': Metabolite('glu__L_c', compartment='c'),
                    'akg': Metabolite('akg_c', compartment='c'),
                    'nh4': Metabolite('nh4_c', compartment='c'),
                }
                
                reactions_list = []
                
                # Add exchange reactions
                glc_ex = Reaction('EX_glc__D')
                glc_ex.add_metabolites({metabolites_dict['glucose']: 1})
                glc_ex.lower_bound = -10
                glc_ex.upper_bound = 0
                reactions_list.append(glc_ex)
                
                # Add pathways based on selection
                if "Glycolysis" in central_carbon:
                    glyc = Reaction('GLYCOLYSIS')
                    glyc.add_metabolites({
                        metabolites_dict['glucose']: -1,
                        metabolites_dict['pyruvate']: 2,
                        metabolites_dict['atp']: -2,
                        metabolites_dict['adp']: 2,
                    })
                    reactions_list.append(glyc)
                
                if "Pentose Phosphate Pathway" in central_carbon:
                    ppp = Reaction('PPP')
                    ppp.add_metabolites({
                        metabolites_dict['glucose']: -1,
                        metabolites_dict['nadph']: -2,
                        metabolites_dict['nadp']: 2,
                    })
                    reactions_list.append(ppp)
                
                if "TCA Cycle" in central_carbon:
                    tca = Reaction('TCA')
                    tca.add_metabolites({
                        metabolites_dict['pyruvate']: -1,
                        metabolites_dict['nadh']: -1,
                        metabolites_dict['atp']: 1,
                    })
                    reactions_list.append(tca)
                
                if "Amino Acid Biosynthesis" in secondary_metabolism:
                    aa_syn = Reaction('GLUTDT')
                    aa_syn.add_metabolites({
                        metabolites_dict['akg']: -1,
                        metabolites_dict['nh4']: -1,
                        metabolites_dict['nadph']: -1,
                        metabolites_dict['nadp']: 1,
                        metabolites_dict['glutamate']: 1,
                    })
                    reactions_list.append(aa_syn)
                    
                    glu_ex = Reaction('EX_glu__L')
                    glu_ex.add_metabolites({metabolites_dict['glutamate']: 1})
                    glu_ex.lower_bound = 0
                    glu_ex.upper_bound = 1000
                    reactions_list.append(glu_ex)
                
                # Add ATP synthesis
                atp_syn = Reaction('ATPM')
                atp_syn.add_metabolites({metabolites_dict['atp']: -1, metabolites_dict['adp']: 1})
                reactions_list.append(atp_syn)
                
                # Add reactions to model
                model.add_reactions(reactions_list)
                
                # Set objective
                model.objective = objective_options[objective_choice]
                
                # Store in session
                st.session_state.model = model
                st.session_state.reactions_list = reactions_list
                
                st.success("✓ Model built successfully!")
                
            except Exception as e:
                st.error(f"Error building model: {str(e)}")

with col_build_right:
    if st.button("🔄 Reset", use_container_width=True):
        st.session_state.model = None
        st.session_state.reactions_list = []
        st.rerun()

# Display Model Results
if st.session_state.model is not None:
    st.divider()
    st.markdown('<p class="section-header">📈 Model Results</p>', unsafe_allow_html=True)
    
    model = st.session_state.model
    
    col_result1, col_result2, col_result3, col_result4 = st.columns(4)
    
    with col_result1:
        st.metric("Reactions", len(model.reactions))
    
    with col_result2:
        st.metric("Metabolites", len(model.metabolites))
    
    with col_result3:
        st.metric("Genes", len(model.genes))
    
    with col_result4:
        st.metric("Compartments", len(model.compartments))
    
    # Display reactions table
    st.markdown("#### Reactions in Model")
    
    reactions_data = {
        "Reaction ID": [r.id for r in model.reactions],
        "Name": [r.name if r.name else r.id for r in model.reactions],
        "Formula": [list(r.metabolites.keys()).__str__()[:30] for r in model.reactions]
    }
    
    reactions_df = pd.DataFrame(reactions_data)
    st.dataframe(reactions_df, use_container_width=True, hide_index=True)
    
    # Display metabolites
    st.markdown("#### Metabolites in Model")
    
    metabolites_data = {
        "Metabolite ID": [m.id for m in model.metabolites],
        "Compartment": [m.compartment for m in model.metabolites],
        "Name": [m.name if m.name else m.id for m in model.metabolites]
    }
    
    metabolites_df = pd.DataFrame(metabolites_data)
    st.dataframe(metabolites_df, use_container_width=True, hide_index=True)
    
    # Download section
    st.divider()
    st.markdown('<p class="section-header">💾 Export Model</p>', unsafe_allow_html=True)
    
    col_down1, col_down2 = st.columns([1, 1])
    
    with col_down1:
        # Export as SBML
        sbml_content = tmpfile = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.xml')
        write_sbml_model(model, sbml_content.name)
        
        with open(sbml_content.name, 'r') as f:
            sbml_data = f.read()
        
        st.download_button(
            label="📥 Download SBML XML",
            data=sbml_data,
            file_name=f"{organism_name}_model.xml",
            mime="text/xml",
            use_container_width=True
        )
        
        os.remove(sbml_content.name)
    
    with col_down2:
        # Export as JSON
        json_data = model.to_json()
        st.download_button(
            label="📥 Download JSON",
            data=json_data,
            file_name=f"{organism_name}_model.json",
            mime="application/json",
            use_container_width=True
        )

# Footer
st.divider()
st.markdown("""
    ---
    **CarveMe Metabolic Model Builder** | Built with Streamlit
    
    - **SBML Format**: Compatible with COBRApy, Reframed, and other constraint-based modeling tools
    - **Objective**: Customize your model's optimization objective
    - **Export**: Download in multiple formats for further analysis
    
    For full genome-scale model reconstruction with CarveMe, download the complete genome and use the command-line tool.
""")
