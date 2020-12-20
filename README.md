Rzeczy dodane do call:
* obliczenie poprzedniej akcji na podstawie zmiany współrzędnych
* dodawanie lokacji z dołami do dedykowanej listy
* stworzenie listy z możliwymi lokacjami dołów. Lista jest tworzona na podstawie 'breeze' odczytanego z percept. Po wykryciu 'breeze' brane sa pod uwagę 3 lokacje w których może być dół ( 3 ponieważ z lokacją z 'breeze' sąsiadują 4 lokacje a z jedenj agent przyszedł więc nie mogło być tam dołu). Lokacje sa obliczane ze względu na ostatnią akcję. Lokacje są usuwane z tej listy w momencie gdy agent wejdzie na to pole lub gdy w liście pojawi się ta sama lokacja dwa razy, traktowana jest ona wtedy jako dół i dodana do listy lokacji z dołami. Nie będzie to prawda w każdym przypadku, czasami może się zdarzyć, że zwykła lokacja zostanie potraktowana jako dół, ale w znacznej większości sytuacji to założenie sprawdza się bardzo dobrze i pozwala na wykrywanie dołów bez wchodzenia do nich.
* licznik zliczający ilośc wystąpień z rzędu 'bump' w percept wykorzystany w celu wykonania akcji o przeciwnym kerunku do poprzedniej akcji w momencie gdyby agent się zablokował w jednek lokacji i cały czas uderzał w ścianę, licznik został ustawiony na wartość 5.
* dobór nagród i kar:  
 Wybór tego czy w danym momencie agent ma być nagradzany czy karany został podjęty intuuicyjnie, a konkretne wartości kar i nagród zostały dobrane na podstawie testów.
  * nagroda za odkrycie nowego pola -> 100
  * kara za ruch na pole, które zostało już wczesniej odwiedzone -> -10
  * kara za wejście na pole z listy prawdopodobnych dołów -> -100
  * kara za wejście na pole z listy dołów -> -10000

Rzeczy dodane do funkcji self.comp_value_and_policy():
* implementacja algorytmu value iteration z pseudokodu z zajęć.
* funkcja do wygodniego wyswietlania planszy z wartosciami self.V dla każdego pola

Rzeczy dodane do main.py
* oznaczanie na czerwono lokacji odwiedzonych
