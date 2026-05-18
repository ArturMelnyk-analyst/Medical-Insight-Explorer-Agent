# Example Prompts

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

## Unsafe or Unsupported Prompts to Avoid

Do not use diagnosis-style prompts such as:

```text
Who is sick?
Diagnose this patient.
What treatment should this patient receive?
```

The app is designed for claims analytics, not clinical decision-making.

## Recommended Demo Sequence

1. `Show top inpatient providers`
2. `Show reimbursement distribution`
3. Switch language to Deutsch
4. `Zeige die wichtigsten stationären Provider`
5. `Wie hoch ist das durchschnittliche Alter der Beneficiaries?`