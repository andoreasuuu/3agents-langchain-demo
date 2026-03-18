# 3agents-langchain-demo
[School assigment] Creating three agents for different purposes and with different functionality.

# Köra agenterna

Alla agenter körs från terminalen:

# 1. Kanjiassistent

```bash
py -m examples.agent-lecture.kanji_agent
```

Vad den gör
- Förklarar kanji och japanska ord
- Ger läsningar (kun/on)
- Ger exempelord med japanska tecken
- Anpassar nivå (t.ex. nybörjare)

Exempel på frågor
- Förklara kanji 水
- Vad betyder 食べる?
- Vad är skillnaden mellan は och が?

# 2. Rese-/researchagent

```bash
py -m examples.agent-lecture.travel_research_agent
```

Vad den gör
- Läser webbsidor och sammanfattar innehåll
- Analyserar och jämför resmål
- Kan använda lokala reseanteckningar
- Kan göra enkla budgetberäkningar

Exempel på frågor
- Läs filen data/travel_notes.txt och föreslå vilket resmål som passar bäst för kultur
- Läs den här sidan och sammanfatta den:
https://en.wikipedia.org/wiki/Kyoto

# 3. Beräkningsassistent

```bash
py -m examples.agent-lecture.calculation_agent
```

Vad den gör
- Utför matematiska beräkningar
- Räknar procent, budget och vardagsekonomi
- Kan läsa filer med siffror och analysera dem

Exempel på frågor
- Vad är 15 procent av 2490?
- Räkna ut (3500 + 2200) / 2
- Läs filen data/budget.txt och räkna ut hur mycket pengar som är kvar efter utgifter

---
Exempelfiler
Projektet innehåller exempeldata i data/:
- japanese_notes.txt – japanska begrepp
- travel_notes.txt – reseidéer och budget
- budget.txt – enkel ekonomi

Alla agenter:
- använder samma grundstruktur
- har egen systemprompt