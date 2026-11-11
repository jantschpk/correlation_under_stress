# Hausarbeit Datenanalyse I

Nötige Dateien:
- Tschapka_645515_DAI.ipynb
- bibliography.bib
- sampling.py
- bootstrap.py 
- constituents.csv
- requirements.txt
- harvard-cite-them-right.csl

(Nur damit werden Quellenangaben richtig erstellt. Kann über https://github.com/citation-style-language/styles/blob/master/harvard-cite-them-right.csl neu geladen werden)

Zur Aktualisierung der S&P-500 Liste kann update_csv.py verwendet werden. Wichtig: Dadurch ändern sich im Zweifel jedoch die Ergebnisse aus der Arbeit. Für die Aktualisierung der CSV wird bei Bedarf zusätzlich die Python Library requests benötigt.

# Originales Setup: Quarto + LaTeX
Der ursprüngliche PDF-Export erfolgt über Quarto. Quarto verarbeitet das
Jupyter Notebook und erzeugt daraus zunächst ein für den PDF-Export geeignetes
Dokument. Für die eigentliche PDF-Erstellung wird anschließend LaTeX verwendet.
Dafür werden benötigt:
- Python
- Jupyter
- Quarto
- eine LaTeX-Distribution

_WICHTIG: Ein Export mit Quarto ist nötig, um die adäquate Formatierung und die Erstellung der Referenzen beim Export zu gewährleisten. Es ist auch ein Export ohne Quarto möglich, siehe unten._

## Python
Für die Erstellung wurde Python Version 3.13.9 genutzt. Es empfiehlt sich, eine virtuelle Python-Umgebung zu verwenden.

Virtuelle Umgebung erstellen 

python -m venv .venv

Aktivieren


Windows PowerShell:
.venv\Scripts\Activate.ps1

macOS / Linux:
source .venv/bin/activate

Anschließend können die benötigten Python-Pakete installiert werden:

pip install -r requirements.txt


## Quarto installieren
Die Installationsanleitung befindet sich auf der offiziellen Quarto-Website:
https://quarto.org/docs/get-started/
Nach der Installation kann überprüft werden, ob Quarto korrekt eingerichtet ist:

quarto check

Die installierte Version kann mit folgendem Befehl angezeigt werden:


quarto --version

## LaTeX installieren
Für den PDF-Export über Quarto wird eine LaTeX-Distribution benötigt.
Beispiele:

Windows: MiKTeX


macOS: MacTeX


Linux: TeX Live

Nach der Installation sollte Quarto die LaTeX-Installation erkennen:

quarto check

Bei fehlenden LaTeX-Paketen müssen diese gegebenenfalls nachinstalliert werden.

## PDF mit Quarto erzeugen
Der Export direkt über die Kommandozeile erfolgen:

quarto render Tschapka_645515_DAI.ipynb --to pdf


## Alternative: Export ohne Quarto
Die .ipynb-Datei ist ein standardisiertes Jupyter Notebook und kann deshalb
auch ohne Quarto weiterverarbeitet werden.
Eine Möglichkeit ist die Verwendung von Jupyter nbconvert.
Zunächst muss Jupyter installiert sein:

pip install jupyter

Anschließend kann das Notebook beispielsweise in HTML umgewandelt werden:

jupyter nbconvert Tschapka_645515_DAI.ipynb --to html


Diese Datei kann anschließend im Browser geöffnet oder weiterverarbeitet werden. Vorsicht: Hier ist die Formatierung nicht richtig!