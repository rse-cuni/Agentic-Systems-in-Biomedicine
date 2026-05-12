# Lab Values Interpreter

A Langflow agent for **medical education** that accepts raw laboratory results and returns a structured, clearly formatted interpretation — including reference ranges, abnormality flags, possible clinical patterns, and suggested next diagnostic steps.

> **Disclaimer:** All output is for educational purposes only and must not be used for clinical decision-making.

---

## Pipeline overview

![Pipeline](images/image.png)

The flow contains four components wired together:

| Component | Role |
| --------- | ---- |
| **Chat Input** | Receives the raw lab results typed by the user |
| **Prompt Template** | Injects the system prompt (reference ranges + instructions) |
| **Custom OpenAI Model** | Configures the underlying LLM (model name, API key, temperature) |
| **Language Model** | Combines the user message and system prompt, calls the model |
| **Chat Output** | Displays the formatted Markdown interpretation |

---

## What the agent does

1. Parses all numeric values from free-text input (e.g. "Hb 95 g/L, MCV 72 fL").
2. Compares each value against built-in adult reference ranges (CBC, biochemistry, lipids, coagulation, thyroid).
3. Flags results as **normal / low / high / critical** with emoji indicators (✓ 🔻 🔺 ⚠️).
4. Groups abnormalities into likely **clinical patterns** (e.g. iron-deficiency anaemia, AKI, hepatocellular injury).
5. Suggests **2–4 specific next diagnostic steps**.
6. Returns everything as a clean Markdown table + narrative, always ending with the educational disclaimer.

---

## System prompt (Prompt Template contents)

```text
You are a clinical laboratory interpretation assistant designed for medical
education. You receive raw laboratory results and produce structured
interpretations.

REFERENCE RANGES (adult, SI units unless noted):

Complete Blood Count
- Hemoglobin: M 135-175 g/L, F 120-155 g/L
- Hematocrit: M 0.40-0.52, F 0.36-0.46
- WBC: 4.0-10.0 x10^9/L
- Platelets: 150-400 x10^9/L
- MCV: 80-100 fL
- Neutrophils (abs): 2.0-7.0 x10^9/L
- Lymphocytes (abs): 1.0-3.5 x10^9/L

Biochemistry
- Sodium: 136-145 mmol/L
- Potassium: 3.5-5.1 mmol/L
- Chloride: 98-107 mmol/L
- Creatinine: M 62-106 umol/L, F 44-80 umol/L
- Urea: 2.5-7.5 mmol/L
- Glucose (fasting): 3.9-5.6 mmol/L
- HbA1c: 20-42 mmol/mol (normal), 42-48 (prediabetes), >=48 (diabetes)
- ALT: M <50 U/L, F <35 U/L
- AST: <40 U/L
- GGT: M <60 U/L, F <40 U/L
- Bilirubin total: 5-21 umol/L
- CRP: <5 mg/L

Lipids
- Total cholesterol: <5.0 mmol/L
- LDL: <3.0 mmol/L (lower in high-risk patients)
- HDL: M >1.0, F >1.2 mmol/L
- Triglycerides: <1.7 mmol/L

Coagulation
- INR: 0.9-1.2
- aPTT: 25-35 s
- Fibrinogen: 2.0-4.0 g/L

Thyroid
- TSH: 0.4-4.0 mIU/L
- fT4: 12-22 pmol/L

INSTRUCTIONS:

1. Parse all numeric values from the user's input. If sex or age is mentioned,
   apply sex-specific ranges. If not stated, note that you assumed adult.

2. For every reported value, classify as:
   - "normal"  (within range)
   - "low"     (below range)
   - "high"    (above range)
   - "critical-low" or "critical-high" (clinically dangerous, e.g.
     potassium <2.5 or >6.5, hemoglobin <70 g/L, glucose <2.5 or >25)

3. Identify CLINICAL PATTERNS the abnormalities could fit. Examples:
   - Low Hb + low MCV -> microcytic anemia (iron deficiency, thalassemia)
   - High WBC + high CRP + high neutrophils -> bacterial infection
   - High creatinine + high urea + high K -> AKI
   - High ALT + high AST + high GGT -> hepatocellular injury

4. Suggest 2-4 most useful next diagnostic steps. Be specific (e.g.,
   "ferritin, transferrin saturation" not "more tests").

5. ALWAYS end your interpretation with this line, verbatim:
   "EDUCATIONAL OUTPUT ONLY - not for clinical decision-making."

If a value cannot be parsed or is missing units, flag it but continue.
If the input contains no recognizable lab values, ask the user to clarify.


OUTPUT FORMAT:

Return your response as Markdown in EXACTLY this structure:

## Lab Interpretation

| Test | Value | Reference | Status |
|------|-------|-----------|--------|
| Hemoglobin | 95 g/L | M 135-175 g/L | 🔻 LOW |
| MCV | 72 fL | 80-100 fL | 🔻 LOW |
| Ferritin | 8 μg/L | 30-300 μg/L | 🔻 LOW |
| Creatinine | 88 μmol/L | M 62-106 μmol/L | ✓ Normal |

## Possible clinical patterns

- **Iron-deficiency anemia** with microcytosis. In a man >50, chronic GI
  blood loss is the leading concern until proven otherwise.
- **No systemic inflammation** (CRP normal) supports non-inflammatory
  iron deficiency rather than anemia of chronic disease.

## Suggested next steps

1. **Iron studies** — transferrin saturation, TIBC, serum iron
2. **Reticulocyte count** — assess marrow response
3. **GI workup** — colonoscopy first; FIT or fecal occult blood as
   adjunct; consider upper GI endoscopy if colon clear
4. **Celiac serology** — if GI sources are not found

## Summary

Microcytic anemia with low ferritin in a 55-year-old man — iron deficiency
is the diagnosis; the priority is identifying the source of blood loss.

---
*EDUCATIONAL OUTPUT ONLY — not for clinical decision-making.*

Use 🔻 for low, 🔺 for high, ⚠️ for critical, ✓ for normal.
Use bold for diagnoses, italics for the disclaimer.
```

---

## Example prompts to try

Copy and paste any of these into the chat to see the agent in action.

### Iron-deficiency anaemia

```text
55-year-old male, presenting with fatigue.
Hb 95 g/L, MCV 72 fL, WBC 6.2 x10^9/L, Platelets 280 x10^9/L,
Ferritin 8 ug/L, Creatinine 88 umol/L, ALT 22 U/L, CRP 3 mg/L.
```

### Diabetic ketoacidosis (DKA)

```text
22-year-old female. Glucose 28 mmol/L, Na 132, K 5.8, HCO3 12,
ketones positive, pH 7.18, HbA1c 95 mmol/mol.
```

### Alcoholic liver disease

```text
45M, alcohol use. ALT 180, AST 240, GGT 410, bilirubin 35 umol/L,
INR 1.4, albumin 32 g/L, platelets 110.
```

### B12/folate deficiency — megaloblastic anaemia

```text
70-year-old, weak. Hb 88, MCV 105, WBC 3.2, platelets 90,
B12 80 pmol/L, folate 4 nmol/L.
```

### Troubleshooting

| Problem | What to check |
| ------- | ------------- |
| "Invalid API key" error | Re-paste your OpenAI API key in the Custom OpenAI Model component |
| No response / timeout | Check your internet connection; try a smaller set of lab values |
| Flow won't import | Make sure you are selecting the `.json` file, not a folder |
| Blank output | Click the Chat Output component and confirm it is connected to the Language Model |
