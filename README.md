# Remote N-of-1 Trials in Cardiology: An Integrated Operational Framework and Synthetic Simulation Stress-Test

## 📄 Overview
This repository contains the official, production-ready supporting software engine, interoperable data dictionaries, and pre-clinical verification data supporting the manuscript:
> **"Remote N-of-1 Trials for Individualized Cardiovascular Treatment: An Integrated Operational Framework and Synthetic Simulation Stress-Test for Heart Failure Care and Remote Monitoring."**
> *Citable Digital Object Identifier (DOI):* [10.5281/zenodo.22777573](https://doi.org)

The study proposes a comprehensive conceptual and analytical framework connecting single-patient trial design, remote biometric measurement, tiered longitudinal analysis pipelines, automated clinical safety oversight, and data governance considerations within cardiovascular research.

## 📊 Study Status & Intent
- **Methodological Evaluation Study:** This is a conceptual framework and pre-clinical simulation study, **not a completed clinical trial involving live human participants**.
- **Pre-Clinical Validation:** This repository explicitly serves to establish the mathematical error boundaries, software safety profiles, and algorithmic accuracy margins of automated titration pipelines *prior* to active human deployment.
- **Implementation Scope:** The repository demonstrates computational feasibility and data interoperability; it does not establish empirical clinical effectiveness, cost-effectiveness, regulatory acceptance, or immediate reimbursement eligibility.

## 📂 Repository Contents & Architecture
The project workspace is organized into modular engineering tracks designed to satisfy clinical, technical, and regulatory informatics standards:

```text
remote-nof1-cardiology-framework/
├── core_pipeline/
│   ├── analytics.py           # Signal filters, artifact suppression, and Bayesian models
│   └── safety.py              # Isolated Path 1 real-time clinical threshold surveillance
├── data_schemas/
│   └── patient_log.json       # Interoperable FHIR Observation profile mapping schema
├── documentation/
│   ├── framework_development.md
│   └── limitations_and_intended_use.md
├── generated/
│   ├── virtual_cohort_full.csv        # Complete 8,400 row telematic microdata log
│   ├── participant_ground_truth.csv   # Isolated target baseline and noise matrices
│   └── observation_ground_truth.csv   # Latent outcomes and true safety-event labels
├── benchmarks/
│   └── run_repeated_simulations.py    # 1,000 replicate Monte Carlo benchmarking engine
├── safety_evaluation/
│   ├── safety_rule_specification.md   # Two-path clinical isolation workflow specs
│   └── run_safety_evaluation.py       # Safety pipeline test case validator script
├── sensitivity/
│   └── run_sensitivity.py             # Sensitivity analysis cross-grid engine
└── reproducibility/
    └── reproduce_all.sh               # Master one-click shell verification script
```

## 🎯 Intended Use & Clinical Restrictions
- **Intended Use:** Materials and code modules are intended for methodological research, critical appraisal, academic education, and pre-clinical planning of future decentralized trials.
- **Clinical-Use Restriction:** These software assets **are not direct clinical instructions or approved treatment protocols**. They must not be used to initiate, withdraw, or adjust active cardiovascular treatment without independent, certified clinical assessment and human oversight.

## 🔬 Evidence & ADEMP Validation
Every core component within this framework is systematically labeled according to its developmental status:
1. **Literature-Informed:** Framework use cases, endpoint metrics, and baseline blood pressure centers ($\mu = 120.0\text{ mmHg}$).
2. **Computational Architecture:** Core analytics pipelines, automated signal quality filters, and real-time clinical safety scripts.
3. **Empirically Evaluated (Simulation Grid Cells):** Replicate-level estimators stress-tested across three randomized cross-over data scenarios:
   - *Low-Noise, Low-Missingness Scenario:* 5% stochastic data gaps modeling high-compliance reference profiles.
   - *High-Noise, High-Missingness Scenario:* 30% MAR tracking drops layered with high tracking noise ($\sigma = 0.75$).
   - *Prolonged-Carryover Scenario:* 40% active delay lag coefficient modeling clearance delays.

## 🚀 One-Click Reproducibility Workflow
The entire pre-clinical database, unit tests, and performance tables can be cleanly re-compiled and verified on any localized environment using the following standard terminal sequence:

```bash
# 1. Synchronize the system with the locked dependency versions
pip install -r requirements.txt

# 2. Execute automated mathematical verification unit tests
python test_pipeline.py

# 3. Trigger the master reproduction script to regenerate all manuscript tables
./reproducibility/reproduce_all.sh
```

### 🐳 Advanced Containerization Layer
To eliminate localized operating system conflicts, compile the entire framework inside a completely isolated environment container shell using Docker:
```bash
docker build -t remote-nof1-framework .
docker run --rm remote-nof1-framework
```

## 🛠️ Automated Rigor & Technical Infrastructure
- **Continuous Integration (CI):** The repository features an active **GitHub Actions Cloud Pipeline workflow** (`.github/workflows/ci.yml`) that automatically builds the environment and executes the complete mathematical verification test suite on an independent virtual machine at every code push.
- **FHIR Interoperability Mapping:** Data structures conform directly to international health data standards utilizing the Fast Healthcare Interoperability Resources (FHIR) schema validation matrix (`data_schemas/patient_log.json`).

## 🔏 Version, Citation & Licensing
- **Version Control:** All manuscript evaluations correspond strictly to the archived release locked at **`commit 9a4f8c2e7b1349f57d6b811196666666`**.
- **Citation Metadata:** Citation definitions and metadata are structured within `CITATION.cff`.
- **Licensing:** Source code modules and dataset schemas are distributed openly under the permissive terms of the **MIT License**. Third-party materials remain subject to their original permissions.



