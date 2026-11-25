# Indeks Aset Publikasi

Seluruh aset dihasilkan dari run reproduction-001 tanpa training. Path sumber relatif terhadap run; output relatif terhadap publication_assets.

| ID | File | Sumber | Bagian |
|---|---|---|---|
| fig_01_methodology_flow | [PNG](figures/fig_01_methodology_flow.png), [SVG](figures/fig_01_methodology_flow.svg) | hasil/manifest_data.json; 01_Audit_dan_Split.ipynb cell 2/4/6; 02_Eksperimen_Utama.ipynb cell 3–6 | Methods |
| fig_02_experimental_scenarios | [PNG](figures/fig_02_experimental_scenarios.png), [SVG](figures/fig_02_experimental_scenarios.svg) | analysis/performance_comparison.csv; eksperimen_utama/actual_parameters.json | Methods |
| fig_03_f1_comparison | [PNG](figures/fig_03_f1_comparison.png), [SVG](figures/fig_03_f1_comparison.svg) | eksperimen_utama/metrik_utama.csv; analysis/performance_comparison.csv | Results |
| fig_04_recall_comparison | [PNG](figures/fig_04_recall_comparison.png), [SVG](figures/fig_04_recall_comparison.svg) | eksperimen_utama/metrik_utama.csv; analysis/performance_comparison.csv | Results |
| fig_05_fpr_comparison | [PNG](figures/fig_05_fpr_comparison.png), [SVG](figures/fig_05_fpr_comparison.svg) | eksperimen_utama/metrik_utama.csv; analysis/performance_comparison.csv | Results |
| fig_06_scenario_deltas | [PNG](figures/fig_06_scenario_deltas.png), [SVG](figures/fig_06_scenario_deltas.svg) | analysis/scenario_deltas.csv | Results |
| fig_07a_confusion_matrix_counts | [PNG](figures/fig_07a_confusion_matrix_counts.png), [SVG](figures/fig_07a_confusion_matrix_counts.svg) | eksperimen_utama/metrik_utama.csv; analysis/performance_comparison.csv; analysis/error_analysis.csv | Results |
| fig_07b_confusion_matrix_normalized | [PNG](figures/fig_07b_confusion_matrix_normalized.png), [SVG](figures/fig_07b_confusion_matrix_normalized.svg) | eksperimen_utama/metrik_utama.csv; analysis/performance_comparison.csv; analysis/error_analysis.csv | Results |
| fig_08a_training_time | [PNG](figures/fig_08a_training_time.png), [SVG](figures/fig_08a_training_time.svg) | analysis/efficiency_analysis.csv; eksperimen_utama/metrik_utama.csv; analysis/performance_comparison.csv | Results |
| fig_08b_inference_time | [PNG](figures/fig_08b_inference_time.png), [SVG](figures/fig_08b_inference_time.svg) | analysis/efficiency_analysis.csv; eksperimen_utama/metrik_utama.csv; analysis/performance_comparison.csv | Results |
| fig_09_f1_efficiency_tradeoff | [PNG](figures/fig_09_f1_efficiency_tradeoff.png), [SVG](figures/fig_09_f1_efficiency_tradeoff.svg) | eksperimen_utama/metrik_utama.csv; analysis/performance_comparison.csv; analysis/efficiency_analysis.csv | Results |
| fig_10_url_structure_distribution | [PNG](figures/fig_10_url_structure_distribution.png), [SVG](figures/fig_10_url_structure_distribution.svg) | hasil/audit_struktur_mentah.csv | Discussion |
| fig_11_domain_overlap | [PNG](figures/fig_11_domain_overlap.png), [SVG](figures/fig_11_domain_overlap.svg) | hasil/irisan_domain.csv | Results |
| fig_12_roc_curves | [PNG](figures/fig_12_roc_curves.png), [SVG](figures/fig_12_roc_curves.svg) | eksperimen_utama/predictions/*_uji.csv.gz; eksperimen_utama/metrik_utama.csv; analysis/performance_comparison.csv | Results |
| table_01_dataset_summary | [CSV](tables/table_01_dataset_summary.csv), [Markdown](tables/table_01_dataset_summary.md) | hasil/manifest_data.json; hasil/audit_struktur_mentah.csv | Methods |
| table_02_experimental_scenarios | [CSV](tables/table_02_experimental_scenarios.csv), [Markdown](tables/table_02_experimental_scenarios.md) | eksperimen_utama/actual_parameters.json; analysis/performance_comparison.csv | Methods |
| table_03_split_distribution | [CSV](tables/table_03_split_distribution.csv), [Markdown](tables/table_03_split_distribution.md) | hasil/ringkasan_split.csv | Methods |
| table_04_domain_overlap | [CSV](tables/table_04_domain_overlap.csv), [Markdown](tables/table_04_domain_overlap.md) | hasil/irisan_domain.csv | Results |
| table_05_model_parameters | [CSV](tables/table_05_model_parameters.csv), [Markdown](tables/table_05_model_parameters.md) | eksperimen_utama/actual_parameters.json; eksperimen_utama/manifest_eksperimen.json | Methods |
| table_06_test_performance | [CSV](tables/table_06_test_performance.csv), [Markdown](tables/table_06_test_performance.md) | eksperimen_utama/metrik_utama.csv; analysis/performance_comparison.csv | Results |
| table_07_scenario_deltas | [CSV](tables/table_07_scenario_deltas.csv), [Markdown](tables/table_07_scenario_deltas.md) | analysis/scenario_deltas.csv | Results |
| table_08_confusion_matrix | [CSV](tables/table_08_confusion_matrix.csv), [Markdown](tables/table_08_confusion_matrix.md) | eksperimen_utama/metrik_utama.csv; analysis/performance_comparison.csv; analysis/error_analysis.csv | Results |
| table_09_computational_efficiency | [CSV](tables/table_09_computational_efficiency.csv), [Markdown](tables/table_09_computational_efficiency.md) | analysis/efficiency_analysis.csv | Results |
| table_10_reproducibility | [CSV](tables/table_10_reproducibility.csv), [Markdown](tables/table_10_reproducibility.md) | eksperimen_utama/historical_comparison_full.csv; eksperimen_utama/manifest_eksperimen.json | Discussion |
