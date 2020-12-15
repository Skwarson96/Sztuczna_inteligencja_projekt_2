# lokalizacja

Rzeczy dodane do call:
* obliczenie poprzedniej akcji na podstawie zmiany współrzędnych
* doodawanie lokacji z dołami do dedykowanej listy
* stworzenie listy z możliwymi lokacjami dołów. Lista jest tworzona na podstawie 'breeze' odczytanego z percept. Po wykryciu 'breeze' brane sa pod uwagę 3 lokacje w których może być dół ( 3 ponieważ z lokacją z 'breeze' sąsiadują 4 lokacje a z jedenj agent przyszedł więc nie mogło być tam dołu). Lokacje sa obliczane ze względu na ostatnią akcję. Lokacje są usuwane z tej listy w momencie gdy agent wejdzie na to pole. Gdy w liście pojawi się ta sama lokacja dwa razy traktowana jest ona jako dół. Nie będzie to prawda w każdym przypadku, czasami może się zdarzyć, że zwykła lokacja zostanie potraktowana jako dół, ale w znacznej większości sytuacji to założenie sprawdza się bardzo dobrze i pozwala na wykrywanie dołów bez wchodzenia do nich.
* licznik zliczający ilośc wystąpień z rzędu 'bump' w percept wykorzystany w celu wykonania akcji o przeciwnym kerunku do poprzedniej akcji w momencie gdyby agent się zablokował w jednek lokacji i cały czas uderzał w ścianę.

Rzeczy dodane do funkcji self.comp_value_and_policy():
* implementacja algorytmu value iteration z pseudokodu z zajęć.
