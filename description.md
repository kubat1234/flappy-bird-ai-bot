# Agent AI grający w Flappy Bird

**Cel:** Stworzenie agenta ai grającego w autorską wersje flappy bird z ruszającymi się rurami

**Algorytmy:** Algorytm NEAT (NeuroEvolution of Augmenting Topologies): Metoda ewolucyjna optymalizująca zarówno wagi, jak i strukturę sieci neuronowej.

**Narzędzia:** Język Python, Biblioteki: neat-python, pygame

**Wkład własny:**

- Implementację silnika gry Flappy Bird od podstaw (fizyka skoku, kolizje, generator rur), aby dostosować go do interfejsu agenta AI.

- Zaprojektowanie i dostrojenie funkcji fitness (wskaźnik oceniający jakość osobnika).

- Optymalizację parametrów konfiguracyjnych NEAT (wielkość populacji, prawdopodobieństwo mutacji połączeń/neuronów).

- Przygotowanie modułu wizualizacyjnego, wyświetlającego najlepszą sieć neuronową danej generacji.

**Spodziewane wyniki:** Agent powinien umieć grać w grę (przejść przez zadowalającą ilość przeszkód bez kolizji), dla gier o różnym poziomie trudności (różne wielkości przerw, odleglosci miedzy rurami oraz ich predkości)