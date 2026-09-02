# Example Prompts

This file provides representative English and German prompts for demonstrating the supported analytical capabilities of **Medical Insight Explorer Agent v1.2.0**.

## English Prompts

### Table and Dataset Structure

```text
Show me the shape of all tables
```

### Inpatient Claims

```text
Give me an inpatient summary
Show top inpatient providers
Show inpatient claims by state
```

### Outpatient Claims

```text
Give me an outpatient summary
Show top outpatient providers
Show outpatient claims by state
```

### Beneficiary Analytics

```text
What is the average beneficiary age?
```

### Reimbursement Analytics

```text
What is the diabetes cost summary?
Show reimbursement distribution
```

### Multi-Step Comparisons

```text
Compare inpatient and outpatient provider activity
Compare inpatient and outpatient claims by state
Compare inpatient and outpatient claim summaries
```

---

## German Prompts

### Tabellenstruktur

```text
Zeige die Form aller Tabellen
```

### Stationäre Claims

```text
Gib mir eine Zusammenfassung der stationären Claims
Zeige die wichtigsten stationären Provider
Zeige stationäre Claims nach Bundesstaat
```

### Ambulante Claims

```text
Gib mir eine Zusammenfassung der ambulanten Claims
Zeige die wichtigsten ambulanten Provider
Zeige ambulante Claims nach Bundesstaat
```

### Beneficiary-Analyse

```text
Wie hoch ist das durchschnittliche Alter der Beneficiaries?
```

### Erstattungsanalyse

```text
Wie sieht die Kostenzusammenfassung für Diabetes aus?
Zeige die Verteilung der Erstattungsbeträge
```

### Mehrstufige Vergleiche

```text
Vergleiche stationäre und ambulante Provider
Vergleiche stationäre und ambulante Claims nach Bundesstaaten
Vergleiche die Zusammenfassungen der stationären und ambulanten Claims
```

---

## Unsupported and Causal Examples

The application is designed for descriptive healthcare claims analytics.

Requests outside the approved analytical scope should use controlled fallback behavior rather than unrestricted analysis.

Examples include:

```text
Who is sick?
Diagnose this patient.
What treatment should this patient receive?
Does diabetes cause higher inpatient reimbursement?
```

These requests fall outside the project's descriptive analytical scope.

---

## Recommended Demo Sequence

A concise v1.2.0 demonstration is:

1. Select `English`.
2. Select `Hospital Operations Analyst`.
3. Run `Show top inpatient providers`.
4. Review the **Single-step** workflow status, analytical response, and provider chart.
5. Run `Compare inpatient and outpatient provider activity`.
6. Review the **Multi-step** workflow status and combined inpatient/outpatient results.
7. Confirm that all executed analytical results appear in the text while one primary visualization is displayed.
8. Switch the interface language to `Deutsch`.
9. Select a German persona-guided analytical question.
10. Run a supported German single-step or multi-step analysis.
11. Review the localized response, workflow status, and visualization when available.

This sequence demonstrates the main v1.2.0 progression:

```text
single-step analytics
        ↓
bounded multi-step analytics
        ↓
multi-result synthesis
        ↓
bilingual interaction
```