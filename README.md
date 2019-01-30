Um den Python Code der Bachelorarbeit ausführen zu können müssen folgende Schritte befolgt werden.
Außerdem existiert eine gehostete Version auf https://mybinder.org/v2/gh/DATADEER/BA-GAME-RECOMMENDER.git/master
Wer die gehostete Version verwendet, kann gleich bei Schritt 3. (Ausführung) der Anleitung einsteigen.

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/DATADEER/BA-GAME-RECOMMENDER.git/master)
## Repository
* Das benötigte Repository mit dem Code ist 
  * auf der beigelegten CD zu finden und liegt im Ordner `/CODE/`
  * ist außerdem auf https://github.com/DATADEER/BA-GAME-RECOMMENDER.git zu finden

## Dependencies

1. Es wird **Python 3.7** zur Ausführung des Code benötigt.
https://www.python.org/downloads/

2. Die Dependcies können mit **Pipenv** installiert werden.
https://github.com/pypa/pipenv
_Zur Installation von Pipenv wird möglicherweise der Paketmanager **Pip** benötigt._

3. Die Dependencies des Python Scripts können nun mithilfe von Pipenv installiert werden. Dafür müssen lediglich folgende Befehle ausgeführt werden.
* `pipenv install` um eine neue **virtuelle Umgebung** mit Python 3.7 zu **erstellen** und alle **dependencies** aus dem Pipfile darin zu **installieren**.

## Ausführung

* `pipenv shell` um eine shell in der **virtuellen Umgebung** zu **öffnen** und zugriff auf die installierte dependencies zu haben.
* `jupyter notebook` um den **jupyter notebook server** zu **starten**, der das Python Script beeinhaltet und ausführen kann.

4. Der **Jupyter Notebook Server** sollte nun von alleine die richtige Seite im Standard-Browser geöffnet haben. Wenn dem nicht so ist, sollte die benötigte URL bei Server Start in der Shell als 
`The Jupyter Notebook is running at:http://localhost:8888/?token=420765c8cab3af627b6dcea4ddb8aadc7c48394e0cb9d3ab` zu finden sein.

5. Um das Beispiel Script für Spielempfehlungen auszuführend, muss folgendes Notebook geöffnet werden. `http://localhost:8888/notebooks/notebooks/get_game_recommendations.ipynb`
6. Zum Ausführen des Notebooks auf `Kernel` -> `Restart & Run All` drücken.

## Navigation

Der gesamte Code und das ausführbare Script können mithilfe des jupyter notebooks erkundet werden.

* Das **ausführbare Script** befindet sich im in `http://localhost:8888/notebooks/notebooks/get_game_recommendations.ipynb`
* Alle selbstgeschriebenen **Module** befinden sich in /modules/
* Die verwendeten **Rohdaten** liegen in /sample_data/





