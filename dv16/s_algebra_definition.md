# Definition: Singularitäts-Algebra (S-Algebra)

## 1. Motivation

Die Cayley-Dickson-Konstruktion erzeugt Algebren, die ab einer Dimension von 16 (Sedenionen) Nullteiler enthalten. Diese Nullteiler stellen Singularitäten dar, die die Divisionseigenschaft der Algebra zerstören. Die DV-Mathematik führt eine **Singularity Treatment Operation (STO)** ein, um diese Singularitäten zu behandeln.

Der Begriff **Singularitäts-Algebra (S-Algebra)** wird eingeführt, um diese neue Klasse von Algebren zu formalisieren, die explizit für den Umgang mit internen Singularitäten konzipiert sind.

## 2. Formale Definition

Eine **Singularitäts-Algebra** (S-Algebra) ist ein Tupel $(\mathcal{A}, +, \cdot, \text{STO})$, wobei:

1.  $(\mathcal{A}, +, \cdot)$ eine Algebra über einem Körper $\mathbb{K}$ ist (typischerweise $\mathbb{R}$).
2.  $\text{STO}: \mathcal{A} \to \mathcal{A}$ eine **Singularity Treatment Operation** ist, eine lineare Abbildung, die so definiert ist, dass sie die algebraische Struktur modifiziert, um die Divisionseigenschaft zu erhalten oder wiederherzustellen.

### Eigenschaften der STO

Die STO muss folgende Eigenschaften erfüllen:

-   **Nicht-Trivialität:** Für mindestens ein Element $v \in \mathcal{A}$ muss $\text{STO}(v) \neq v$ gelten.
-   **Norm-Erhaltung (optional, aber empfohlen):** $|\text{STO}(v)| = |v|$ für alle $v \in \mathcal{A}$.
-   **Singularitäts-Auflösung:** Für jedes Nullteiler-Paar $(a, b)$ mit $a \cdot b = 0$ muss gelten:
    -   $\text{STO}(a) \cdot b \neq 0$ ODER
    -   $a \cdot \text{STO}(b) \neq 0$

### ASTO als spezifische Implementierung

Die **Asymmetric Singularity Treatment Operation (ASTO)**, wie in DV¹⁶ verwendet, ist eine spezifische Implementierung der STO für Algebren, die durch die Cayley-Dickson-Konstruktion erzeugt werden. Für eine Algebra $\mathcal{A} = \mathcal{B} \oplus \mathcal{B}e$, wobei $\mathcal{B}$ die vorhergehende Algebra in der Sequenz ist, ist ASTO definiert als:

$\text{ASTO}(v) = (\text{STO}(a), b)$ für $v = (a, b) \in \mathcal{A}$

## 3. Klassifizierung

-   **DV-Algebren** sind eine spezifische Familie von S-Algebren, die durch die Cayley-Dickson-Konstruktion und eine zyklische Permutation als STO erzeugt werden.
-   **DV¹⁶** ist die erste nicht-triviale S-Algebra in dieser Familie, da sie die erste ist, die eine STO *benötigt*, um konsistent zu sein.

## 4. Fazit

Der Begriff "S-Algebra" bietet einen formalen Rahmen, um Algebren zu beschreiben, deren Definition eine explizite Methode zur Behandlung von Singularitäten (wie Nullteilern) beinhaltet. Dies unterscheidet sie von klassischen Algebren und eröffnet ein neues Feld der algebraischen Untersuchung.
