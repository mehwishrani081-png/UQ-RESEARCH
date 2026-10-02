# Phase 1 — Novelty/Baseline Reading Table

**Reading date:** 2026-10-03  
**Purpose:** structured extraction for the CoBra related-work and novelty analysis.  
**Rule:** entries below distinguish what the cited source explicitly states from project-level implications. No scientific result from this table is treated as a CoBra result.

| Paper | Task (classification/segmentation) | Reference used (single mask / majority vote / multiple raters) | Guarantee type (marginal coverage / risk control / none) | Datasets used | What it explicitly does NOT handle | Why it matters to CoBra |
|---|---|---|---|---|---|---|
| Angelopoulos & Bates, *A Gentle Introduction to Conformal Prediction and Distribution-Free Uncertainty Quantification* (2022) | Classification and structured outputs, including segmentation examples | Standard CP formulation uses a held-out ground-truth label/target; it is not a multi-rater framework | Marginal, finite-sample coverage under exchangeability | Tutorial/examples span classification, computer vision, NLP and other settings; it is a tutorial rather than a single LIDC experiment | Standard split CP does not by itself resolve ambiguous/multi-expert ground truth or remove the exchangeability requirement | Supplies the baseline split-CP logic, calibration quantile correction and exchangeability assumption against which CoBra's multi-rater setting must be distinguished. |
| Davenport, *Conformal confidence sets for biomedical image segmentation* (arXiv:2410.03406, 2024) | Segmentation | Single ground-truth mask per calibration image | Marginal inner/outer confidence coverage for the whole mask | 1,798 polyp images assembled from five open-source datasets; PraNet scores | Does not model multiple expert annotations or ambiguous ground truth; experiments are not LIDC-IDRI | Direct B1 baseline: calibrates maxima of transformed scores inside/outside the truth; identity scores give tight inner sets while distance-transformed scores give tighter outer sets. |
| Mossina & Friedrich, *Conformal Prediction for Image Segmentation Using Morphological Prediction Sets* (MICCAI 2025) | Binary segmentation | Single expert ground-truth mask in the calibration formulation | Marginal coverage of a user-selected fraction of ground-truth pixels | Medical imaging applications including WBC, UniverSeg and polyp experiments reported in the paper | Does not distinguish aleatoric vs epistemic uncertainty and does not solve multi-rater aggregation; calibration assumes held-out exchangeable data | Direct B2 baseline: prediction sets are nested morphological dilations; the nonconformity score is the smallest number of dilations reaching coverage ratio tau, then the corrected empirical quantile determines the inference margin. |
| Angelopoulos et al., *Conformal Risk Control* (ICLR 2024) | General prediction/risk control, with computer-vision segmentation examples | Standard single target/ground-truth risk evaluation | Risk control: expected value of a bounded monotone loss; standard CP is recovered as a special case | Computer-vision and NLP worked examples, including false-negative, graph-distance and token-level F1 applications | CRC requires the loss to be monotone in the calibration parameter; it is not itself a multi-rater/ambiguous-ground-truth solution | Direct B3 basis: CoBra can formulate coverage/error as a monotone risk and use CRC where its monotonicity assumptions genuinely hold. |
| Angelopoulos et al., *Learn then Test: Calibrating Predictive Algorithms to Achieve Risk Control* (2022/Annals of Applied Statistics 2025) | Classification, segmentation, outlier detection and other prediction problems | Standard calibration targets with observed labels; not designed specifically for multiple expert masks | Risk control through multiple hypothesis testing; finite-sample control | Worked examples in computer vision and tabular medical data | Does not itself provide a multi-rater segmentation guarantee; its fixed-sequence construction needs a correctly specified family of hypotheses and valid p-values | Basis for T3: candidate lambda values become hypotheses H_lambda: R(lambda)>alpha; fixed-sequence testing can search from stricter to looser candidates while controlling the testing error. The paper gives a hybrid Hoeffding-Bentkus p-value for bounded losses. |
| Stutz et al., *Conformal prediction under ambiguous ground truth* (TMLR 2023; arXiv:2307.09302) | Classification, including multi-label extensions | Multiple expert labels aggregated into a non-degenerate distribution rather than a single voted label | Coverage with respect to the aggregated label distribution P_agg; Monte Carlo CP gives a 1-2alpha-type guarantee in the p-value construction | Synthetic toy data and CIFAR-10H/skin-condition classification case study | It is not an image-segmentation method and does not provide a spatial/mask-specific multi-rater guarantee for LIDC | Critical ambiguity baseline: shows why majority-vote calibration can under-cover expert uncertainty and introduces Monte Carlo CP by sampling pseudo-labels from an expert-derived P_agg. |
| Gauthier, Bach & Jordan, *E-Values Expand the Scope of Conformal Prediction* (arXiv:2503.13050, 2025) | Classification/general CP, including ambiguous ground truth | Multiple expert labels/annotations represented through an aggregated conditional distribution | 1-alpha coverage is established for the e-value ambiguous-ground-truth construction | CIFAR-10/CIFAR-10H examples and other conformal-e-prediction case studies | It does not provide a ready-made LIDC multi-rater segmentation implementation; adapting it to spatial masks requires a new, verified construction | Stretch target T2: the paper explicitly contrasts the 1-2alpha p-value approach for ambiguous ground truth with an e-value construction that can recover 1-alpha coverage. |
| Kahl et al., *ValUES: A Framework for Systematic Validation of Uncertainty Estimation in Semantic Segmentation* (ICLR 2024) | Segmentation | Multiple raters on LIDC are used as an aleatoric-uncertainty reference; four-rater LIDC subset | No conformal guarantee; empirical UQ validation | LIDC-IDRI, GTA5/Cityscapes, plus a toy dataset | It is not a conformal calibration framework and does not combine AU and EU models in the way later Christensen et al. study; its focus is systematic empirical UQ validation and downstream tasks | Establishes a strong prior benchmark for LIDC multi-rater uncertainty, including aggregation choices. A CoBra novelty claim cannot simply be another broad LIDC uncertainty audit because this literature already provides systematic empirical auditing. |
| Christensen et al., *Rethinking Uncertainty Quantification and Entanglement in Image Segmentation* (arXiv:2603.18792, 2026) | Segmentation | Four LIDC annotations per selected 2D slice; multi-annotator reference | No conformal guarantee; empirical UQ/entanglement evaluation | LIDC-IDRI and Cháks.u IMAGE; LIDC uses 15,096 four-annotation slices and patient-level 60/20/20 split | Does not provide a conformal coverage guarantee or a multi-rater conformal calibration method; it studies AU/EU/TU combinations and their entanglement | Directly closes much of the old “compare MC Dropout/ensemble/ProbUNet/soft-label uncertainty on LIDC” space. Crucially, the paper reports that LIDC disagreement is dominated by nodule presence/absence rather than boundary delineation, which changes what a meaningful CoBra novelty claim must address. |

## Source-derived technical notes

### Split conformal baseline
Angelopoulos & Bates describe conformal prediction as distribution-free under exchangeability. For a calibration set of size n, the finite-sample correction accounts for the additional test point; a common formulation uses the empirical quantile at ceil((n+1)(1-alpha))/n. The central CoBra implication is that patient-level dependence must be handled before applying the exchangeability argument to image/slice-derived samples.

### Davenport B1
Davenport defines inner and outer confidence functions so that, marginally, the inner set is contained in the true mask and the true mask is contained in the outer set. Calibration is based on maxima of transformed score values within and outside the ground truth. The paper defines a signed distance transform using distance to the predicted-mask boundary; in its polyp experiment it selected identity/original scores for inner sets and Euclidean distance-transformed scores for outer sets. The paper explicitly recommends an independent learning set for choosing score transformations.

### Mossina & Friedrich B2
The prediction sets are nested dilations: C_lambda(X) = delta_B^lambda(Yhat). The nonconformity score is the smallest integer lambda for which at least tau of the ground-truth pixels are contained. The corrected calibration value is the ceil((n+1)(1-alpha))-th largest score. Their proof uses the nested-set property/monotone binary loss, and the paper explicitly warns that selecting the morphological operation/structuring element using the calibration set would violate the assumptions needed for conformal validity.

### CRC B3
CRC controls the expected value of a bounded monotone loss. The essential structural condition is monotonicity of the loss as the prediction-set parameter changes. For segmentation, a false-negative proportion can be monotone when increasing the prediction set only adds pixels. CoBra must test this property rather than assume it.

### LTT / T3
LTT reframes risk calibration as multiple testing. For candidate parameters lambda_j, hypotheses are of the form H_j: R(lambda_j) > alpha; rejecting a null identifies a candidate whose risk is controlled. The published Learn-then-Test paper uses fixed-sequence testing and a hybrid Hoeffding-Bentkus p-value for bounded losses. The exact HB expression in the paper is based on the empirical risk and the binomial tail, so CoBra must implement and unit-test the exact formula rather than an approximation.

### Ambiguous ground truth
Stutz et al. show that majority-vote calibration targets a voted distribution rather than the underlying ambiguous label distribution. Their Monte Carlo CP samples multiple pseudo-labels from an expert-derived aggregated distribution. Gauthier et al. later give an e-value construction for the same ambiguous-ground-truth setting and establish a 1-alpha coverage guarantee for that construction.

## Why the faithfulness-audit-alone framing is saturated

A CoBra novelty claim framed only as “performing a faithfulness/UQ audit of segmentation uncertainty on LIDC” would overlap substantially with established work. ValUES already provides a systematic validation framework for semantic-segmentation uncertainty, explicitly using four-rater LIDC masks as an aleatoric reference and evaluating uncertainty measures, prediction models and aggregation strategies across downstream tasks. Christensen et al. subsequently build on ValUES and evaluate 4 x 5 aleatoric/epistemic model combinations on LIDC and Cháks.u IMAGE, including ambiguity modeling, OOD detection and calibration. Their LIDC protocol uses 2D slices with four annotations and a patient-level split, and they explicitly report that LIDC disagreement is dominated by nodule presence/absence rather than boundary delineation. Therefore, a defensible CoBra contribution needs to move beyond another descriptive uncertainty/faithfulness audit and instead make a clearly specified methodological contribution around multi-rater conformal guarantees, aggregation/target construction, risk control, or another capability not supplied by these works. This is a literature-based framing inference, not a claim made verbatim by either paper.

## Scope distinction

- Davenport: spatial marginal inner/outer mask coverage, single ground truth.
- Mossina–Friedrich: morphological nested-set coverage, single expert ground truth.
- CRC: expected risk control for bounded monotone losses.
- LTT: multiple-testing formulation for risk-control calibration.
- Stutz: ambiguous labels via Monte Carlo p-value conformal prediction.
- Gauthier–Bach–Jordan: e-value conformal prediction, including ambiguous ground truth.
- ValUES: empirical uncertainty-method validation, not conformal guarantees.
- Christensen et al.: empirical AU/EU entanglement benchmark, not conformal guarantees.
- Angelopoulos–Bates tutorial: foundational split-CP framework.

## Primary sources

1. Angelopoulos & Bates — arXiv:2107.07511.
2. Davenport — arXiv:2410.03406.
3. Mossina & Friedrich — arXiv:2503.05618 / MICCAI 2025.
4. Angelopoulos et al. — arXiv:2208.02814 / ICLR 2024.
5. Angelopoulos et al. — arXiv:2110.01052 / Annals of Applied Statistics.
6. Stutz et al. — arXiv:2307.09302 / TMLR.
7. Gauthier et al. — arXiv:2503.13050.
8. Kahl et al. — ICLR 2024, ValUES.
9. Christensen et al. — arXiv:2603.18792.
