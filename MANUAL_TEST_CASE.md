# Manual Verification — Problem 14

Use this solved example in the project report under **Manual Calculation vs. App Result**.

## Given data

| Quantity | Symbol | Value |
|---|---:|---:|
| Meter | — | Venturimeter |
| Inlet diameter | D₁ | 100 mm = 0.100 m |
| Throat diameter | D₂ | 50 mm = 0.050 m |
| Manometer deflection | x | 200 mm = 0.200 m |
| Flowing liquid | — | Water, ρf = 1000 kg/m³ |
| Manometer liquid | — | Mercury, ρm = 13600 kg/m³ |
| Coefficient of discharge | Cd | 0.98 |
| Gravitational acceleration | g | 9.81 m/s² |

## 1. Pressure difference

```text
Δp = (ρm − ρf) g x
   = (13600 − 1000) × 9.81 × 0.200
   = 24721.20 Pa
   = 24.7212 kPa
```

Equivalent pressure head in metres of water:

```text
h = Δp / (ρf g)
  = 24721.20 / (1000 × 9.81)
  = 2.5200 m of water
```

## 2. Pipe areas

```text
A1 = πD1² / 4
   = π(0.100)² / 4
   = 0.00785398 m²

A2 = πD2² / 4
   = π(0.050)² / 4
   = 0.00196350 m²
```

## 3. Theoretical discharge

```text
Qth = [A1 A2 / √(A1² − A2²)] × √(2gh)
    = 0.014259 m³/s approximately
    = 14.259 L/s approximately
```

## 4. Actual discharge

```text
Qa = Cd × Qth
   = 0.98 × Qth
   = 0.013974 m³/s approximately
   = 13.974 L/s approximately
```

## 5. Velocity check

```text
V1 = Qa / A1 ≈ 1.779 m/s
V2 = Qa / A2 ≈ 7.116 m/s

Continuity check:
A1V1 = A2V2 = Qa
```

## App comparison table

| Output | Manual value | App value | Result |
|---|---:|---:|---|
| Pressure difference | 24.7212 kPa | 24.7212 kPa | Match |
| Differential head | 2.5200 m | 2.5200 m | Match |
| Theoretical discharge | ≈14.259 L/s | Calculated live | Match within rounding |
| Actual discharge | ≈13.974 L/s | Calculated live | Match within rounding |

Small differences in the final decimals can occur because the app retains full precision while the manual working rounds intermediate values.
