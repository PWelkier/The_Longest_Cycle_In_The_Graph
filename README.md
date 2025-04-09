# 🧠 Edytor Grafów z Szukaniem Najdłuższego Cyklu

Projekt to aplikacja graficzna zbudowana przy użyciu biblioteki `tkinter` oraz `networkx`, służąca do tworzenia grafów skierowanych i wyszukiwania w nich najdłuższego cyklu.

## ⚙️ Funkcje

- ➕ Dodawanie wierzchołków do grafu w interfejsie graficznym  
- 🔗 Łączenie wierzchołków krawędziami skierowanymi poprzez kliknięcia  
- 🧭 Automatyczne rozmieszczanie wierzchołków w okręgu  
- 🔍 Znajdowanie najdłuższego cyklu w grafie przy pomocy `networkx`  
- 🎯 Wizualne podświetlanie znalezionego cyklu  
- 📘 Instrukcja obsługi dostępna z poziomu aplikacji  

## 📝 Instrukcja użytkowania

1. Kliknij „**+ Dodaj wierzch.**” aby dodawać wierzchołki.  
2. Po dodaniu wszystkich wierzchołków kliknij „**Zakoncz dodawanie**”.  
3. Aby dodać krawędź:  
   - kliknij **lewym przyciskiem myszy** na wierzchołek początkowy,  
   - a potem **prawym przyciskiem myszy** na wierzchołek końcowy.  
4. Po zbudowaniu grafu kliknij „**Znajdź najdłuższy cykl**”, aby wyświetlić wynik.

## 🛠️ Technologie

- 🐍 **Python 3**  
- 🪟 **tkinter** – GUI  
- 🌐 **networkx** – operacje na grafach  
- 📊 **matplotlib** – wizualizacja grafu  
